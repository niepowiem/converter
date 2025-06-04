import sys
import os
import json
import yaml
import xmltodict
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QMessageBox
)
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal

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


# ---- Task9: Worker i sygnały ----

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal()


class FileConverterWorker(QRunnable):
    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            data = load_file(self.input_file)
            save_file(self.output_file, data)
            self.signals.success.emit()
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


# ---- UI ----

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter plików (JSON/YAML/XML) [z wielowątkowością]")
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

        self.convert_btn = QPushButton("Konwertuj (w tle)")
        self.convert_btn.clicked.connect(self.convert)
        self.layout.addWidget(self.convert_btn)

        self.input_file = None
        self.output_file = None

        self.threadpool = QThreadPool()

    def choose_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Plik wejściowy", "", "Pliki (*.json *.yml *.yaml *.xml)")
        if path:
            self.input_file = path
            self.label.setText(f"📥 Wejście: {os.path.basename(path)}")

    def choose_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "Plik wyjściowy", "", "Pliki (*.json *.yml *.yaml *.xml)")
        if path:
            self.output_file = path
            self.label.setText(f"{self.label.text()}\n📤 Wyjście: {os.path.basename(path)}")

    def convert(self):
        if not self.input_file or not self.output_file:
            QMessageBox.warning(self, "Błąd", "Musisz wybrać oba pliki.")
            return

        self.convert_btn.setEnabled(False)
        self.label.setText("🔄 Trwa konwersja...")

        worker = FileConverterWorker(self.input_file, self.output_file)
        worker.signals.success.connect(self.on_success)
        worker.signals.error.connect(self.on_error)
        worker.signals.finished.connect(self.on_finished)

        self.threadpool.start(worker)

    def on_success(self):
        QMessageBox.information(self, "Sukces", "✅ Konwersja zakończona pomyślnie.")

    def on_error(self, message):
        QMessageBox.critical(self, "Błąd", f"❌ {message}")

    def on_finished(self):
        self.convert_btn.setEnabled(True)
        self.label.setText("✅ Gotowe. Możesz konwertować ponownie.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
