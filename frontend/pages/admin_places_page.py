"""
Admin Places page — CRUD table for managing places.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from frontend.components.dialogs import PlaceFormDialog, ConfirmDialog, PlaceDetailsDialog


class AdminPlacesPage(QWidget):
    def __init__(self, api_client, toast_fn):
        super().__init__()
        self.api = api_client
        self.toast = toast_fn
        self.types = []
        self.places_list = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("🏨  Mekan Yönetimi")
        title.setProperty("class", "page-title")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("➕  Mekan Ekle")
        add_btn.setProperty("class", "primary-btn")
        add_btn.clicked.connect(self._add_place)
        header.addWidget(add_btn)
        layout.addLayout(header)

        sub = QLabel("Tüm mekanları oluştur, düzenle ve yönet")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "İsim", "Tip", "Durum", "Düzenle", "Sil"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)  # QSS handles border bottoms instead
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.table)

    def load_data(self):
        try:
            self.types = self.api.get_types()
        except:
            self.types = []

        self.table.setRowCount(0)
        try:
            places = self.api.get_places(limit=100)
            self.places_list = places
            self.table.setRowCount(len(places))
            for i, p in enumerate(places):
                self.table.setItem(i, 0, QTableWidgetItem(str(p["id"])))
                self.table.setItem(i, 1, QTableWidgetItem(p["name"]))
                self.table.setItem(i, 2, QTableWidgetItem(p.get("type_name", "")))

                status_text = "AKTİF" if p["is_active"] else "PASİF"
                active = QLabel(f"  {status_text}  ")
                active.setProperty("class", "status-active" if p["is_active"] else "status-passive")
                active.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 3, active)

                # Edit button wrapper
                edit_w = QWidget()
                edit_l = QHBoxLayout(edit_w)
                edit_l.setContentsMargins(4, 4, 4, 4)
                edit_btn = QPushButton("✏️")
                edit_btn.setProperty("class", "outline-btn")
                edit_btn.setProperty("icon_btn", "true")
                edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                edit_btn.clicked.connect(lambda checked, data=p: self._edit_place(data))
                edit_l.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 4, edit_w)

                # Delete button wrapper
                del_w = QWidget()
                del_l = QHBoxLayout(del_w)
                del_l.setContentsMargins(4, 4, 4, 4)
                del_btn = QPushButton("🗑️")
                del_btn.setProperty("class", "danger-btn")
                del_btn.setProperty("icon_btn", "true")
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                pid = p["id"]
                del_btn.clicked.connect(lambda checked, pid=pid: self._delete_place(pid))
                del_l.addWidget(del_btn, alignment=Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 5, del_w)

                self.table.setRowHeight(i, 64)
        except Exception as e:
            self.toast(f"Error: {e}", "error")

    def _add_place(self):
        if not self.types:
            try:
                self.types = self.api.get_types()
            except:
                self.toast("Tipler yüklenemedi", "error")
                return

        dlg = PlaceFormDialog(self, self.types)
        if dlg.exec() and dlg.result_data:
            try:
                self.api.create_place(**dlg.result_data)
                self.toast("Mekan oluşturuldu!", "success")
                self.load_data()
            except Exception as e:
                self.toast(f"Hata: {e}", "error")

    def _edit_place(self, data):
        if not self.types:
            try:
                self.types = self.api.get_types()
            except:
                pass

        dlg = PlaceFormDialog(self, self.types, data)
        if dlg.exec() and dlg.result_data:
            try:
                self.api.update_place(data["id"], **dlg.result_data)
                self.toast("Mekan güncellendi!", "success")
                self.load_data()
            except Exception as e:
                self.toast(f"Hata: {e}", "error")

    def _delete_place(self, pid):
        dlg = ConfirmDialog(self, "Mekanı Sil", "Bu mekanı deaktif etmek istediğinize emin misiniz?")
        if dlg.exec():
            try:
                self.api.delete_place(pid)
                self.toast("Mekan deaktif edildi", "success")
                self.load_data()
            except Exception as e:
                self.toast(f"Hata: {e}", "error")

    def _on_item_double_clicked(self, item):
        row = item.row()
        if hasattr(self, "places_list") and row < len(self.places_list):
            data = self.places_list[row]
            dlg = PlaceDetailsDialog(self, data, on_edit=self._edit_place)
            dlg.exec()
