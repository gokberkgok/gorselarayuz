"""
Home page — shows 5 random places as cards.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QGridLayout, QFrame, QPushButton
)
from PyQt6.QtCore import pyqtSignal, Qt
from frontend.components.card import PlaceCard


class HomePage(QWidget):
    reserve_requested = pyqtSignal(dict)

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Welcome banner
        banner = QFrame()
        banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1890FF, stop:1 #40A9FF);
                border-radius: 12px;
                padding: 16px 24px;
            }
        """)
        banner_layout = QVBoxLayout(banner)
        welcome = QLabel(f"👋  Tekrar Hoş Geldiniz, {self.api.user_name or 'Kullanıcı'}!")
        welcome.setStyleSheet("font-size: 20px; font-weight: 700; color: white; background: transparent;")
        banner_layout.addWidget(welcome)

        welcome_sub = QLabel("Bugün harika mekanlar keşfedin ve rezervasyon yapın")
        welcome_sub.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.85); background: transparent;")
        banner_layout.addWidget(welcome_sub)
        layout.addWidget(banner)

        # Section title
        section_row = QHBoxLayout()
        sec_title = QLabel("🌟  Öne Çıkan Mekanlar")
        sec_title.setProperty("class", "page-title")
        section_row.addWidget(sec_title)
        section_row.addStretch()

        refresh_btn = QPushButton("🔄  Yenile")
        refresh_btn.setProperty("class", "outline-btn")
        refresh_btn.clicked.connect(self.load_data)
        section_row.addWidget(refresh_btn)
        layout.addLayout(section_row)

        # Cards grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

    def load_data(self):
        # Clear existing
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            places = self.api.get_random_places(5)
            for i, p in enumerate(places):
                card = PlaceCard(p)
                card.reserve_clicked.connect(self.reserve_requested.emit)
                row, col = divmod(i, 3)
                self.grid_layout.addWidget(card, row, col)
        except Exception as e:
            err = QLabel(f"❌ Mekanlar yüklenirken hata oluştu: {e}")
            err.setStyleSheet("color: #FF6B6B; font-size: 14px;")
            self.grid_layout.addWidget(err, 0, 0)
