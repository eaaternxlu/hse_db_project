from PyQt5.QtWidgets import QTableWidgetItem, QInputDialog, QTableWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox
from app.utils.db_utils import execute_procedure
from PyQt5.QtCore import Qt


class UtilitiesTab(QWidget):
    def __init__(self):
        super().__init__()

        self.output_table = QTableWidget()

        self.display_players_btn = QPushButton("Display Players")
        self.display_contracts_btn = QPushButton("Display Contracts")
        self.display_statistics_btn = QPushButton("Display Statistics")
        self.display_avg_performance_btn = QPushButton("Display Avg Performance")
        self.search_player_btn = QPushButton("Search by Last Name")
        self.delete_player_btn = QPushButton("Delete Player")
        self.delete_selected_btn = QPushButton("Delete Selected")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.output_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.output_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.output_table)

        # Connect buttons to respective methods
        self.delete_player_btn.clicked.connect(self.delete_player)
        self.display_players_btn.clicked.connect(self.display_players_contents)
        self.display_contracts_btn.clicked.connect(self.display_contracts_contents)
        self.display_statistics_btn.clicked.connect(self.display_statistics_contents)
        self.display_avg_performance_btn.clicked.connect(self.display_avg_performance)
        self.search_player_btn.clicked.connect(self.search_by_last_name)
        self.delete_selected_btn.clicked.connect(self.delete_selected)

        # Add buttons to the layout
        layout.addWidget(self.search_player_btn)
        layout.addWidget(self.delete_player_btn)
        layout.addWidget(self.delete_selected_btn)
        layout.addWidget(self.display_players_btn)
        layout.addWidget(self.display_contracts_btn)
        layout.addWidget(self.display_statistics_btn)
        layout.addWidget(self.display_avg_performance_btn)

        self.setLayout(layout)

    def delete_selected(self):
        selected_row = self.output_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        # Assuming the first column contains the primary key (e.g., player ID)
        primary_key_item = self.output_table.item(selected_row, 0)
        primary_key = primary_key_item.text()

        # Confirmation dialog
        confirm = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete the item with ID {primary_key}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            # Delete from database
            try:
                execute_procedure("delete_by_id", int(primary_key))
                # Remove from the table
                self.output_table.removeRow(selected_row)
                QMessageBox.information(self, "Success", f"Item with ID {primary_key} deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete item with ID {primary_key}:\n{e}")

    def delete_player(self):
        last_name, ok = QInputDialog.getText(self, "Delete Player", "Enter the last name:")
        if ok:
            execute_procedure("delete_player", last_name)
            QMessageBox.information(self, "Success", "Player deleted successfully!")

    def search_by_last_name(self):
        last_name, ok = QInputDialog.getText(self, "Search Player", "Enter the last name:")
        if last_name and ok:
            result = execute_procedure("search_by_last_name", last_name)
            self.show_results(result, 'search_by_last_name')

    def display_players_contents(self):
        result = execute_procedure("display_players_contents")
        self.show_results(result, 'players')

    def display_avg_performance(self):
        result = execute_procedure("display_avg_performance_contents")
        self.show_results(result, 'avg_performance')

    def display_contracts_contents(self):
        result = execute_procedure("display_contracts_contents")
        self.show_results(result, 'contracts')

    def display_statistics_contents(self):
        result = execute_procedure("display_statistics_contents")
        self.show_results(result, 'statistics')

    def show_results(self, results, table_name):
        if results:
            # Set row count and column count
            self.output_table.setRowCount(len(results))
            self.output_table.setColumnCount(len(results[0]))

            # Set column names explicitly for different tables
            if table_name == 'players':
                column_headers = ["Player ID", "First Name", "Last Name", "Date of Birth", "Nationality",
                                  "Main Position", "Estimated Market Price"]
            elif table_name == 'search_by_last_name':
                column_headers = ["Player ID", "First Name", "Last Name", "Date of Birth", "Nationality",
                                  "Main Position", "Estimated Market Price", "Matches Played",
                                  "Total Play Time (minutes)",
                                  "Goals", "Assists", "Tackles", "Saves", "Yellow Cards", "Red Cards"]
            elif table_name == 'contracts':
                column_headers = ["Player ID", "First Name", "Last Name", "Sign Date", "End Date", "Monthly Salary"]
            elif table_name == 'statistics':
                column_headers = ["Player ID", "First Name", "Last Name", "Matches Played", "Total Play Time", "Goals",
                                  "Assists",
                                  "Tackles", "Saves", "Yellow Cards", "Red Cards"]
            elif table_name == 'avg_performance':
                column_headers = ["Player ID", "First Name", "Last Name", "Average Performance"]
            else:
                column_headers = ["Unknown Columns"]

            # Set the column headers in the table
            self.output_table.setHorizontalHeaderLabels(column_headers)

            # Fill the table with data
            for row_idx, row in enumerate(results):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable
                    self.output_table.setItem(row_idx, col_idx, item)
        else:
            self.output_table.setRowCount(0)
            self.output_table.setColumnCount(0)
            QMessageBox.information(self, "Results", "No data found!")
