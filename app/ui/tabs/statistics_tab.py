from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from app.utils.db_utils import execute_procedure


class StatisticsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.stats_player_id_input = QLineEdit()
        self.matches_played_input = QLineEdit()
        self.total_play_time_input = QLineEdit()
        self.goals_input = QLineEdit()
        self.assists_input = QLineEdit()
        self.tackles_input = QLineEdit()
        self.saves_input = QLineEdit()
        self.yellow_cards_input = QLineEdit()
        self.red_cards_input = QLineEdit()

        self.update_statistics_btn = QPushButton("Update Statistics")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input fields for statistics
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Player ID:"))
        form_layout.addWidget(self.stats_player_id_input)
        form_layout.addWidget(QLabel("Matches Played:"))
        form_layout.addWidget(self.matches_played_input)
        form_layout.addWidget(QLabel("Total Play Time:"))
        form_layout.addWidget(self.total_play_time_input)
        form_layout.addWidget(QLabel("Goals:"))
        form_layout.addWidget(self.goals_input)
        form_layout.addWidget(QLabel("Assists:"))
        form_layout.addWidget(self.assists_input)
        form_layout.addWidget(QLabel("Tackles:"))
        form_layout.addWidget(self.tackles_input)
        form_layout.addWidget(QLabel("Saves:"))
        form_layout.addWidget(self.saves_input)
        form_layout.addWidget(QLabel("Yellow Cards:"))
        form_layout.addWidget(self.yellow_cards_input)
        form_layout.addWidget(QLabel("Red Cards:"))
        form_layout.addWidget(self.red_cards_input)

        layout.addLayout(form_layout)

        self.update_statistics_btn.clicked.connect(self.update_statistics)

        layout.addWidget(self.update_statistics_btn)
        self.setLayout(layout)

    def update_statistics(self):
        # Check if required fields are empty
        if not self.stats_player_id_input.text() or not self.matches_played_input.text() or \
                not self.total_play_time_input.text() or not self.goals_input.text() or \
                not self.assists_input.text() or not self.tackles_input.text() or \
                not self.saves_input.text() or not self.yellow_cards_input.text() or \
                not self.red_cards_input.text():
            QMessageBox.warning(self, "Input Error", "Please fill in all fields before updating statistics.")
            return

        try:
            # Convert values to appropriate types
            player_id = int(self.stats_player_id_input.text())
            matches_played = int(self.matches_played_input.text())
            total_play_time = int(self.total_play_time_input.text())
            goals = int(self.goals_input.text())
            assists = int(self.assists_input.text())
            tackles = int(self.tackles_input.text())
            saves = int(self.saves_input.text())
            yellow_cards = int(self.yellow_cards_input.text())
            red_cards = int(self.red_cards_input.text())

            execute_procedure(
                "update_statistics",
                player_id,
                matches_played,
                total_play_time,
                goals,
                assists,
                tackles,
                saves,
                yellow_cards,
                red_cards
            )
            QMessageBox.information(self, "Success", "Statistics updated successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "All numerical fields must be valid numbers.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating statistics:\n{e}")
