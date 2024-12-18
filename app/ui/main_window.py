from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from app.ui.tabs.player_tab import PlayerTab
from app.ui.tabs.contract_tab import ContractTab
from app.ui.tabs.statistics_tab import StatisticsTab
from app.ui.tabs.utilities_tab import UtilitiesTab
from app.ui.tabs.database_tab import DatabaseTab


class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FC Barcelona Database Management")
        self.setGeometry(0, 0, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.player_tab = PlayerTab()
        self.contract_tab = ContractTab()
        self.statistics_tab = StatisticsTab()
        self.utilities_tab = UtilitiesTab()
        self.database_tab = DatabaseTab()

        self.tabs.addTab(self.player_tab, "Player Management")
        self.tabs.addTab(self.statistics_tab, "Statistics Management")
        self.tabs.addTab(self.contract_tab, "Contract Management")
        self.tabs.addTab(self.utilities_tab, "Utilities")
        self.tabs.addTab(self.database_tab, "Database Management")
