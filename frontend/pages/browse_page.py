"""
Browse page — list all places with type filter and search.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QScrollArea, QGridLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from frontend.components.card import PlaceCard


class BrowsePage(QWidget):
    reserve_requested = pyqtSignal(dict)

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.types = []
        self._build_ui()
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(400)
        self.search_timer.timeout.connect(self.load_data)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        title = QLabel("🔍  Mekanlara Göz At")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        sub = QLabel("Mükemmel mekanı bulmak için ara ve filtrele")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        # Filter bar
        filter_row = QHBoxLayout()
        filter_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔎  Mekan ara...")
        self.search_input.setMinimumHeight(44)
        self.search_input.textChanged.connect(lambda: self.search_timer.start())
        filter_row.addWidget(self.search_input, 2)

        self.type_filter = QComboBox()
        self.type_filter.setMinimumHeight(44)
        self.type_filter.setMinimumWidth(180)
        self.type_filter.addItem("Tüm Tipler", None)
        self.type_filter.currentIndexChanged.connect(self.load_data)
        filter_row.addWidget(self.type_filter, 1)

        layout.addLayout(filter_row)

        # Results grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

    def load_data(self):
        # Load types if not loaded
        if not self.types:
            try:
                self.types = self.api.get_types()
                self.type_filter.blockSignals(True)
                self.type_filter.clear()
                self.type_filter.addItem("Tüm Tipler", None)
                for t in self.types:
                    self.type_filter.addItem(t["name"], t["id"])
                self.type_filter.blockSignals(False)
            except:
                pass

        # Clear grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        type_id = self.type_filter.currentData()
        search = self.search_input.text().strip() or None

        try:
            places = self.api.get_places(type_id=type_id, search=search, limit=50)
            if not places:
                empty = QLabel("📭  Mekan bulunamadı")
                empty.setStyleSheet("font-size: 18px; color: #888; padding: 40px;")
                empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid_layout.addWidget(empty, 0, 0, 1, 3)
                return

            for i, p in enumerate(places):
                card = PlaceCard(p)
                card.reserve_clicked.connect(self.reserve_requested.emit)
                row, col = divmod(i, 3)
                self.grid_layout.addWidget(card, row, col)
        except Exception as e:
            err = QLabel(f"❌ Hata: {e}")
            err.setStyleSheet("color: #FF6B6B;")
            self.grid_layout.addWidget(err, 0, 0)
