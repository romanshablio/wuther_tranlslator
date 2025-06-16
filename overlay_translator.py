import sys
import json
import os
import pytesseract
from PIL import Image
import mss
from googletrans import Translator
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QTimer

# === Настройки пути к tesseract ===
pytesseract.pytesseract_cmd = '/opt/homebrew/bin/tesseract'

# === Путь к config-файлу ===
CONFIG_PATH = "config.json"

# === Значения по умолчанию ===
DEFAULT_CONFIG = {
    "x": 300,
    "y": 500,
    "width": 900,
    "height": 150
}

# === Загрузка или создание конфигурации ===
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_PATH, 'w') as f:
        json.dump(DEFAULT_CONFIG, f)

# === Область OCR ===
capture_area = {
    'top': config["y"] + config["height"],
    'left': config["x"],
    'width': config["width"],
    'height': 100
}

# === Приложение PyQt5 ===
app = QApplication(sys.argv)

class TranslatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перевод")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        self.setGeometry(config["x"], config["y"], config["width"], config["height"])
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Текст
        self.label = QLabel("Ожидание текста...")
        self.label.setStyleSheet("color: white; font-size: 16pt;")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # Кнопка закрытия
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(lambda: sys.exit())
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)


        # Кнопка "Продолжить"
        self.resume_button = QPushButton("Продолжить")
        self.resume_button.clicked.connect(self.force_translate_now)
        layout.addWidget(self.resume_button, alignment=Qt.AlignCenter)

    def update_translation(self, text):
        if self.label.text() != text:
            self.label.setText(text)

    def moveEvent(self, event):
        self.save_config()
    def resizeEvent(self, event):
        self.save_config()

    def save_config(self):
        geo = self.geometry()
        data = {
            "x": geo.x(),
            "y": geo.y(),
            "width": geo.width(),
            "height": geo.height()
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f)
            
    def force_translate_now(self):
            global force_translate
            force_translate = True

# === Создаём окно ===
window = TranslatorWindow()
window.show()

translator = Translator()

# Глобальная переменная для хранения предыдущего текста
previous_ocr = ""
force_translate = False

def update_overlay():
    global previous_ocr, force_translate

    geo = window.geometry()
    capture_area["left"] = geo.x()
    capture_area["top"] = geo.y() + geo.height()
    capture_area["width"] = geo.width()

    with mss.mss() as sct:
        screenshot = sct.grab(capture_area)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        extracted = pytesseract.image_to_string(img, lang='eng').strip()

        if extracted and (extracted != previous_ocr or force_translate):
            previous_ocr = extracted
            force_translate = False  # сбрасываем флаг
            try:
                translated = translator.translate(extracted, src='en', dest='ru').text
                print("OCR:", extracted)
                print("Перевод:", translated)
                window.update_translation(translated)
            except Exception as e:
                window.update_translation(f"Ошибка перевода: {e}")

        elif not extracted:
            previous_ocr = ""
            window.update_translation("")

# === Таймер обновления ===
timer = QTimer()
timer.timeout.connect(update_overlay)
timer.start(1500)

sys.exit(app.exec_())
