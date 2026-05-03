"""
Admin Reservations page — view all reservations, approve/reject.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView,
    QComboBox
)
from PyQt6.QtCore import Qt


from frontend.components.dialogs import ReservationDetailsDialog


class AdminReservationsPage(QWidget):
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
        title = QLabel("📋  Tüm Rezervasyonlar")
        title.setProperty("class", "page-title")
        header.addWidget(title)
        header.addStretch()

        self.status_filter = QComboBox()
        self.status_filter.setMinimumWidth(160)
        self.status_filter.setMinimumHeight(40)
        self.status_filter.addItem("Tüm Durumlar", None)
        self.status_filter.addItem("⏳ Bekliyor", "pending")
        self.status_filter.addItem("✅ Onaylandı", "approved")
        self.status_filter.addItem("❌ İptal Edildi", "cancelled")
        self.status_filter.addItem("🚫 Reddedildi", "rejected")
        self.status_filter.currentIndexChanged.connect(self.load_data)
        header.addWidget(self.status_filter)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setProperty("class", "outline-btn")
        refresh_btn.clicked.connect(self.load_data)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        sub = QLabel("Tüm rezervasyonları incele ve yönet")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Kullanıcı", "Mekan", "Tarih", "Başlangıç", "Bitiş", "Durum", "Onayla", "Reddet"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
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
        status = self.status_filter.currentData()
        try:
            reservations = self.api.get_all_reservations(status_filter=status)
            self.reservations_list = reservations
            self.table.setRowCount(len(reservations))
            for i, r in enumerate(reservations):
                self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
                self.table.setItem(i, 1, QTableWidgetItem(r.get("user_name", "")))
                self.table.setItem(i, 2, QTableWidgetItem(r.get("place_name", "")))
                self.table.setItem(i, 3, QTableWidgetItem(str(r["date"])))
                self.table.setItem(i, 4, QTableWidgetItem(str(r["start_time"])))
                self.table.setItem(i, 5, QTableWidgetItem(str(r["end_time"])))

                st = r["status"]
                
                tr_status = st
                if st == "pending": tr_status = "BEKLİYOR"
                elif st == "approved": tr_status = "ONAYLANDI"
                elif st == "cancelled": tr_status = "İPTAL"
                elif st == "rejected": tr_status = "REDDEDİLDİ"

                st_lbl = QLabel(f"  {tr_status}  ")
                st_lbl.setProperty("class", f"status-{st}")
                st_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 6, st_lbl)

                if st == "pending":
                    app_w = QWidget()
                    app_l = QHBoxLayout(app_w)
                    app_l.setContentsMargins(4, 4, 4, 4)
                    approve_btn = QPushButton("✅")
                    approve_btn.setProperty("class", "success-btn")
                    approve_btn.setProperty("icon_btn", "true")
                    approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    rid = r["id"]
                    approve_btn.clicked.connect(lambda checked, rid=rid: self._approve(rid))
                    app_l.addWidget(approve_btn, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.table.setCellWidget(i, 7, app_w)

                    rej_w = QWidget()
                    rej_l = QHBoxLayout(rej_w)
                    rej_l.setContentsMargins(4, 4, 4, 4)
                    reject_btn = QPushButton("🚫")
                    reject_btn.setProperty("class", "danger-btn")
                    reject_btn.setProperty("icon_btn", "true")
                    reject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    reject_btn.clicked.connect(lambda checked, rid=rid: self._reject(rid))
                    rej_l.addWidget(reject_btn, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.table.setCellWidget(i, 8, rej_w)
                else:
                    self.table.setItem(i, 7, QTableWidgetItem("—"))
                    self.table.setItem(i, 8, QTableWidgetItem("—"))

                self.table.setRowHeight(i, 64)
        except Exception as e:
            self.toast(f"Hata: {e}", "error")

    def _approve(self, rid):
        try:
            self.api.approve_reservation(rid)
            self.toast("Rezervasyon onaylandı!", "success")
            self.load_data()
        except Exception as e:
            self.toast(f"Hata: {e}", "error")

    def _reject(self, rid):
        try:
            self.api.reject_reservation(rid)
            self.toast("Rezervasyon reddedildi", "info")
            self.load_data()
        except Exception as e:
            self.toast(f"Hata: {e}", "error")

    def _on_item_double_clicked(self, item):
        row = item.row()
        if hasattr(self, "reservations_list") and row < len(self.reservations_list):
            data = self.reservations_list[row]
            dlg = ReservationDetailsDialog(self, data, on_approve=self._approve, on_reject=self._reject)
            dlg.exec()
