from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from app.utils.helpers import is_valid_date
from app.utils.db_utils import execute_procedure


class ContractTab(QWidget):
    def __init__(self):
        super().__init__()

        self.contract_player_id_input = QLineEdit()
        self.sign_date_input = QLineEdit()
        self.end_date_input = QLineEdit()
        self.monthly_salary_input = QLineEdit()

        self.update_contract_btn = QPushButton("Update Contract")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input fields for contracts
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Player ID:"))
        form_layout.addWidget(self.contract_player_id_input)
        form_layout.addWidget(QLabel("Sign Date (YYYY-MM-DD):"))
        form_layout.addWidget(self.sign_date_input)
        form_layout.addWidget(QLabel("End Date (YYYY-MM-DD):"))
        form_layout.addWidget(self.end_date_input)
        form_layout.addWidget(QLabel("Monthly Salary:"))
        form_layout.addWidget(self.monthly_salary_input)

        layout.addLayout(form_layout)

        # Buttons
        self.update_contract_btn.clicked.connect(self.update_contract)

        layout.addWidget(self.update_contract_btn)
        self.setLayout(layout)

    def update_contract(self):
        # Check if required fields are empty
        if not self.contract_player_id_input.text() or not self.sign_date_input.text() or \
                not self.end_date_input.text() or not self.monthly_salary_input.text():
            QMessageBox.warning(self, "Input Error", "Please fill in all fields before updating a contract.")
            return

        if not is_valid_date(self.sign_date_input.text() or self.end_date_input.text()):
            QMessageBox.warning(self, "Input Error", "Date must be in the format YYYY-MM-DD.")
            return

        try:
            # Convert values to appropriate types
            player_id = int(self.contract_player_id_input.text())
            monthly_salary = float(self.monthly_salary_input.text())
            execute_procedure(
                "update_contract",
                player_id,
                self.sign_date_input.text(),
                self.end_date_input.text(),
                monthly_salary
            )
            QMessageBox.information(self, "Success", "Contract updated successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error",
                                "Player ID must be an integer and Monthly Salary must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating contract:\n{e}")
