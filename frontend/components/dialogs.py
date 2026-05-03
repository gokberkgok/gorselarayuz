"""
Dialog components — Reservation dialog, Confirm dialog, Place form dialog.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QDateEdit, QTimeEdit, QComboBox,
    QFormLayout, QWidget, QFileDialog
)
from PyQt6.QtCore import QDate, QTime, Qt
from PyQt6.QtGui import QPixmap


class ReservationDialog(QDialog):
    """Modal dialog for creating a reservation."""

    def __init__(self, parent, place_data: dict):
        super().__init__(parent)
        self.place_data = place_data
        self.result_data = None
        self.setWindowTitle("Rezervasyon Yap")
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
        date_lbl = QLabel("Tarih")
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
        st_lbl = QLabel("Başlangıç Saati")
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
        et_lbl = QLabel("Bitiş Saati")
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
        cancel_btn = QPushButton("İptal")
        cancel_btn.setProperty("class", "outline-btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        submit_btn = QPushButton("✅  Rezervasyonu Onayla")
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
        self.setWindowTitle("Mekanı Düzenle" if self.editing else "Yeni Mekan Ekle")
        self.setFixedSize(450, 520)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)

        title = QLabel("🏨  " + ("Mekanı Düzenle" if self.editing else "Yeni Mekan Oluştur"))
        title.setProperty("class", "card-title")
        layout.addWidget(title)

        # Form (Stacked modern layout)
        form = QVBoxLayout()
        form.setSpacing(16)

        # Name
        name_l = QVBoxLayout()
        name_l.setSpacing(6)
        name_lbl = QLabel("Mekan Adı")
        name_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Mekan adı girin...")
        self.name_input.setFixedHeight(40)
        if place_data:
            self.name_input.setText(place_data.get("name", ""))
        name_l.addWidget(name_lbl)
        name_l.addWidget(self.name_input)
        form.addLayout(name_l)

        # Type
        type_l = QVBoxLayout()
        type_l.setSpacing(6)
        type_lbl = QLabel("Mekan Tipi")
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

        # Image
        img_l = QVBoxLayout()
        img_l.setSpacing(6)
        img_lbl = QLabel("Mekan Resmi (İsteğe Bağlı)")
        img_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        img_row = QHBoxLayout()
        self.img_input = QLineEdit()
        self.img_input.setPlaceholderText("Resim dosyası seçin...")
        self.img_input.setFixedHeight(40)
        self.img_input.setReadOnly(True)
        if place_data:
            self.img_input.setText(place_data.get("image_url", ""))
        img_btn = QPushButton("📁 Göz At")
        img_btn.setProperty("class", "outline-btn")
        img_btn.setFixedHeight(40)
        img_btn.clicked.connect(self._browse_image)
        img_row.addWidget(self.img_input)
        img_row.addWidget(img_btn)
        img_l.addWidget(img_lbl)
        img_l.addLayout(img_row)
        form.addLayout(img_l)

        # Description
        desc_l = QVBoxLayout()
        desc_l.setSpacing(6)
        desc_lbl = QLabel("Açıklama")
        desc_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #54657E;")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Mekan hakkında kısa açıklama...")
        self.desc_input.setMaximumHeight(80)
        if place_data:
            self.desc_input.setText(place_data.get("description", ""))
        desc_l.addWidget(desc_lbl)
        desc_l.addWidget(self.desc_input)
        form.addLayout(desc_l)

        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("İptal")
        cancel_btn.setProperty("class", "outline-btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("💾  Kaydet" if self.editing else "➕  Oluştur")
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
            "image_url": self.img_input.text().strip(),
        }
        self.accept()

    def _browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Resim Seç", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.img_input.setText(file_path)


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
        no_btn = QPushButton("Hayır")
        no_btn.setProperty("class", "outline-btn")
        no_btn.clicked.connect(self.reject)
        btn_row.addWidget(no_btn)

        yes_btn = QPushButton("Evet")
        yes_btn.setProperty("class", "primary-btn")
        yes_btn.clicked.connect(self.accept)
        btn_row.addWidget(yes_btn)
        layout.addLayout(btn_row)


class ReservationDetailsDialog(QDialog):
    """Modal dialog for viewing reservation details."""

    def __init__(self, parent, reservation_data: dict, on_approve=None, on_reject=None):
        super().__init__(parent)
        self.setWindowTitle("Rezervasyon Detayları")
        self.setFixedSize(400, 500)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)

        # Title
        title = QLabel(f"📄  Rezervasyon #{reservation_data.get('id', '')}")
        title.setProperty("class", "card-title")
        layout.addWidget(title)

        # Image (if available)
        img_url = reservation_data.get("place_image_url", "")
        if img_url:
            try:
                pixmap = QPixmap(img_url)
                if not pixmap.isNull():
                    img_lbl = QLabel()
                    pixmap = pixmap.scaledToWidth(344, Qt.TransformationMode.SmoothTransformation)
                    img_lbl.setPixmap(pixmap)
                    img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(img_lbl)
            except Exception:
                pass

        # Details Layout
        details = QVBoxLayout()
        details.setSpacing(12)

        def add_row(lbl_text, val_text):
            row = QHBoxLayout()
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet("color: #94a3b8; font-weight: 600; min-width: 100px;")
            val = QLabel(str(val_text))
            val.setStyleSheet("color: #f8fafc; font-weight: 500;")
            val.setWordWrap(True)
            row.addWidget(lbl)
            row.addWidget(val, 1)
            details.addLayout(row)

        add_row("Mekan:", reservation_data.get("place_name", "Bilinmiyor"))
        add_row("Tarih:", reservation_data.get("date", ""))
        add_row("Saat:", f"{reservation_data.get('start_time', '')} - {reservation_data.get('end_time', '')}")
        
        status = reservation_data.get("status", "unknown")
        tr_status = status
        if status == "pending": tr_status = "BEKLİYOR"
        elif status == "approved": tr_status = "ONAYLANDI"
        elif status == "cancelled": tr_status = "İPTAL"
        elif status == "rejected": tr_status = "REDDEDİLDİ"
        add_row("Durum:", tr_status)

        layout.addLayout(details)
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        if on_reject and reservation_data.get("status") == "pending":
            reject_btn = QPushButton("🚫 Reddet")
            reject_btn.setProperty("class", "danger-btn")
            reject_btn.clicked.connect(lambda: [self.accept(), on_reject(reservation_data["id"])])
            btn_row.addWidget(reject_btn)

        if on_approve and reservation_data.get("status") == "pending":
            approve_btn = QPushButton("✅ Onayla")
            approve_btn.setProperty("class", "success-btn")
            approve_btn.clicked.connect(lambda: [self.accept(), on_approve(reservation_data["id"])])
            btn_row.addWidget(approve_btn)

        close_btn = QPushButton("Kapat")
        close_btn.setProperty("class", "outline-btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)


class PlaceDetailsDialog(QDialog):
    """Modal dialog for viewing place details."""

    def __init__(self, parent, place_data: dict, on_edit=None):
        super().__init__(parent)
        self.setWindowTitle("Mekan Detayları")
        self.setFixedSize(450, 500)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)

        # Title
        title = QLabel(f"🏨  {place_data.get('name', 'Bilinmeyen Mekan')}")
        title.setProperty("class", "card-title")
        title.setWordWrap(True)
        layout.addWidget(title)

        # Image (if available)
        img_url = place_data.get("image_url", "")
        if img_url:
            try:
                pixmap = QPixmap(img_url)
                if not pixmap.isNull():
                    img_lbl = QLabel()
                    pixmap = pixmap.scaledToWidth(394, Qt.TransformationMode.SmoothTransformation)
                    img_lbl.setPixmap(pixmap)
                    img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(img_lbl)
            except Exception:
                pass

        # Details
        details = QVBoxLayout()
        details.setSpacing(12)

        def add_row(lbl_text, val_text):
            row = QHBoxLayout()
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet("color: #94a3b8; font-weight: 600; min-width: 100px;")
            val = QLabel(str(val_text))
            val.setStyleSheet("color: #f8fafc; font-weight: 500;")
            val.setWordWrap(True)
            row.addWidget(lbl)
            row.addWidget(val, 1)
            details.addLayout(row)

        add_row("Tip:", place_data.get("type_name", "Diğer"))
        add_row("Açıklama:", place_data.get("description", ""))
        add_row("Durum:", "AKTİF" if place_data.get("is_active") else "PASİF")

        layout.addLayout(details)
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        if on_edit:
            edit_btn = QPushButton("✏️ Mekanı Düzenle")
            edit_btn.setProperty("class", "primary-btn")
            edit_btn.clicked.connect(lambda: [self.accept(), on_edit(place_data)])
            btn_row.addWidget(edit_btn)

        close_btn = QPushButton("Kapat")
        close_btn.setProperty("class", "outline-btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
