import os
import re
import sys
import io
import subprocess
import tempfile
from contextlib import redirect_stderr
from pathlib import Path
from tqdm import tqdm as _tqdm

import _patch_env  # noqa: F401

if sys.platform == "win32":
    _orig_popen_init = subprocess.Popen.__init__
    def _patched_popen_init(self, *args, **kwargs):
        kwargs["creationflags"] = kwargs.get("creationflags", 0) | 0x08000000
        _orig_popen_init(self, *args, **kwargs)
    subprocess.Popen.__init__ = _patched_popen_init

from audio_separator.separator import Separator


def _install_tqdm_safe_refresh():
    if getattr(_tqdm.refresh, "_audio_converter_safe", False):
        return

    def safe_refresh(self, nolock=False, lock_args=None):
        if self.disable:
            return

        acquired = False
        if not nolock:
            if lock_args:
                acquired = self._lock.acquire(*lock_args)
                if not acquired:
                    return False
            else:
                self._lock.acquire()
                acquired = True
        try:
            self.display()
        finally:
            if acquired:
                self._lock.release()
        return True

    safe_refresh._audio_converter_safe = True
    _tqdm.refresh = safe_refresh


_install_tqdm_safe_refresh()


class ProcessingStopped(Exception):
    pass


class _TqdmCapture:
    def __init__(self, on_progress):
        self.on_progress = on_progress
        self._orig_stderr = sys.stderr
        self._buf = io.StringIO()
        self._pct = re.compile(r"(\d+)%")
        self._speed = re.compile(r"([\d.]+)\s*([KMG]?i?B/s|it/s|samples/s|rows/s|s/it)")
        self._last_pct = -1
        self._step = 0

    def write(self, data):
        # In a windowed PyInstaller build stderr can be missing or already
        # closed. Do not let that break tqdm's construction/cleanup.
        try:
            if self._orig_stderr is not None:
                self._orig_stderr.write(data)
                self._orig_stderr.flush()
        except (AttributeError, OSError, ValueError):
            pass
        self._buf.write(data)
        m = self._pct.search(data)
        if m:
            pct = int(m.group(1))
            if self._last_pct >= 50 and pct < 10:
                self._step += 1
            self._last_pct = pct
            s = self._speed.search(data)
            speed = s.group(1) + s.group(2) if s else ""
            self.on_progress(pct, self._step, speed)

    def flush(self):
        try:
            if self._orig_stderr is not None:
                self._orig_stderr.flush()
        except (AttributeError, OSError, ValueError):
            pass


def _model_path(models_dir, model_filename):
    return models_dir / model_filename


def run_separator(input_file, output_dir, model_filename, single_stem, progress_callback,
                  separate_only_mode=False, stop_check=lambda: False):
    temp_dir = Path(tempfile.gettempdir()) / "separated"
    temp_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(input_file).stem
    stem_map = {"Vocals": "vocal", "Instrumental": "instrument"}
    stem_key = stem_map.get(single_stem, single_stem.lower())

    if getattr(sys, 'frozen', False):
        models_dir = Path(sys.executable).parent / "models" / "audio-separator-models"
    else:
        models_dir = Path(__file__).parent / "models" / "audio-separator-models"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = _model_path(models_dir, model_filename)
    needs_download = not model_path.exists() and not any(models_dir.glob(f"*{Path(model_filename).stem}*"))

    if separate_only_mode:
        dw = 0.2 if needs_download else 0.0
        sw = 0.8 if needs_download else 1.0
    else:
        dw = 0.2 if needs_download else 0.0
        sw = 0.6 if needs_download else 0.8

    _max_seen = 0
    stop_raised = False

    def _cap(v):
        nonlocal _max_seen
        if v > _max_seen:
            _max_seen = v
        return _max_seen

    def _on_dl_progress(pct, step, speed):
        nonlocal stop_raised
        if stop_check() and pct > 0 and not stop_raised:
            stop_raised = True
            raise ProcessingStopped("Stopped by user")
        total = _cap(int(pct * dw))
        txt = f"Downloading model... {total}%"
        if speed:
            txt += f" ({speed})"
        progress_callback(total, txt)

    def _on_sep_progress(pct, step, speed):
        nonlocal stop_raised
        if stop_check() and pct > 0 and not stop_raised:
            stop_raised = True
            raise ProcessingStopped("Stopped by user")
        offset = int(dw * 100)
        step0_max = int(sw * 100 * 0.97)
        step1_max = int(sw * 100 * 0.03)
        if step == 0:
            total = _cap(offset + int(step0_max * pct / 100))
        else:
            total = _cap(offset + step0_max + int(step1_max * pct / 100))
        txt = f"Separating audio... {total}%"
        if speed:
            txt += f" ({speed})"
        progress_callback(total, txt)

    separator = Separator(
        output_dir=str(temp_dir),
        output_format="WAV",
        model_file_dir=str(models_dir),
        use_directml=True,
    )

    if needs_download:
        cap = _TqdmCapture(_on_dl_progress)
        with redirect_stderr(cap):
            separator.load_model(model_filename=model_filename)
    else:
        progress_callback(0, "Loading model...")
        separator.load_model(model_filename=model_filename)
        progress_callback(0, "Model loaded")

    if stop_check():
        raise ProcessingStopped("Stopped by user")

    cap = _TqdmCapture(_on_sep_progress)
    with redirect_stderr(cap):
        output_files = separator.separate(str(input_file))

    if stop_check():
        raise ProcessingStopped("Stopped by user")

    chosen_file = None
    for f in output_files:
        fp = Path(f)
        if not fp.is_absolute():
            fp = temp_dir / fp
        if not fp.exists():
            continue
        if stem_key in fp.stem.lower():
            chosen_file = fp
            break

    if chosen_file is None and output_files:
        for f in output_files:
            fp = Path(f)
            if not fp.is_absolute():
                fp = temp_dir / fp
            if fp.exists():
                chosen_file = fp
                break

    if not chosen_file or not chosen_file.exists():
        raise FileNotFoundError(
            f"Separator output not found for stem '{single_stem}' "
            f"in {temp_dir}. Separator returned: {output_files}"
        )

    dst = temp_dir / f"{original_name}.{stem_key}.wav"
    if dst.exists():
        dst.unlink()
    chosen_file.rename(dst)

    if separate_only_mode:
        sep_total = 99
    else:
        sep_total = int((dw + sw) * 100)
    progress_callback(sep_total, "Separate done")
    return dst
