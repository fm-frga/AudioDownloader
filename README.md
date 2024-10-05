# YouTube Playlist Audio Downloader

This application allows you to download audio from YouTube playlists in various formats. It's a modern replacement for the obsolete [YouTube-Playlist-MP3-Downloader](https://github.com/fm-frga/YouTube-Playlist-MP3-Downloader).

## Features

- Download audio from YouTube playlists
- Support for multiple audio formats (M4A, MP3, WAV, FLAC, AAC, OPUS, VORBIS, ALAC, AC3, DTS)
- User-friendly graphical interface
- Concurrent downloads for faster processing
- Easily extensible to support additional audio formats
- Cross-platform support (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (must be installed separately and available in your system PATH)

### Windows

1. Install Python from the [official website](https://www.python.org/downloads/windows/).

2. Install FFmpeg (choose one method):

   a) Manual installation:
   - Download the FFmpeg build from [ffmpeg.org](https://www.ffmpeg.org/download.html#build-windows).
   - Extract the archive to a folder (e.g., `C:\ffmpeg`).
   - Add the `bin` folder (e.g., `C:\ffmpeg\bin`) to your system PATH:
     - Right-click on "This PC" or "My Computer" and select "Properties".
     - Click on "Advanced system settings".
     - Click on "Environment Variables".
     - Under "System variables", find and select "Path", then click "Edit".
     - Click "New" and add the path to the `bin` folder.
     - Click "OK" to close all dialogs.

   b) Using Chocolatey package manager:
   - First, install Chocolatey if you haven't already:
     - For PowerShell (Run as Administrator):
       ```
       Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
       ```
     - For CMD (Run as Administrator):
       ```
       @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
       ```
     - For more installation options, refer to the [official Chocolatey documentation](https://docs.chocolatey.org/en-us/choco/setup/#more-install-options).
   - After Chocolatey is installed, run:
     ```
     choco install ffmpeg
     ```

3. Clone the repository:
   ```
   git clone https://github.com/your-username/youtube-playlist-audio-downloader.git
   cd youtube-playlist-audio-downloader
   ```

4. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Linux (Ubuntu/Debian)

1. Install Python and FFmpeg:
   ```
   sudo apt update
   sudo apt install python3 python3-venv ffmpeg
   ```

2. Clone the repository:
   ```
   git clone https://github.com/your-username/youtube-playlist-audio-downloader.git
   cd youtube-playlist-audio-downloader
   ```

3. Create a virtual environment:
   ```
   python3 -m venv YourVenvName
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment (if not already activated):
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. Run the application:
   ```
   python main.py
   ```

3. In the GUI:
   - Enter the YouTube playlist URL
   - Select the desired audio format
   - Click "Download" to start the process

4. The downloaded audio files will be saved in your "Downloads" folder under a subfolder named "YouTube Playlist [Format]".

## Project Structure

- `main.py`: The main script that initializes the application and handles the download process.
- `gui.py`: Contains the GUI implementation using PySide6.
- `audio_formats.py`: Defines the available audio formats and their properties.

## Customization

You can add new audio formats by modifying the `audio_formats.py` file. This file contains the definitions for various audio formats that the downloader supports. Here's how you can add a new format:

1. Open `audio_formats.py` in your text editor.
2. Locate the `AUDIO_FORMATS` list.
3. Add a new `AudioFormat` object to the list. For example:
   ```python
   AudioFormat("WMA", "wma", "bestaudio/best", "wmav2"),
   ```
   The `AudioFormat` class has the following attributes:
   - `name`: The name of the format (as it will appear in the GUI)
   - `extension`: The file extension for the format
   - `ydl_format`: The yt-dlp format string
   - `ffmpeg_codec`: The FFmpeg codec name

4. Save the file. The new format will now be available in the GUI's format selection dropdown.

Remember to choose appropriate values for the yt-dlp format string and FFmpeg codec to ensure compatibility with your desired audio format. Refer to [yt-dlp](https://github.com/yt-dlp/yt-dlp) repo for more information on the YouTubeDL class.

## Available Audio Formats

The application currently supports the following audio formats:

1. M4A (AAC)
2. MP3
3. WAV
4. FLAC
5. AAC
6. OPUS
7. VORBIS (OGG)
8. ALAC
9. AC3
10. DTS

## Troubleshooting

- If you encounter any issues with FFmpeg, ensure it's properly installed and available in your system PATH.
- For Windows users:
  - If you see an error related to `VCRUNTIME140.dll`, you may need to install the [Microsoft Visual C++ Redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).
  - If FFmpeg is not recognized as a command, try restarting your command prompt or PowerShell after installing FFmpeg or adding it to the PATH.

## Requirements

See `requirements.txt` for a list of Python dependencies. The main dependencies include:

- PySide6
- yt-dlp
- FFmpeg (must be installed separately and available in your system PATH)



## License

[MIT License](LICENSE)

## Disclaimer

This tool is for personal use only. Respect copyright laws and YouTube's terms of service when using this application.

The developer of this software takes no responsibility for any misuse of this tool or any violations of YouTube's terms of service or any applicable laws. Users are solely responsible for how they use this software and for ensuring that their use complies with all relevant laws and terms of service.

By using this software, you agree that the developer cannot be held liable for any legal issues, account suspensions, or any other consequences that may arise from your use of this tool.

Use this software at your own risk and discretion. If you do not agree with these terms, do not use this software.
