"""
Dialog components — Reservation dialog, Confirm dialog, Place form dialog.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QDateEdit, QTimeEdit, QComboBox,
    QFormLayout, QWidget
)
from PyQt6.QtCore import QDate, QTime, Qt


class ReservationDialog(QDialog):
    """Modal dialog for creating a reservation."""

    def __init__(self, parent, place_data: dict):
        super().__init__(parent)
        self.place_data = place_data
        self.result_data = None
        self.setWindowTitle("Make a Reservation")
        self.setFixedSize(420, 380)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)

        # Title
        title = QLabel(f"📅  Reserve: {place_data.get('name', '')}")
        title.setProperty("class", "card-title")
        title.setWordWrap(True)
        layout.addWidget(title)

        # Form (Stacked modern layout)
        form = QVBoxLayout()
        form.setSpacing(16)

        # Date
        date_lbl = QLabel("Date")
        date_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate().addDays(1))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.setFixedHeight(40)
        
        date_layout = QVBoxLayout()
        date_layout.setSpacing(6)
        date_layout.addWidget(date_lbl)
        date_layout.addWidget(self.date_edit)
        form.addLayout(date_layout)

        # Time Row
        time_row = QHBoxLayout()
        time_row.setSpacing(16)

        # Start Time
        start_l = QVBoxLayout()
        start_l.setSpacing(6)
        st_lbl = QLabel("Start Time")
        st_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime(9, 0))
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setFixedHeight(40)
        start_l.addWidget(st_lbl)
        start_l.addWidget(self.start_time)
        time_row.addLayout(start_l)

        # End Time
        end_l = QVBoxLayout()
        end_l.setSpacing(6)
        et_lbl = QLabel("End Time")
        et_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime(10, 0))
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setFixedHeight(40)
        end_l.addWidget(et_lbl)
        end_l.addWidget(self.end_time)
        time_row.addLayout(end_l)

        form.addLayout(time_row)
        layout.addLayout(form)
        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "outline-btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        submit_btn = QPushButton("✅  Confirm Reservation")
        submit_btn.setProperty("class", "primary-btn")
        submit_btn.clicked.connect(self._submit)
        btn_row.addWidget(submit_btn)
        layout.addLayout(btn_row)

    def _submit(self):
        self.result_data = {
            "place_id": self.place_data["id"],
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "start_time": self.start_time.time().toString("HH:mm:ss"),
            "end_time": self.end_time.time().toString("HH:mm:ss"),
        }
        self.accept()


class PlaceFormDialog(QDialog):
    """Modal dialog for creating or editing a place."""

    def __init__(self, parent, types: list, place_data: dict = None):
        super().__init__(parent)
        self.result_data = None
        self.editing = place_data is not None
        self.setWindowTitle("Edit Place" if self.editing else "Add New Place")
        self.setFixedSize(450, 420)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)

        title = QLabel("🏨  " + ("Edit Place" if self.editing else "Create New Place"))
        title.setProperty("class", "card-title")
        layout.addWidget(title)

        # Form (Stacked modern layout)
        form = QVBoxLayout()
        form.setSpacing(16)

        # Name
        name_l = QVBoxLayout()
        name_l.setSpacing(6)
        name_lbl = QLabel("Place Name")
        name_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter place name...")
        self.name_input.setFixedHeight(40)
        if place_data:
            self.name_input.setText(place_data.get("name", ""))
        name_l.addWidget(name_lbl)
        name_l.addWidget(self.name_input)
        form.addLayout(name_l)

        # Type
        type_l = QVBoxLayout()
        type_l.setSpacing(6)
        type_lbl = QLabel("Place Type")
        type_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.type_combo = QComboBox()
        self.type_combo.setFixedHeight(40)
        for t in types:
            self.type_combo.addItem(t["name"], t["id"])
        if place_data:
            idx = self.type_combo.findData(place_data.get("type_id"))
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
        type_l.addWidget(type_lbl)
        type_l.addWidget(self.type_combo)
        form.addLayout(type_l)

        # Description
        desc_l = QVBoxLayout()
        desc_l.setSpacing(6)
        desc_lbl = QLabel("Description")
        desc_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Brief description of the place...")
        self.desc_input.setMaximumHeight(80)
        if place_data:
            self.desc_input.setText(place_data.get("description", ""))
        desc_l.addWidget(desc_lbl)
        desc_l.addWidget(self.desc_input)
        form.addLayout(desc_l)

        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "outline-btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("💾  Save" if self.editing else "➕  Create")
        save_btn.setProperty("class", "primary-btn")
        save_btn.clicked.connect(self._submit)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _submit(self):
        name = self.name_input.text().strip()
        if not name:
            return
        self.result_data = {
            "name": name,
            "type_id": self.type_combo.currentData(),
            "description": self.desc_input.toPlainText().strip(),
        }
        self.accept()


class ConfirmDialog(QDialog):
    """Simple confirmation dialog."""

    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(380, 180)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(28, 28, 28, 28)

        msg = QLabel(message)
        msg.setWordWrap(True)
        msg.setStyleSheet("font-size: 15px;")
        layout.addWidget(msg)
        layout.addStretch()

        btn_row = QHBoxLayout()
        no_btn = QPushButton("No")
        no_btn.setProperty("class", "outline-btn")
        no_btn.clicked.connect(self.reject)
        btn_row.addWidget(no_btn)

        yes_btn = QPushButton("Yes")
        yes_btn.setProperty("class", "primary-btn")
        yes_btn.clicked.connect(self.accept)
        btn_row.addWidget(yes_btn)
        layout.addLayout(btn_row)
