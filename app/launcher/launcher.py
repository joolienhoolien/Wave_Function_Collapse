import sys
import configparser

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QComboBox, QCheckBox, QWidget, \
    QToolBar, QStatusBar, QLabel
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
        #Run wfc
        wfc = PygameFrontEnd()
        wfc.solve_wave()

class Settings(QWidget):
    def __init__(self):
        super().__init__()

        #Find current settings
        self.config = configparser.ConfigParser()
        self.config.read('../../settings.ini')

        grid = QGridLayout()

        #Debug
        debug_label = QLabel("Debug:", self)
        self.debug_checkbox = QCheckBox()
        self.debug_checkbox.setChecked(self.config.getboolean('debug', 'DEBUG'))
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)

        #Fail Condition
        fail_condition_label = QLabel("Fail Condition:", self)
        self.fail_condition_combo = QComboBox()
        fail_condition_options = self.config['contradiction']['FAIL_CONDITION_OPTIONS'].split(',')
        self.fail_condition_combo.addItems(fail_condition_options)
        fail_condition = self.config['contradiction']['FAIL_CONDITION']
        self.fail_condition_combo.setCurrentText(fail_condition)
        self.fail_condition_combo.currentTextChanged.connect(self.change_fail_condition)

        #Construct Grid
        grid.addWidget(debug_label, 0, 0)
        grid.addWidget(self.debug_checkbox, 0, 1)
        grid.addWidget(fail_condition_label, 1, 0)
        grid.addWidget(self.fail_condition_combo, 1, 1)
        self.setLayout(grid)

    def toggle_debug(self):
        self.config['debug']['DEBUG'] = str(self.debug_checkbox.isChecked())
        self.write()

    def change_fail_condition(self):
        self.config['contradiction']['FAIL_CONDITION'] = self.fail_condition_combo.currentText()
        self.write()

    def write(self):
        with open('../../settings.ini', 'w') as configfile:
            self.config.write(configfile)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()