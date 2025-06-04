import sys
import os
import json
import yaml
import xmltodict
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QMessageBox
)

SUPPORTED_FORMATS = ['.json', '.xml', '.yml', '.yaml']


def load_file(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'r', encoding='utf-8') as file:
        if ext == '.json':
            return json.load(file)
        elif ext in ['.yml', '.yaml']:
            return yaml.safe_load(file)
        elif ext == '.xml':
            return xmltodict.parse(file.read())
        else:
            raise ValueError("Nieobsługiwany format wejściowy")


def save_file(path, data):
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'w', encoding='utf-8') as file:
        if ext == '.json':
            json.dump(data, file, indent=4, ensure_ascii=False)
        elif ext in ['.yml', '.yaml']:
            yaml.dump(data, file, sort_keys=False, allow_unicode=True)
        elif ext == '.xml':
            if isinstance(data, dict) and len(data) == 1:
                xml_data = xmltodict.unparse(data, pretty=True)
            else:
                xml_data = xmltodict.unparse({'root': data}, pretty=True)
            file.write(xml_data)
        else:
            raise ValueError("Nieobsługiwany format wyjściowy")


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter plików (JSON/YAML/XML)")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Wybierz plik wejściowy i wyjściowy.")
        self.layout.addWidget(self.label)

        self.input_btn = QPushButton("Wybierz plik wejściowy")
        self.input_btn.clicked.connect(self.choose_input)
        self.layout.addWidget(self.input_btn)

        self.output_btn = QPushButton("Wybierz plik wyjściowy")
        self.output_btn.clicked.connect(self.choose_output)
        self.layout.addWidget(self.output_btn)

        self.convert_btn = QPushButton("Konwertuj")
        self.convert_btn.clicked.connect(self.convert)
        self.layout.addWidget(self.convert_btn)

        self.input_file = None
        self.output_file = None

    def choose_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Plik wejściowy", "", "Pliki (*.json *.yml *.yaml *.xml)")
        if path:
            self.input_file = path
            self.label.setText(f"📥 Plik wejściowy: {os.path.basename(path)}")

    def choose_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "Plik wyjściowy", "", "Pliki (*.json *.yml *.yaml *.xml)")
        if path:
            self.output_file = path
            self.label.setText(f"{self.label.text()}\n📤 Plik wyjściowy: {os.path.basename(path)}")

    def convert(self):
        try:
            if not self.input_file or not self.output_file:
                raise ValueError("Musisz wybrać oba pliki.")

            data = load_file(self.input_file)
            save_file(self.output_file, data)
            QMessageBox.information(self, "Sukces", "✅ Konwersja zakończona pomyślnie.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"❌ {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
