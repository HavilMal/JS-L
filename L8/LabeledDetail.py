from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QLineEdit


class LabeledDetail(QWidget):
    def __init__(self, label, data=None):
        super().__init__()
        self.data = data

        layout = QHBoxLayout()
        label = QLabel(str(label))
        layout.addWidget(label, 1)

        self.detail = QLineEdit()
        self.detail.setReadOnly(True)
        layout.addWidget(self.detail, 3)

        self.setLayout(layout)


    def set_data(self, data):
        self.data = data

        if data is None:
            self.detail.setText(str(self.data))
        else:
            self.detail.setText(str(self.data))

    def set_color(self, color):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Text, color)
        self.detail.setPalette(palette)

