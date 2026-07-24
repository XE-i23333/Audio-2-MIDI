import sys
import traceback
from pathlib import Path

import _patch_env  # noqa: F401

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from gui import Converter
except Exception:
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    resource_base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
    app.setWindowIcon(QIcon(str(resource_base / "icon.ico")))
    window = Converter()
    window.show()
    sys.exit(app.exec())
