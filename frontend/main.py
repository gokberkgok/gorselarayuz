"""
Main application entry point — PyQt6 desktop app.
QMainWindow with sidebar navigation and QStackedWidget pages.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QStackedWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt, QSize

from frontend.api_client import ApiClient
from frontend.theme import get_stylesheet
from frontend.components.sidebar import Sidebar
from frontend.components.toast import Toast
from frontend.components.dialogs import ReservationDialog
from frontend.pages.login_page import LoginPage
from frontend.pages.home_page import HomePage
from frontend.pages.browse_page import BrowsePage
from frontend.pages.my_reservations_page import MyReservationsPage
from frontend.pages.settings_page import SettingsPage
from frontend.pages.admin_dashboard_page import AdminDashboardPage
from frontend.pages.admin_places_page import AdminPlacesPage
from frontend.pages.admin_reservations_page import AdminReservationsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReserveApp — Reservation System")
        self.setMinimumSize(QSize(1200, 750))
        self.resize(1400, 850)

        self.api = ApiClient()
        self.current_theme = "light"
        self.sidebar = None
        self.pages = {}

        # Central widget
        self.central = QWidget()
        self.central.setObjectName("centralWidget")
        self.setCentralWidget(self.central)
        self.main_layout = QHBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Full-window stacked widget (login vs app)
        self.root_stack = QStackedWidget()
        self.main_layout.addWidget(self.root_stack)

        # Login page
        self.login_page = LoginPage(self.api)
        self.login_page.login_success.connect(self._on_login)
        self.root_stack.addWidget(self.login_page)

        # App container (sidebar + page stack)
        self.app_container = QWidget()
        self.app_layout = QHBoxLayout(self.app_container)
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.app_layout.setSpacing(0)
        self.root_stack.addWidget(self.app_container)

        self._apply_theme()

    def _on_login(self, data):
        """Called after successful login. Build the app UI."""
        role = data.get("role", "user")

        # Clear existing app layout
        while self.app_layout.count():
            item = self.app_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Sidebar
        self.sidebar = Sidebar(role=role, user_name=data.get("name", "User"))
        self.sidebar.page_changed.connect(self._on_page_changed)
        self.app_layout.addWidget(self.sidebar)

        # Page stack
        self.page_stack = QStackedWidget()
        self.app_layout.addWidget(self.page_stack)

        # Build pages based on role
        self.pages = {}
        if role == "admin":
            dashboard = AdminDashboardPage(self.api)
            dashboard.navigate_requested.connect(self._on_dashboard_navigate)
            self._add_page("admin_dashboard", dashboard)
            self._add_page("admin_places", AdminPlacesPage(self.api, self._show_toast))
            self._add_page("admin_reservations", AdminReservationsPage(self.api, self._show_toast))
            self._add_page("settings", SettingsPage(self.api, self.current_theme))
        else:
            home = HomePage(self.api)
            home.reserve_requested.connect(self._open_reservation_dialog)
            self._add_page("home", home)

            browse = BrowsePage(self.api)
            browse.reserve_requested.connect(self._open_reservation_dialog)
            self._add_page("browse", browse)

            self._add_page("my_reservations", MyReservationsPage(self.api, self._show_toast))
            self._add_page("settings", SettingsPage(self.api, self.current_theme))

        # Connect settings theme signal
        if "settings" in self.pages:
            self.pages["settings"].theme_changed.connect(self._on_theme_changed)

        # Navigate to first page
        first_page = "admin_dashboard" if role == "admin" else "home"
        self._on_page_changed(first_page)
        self.sidebar.set_active(first_page)

        self.root_stack.setCurrentIndex(1)

    def _add_page(self, key, widget):
        self.pages[key] = widget
        self.page_stack.addWidget(widget)

    def _on_dashboard_navigate(self, page_key):
        if self.sidebar:
            self.sidebar.set_active(page_key)
        self._on_page_changed(page_key)

    def _on_page_changed(self, page_key):
        if page_key == "logout":
            self._logout()
            return

        if page_key in self.pages:
            widget = self.pages[page_key]
            self.page_stack.setCurrentWidget(widget)

            # Load/refresh data
            if hasattr(widget, "load_data"):
                widget.load_data()

    def _logout(self):
        self.api.logout()
        self.root_stack.setCurrentIndex(0)

    def _open_reservation_dialog(self, place_data):
        dlg = ReservationDialog(self, place_data)
        if dlg.exec() and dlg.result_data:
            try:
                self.api.create_reservation(**dlg.result_data)
                self._show_toast("Reservation created successfully!", "success")
            except Exception as e:
                self._show_toast(str(e), "error")

    def _show_toast(self, message, toast_type="info"):
        Toast(self, message, toast_type)

    def _on_theme_changed(self, theme):
        self.current_theme = theme
        self._apply_theme()

    def _apply_theme(self):
        base_style = get_stylesheet(self.current_theme)
        
        # Load external style.qss for custom styling
        import os
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        external_style = ""
        if os.path.exists(qss_path):
            try:
                with open(qss_path, "r", encoding="utf-8") as f:
                    external_style = f.read()
            except Exception as e:
                print(f"Error loading style.qss: {e}")
                
        self.setStyleSheet(base_style + "\n" + external_style)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
