"""
Theme system — Dark and Light QSS stylesheets for PyQt6.
"""

COLORS = {
    "light": {
        "bg": "#F4F7F9",
        "card": "#FFFFFF",
        "sidebar": "#FFFFFF",
        "sidebar_text": "#54657E",
        "sidebar_active": "#1890FF",
        "sidebar_active_bg": "#E6F7FF",
        "primary": "#1890FF",
        "primary_hover": "#40A9FF",
        "accent": "#FF4D4F",
        "text": "#262626",
        "text_secondary": "#8C8C8C",
        "border": "#E8E8E8",
        "success": "#52C41A",
        "warning": "#FAAD14",
        "danger": "#FF4D4F",
        "input_bg": "#FFFFFF",
    },
    "dark": {
        "bg": "#141414",
        "card": "#1F1F1F",
        "sidebar": "#1F1F1F",
        "sidebar_text": "#A6A6A6",
        "sidebar_active": "#177DDC",
        "sidebar_active_bg": "#112A45",
        "primary": "#177DDC",
        "primary_hover": "#3C9AE8",
        "accent": "#D9363E",
        "text": "#E0E0E0",
        "text_secondary": "#8C8C8C",
        "border": "#303030",
        "success": "#49AA19",
        "warning": "#D89614",
        "danger": "#D9363E",
        "input_bg": "#141414",
    },
}

def get_stylesheet(theme="light"):
    c = COLORS[theme]
    return f"""
    /* ── Global ─────────────────────────────── */
    QMainWindow, QWidget#centralWidget {{
        background-color: {c['bg']};
    }}
    QWidget {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        font-size: 14px;
        color: {c['text']};
    }}

    /* ── Sidebar ────────────────────────────── */
    QWidget#sidebar {{
        background-color: {c['sidebar']};
        border-right: 1px solid {c['border']};
        min-width: 250px;
        max-width: 250px;
    }}
    QPushButton.nav-btn {{
        background: transparent;
        color: {c['sidebar_text']};
        border: none;
        text-align: left;
        padding: 16px 24px;
        font-size: 15px;
        font-weight: 500;
        border-radius: 8px;
        margin: 4px 16px;
    }}
    QPushButton.nav-btn:hover {{
        background-color: {c['bg']};
        color: {c['primary']};
    }}
    QPushButton.nav-btn[active="true"] {{
        background-color: {c['sidebar_active_bg']};
        color: {c['sidebar_active']};
        font-weight: 600;
        border-left: 4px solid {c['sidebar_active']};
        border-radius: 4px;
    }}
    QLabel#sidebarSubtitle {{
        color: {c['sidebar_text']};
        font-size: 13px;
        padding: 0 24px 24px 24px;
        font-weight: 500;
    }}

    /* ── Cards ──────────────────────────────── */
    QFrame.card {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        padding: 24px;
    }}
    QFrame.card:hover {{
        border: 1px solid {c['primary']};
        background-color: {c['card']};
    }}
    QFrame.stat-card {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        padding: 24px;
    }}

    /* ── Buttons ────────────────────────────── */
    QPushButton.primary-btn {{
        background-color: {c['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
    }}
    QPushButton.primary-btn:hover {{
        background-color: {c['primary_hover']};
    }}
    QPushButton.danger-btn {{
        background-color: {c['danger']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }}
    QPushButton.danger-btn:hover {{
        background-color: #FF7875;
    }}
    QPushButton.success-btn {{
        background-color: {c['success']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }}
    QPushButton.success-btn:hover {{
        background-color: #73D13D;
    }}
    QPushButton.outline-btn {{
        background-color: transparent;
        color: {c['primary']};
        border: 1px solid {c['primary']};
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }}
    QPushButton.outline-btn:hover {{
        background-color: {c['sidebar_active_bg']};
    }}

    /* ── Inputs ─────────────────────────────── */
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {{
        background-color: {c['input_bg']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        color: {c['text']};
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {{
        border: 1px solid {c['primary']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        color: {c['text']};
        selection-background-color: {c['sidebar_active_bg']};
        selection-color: {c['primary']};
    }}

    /* ── Labels ─────────────────────────────── */
    QLabel.page-title {{
        font-size: 28px;
        font-weight: 800;
        color: {c['text']};
        padding-bottom: 4px;
        letter-spacing: -0.5px;
    }}
    QLabel.page-subtitle {{
        font-size: 15px;
        color: {c['text_secondary']};
        padding-bottom: 24px;
    }}
    QLabel.card-title {{
        font-size: 18px;
        font-weight: 700;
        color: {c['text']};
    }}
    QLabel.card-desc {{
        font-size: 14px;
        color: {c['text_secondary']};
        line-height: 1.5;
    }}
    QLabel.stat-value {{
        font-size: 36px;
        font-weight: 800;
        color: {c['primary']};
    }}
    QLabel.stat-label {{
        font-size: 14px;
        color: {c['text_secondary']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* ── Status Badges ──────────────────────── */
    QLabel.status-pending {{
        background-color: #FFFBE6;
        color: #FAAD14;
        border: 1px solid #FFE58F;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }}
    QLabel.status-approved {{
        background-color: #F6FFED;
        color: #52C41A;
        border: 1px solid #B7EB8F;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }}
    QLabel.status-cancelled, QLabel.status-rejected {{
        background-color: #FFF2F0;
        color: #FF4D4F;
        border: 1px solid #FFCCC7;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }}

    /* ── Type Badge ─────────────────────────── */
    QLabel.type-badge {{
        background-color: {c['sidebar_active_bg']};
        color: {c['primary']};
        border: 1px solid #91D5FF;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }}

    /* ── Scroll ─────────────────────────────── */
    QScrollArea {{
        border: none;
        background: transparent;
    }}
    QScrollArea > QWidget > QWidget {{
        background: transparent;
    }}
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: #D9D9D9;
        border-radius: 4px;
        min-height: 40px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #BFBFBF;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    /* ── Table ──────────────────────────────── */
    QTableWidget {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        gridline-color: {c['bg']};
        font-size: 14px;
    }}
    QTableWidget::item {{
        padding: 16px 12px;
        border-bottom: 1px solid {c['bg']};
    }}
    QHeaderView::section {{
        background-color: {c['bg']};
        color: {c['text_secondary']};
        font-weight: 600;
        font-size: 13px;
        padding: 16px 12px;
        border: none;
        border-bottom: 2px solid {c['border']};
        text-align: left;
    }}

    /* ── Dialog ─────────────────────────────── */
    QDialog {{
        background-color: {c['card']};
        border-radius: 16px;
    }}

    /* ── Toggle Switch ─────────────────────── */
    QCheckBox {{
        spacing: 12px;
        font-size: 14px;
        color: {c['text']};
        font-weight: 500;
    }}
    QCheckBox::indicator {{
        width: 44px;
        height: 24px;
        border-radius: 12px;
        background-color: {c['border']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {c['primary']};
    }}

    /* ── Toast ──────────────────────────────── */
    QFrame.toast-success {{
        background-color: {c['success']};
        color: white;
        border-radius: 8px;
        padding: 16px 24px;
        border: 1px solid #389E0D;
    }}
    QFrame.toast-error {{
        background-color: {c['danger']};
        color: white;
        border-radius: 8px;
        padding: 16px 24px;
        border: 1px solid #CF1322;
    }}
    QFrame.toast-info {{
        background-color: {c['primary']};
        color: white;
        border-radius: 8px;
        padding: 16px 24px;
        border: 1px solid #096DD9;
    }}
    """
