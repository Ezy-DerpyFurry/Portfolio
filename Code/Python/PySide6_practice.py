import sys
import random
import string
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QSlider, QLineEdit
from PySide6.QtCore import Qt

### Colours

pink = "#ff80fb"

class FirstWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.texts = ""
        self.digit_length = 5

        self.button = QtWidgets.QPushButton(f"Generate a random password (5 characters)")
        self.button.setStyleSheet(f"""
            color: {pink};
        """)
        self.text = QtWidgets.QLabel("", alignment = QtCore.Qt.AlignCenter)
        self.text.setStyleSheet(f"""
            color: {pink};
        """)
        self.text2 = QtWidgets.QLabel("Password Generator", alignment = QtCore.Qt.AlignCenter)
        self.text2.setStyleSheet(f"""
            color: {pink};
        """)

        self.edit = QLineEdit()
        self.edit.setMinimumHeight(100)
        self.edit.setMaximumHeight(399)
        self.edit.setStyleSheet(f"""
            background-color: dark-grey;
            color: {pink};
        """)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(5)
        self.slider.setMaximum(20)
        self.slider.setMinimum(1)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.button)

        self.edit.returnPressed.connect(self.run_test)
        self.button.clicked.connect(self.magic)
        self.slider.valueChanged.connect(self.set_digit_length)

    @QtCore.Slot()
    def set_digit_length(self):
        self.digit_length = self.slider.value()
        self.button.setText(f"Generate a random password ({self.digit_length} characters)")

    @QtCore.Slot()
    def run_test(self):
        exec(self.edit.text())

    @QtCore.Slot()
    def magic(self):
        self.text.setText(''.join(random.choices(string.ascii_lowercase + string.punctuation + string.digits, k = self.digit_length)))
        self.texts = ""

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = FirstWidget()
    widget.setStyleSheet("""
        background-color: #1a1a1a;
    """)
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec())
