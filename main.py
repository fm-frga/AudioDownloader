import os
import sys
import yt_dlp
from PySide6.QtCore import QObject, Slot, Signal, QThread
from PySide6.QtWidgets import QApplication
from pathlib import Path
import concurrent.futures
import threading
import traceback
from audio_formats import get_format_by_index, AudioFormat

downloads_folder = str(Path.home() / "Downloads")

class DownloadThread(QThread):
    progress_signal = Signal(dict)
    finished_signal = Signal()

    def __init__(self, playlist_url, format_index):
        super().__init__()
        self.playlist_url = playlist_url
        self.format_index = format_index
        self.is_cancelled = False
        self.download_queue = []
        self.queue_lock = threading.Lock()

    def run(self):
        audio_format: AudioFormat = get_format_by_index(self.format_index)
        playlist_folder = os.path.join(downloads_folder, f"YouTube Playlist {audio_format.name}")
        if not os.path.exists(playlist_folder):
            os.mkdir(playlist_folder)

        ydl_opts = {
            'format': audio_format.ydl_format,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format.ffmpeg_codec,
            }],
            'outtmpl': os.path.join(playlist_folder, "%(title)s.%(ext)s"),
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': False,
            'extract_flat': 'in_playlist',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    playlist_info = ydl.extract_info(self.playlist_url, download=False)
                except Exception as e:
                    print(f"Error extracting playlist info: {str(e)}")
                    traceback.print_exc()
                    self.progress_signal.emit({'status': 'error', 'message': f"Error extracting playlist info: {str(e)}"})
                    return

                if 'entries' in playlist_info:
                    entries = playlist_info['entries']
                    self.download_queue = list(enumerate(entries, 1))
                    
                    self.progress_signal.emit({'status': 'downloading'})
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        futures = []
                        for worker_id in range(3):
                            future = executor.submit(self.worker_download, ydl)
                            futures.append(future)
                        
                        concurrent.futures.wait(futures)
                else:
                    self.progress_signal.emit({'status': 'downloading'})
                    try:
                        ydl.download([self.playlist_url])
                    except Exception as e:
                        print(f"Error downloading single video: {str(e)}")
                        traceback.print_exc()
                        self.progress_signal.emit({'status': 'error', 'message': f"Error downloading video: {str(e)}"})
                
                if not self.is_cancelled:
                    self.progress_signal.emit({'status': 'completed'})
        except Exception as e:
            print(f"Unexpected error in download thread: {str(e)}")
            traceback.print_exc()
            self.progress_signal.emit({'status': 'error', 'message': f"Unexpected error: {str(e)}"})
        finally:
            self.finished_signal.emit()

    def worker_download(self, ydl):
        while True:
            with self.queue_lock:
                if not self.download_queue or self.is_cancelled:
                    break
                _, entry = self.download_queue.pop(0)
            
            try:
                ydl.download([entry['url']])
            except Exception as e:
                print(f"Error downloading video: {str(e)}")
                traceback.print_exc()

    def cancel(self):
        self.is_cancelled = True
        self.progress_signal.emit({'status': 'cancelled'})

class DownloaderBackend(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.window.download_signal.connect(self.start_download)
        self.window.cancel_signal.connect(self.cancel_download)
        self.download_thread = None

    @Slot(str, int)
    def start_download(self, url, format_index):
        self.window.reset_for_new_download()
        self.download_thread = DownloadThread(url, format_index)
        self.download_thread.progress_signal.connect(self.window.update_status)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

    @Slot()
    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.cancel()
            self.download_thread.wait()
        self.window.close()

    def download_finished(self):
        self.window.download_finished()
        self.download_thread = None

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        from gui import MainWindow
        window = MainWindow()
        backend = DownloaderBackend(window)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Critical error in main application: {str(e)}")
        traceback.print_exc()