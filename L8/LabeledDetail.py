from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QLineEdit


class LabeledDetail(QWidget):
    def __init__(self, label, data=None):
        super().__init__()
        self.data = data

        layout = QHBoxLayout()
        label = QLabel(str(label))
        layout.addWidget(label)

        self.detail = QLineEdit()
        self.detail.setReadOnly(True)
        layout.addWidget(self.detail)

        self.setLayout(layout)


    def set_data(self, data):
        self.data = data

        if data is None:
            self.detail.setText(str(self.data))
        else:
            self.detail.setText(str(self.data))



