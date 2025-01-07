from PyQt5.QtWidgets import QApplication
from ui import JobScraperApp
import sys

if __name__ == "__main__":
    app = QApplication([])  # Manages all the basic processes related to a GUI application.
    window = JobScraperApp()
    window.show()
    sys.exit(app.exec_())
