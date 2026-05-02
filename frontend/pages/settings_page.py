"""
Settings page — theme toggle and user info.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QCheckBox, QPushButton
)
from PyQt6.QtCore import pyqtSignal, Qt


class SettingsPage(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self, api_client, current_theme="light"):
        super().__init__()
        self.api = api_client
        self.current_theme = current_theme
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("⚙️  Settings")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        sub = QLabel("Customize your experience")
        sub.setProperty("class", "page-subtitle")
        layout.addWidget(sub)

        # User info card
        info_card = QFrame()
        info_card.setProperty("class", "card")
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(12)

        info_title = QLabel("👤  Account Information")
        info_title.setProperty("class", "card-title")
        info_layout.addWidget(info_title)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Name:"))
        name_val = QLabel(self.api.user_name or "—")
        name_val.setStyleSheet("font-weight: 600;")
        name_row.addWidget(name_val)
        name_row.addStretch()
        info_layout.addLayout(name_row)

        role_row = QHBoxLayout()
        role_row.addWidget(QLabel("Role:"))
        role_val = QLabel((self.api.user_role or "—").upper())
        role_val.setStyleSheet("font-weight: 600;")
        role_row.addWidget(role_val)
        role_row.addStretch()
        info_layout.addLayout(role_row)

        id_row = QHBoxLayout()
        id_row.addWidget(QLabel("User ID:"))
        id_val = QLabel(str(self.api.user_id or "—"))
        id_val.setStyleSheet("font-weight: 600;")
        id_row.addWidget(id_val)
        id_row.addStretch()
        info_layout.addLayout(id_row)

        layout.addWidget(info_card)

        # Theme card
        theme_card = QFrame()
        theme_card.setProperty("class", "card")
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setSpacing(12)

        theme_title = QLabel("🎨  Appearance")
        theme_title.setProperty("class", "card-title")
        theme_layout.addWidget(theme_title)

        toggle_row = QHBoxLayout()
        toggle_row.addWidget(QLabel("Dark Mode"))

        self.theme_toggle = QCheckBox()
        self.theme_toggle.setChecked(self.current_theme == "dark")
        self.theme_toggle.toggled.connect(self._on_theme_toggle)
        toggle_row.addWidget(self.theme_toggle)
        toggle_row.addStretch()
        theme_layout.addLayout(toggle_row)

        layout.addWidget(theme_card)
        layout.addStretch()

    def _on_theme_toggle(self, checked):
        theme = "dark" if checked else "light"
        self.current_theme = theme
        self.theme_changed.emit(theme)
