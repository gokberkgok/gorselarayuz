"""
Toast notification — slide-in notification widget.
"""
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt


class Toast(QFrame):
    def __init__(self, parent, message, toast_type="success", duration=3000):
        super().__init__(parent)
        self.setProperty("class", f"toast-{toast_type}")
        self.setFixedHeight(50)
        self.setMinimumWidth(300)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        icons = {"success": "✅", "error": "❌", "info": "ℹ️"}
        lbl = QLabel(f"  {icons.get(toast_type, '')}  {message}")
        lbl.setStyleSheet("color: white; font-weight: 600; font-size: 14px; background: transparent; border: none;")
        layout.addWidget(lbl)

        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)

        self.move(parent.width() - self.width() - 20, 20)
        self.show()
        self.raise_()

        self.fade_in = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_in.start()

        QTimer.singleShot(duration, self._fade_out)

    def _fade_out(self):
        self.fade_out = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out.finished.connect(self.deleteLater)
        self.fade_out.start()
