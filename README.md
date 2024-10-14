# AutoNexusMods

This script automates the process of downloading mods from a specified website using Python. It utilizes computer vision and optical character recognition (OCR) to identify and interact with download buttons on the screen.

## Features

- **Multi-Monitor Support**: The script is designed to work with a setup that includes multiple monitors.
- **OCR Integration**: Uses Tesseract OCR to read button labels and confirm actions.
- **Logging**: Logs actions and errors to a file for easy debugging and tracking.
- **Download Completion Check**: Waits for the download to complete or times out after a specified duration.

## Requirements

- Python 3.x
- Libraries:
  - `pyautogui`
  - `opencv-python`
  - `numpy`
  - `pytesseract`
  - `screeninfo`
  - `logging`
- Tesseract OCR installed on your system. Adjust the path in the script to point to the Tesseract executable.

## Installation

1. Clone this repository or download the `app.py` file.
2. Install the required libraries using pip:
   ```bash
   pip install pyautogui opencv-python numpy pytesseract screeninfo
   ```
3. Install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract) and ensure the path is correctly set in the script.

## Usage

1. Ensure your target website is open on the second monitor.
2. Run the script:
   ```bash
   python app.py
   ```
3. The script will attempt to download a specified number of mods (default is 50). You can adjust this in the `main()` function.

## Logging

All actions and errors are logged to `mod_download_log.txt`. Check this file for details on the script's execution and any issues encountered.

## Notes

- The script assumes the download buttons are colored orange and gray. Adjust the color ranges in the script if necessary.
- Ensure that the screen resolution and layout are consistent to avoid detection issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
