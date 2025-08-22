
Barcode Automation App - README
===============================

Description
-----------
Barcode Automation App is a Python-based graphical interface tool designed to automate the Clock In / Clock Out process within the MIE Kiosk system. It uses barcode scanning, coordinate-based actions, and OCR (optical character recognition) to interact with the interface reliably.

System Requirements
-------------------
Screen settings (MANDATORY for proper function):
- Resolution: 1920x1080
- Scaling: 100%
- The screen must be the primary display
- MIE Kiosk must be open and visible


Operating System:
- Windows 10 or higher
- Local network connection (if applicable)

Python Requirements
-------------------
Python version: 3.10 or above

Required Python packages:
> Install via pip:
    pip install pyautogui pygetwindow pytesseract pillow keyboard

Tesseract OCR (REQUIRED)
------------------------
OCR is used to detect and validate screen content.

1. Download and install Tesseract from:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Recommended install path:
   C:\Program Files\Tesseract-OCR\

3. Ensure `tesseract.exe` is in the system PATH or manually define it in your code:
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Running the App
---------------
To run the app:

1. Open a terminal (CMD or PowerShell)
2. Navigate to the application folder
3. Run:
    python main.py

The app will start in the system tray and listen for barcode input.

Notes
-----
- This application is resolution-sensitive. Any change in display resolution or scaling will cause coordinate-based clicks and OCR to fail.
- Make sure the MIE Kiosk is fully visible and buttons are not obstructed.
- Logs are automatically saved to the /logs directory.
