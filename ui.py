from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget
from file_handling import process_html_file, save_to_csv


class JobScraperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Job Scraper")
        self.setGeometry(800, 400, 500, 300)

        # Create main layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()  # A vertical layout to organize the UI elements from top to bottom.
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # Label
        self.label = QLabel("Upload an HTML file to scrape job listings and save to CSV")
        self.label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.label)

        # Buttons
        self.upload_button = QPushButton("Upload File")
        self.upload_button.setStyleSheet("font-size: 12pt;")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.process_button = QPushButton("Save to CSV")
        self.process_button.setStyleSheet("font-size: 12pt;")
        self.process_button.clicked.connect(self.process_and_save)
        self.layout.addWidget(self.process_button)

        self.file_path = None

    def upload_file(self):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open HTML File", "", "HTML Files (*.html)")
        if file_path:
            self.file_path = file_path
            # todo logs: QMessageBox.information(self, "File Uploaded", "File uploaded successfully!")

    def process_and_save(self):
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please upload a file first.")
            return

        try:
            jobs = process_html_file(self.file_path)
            if jobs:
                save_to_csv(jobs)
                # todo logs: QMessageBox.information(self, "Success", f"Processed {len(jobs)} jobs. Data saved to 'jobs.csv'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
