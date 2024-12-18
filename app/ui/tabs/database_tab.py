from PyQt5.QtWidgets import QInputDialog, QWidget, QVBoxLayout, QPushButton, QMessageBox
from app.utils.db_utils import execute_procedure
import psycopg2


def delete_database():

    db_name = 'football_management'
    conn = psycopg2.connect(
        dbname="postgres", user="admin", password="secure_password", host='localhost', port='5433'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Завершаем все подключения к базе данных
    cursor.execute(f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{db_name}'
        AND pid <> pg_backend_pid();
    """)

    cursor.execute(f"DROP DATABASE {db_name}")


class DatabaseTab(QWidget):
    def __init__(self):
        super().__init__()

        self.clean_table_btn = QPushButton("Clean Table")
        self.clean_all_tables_btn = QPushButton("Clean All Tables")
        self.drop_db_btn = QPushButton("Drop Database")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.clean_table_btn.clicked.connect(self.clean_table)
        self.clean_all_tables_btn.clicked.connect(self.clean_all_tables)

        layout.addWidget(self.clean_table_btn)
        layout.addWidget(self.clean_all_tables_btn)

        self.drop_db_btn.clicked.connect(self.drop_database)

        layout.addWidget(self.drop_db_btn)
        self.setLayout(layout)

    def drop_database(self):
        confirm = QMessageBox.question(
            self, "Confirm Drop", "Are you sure you want to drop the entire database?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                delete_database()
                QMessageBox.information(self, "Success", "Database dropped successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to drop database:\n{e}")

    def clean_table(self):
        table_name, ok = self.get_table_name()
        if ok:
            execute_procedure("clean_table", table_name)
            QMessageBox.information(self, "Success", f"Table '{table_name}' cleaned successfully!")

    def clean_all_tables(self):
        execute_procedure("clean_all_tables")
        QMessageBox.information(self, "Success", "All tables cleaned successfully!")

    def get_table_name(self):
        table_name, ok = QInputDialog.getText(self, "Table Name", "Enter table name:")
        return table_name, ok
