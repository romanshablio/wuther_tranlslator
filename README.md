# wuther_tranlslator

A Python 3.11 screen text translator.

This project recognizes subtitles or text from the screen in real time, translates it from English to Russian, and displays the result in an overlay window above other applications, such as a game or video player.

## Features

- Screen text recognition through Tesseract OCR.
- Translation through Google Translate API without an API key.
- Movable, resizable, semi-transparent always-on-top overlay window.
- Continue button for manual translation updates.
- Overlay size and position saved in `config.json`.

## Requirements

- Python 3.11 recommended.
- macOS with PyQt5 support, tested on macOS 13-14.
- Installed Tesseract OCR through Homebrew.

## Installation

### 1. Install Tesseract OCR on macOS

```bash
brew install tesseract
```

### 2. Clone the Project

```bash
git clone https://github.com/romanshablio/wuther_tranlslator.git
cd wuther_tranlslator
```

### 3. Create a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install dependencies manually:

```bash
pip install PyQt5 pytesseract pillow mss googletrans==4.0.0-rc1
```

## Running

```bash
python overlay_translator.py
```

An overlay window appears above other windows. You can resize and move it. The settings are saved automatically.

## Project Structure

| File | Purpose |
| --- | --- |
| `overlay_translator.py` | Main script. |
| `config.json` | Saves overlay position and size. |
| `README.md` | Launch instructions. |

## Settings

The OCR area is calculated automatically from the translation window size.

## Troubleshooting

- Make sure `tesseract` is installed and available at `/opt/homebrew/bin/tesseract`.
- Check that PyQt5 is installed in the active environment.
- Allow screen access in `System Settings > Privacy > Screen Recording`.

## License

MIT License.
