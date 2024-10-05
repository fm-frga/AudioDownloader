from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QPushButton, QWidget, QComboBox, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QLinearGradient, QPalette, QColor
from audio_formats import get_format_names
import traceback

class MainWindow(QMainWindow):
    download_signal = Signal(str, int)
    cancel_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Playlist Downloader")
        self.setGeometry(100, 100, 600, 350)

        try:
            self.setup_ui()
        except Exception as e:
            self.show_error_message("Error setting up UI", str(e))

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#1E3A8A"))  # Dark blue
        gradient.setColorAt(1, QColor("#3B82F6"))  # Light blue

        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        title_label = QLabel("YouTube Playlist Downloader")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin: 20px 0;
        """)
        main_layout.addWidget(title_label)

        self.playlist_link_input = QLineEdit()
        self.playlist_link_input.setPlaceholderText("Enter playlist link...")
        self.playlist_link_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 12px;
                border: 2px solid #60A5FA;
                border-radius: 8px;
                background-color: #E0F2FE;
                color: #1E3A8A;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)
        main_layout.addWidget(self.playlist_link_input)

        format_layout = QHBoxLayout()
        format_label = QLabel("Select Format:")
        format_label.setStyleSheet("color: white; font-size: 18px;")
        self.format_combo = QComboBox()
        try:
            self.format_combo.addItems(get_format_names())
        except Exception as e:
            self.show_error_message("Error loading audio formats", str(e))
        self.format_combo.setStyleSheet("""
            QComboBox {
                font-size: 18px;
                padding: 8px;
                border: 2px solid #60A5FA;
                border-radius: 8px;
                background-color: #E0F2FE;
                color: #1E3A8A;
            }
        """)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        main_layout.addLayout(format_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        self.download_button = QPushButton("Download")
        self.cancel_button = QPushButton("Cancel")
        for button in (self.download_button, self.cancel_button):
            button.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 12px 24px;
                    background-color: #10B981;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
                QPushButton:disabled {
                    background-color: #9CA3AF;
                }
            """)
            button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.on_download_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 24px;
            color: white;
            margin: 20px 0;
        """)
        main_layout.addWidget(self.status_label)

    def closeEvent(self, event):
        try:
            self.cancel_signal.emit()
            event.accept()
        except Exception as e:
            self.show_error_message("Error while closing", str(e))
            event.ignore()

    def on_download_clicked(self):
        try:
            playlist_link = self.playlist_link_input.text()
            format_index = self.format_combo.currentIndex() + 1
            if playlist_link:
                self.download_signal.emit(playlist_link, format_index)
                self.download_button.setEnabled(False)
                self.cancel_button.setEnabled(True)
            else:
                self.status_label.setText("Please enter a playlist link.")
        except Exception as e:
            self.show_error_message("Error starting download", str(e))

    def on_cancel_clicked(self):
        try:
            self.cancel_signal.emit()
        except Exception as e:
            self.show_error_message("Error cancelling download", str(e))

    def update_status(self, data):
        try:
            status = data['status']
            if status == 'downloading':
                self.status_label.setText("Downloading...")
            elif status == 'completed':
                self.status_label.setText("Download finished!")
                self.playlist_link_input.clear()
            elif status == 'cancelled':
                self.status_label.setText("Download cancelled.")
            elif status == 'error':
                self.status_label.setText(f"Error: {data['message']}")
                print(f"Error occurred: {data['message']}")
        except Exception as e:
            self.show_error_message("Error updating status", str(e))

    def download_finished(self):
        try:
            self.download_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
        except Exception as e:
            self.show_error_message("Error finishing download", str(e))
        
    def reset_for_new_download(self):
        try:
            self.status_label.setText("")
        except Exception as e:
            self.show_error_message("Error resetting for new download", str(e))

    def show_error_message(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setDetailedText(traceback.format_exc())
        error_box.exec()
        print(f"Error: {title}\n{message}\n{traceback.format_exc()}")