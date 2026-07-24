import os
import sys
from pathlib import Path


def patch_path():
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
        ffmpeg_dir = base / "ffmpeg"
        torch_lib_dir = base / "torch" / "lib"
    else:
        base = Path(__file__).resolve().parent
        ffmpeg_dir = base / "ffmpeg"
        torch_lib_dir = base / "Lib" / "site-packages" / "torch" / "lib"

    # Make the bundled FFmpeg available to subprocesses.
    if ffmpeg_dir.is_dir():
        ffmpeg_path = str(ffmpeg_dir)
        current_path = os.environ.get("PATH", "")
        if ffmpeg_path not in current_path:
            os.environ["PATH"] = ffmpeg_path + os.pathsep + current_path

    # torch-directml also depends on PyTorch's native libraries.
    if hasattr(os, "add_dll_directory") and torch_lib_dir.is_dir():
        os.add_dll_directory(str(torch_lib_dir))


patch_path()
