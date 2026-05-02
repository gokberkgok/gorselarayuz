"""
Login / Register page with tab switching.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QStackedWidget, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import os


class LoginPage(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self._build_ui()

    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Left decorative panel
        left = QFrame()
        left.setStyleSheet("""
            QFrame {
                background-color: #F0F5FA;
                border-right: 1px solid #E8E8E8;
            }
        """)
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo Image
        logo_lbl = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(pixmap)
        else:
            logo_lbl.setText("ReserveApp")
            logo_lbl.setStyleSheet("font-size: 36px; font-weight: 700; color: #1890FF;")
        
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_lbl)
        left_layout.addSpacing(20)

        tagline = QLabel("Modern & Corporate\nReservation System")
        tagline.setStyleSheet("font-size: 18px; color: #54657E; font-weight: 500;")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(tagline)

        outer.addWidget(left, 1)

        # Right form panel
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(60, 40, 60, 40)

        # Tab buttons
        tab_row = QHBoxLayout()
        self.login_tab_btn = QPushButton("Login")
        self.login_tab_btn.setProperty("class", "primary-btn")
        self.login_tab_btn.clicked.connect(lambda: self._switch_tab(0))
        tab_row.addWidget(self.login_tab_btn)

        self.register_tab_btn = QPushButton("Register")
        self.register_tab_btn.setProperty("class", "outline-btn")
        self.register_tab_btn.clicked.connect(lambda: self._switch_tab(1))
        tab_row.addWidget(self.register_tab_btn)
        right_layout.addLayout(tab_row)
        right_layout.addSpacing(20)

        # Stacked forms
        self.stack = QStackedWidget()

        # Login form
        login_form = QWidget()
        lf = QVBoxLayout(login_form)
        lf.setSpacing(14)

        lbl = QLabel("Welcome Back")
        lbl.setProperty("class", "page-title")
        lf.addWidget(lbl)

        sub = QLabel("Sign in to your account")
        sub.setProperty("class", "page-subtitle")
        lf.addWidget(sub)

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("📧  Email address")
        self.login_email.setMinimumHeight(48)
        lf.addWidget(self.login_email)

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("🔒  Password")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setMinimumHeight(48)
        lf.addWidget(self.login_pass)

        self.login_error = QLabel("")
        self.login_error.setStyleSheet("color: #FF6B6B; font-size: 13px;")
        lf.addWidget(self.login_error)

        login_btn = QPushButton("🔑  Sign In")
        login_btn.setProperty("class", "primary-btn")
        login_btn.setMinimumHeight(48)
        login_btn.clicked.connect(self._do_login)
        lf.addWidget(login_btn)
        lf.addStretch()

        self.stack.addWidget(login_form)

        # Register form
        reg_form = QWidget()
        rf = QVBoxLayout(reg_form)
        rf.setSpacing(14)

        lbl2 = QLabel("Create Account")
        lbl2.setProperty("class", "page-title")
        rf.addWidget(lbl2)

        sub2 = QLabel("Fill in your details to get started")
        sub2.setProperty("class", "page-subtitle")
        rf.addWidget(sub2)

        self.reg_name = QLineEdit()
        self.reg_name.setPlaceholderText("👤  Full name")
        self.reg_name.setMinimumHeight(48)
        rf.addWidget(self.reg_name)

        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("📧  Email address")
        self.reg_email.setMinimumHeight(48)
        rf.addWidget(self.reg_email)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("🔒  Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setMinimumHeight(48)
        rf.addWidget(self.reg_pass)

        self.reg_error = QLabel("")
        self.reg_error.setStyleSheet("color: #FF6B6B; font-size: 13px;")
        rf.addWidget(self.reg_error)

        reg_btn = QPushButton("✨  Create Account")
        reg_btn.setProperty("class", "primary-btn")
        reg_btn.setMinimumHeight(48)
        reg_btn.clicked.connect(self._do_register)
        rf.addWidget(reg_btn)
        rf.addStretch()

        self.stack.addWidget(reg_form)
        right_layout.addWidget(self.stack)

        outer.addWidget(right, 1)

    def _switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        if idx == 0:
            self.login_tab_btn.setProperty("class", "primary-btn")
            self.register_tab_btn.setProperty("class", "outline-btn")
        else:
            self.login_tab_btn.setProperty("class", "outline-btn")
            self.register_tab_btn.setProperty("class", "primary-btn")
        # Force style refresh
        for btn in [self.login_tab_btn, self.register_tab_btn]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _do_login(self):
        email = self.login_email.text().strip()
        pwd = self.login_pass.text().strip()
        if not email or not pwd:
            self.login_error.setText("Please fill all fields")
            return
        try:
            data = self.api.login(email, pwd)
            self.login_success.emit(data)
        except Exception as e:
            self.login_error.setText(str(e))

    def _do_register(self):
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        pwd = self.reg_pass.text().strip()
        if not name or not email or not pwd:
            self.reg_error.setText("Please fill all fields")
            return
        try:
            data = self.api.register(name, email, pwd)
            self.login_success.emit(data)
        except Exception as e:
            self.reg_error.setText(str(e))
