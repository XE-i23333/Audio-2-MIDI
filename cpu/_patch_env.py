import os
import sys
from pathlib import Path


def patch_path():
    if getattr(sys, "frozen", False):
        _base = Path(sys._MEIPASS)
        _ffmpeg = _base / "ffmpeg"
        _cuda = _base / "torch" / "lib"
    else:
        _base = Path(__file__).resolve().parent
        _ffmpeg = _base / "ffmpeg"
        _cuda = _base / "Lib" / "site-packages" / "torch" / "lib"

    # ffmpeg → PATH for subprocess
    _s = str(_ffmpeg)
    _curr = os.environ.get("PATH", "")
    if _s not in _curr:
        os.environ["PATH"] = _s + os.pathsep + _curr

    # CUDA/cuDNN dll → add_dll_directory for ctypes/native module loading
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(str(_cuda))


patch_path()
