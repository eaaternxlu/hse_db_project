from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from app.utils.helpers import is_valid_date
from app.utils.db_utils import execute_procedure


class PlayerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.nationality_input = QLineEdit()
        self.main_position_input = QLineEdit()
        self.estimated_market_price_input = QLineEdit()
        self.player_id_input = QLineEdit()

        self.add_player_btn = QPushButton("Add Player")
        self.update_player_btn = QPushButton("Update Player")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input fields for player
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("First Name:"))
        form_layout.addWidget(self.first_name_input)
        form_layout.addWidget(QLabel("Last Name:"))
        form_layout.addWidget(self.last_name_input)
        form_layout.addWidget(QLabel("Date of Birth (YYYY-MM-DD):"))
        form_layout.addWidget(self.dob_input)
        form_layout.addWidget(QLabel("Nationality:"))
        form_layout.addWidget(self.nationality_input)
        form_layout.addWidget(QLabel("Main Position:"))
        form_layout.addWidget(self.main_position_input)
        form_layout.addWidget(QLabel("Estimated Market Price:"))
        form_layout.addWidget(self.estimated_market_price_input)
        form_layout.addWidget(QLabel("Player ID (for updating):"))
        form_layout.addWidget(self.player_id_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_player_btn.clicked.connect(self.add_player)
        self.update_player_btn.clicked.connect(self.update_player)

        button_layout.addWidget(self.add_player_btn)
        button_layout.addWidget(self.update_player_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_player(self):
        # Check for empty fields
        if not self.first_name_input.text() or not self.last_name_input.text() or not self.dob_input.text() or \
                not self.nationality_input.text() or not self.main_position_input.text() or \
                not self.estimated_market_price_input.text():
            QMessageBox.warning(self, "Input Error", "Please fill in all fields before adding a player.")
            return

        # Validate date
        if not is_valid_date(self.dob_input.text()):
            QMessageBox.warning(self, "Input Error", "Date of Birth must be in the format YYYY-MM-DD.")
            return

        try:
            # Validate market price
            estimated_market_price = float(self.estimated_market_price_input.text())

            execute_procedure(
                "add_player",
                self.first_name_input.text(),
                self.last_name_input.text(),
                self.dob_input.text(),
                self.nationality_input.text(),
                self.main_position_input.text(),
                estimated_market_price
            )
            QMessageBox.information(self, "Success", "Player added successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Estimated Market Price must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding player:\n{e}")

    def update_player(self):
        # Check if player ID is provided
        if not self.player_id_input.text() or not self.first_name_input.text() or not self.last_name_input.text() or \
                not self.dob_input.text() or not self.nationality_input.text() or not self.main_position_input.text() \
                or not self.estimated_market_price_input.text():
            QMessageBox.warning(self, "Input Error", "Please fill in all fields before updating a player.")
            return

        if not is_valid_date(self.dob_input.text()):
            QMessageBox.warning(self, "Input Error", "Date of Birth must be in the format YYYY-MM-DD.")
            return

        try:
            # Convert player ID and market price to appropriate types
            player_id = int(self.player_id_input.text())
            estimated_market_price = float(self.estimated_market_price_input.text())

            execute_procedure(
                "update_player",
                player_id,
                self.first_name_input.text(),
                self.last_name_input.text(),
                self.dob_input.text(),
                self.nationality_input.text(),
                self.main_position_input.text(),
                estimated_market_price
            )
            QMessageBox.information(self, "Success", "Player updated successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error",
                                "Player ID must be a valid integer and Market Price a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating player:\n{e}")
