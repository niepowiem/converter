import sys
import os
import json

# Obsługiwane formaty
SUPPORTED_FORMATS = ['.json', '.xml', '.yml', '.yaml']

def parse_arguments():
    if len(sys.argv) != 3:
        print("❌ Błąd: Należy podać dokładnie dwa argumenty: ścieżkę do pliku wejściowego i wyjściowego.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    _, input_ext = os.path.splitext(input_path)
    _, output_ext = os.path.splitext(output_path)

    if input_ext.lower() not in SUPPORTED_FORMATS:
        print(f"❌ Błąd: Format wejściowy {input_ext} nie jest obsługiwany.")
        sys.exit(1)

    if output_ext.lower() not in SUPPORTED_FORMATS:
        print(f"❌ Błąd: Format wyjściowy {output_ext} nie jest obsługiwany.")
        sys.exit(1)

    return input_path, output_path


def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("✅ Plik JSON poprawnie wczytany.")
            return data
    except FileNotFoundError:
        print(f"❌ Błąd: Nie znaleziono pliku: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Błąd składni JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Inny błąd przy wczytywaniu JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file, output_file = parse_arguments()

    # Jeśli wejściowy to JSON – wczytaj
    if input_file.endswith(".json"):
        json_data = load_json_file(input_file)
