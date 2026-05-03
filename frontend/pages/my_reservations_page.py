"""
My Reservations page — user's reservations with status and cancel.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from frontend.components.dialogs import ReservationDetailsDialog


class MyReservationsPage(QWidget):
    def __init__(self, api_client, toast_fn):
        super().__init__()
        self.api = api_client
        self.toast = toast_fn
        self.reservations_list = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("📋  Rezervasyonlarım")
        title.setProperty("class", "page-title")
        header.addWidget(title)
        header.addStretch()

        refresh_btn = QPushButton("🔄  Yenile")
        refresh_btn.setProperty("class", "outline-btn")
        refresh_btn.clicked.connect(self.load_data)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        sub = QLabel("Rezervasyonlarınızı takip edin ve yönetin")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Mekan", "Tarih", "Başlangıç", "Bitiş", "Durum", "İşlem"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 160)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 160)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.table)

    def load_data(self):
        self.table.setRowCount(0)
        try:
            reservations = self.api.get_my_reservations()
            self.reservations_list = reservations
            self.table.setRowCount(len(reservations))
            for i, r in enumerate(reservations):
                self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
                self.table.setItem(i, 1, QTableWidgetItem(r.get("place_name", "")))
                self.table.setItem(i, 2, QTableWidgetItem(str(r["date"])))
                self.table.setItem(i, 3, QTableWidgetItem(str(r["start_time"])))
                self.table.setItem(i, 4, QTableWidgetItem(str(r["end_time"])))

                status = r["status"]
                
                tr_status = status
                if status == "pending": tr_status = "BEKLİYOR"
                elif status == "approved": tr_status = "ONAYLANDI"
                elif status == "cancelled": tr_status = "İPTAL"
                elif status == "rejected": tr_status = "REDDEDİLDİ"

                status_lbl = QLabel(f"  {tr_status}  ")
                status_lbl.setProperty("class", f"status-{status}")
                status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 5, status_lbl)

                if status in ("pending", "approved"):
                    cancel_w = QWidget()
                    cancel_l = QHBoxLayout(cancel_w)
                    cancel_l.setContentsMargins(4, 4, 4, 4)
                    cancel_btn = QPushButton("❌ İptal Et")
                    cancel_btn.setProperty("class", "danger-btn")
                    cancel_btn.setFixedHeight(36)
                    cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    rid = r["id"]
                    cancel_btn.clicked.connect(lambda checked, rid=rid: self._cancel(rid))
                    cancel_l.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.table.setCellWidget(i, 6, cancel_w)
                else:
                    self.table.setItem(i, 6, QTableWidgetItem("—"))

                self.table.setRowHeight(i, 64)
        except Exception as e:
            self.toast(f"Hata: {e}", "error")

    def _cancel(self, rid):
        try:
            self.api.cancel_reservation(rid)
            self.toast("Rezervasyon iptal edildi", "success")
            self.load_data()
        except Exception as e:
            self.toast(f"Hata: {e}", "error")

    def _on_item_double_clicked(self, item):
        row = item.row()
        if hasattr(self, "reservations_list") and row < len(self.reservations_list):
            data = self.reservations_list[row]
            dlg = ReservationDetailsDialog(self, data)
            dlg.exec()
