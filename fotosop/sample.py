import sys
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget


class Worker(QObject):
    finished = pyqtSignal()
    progress_updated = pyqtSignal(int)

    @pyqtSlot()
    def run_task(self):
        for i in range(1, 11):
            time.sleep(1)  # Simulate a time-consuming task
            self.progress_updated.emit(i * 10)
            print("nigger", i)

        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Concurrent Task with QThread')
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel('Progress: 0%')
        self.button_start = QPushButton('Start Task')
        self.button_start.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_start)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)

        self.thread.started.connect(self.worker.run_task)

        self.setLayout(layout)

    def start_task(self):
        self.button_start.setEnabled(False)
        self.thread.start()

    @pyqtSlot(int)
    def update_progress(self, progress):
        self.label.setText(f'Progress: {progress}%')

    @pyqtSlot()
    def task_finished(self):
        self.thread.quit()
        self.thread.wait()
        self.label.setText('Task completed!')
        self.button_start.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())