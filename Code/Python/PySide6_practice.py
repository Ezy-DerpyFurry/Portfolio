import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class FirstWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.texts = ""
        self.digit_length = 5

        self.button = QtWidgets.QPushButton(f"Generate a random number (5 digits)")
        self.text = QtWidgets.QLabel("", alignment = QtCore.Qt.AlignCenter)
        self.text2 = QtWidgets.QLabel("Number Generator", alignment = QtCore.Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(5)
        self.slider.setMaximum(20)
        self.slider.setMinimum(1)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.slider.valueChanged.connect(self.test)

    @QtCore.Slot()
    def test(self):
        self.digit_length = self.slider.value()
        self.button.setText(f"Generate a random number ({self.digit_length} digits)")

    @QtCore.Slot()
    def magic(self):
        for i in range(self.digit_length):
            self.texts = self.texts + str(random.randint(1,9))
            self.text.setText(self.texts)
        self.texts = ""

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = FirstWidget()
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec())
