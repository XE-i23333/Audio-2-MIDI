import sys
import logging
from collections import deque
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QTimer


class _LogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.buffer = deque()
        self._orig_stderr = sys.__stderr__

    def emit(self, record):
        msg = self.format(record) + "\n"
        if self._orig_stderr is not None:
            self._orig_stderr.write(msg)
            self._orig_stderr.flush()
        self.buffer.append(msg)


class _StreamCapture:
    def __init__(self, original):
        self._orig = original
        self.buffer = deque()
        self.encoding = getattr(original, "encoding", "utf-8")
        self.errors = getattr(original, "errors", "strict")

    def __getattr__(self, name):
        return getattr(self._orig, name)

    def write(self, data):
        if self._orig is not None:
            self._orig.write(data)
        if data.strip():
            self.buffer.append(data)

    def flush(self):
        if self._orig is not None:
            self._orig.flush()

    def isatty(self):
        return False

    def fileno(self):
        return self._orig.fileno()

    def close(self):
        pass


_handler = _LogHandler()
_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(_handler)
logging.getLogger().setLevel(logging.INFO)

_stdout_capture = _StreamCapture(sys.stdout)
_stderr_capture = _StreamCapture(sys.stderr)
sys.stdout = _stdout_capture
sys.stderr = _stderr_capture


class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Output")
        self.setGeometry(300, 300, 700, 500)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.text_edit.clear)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self._flush_all()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._flush_all)
        self._timer.start(200)

    def set_language_texts(self, title, clear_text):
        self.setWindowTitle(title)
        self.clear_btn.setText(clear_text)

    def _flush_all(self):
        for buf in (_handler.buffer, _stdout_capture.buffer, _stderr_capture.buffer):
            while buf:
                self._append(buf.popleft())

    def _append(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.insertPlainText(text)
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
