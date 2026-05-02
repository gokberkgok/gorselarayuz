"""
Sidebar navigation component.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import os


class Sidebar(QWidget):
    page_changed = pyqtSignal(str)

    USER_PAGES = [
        ("🏠", "Home", "home"),
        ("🔍", "Browse", "browse"),
        ("📋", "My Reservations", "my_reservations"),
        ("⚙️", "Settings", "settings"),
    ]
    ADMIN_PAGES = [
        ("📊", "Dashboard", "admin_dashboard"),
        ("🏨", "Manage Places", "admin_places"),
        ("📋", "Reservations", "admin_reservations"),
        ("⚙️", "Settings", "settings"),
    ]

    def __init__(self, role="user", user_name="User"):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(260)
        self.role = role
        self.buttons = {}
        self.current_page = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 24)
        layout.setSpacing(8)

        # Logo Image
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(20, 0, 20, 16)
        logo_lbl = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Scale to a reasonable height, keeping aspect ratio
            pixmap = pixmap.scaledToHeight(40, Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(pixmap)
        else:
            logo_lbl.setText("ReserveApp")
            logo_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #1890FF;")
        
        logo_layout.addWidget(logo_lbl)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)

        # Top spacer to push buttons slightly down
        layout.addSpacing(8)

        pages = self.ADMIN_PAGES if role == "admin" else self.USER_PAGES
        for icon, label, key in pages:
            btn = QPushButton(f"  {icon}   {label}")
            btn.setProperty("class", "nav-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor if hasattr(Qt, 'CursorShape') else None)
            btn.clicked.connect(lambda checked, k=key: self._on_click(k))
            layout.addWidget(btn)
            self.buttons[key] = btn

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Bottom User Info Area
        user_info_layout = QVBoxLayout()
        user_info_layout.setContentsMargins(20, 0, 20, 8)
        
        # A tiny separator line
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #334155; margin-bottom: 8px;")
        user_info_layout.addWidget(sep)

        subtitle = QLabel(f"<b>{user_name}</b><br><span style='color:#94a3b8; font-size:12px;'>{'Admin' if role == 'admin' else 'User'}</span>")
        subtitle.setStyleSheet("color: #f8fafc; font-size: 14px;")
        subtitle.setWordWrap(True)
        user_info_layout.addWidget(subtitle)
        
        layout.addLayout(user_info_layout)

        # Logout button
        logout_btn = QPushButton("  🚪   Logout")
        logout_btn.setProperty("class", "nav-btn logout-btn")
        logout_btn.clicked.connect(lambda: self.page_changed.emit("logout"))
        layout.addWidget(logout_btn)
        layout.addSpacing(12)

    def _on_click(self, key):
        self.set_active(key)
        self.page_changed.emit(key)

    def set_active(self, key):
        self.current_page = key
        for k, btn in self.buttons.items():
            btn.setProperty("active", "true" if k == key else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)


from PyQt6.QtCore import Qt
