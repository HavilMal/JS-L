from pathlib import Path

from datetime import datetime
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QListWidget, \
    QFileDialog, QLineEdit, QDateEdit, QDateTimeEdit, QMessageBox

from LabeledDetail import LabeledDetail
from parse import LogLoader, details

DETAIL_NAMES = ["Time", "User ID", "Origin IP", "Origin port", "Response IP", "Response port", "Method", "Host", "URI", "Status code"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log viewer")
        self.index = 0

        self.log_loader = LogLoader()
        self.logs = []

        top_layout = QVBoxLayout()
        master_detail_label = QHBoxLayout()

        file_picker_layout = QHBoxLayout()
        self.file_path = QLineEdit("")
        self.file_path.setReadOnly(True)
        file_picker_layout.addWidget(self.file_path)

        button = QPushButton("Load logs")
        button.clicked.connect(self.select_file)
        file_picker_layout.addWidget(button)

        top_layout.addLayout(file_picker_layout)
        top_layout.addLayout(master_detail_label)

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(lambda: self.handle_nav_button(self.index - 1))
        nav_layout.addWidget(self.prev_button, 1)
        nav_layout.addStretch(2)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(lambda: self.handle_nav_button(self.index + 1))
        nav_layout.addWidget(self.next_button, 1)
        top_layout.addLayout(nav_layout)

        master_layout = QVBoxLayout()
        detail_layout = QVBoxLayout()

        master_detail_label.addLayout(master_layout)
        master_detail_label.addLayout(detail_layout)

        self.list_widget = QListWidget()
        self.list_widget.clicked.connect(lambda x: self.update_detail(x.row()))

        filter_layout = QHBoxLayout()
        from_label = QLabel("From")
        from_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        filter_layout.addWidget(from_label)
        self.from_date = QDateTimeEdit()
        self.from_date.editingFinished.connect(self.handle_filters)
        filter_layout.addWidget(self.from_date)

        to_label = QLabel("To:")
        to_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        filter_layout.addWidget(to_label)
        self.to_date = QDateTimeEdit()
        self.to_date.editingFinished.connect(self.handle_filters)
        filter_layout.addWidget(self.to_date)


        master_layout.addLayout(filter_layout)
        master_layout.addWidget(self.list_widget)


        self.details: dict[str, LabeledDetail] = {}
        for i, n in zip(details, DETAIL_NAMES):
            detail = LabeledDetail(n, "")
            self.details[i] = detail
            detail_layout.addWidget(detail)


        widget = QWidget()
        widget.setLayout(top_layout)
        self.setCentralWidget(widget)

    def select_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.show()
        dialog.fileSelected.connect(self.handle_load_logs)

    def handle_nav_button(self, index):
        self.list_widget.setCurrentRow(index)
        self.update_detail(index)

    def update_detail(self, index):
        self.index = index
        log = self.logs[index]

        if self.index == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)

        # for empty list
        if self.index >= len(self.logs) - 1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)


        for key in details:
            self.details[key].set_data(log[key])

        if 100 <= log["status_code"] <= 199:
            self.details["status_code"].set_color(QColorConstants.Blue)
        elif 200 <= log["status_code"] <= 299:
            self.details["status_code"].set_color(QColorConstants.Green)
        elif 300 <= log["status_code"] <= 399:
            self.details["status_code"].set_color(QColorConstants.Yellow)
        elif 400 <= log["status_code"] <= 499:
            self.details["status_code"].set_color(QColor(255, 156, 28))
        elif 500 <= log["status_code"] <= 599:
            self.details["status_code"].set_color(QColorConstants.Red)



    def handle_load_logs(self, path):
        if not self.load_logs(path):
            err_message = QMessageBox().critical(self, "Invalid log file", "Provided log file is invalid and could not be loaded.")

            return


        self.file_path.setText(path)

        if len(self.logs) != 0:
            f_date: datetime  = self.logs[0]["ts"]
            t_date: datetime = self.logs[-1]["ts"]
            self.from_date.setDateTime(QDateTime(f_date.year, f_date.month, f_date.day, f_date.hour, f_date.minute, f_date.second))
            self.to_date.setDateTime(QDateTime(t_date.year, t_date.month, t_date.day, t_date.hour, t_date.minute, t_date.second))


    def handle_filters(self):
        f_date = self.from_date.dateTime().toPython()
        t_date = self.to_date.dateTime().toPython()

        self.logs = self.log_loader.filter_logs(f_date, t_date)
        self.update_logs()


    def update_logs(self):
        l = map(lambda x: x["raw"][:30] + "..." if len(x["raw"]) > 30 else x["raw"], self.logs)

        self.list_widget.clear()
        self.list_widget.addItems(l)


    def load_logs(self, path):
        try:
            self.logs = self.log_loader.parse_logs(Path(path))
        except ValueError:
            return False

        self.update_logs()

        if len(self.logs) != 0:
            self.update_detail(0)

        return True




