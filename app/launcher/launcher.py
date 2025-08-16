import sys
import configparser

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QComboBox, QCheckBox, QWidget, \
    QToolBar, QStatusBar, QLabel, QSpinBox, QLineEdit
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

        #Display - width
        screen_width_label = QLabel("Screen Width:", self)
        self.screen_width = QSpinBox(self)
        self.screen_width.setRange(50, 1900)
        self.screen_width.setSingleStep(50)
        self.screen_width.setValue(self.config.getint('display', 'SCREEN_WIDTH'))
        self.screen_width.lineEdit().setReadOnly(True)
        self.screen_width.textChanged.connect(self.change_screen_width)
        #Height
        screen_height_label = QLabel("Screen Height:", self)
        self.screen_height = QSpinBox(self)
        self.screen_height.setRange(50, 1000)
        self.screen_height.setSingleStep(50)
        self.screen_height.setValue(self.config.getint('display', 'SCREEN_HEIGHT'))
        self.screen_height.lineEdit().setReadOnly(True)
        self.screen_height.textChanged.connect(self.change_screen_height)

        #Grid
        dimension_width_label = QLabel("Number of Tiles Wide:", self)
        self.dimension_width = QSpinBox(self)
        self.dimension_width.setRange(1, 200)
        self.dimension_width.setSingleStep(10)
        self.dimension_width.setValue(self.config.getint('grid', 'grid_dim_width'))
        self.dimension_width.textChanged.connect(self.change_dimension_width)

        dimension_height_label = QLabel("Number of Tiles Tall:", self)
        self.dimension_height = QSpinBox(self)
        self.dimension_height.setRange(1, 200)
        self.dimension_height.setSingleStep(10)
        self.dimension_height.setValue(self.config.getint('grid', 'grid_dim_height'))
        self.dimension_height.textChanged.connect(self.change_dimension_height)



        #Construct Grid
        grid.addWidget(debug_label, 0, 0)
        grid.addWidget(self.debug_checkbox, 0, 1)
        grid.addWidget(fail_condition_label, 1, 0)
        grid.addWidget(self.fail_condition_combo, 1, 1)
        grid.addWidget(screen_width_label, 2, 0)
        grid.addWidget(self.screen_width, 2, 1)
        grid.addWidget(screen_height_label, 3, 0)
        grid.addWidget(self.screen_height, 3, 1)
        grid.addWidget(dimension_width_label, 4, 0)
        grid.addWidget(self.dimension_width, 4, 1)
        grid.addWidget(dimension_height_label, 5, 0)
        grid.addWidget(self.dimension_height, 5, 1)
        self.setLayout(grid)

    def toggle_debug(self):
        self.config['debug']['DEBUG'] = str(self.debug_checkbox.isChecked())
        self.write()

    def change_fail_condition(self):
        self.config['contradiction']['FAIL_CONDITION'] = self.fail_condition_combo.currentText()
        self.write()

    def change_screen_width(self):
        self.config['display']['SCREEN_WIDTH'] = self.screen_width.text()
        self.write()

    def change_screen_height(self):
        self.config['display']['SCREEN_HEIGHT'] = self.screen_height.text()
        self.write()

    def change_dimension_width(self):
        self.config['grid']['grid_dim_width'] = self.dimension_width.text()
        self.write()

    def change_dimension_height(self):
        self.config['grid']['grid_dim_height'] = self.dimension_height.text()
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