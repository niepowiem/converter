import sys
import os
import json
import yaml  # <- nowa biblioteka

SUPPORTED_FORMATS = ['.json', '.xml', '.yml', '.yaml']

def parse_arguments():
    if len(sys.argv) != 3:
        print("❌ Błąd: Podaj dwa argumenty: ścieżkę do pliku wejściowego i wyjściowego.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    _, input_ext = os.path.splitext(input_path)
    _, output_ext = os.path.splitext(output_path)

    if input_ext.lower() not in SUPPORTED_FORMATS:
        print(f"❌ Nieobsługiwany format wejściowy: {input_ext}")
        sys.exit(1)

    if output_ext.lower() not in SUPPORTED_FORMATS:
        print(f"❌ Nieobsługiwany format wyjściowy: {output_ext}")
        sys.exit(1)

    return input_path, output_path


def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("✅ Plik JSON poprawnie wczytany.")
            return data
    except FileNotFoundError:
        print(f"❌ Nie znaleziono pliku: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Błąd składni JSON: {e}")
        sys.exit(1)


def load_yaml_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            print("✅ Plik YAML poprawnie wczytany.")
            return data
    except FileNotFoundError:
        print(f"❌ Nie znaleziono pliku: {path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Błąd składni YAML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Inny błąd przy wczytywaniu YAML: {e}")
        sys.exit(1)


def save_json_file(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"✅ Dane zapisane do pliku JSON: {path}")
    except Exception as e:
        print(f"❌ Błąd zapisu do pliku JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file, output_file = parse_arguments()

    if input_file.endswith(".json"):
        data = load_json_file(input_file)
    elif input_file.endswith(".yml") or input_file.endswith(".yaml"):
        data = load_yaml_file(input_file)
    else:
        print("ℹ️ W tej wersji obsługiwane są tylko wejściowe pliki JSON i YAML.")
        sys.exit(1)

    if output_file.endswith(".json"):
        save_json_file(output_file, data)
    else:
        print("ℹ️ W tej wersji obsługiwany jest tylko zapis do JSON.")
        sys.exit(1)
