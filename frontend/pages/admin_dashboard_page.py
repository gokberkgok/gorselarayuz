"""
Admin Dashboard — overview stats with cards.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal


class AdminDashboardPage(QWidget):
    navigate_requested = pyqtSignal(str)

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header Row
        header = QHBoxLayout()
        title_l = QVBoxLayout()
        title = QLabel("📊  Yönetici Paneli")
        title.setProperty("class", "page-title")
        sub = QLabel("Rezervasyon sistemine genel bakış")
        sub.setProperty("class", "page-subtitle")
        title_l.addWidget(title)
        title_l.addWidget(sub)
        header.addLayout(title_l)
        header.addStretch()

        # Quick Actions
        qa_layout = QHBoxLayout()
        qa_layout.setSpacing(6)
        
        btn_places = QPushButton("🏨 Mekanları Yönet")
        btn_places.setProperty("class", "primary-btn")
        btn_places.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_places.clicked.connect(lambda: self.navigate_requested.emit("admin_places"))
        
        btn_res = QPushButton("📋 Tüm Rezervasyonlar")
        btn_res.setProperty("class", "outline-btn")
        btn_res.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_res.clicked.connect(lambda: self.navigate_requested.emit("admin_reservations"))
        
        qa_layout.addWidget(btn_places)
        qa_layout.addWidget(btn_res)
        header.addLayout(qa_layout)
        
        layout.addLayout(header)

        # Stats Grid (Using Grid to prevent squishing)
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(10)
        layout.addLayout(self.stats_grid)

        # Recent Reservations Section
        res_title = QLabel("🕒 Son Rezervasyon İstekleri")
        res_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #ffffff; margin-top: 16px; margin-bottom: 8px;")
        layout.addWidget(res_title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Kullanıcı", "Mekan", "Tarih & Saat", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 120)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.table)

    def _make_stat_card(self, icon, label, value, color="#60a5fa"):
        card = QFrame()
        card.setProperty("class", "card")
        card.setMinimumHeight(70)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        cl = QHBoxLayout(card)
        cl.setContentsMargins(16, 12, 16, 12)
        cl.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 24px; background: transparent; border: none;")
        cl.addWidget(icon_lbl)

        text_l = QVBoxLayout()
        text_l.setSpacing(0)
        val_lbl = QLabel(str(value))
        val_lbl.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: 700; background: transparent;")
        name_lbl = QLabel(label)
        name_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600; background: transparent;")
        
        text_l.addWidget(val_lbl)
        text_l.addWidget(name_lbl)
        cl.addLayout(text_l)
        cl.addStretch()

        return card

    def load_data(self):
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            stats = self.api.get_stats()
            cards = [
                ("👥", "Kullanıcılar", stats["total_users"], "#60a5fa"),
                ("🏨", "Mekanlar", stats["total_places"], "#34d399"),
                ("📋", "Toplam Rez.", stats["total_reservations"], "#a78bfa"),
                ("⏳", "Bekliyor", stats["pending_reservations"], "#fbbf24"),
                ("✅", "Onaylandı", stats["approved_reservations"], "#10b981"),
            ]
            for i, (icon, label, value, color) in enumerate(cards):
                card = self._make_stat_card(icon, label, value, color)
                row, col = divmod(i, 3) # Wrap at 3 cards per row
                self.stats_grid.addWidget(card, row, col)
        except Exception as e:
            err = QLabel(f"❌ İstatistikler yüklenirken hata oluştu: {e}")
            err.setStyleSheet("color: #ef4444;")
            self.stats_grid.addWidget(err, 0, 0)

        self.table.setRowCount(0)
        try:
            reservations = self.api.get_all_reservations()
            recent = reservations[:5]
            self.table.setRowCount(len(recent))
            for i, r in enumerate(recent):
                self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
                self.table.setItem(i, 1, QTableWidgetItem(r.get("user_name", "")))
                self.table.setItem(i, 2, QTableWidgetItem(r.get("place_name", "")))
                self.table.setItem(i, 3, QTableWidgetItem(f"{r['date']} {r['start_time']}"))
                
                st = r["status"]
                
                # Türkçe Durum Metinleri
                tr_status = st
                if st == "pending": tr_status = "BEKLİYOR"
                elif st == "approved": tr_status = "ONAYLANDI"
                elif st == "cancelled": tr_status = "İPTAL"
                elif st == "rejected": tr_status = "REDDEDİLDİ"

                st_lbl = QLabel(f"  {tr_status}  ")
                st_lbl.setProperty("class", f"status-{st}")
                st_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 4, st_lbl)
                self.table.setRowHeight(i, 60)
        except Exception as e:
            print("Son rezervasyonlar yüklenirken hata oluştu:", e)
