"""
Reusable Place Card component.
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt


# Icon mapping for place types
TYPE_ICONS = {
    "Hotel": "🏨",
    "Restaurant": "🍽️",
    "Room": "🚪",
    "Cafe": "☕",
    "Spa": "💆",
}


class PlaceCard(QFrame):
    """Card widget displaying place information with a Reserve button."""
    reserve_clicked = pyqtSignal(dict)

    def __init__(self, place_data: dict, show_reserve=True):
        super().__init__()
        self.place_data = place_data
        self.setProperty("class", "card")
        self.setMinimumHeight(240)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header row: icon + type badge
        header = QHBoxLayout()
        type_name = place_data.get("type_name", "Other")
        icon = TYPE_ICONS.get(type_name, "📍")

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 32px; background: transparent; border: none;")
        header.addWidget(icon_lbl)
        header.addStretch()

        badge = QLabel(f"  {type_name}  ")
        badge.setProperty("class", "type-badge")
        header.addWidget(badge)
        layout.addLayout(header)

        # Name
        name = QLabel(place_data.get("name", ""))
        name.setProperty("class", "card-title")
        name.setWordWrap(True)
        layout.addWidget(name)

        # Description
        desc_text = place_data.get("description", "")
        if len(desc_text) > 100:
            desc_text = desc_text[:100] + "..."
        desc = QLabel(desc_text)
        desc.setProperty("class", "card-desc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        if show_reserve:
            reserve_btn = QPushButton("📅  Reserve Now")
            reserve_btn.setProperty("class", "primary-btn")
            reserve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            reserve_btn.clicked.connect(lambda: self.reserve_clicked.emit(self.place_data))
            layout.addWidget(reserve_btn)
