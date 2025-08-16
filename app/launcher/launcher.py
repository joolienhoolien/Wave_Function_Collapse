import sys
import configparser

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QComboBox, QCheckBox, QWidget, \
    QToolBar, QStatusBar
from app.pygame_frontend.pygame_frontend import PygameFrontEnd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wave Function Collapse Launcher")
        self.setMinimumSize(300, 300)

        #Set up settings
        self.settings = Settings()
        self.setCentralWidget(self.settings)

        #Set actions
        start_button = QPushButton("Start", self)
        start_button.clicked.connect(self.start)

        #Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.addWidget(start_button)


    def start(self):
        wfc = PygameFrontEnd()
        wfc.solve_wave()

class Settings(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()

        #Instantiate Widgets
        debug_checkbox = QCheckBox("Debug")


        #Construct Grid
        grid.addWidget(debug_checkbox, 0, 0)

        self.setLayout(grid)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()