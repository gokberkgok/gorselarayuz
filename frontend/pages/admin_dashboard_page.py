"""
Admin Dashboard — overview stats with cards.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt


class AdminDashboardPage(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("📊  Admin Dashboard")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        sub = QLabel("Overview of the reservation system")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(16)
        layout.addLayout(self.stats_grid)
        layout.addStretch()

    def _make_stat_card(self, icon, label, value, color="#6C63FF"):
        card = QFrame()
        card.setProperty("class", "stat-card")
        card.setMinimumHeight(140)
        cl = QVBoxLayout(card)
        cl.setSpacing(8)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 32px; background: transparent; border: none;")
        cl.addWidget(icon_lbl)

        val_lbl = QLabel(str(value))
        val_lbl.setProperty("class", "stat-value")
        val_lbl.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: 700;")
        cl.addWidget(val_lbl)

        name_lbl = QLabel(label)
        name_lbl.setProperty("class", "stat-label")
        cl.addWidget(name_lbl)

        return card

    def load_data(self):
        # Clear
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            stats = self.api.get_stats()
            cards = [
                ("👥", "Total Users", stats["total_users"], "#1890FF"),
                ("🏨", "Active Places", stats["total_places"], "#52C41A"),
                ("📋", "Total Reservations", stats["total_reservations"], "#722ED1"),
                ("⏳", "Pending", stats["pending_reservations"], "#FAAD14"),
                ("✅", "Approved", stats["approved_reservations"], "#52C41A"),
            ]
            for i, (icon, label, value, color) in enumerate(cards):
                card = self._make_stat_card(icon, label, value, color)
                row, col = divmod(i, 3)
                self.stats_grid.addWidget(card, row, col)
        except Exception as e:
            err = QLabel(f"❌ Error loading stats: {e}")
            err.setStyleSheet("color: #FF6B6B;")
            self.stats_grid.addWidget(err, 0, 0)
