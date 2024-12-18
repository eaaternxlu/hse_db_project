from PyQt5.QtWidgets import QApplication
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ui.main_window import DatabaseApp

os.environ['QT_QPA_PLATFORM'] = 'windows'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())
