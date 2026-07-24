from PyQt6.QtCore import QThread, pyqtSignal

class Worker(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal()

    def __init__(self, func=None, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            if self.func:
                self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.progress_signal.emit(0, f"Error: {str(e)}")
        finally:
            self.finished_signal.emit()
