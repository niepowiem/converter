import sys
import os
import json
import yaml
import xmltodict  # ← NOWOŚĆ

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
            print("✅ JSON wczytany.")
            return data
    except Exception as e:
        print(f"❌ Błąd JSON: {e}")
        sys.exit(1)


def load_yaml_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            print("✅ YAML wczytany.")
            return data
    except Exception as e:
        print(f"❌ Błąd YAML: {e}")
        sys.exit(1)


def load_xml_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = xmltodict.parse(file.read())
            print("✅ XML wczytany.")
            return data
    except FileNotFoundError:
        print(f"❌ Nie znaleziono pliku XML: {path}")
        sys.exit(1)
    except xmltodict.expat.ExpatError as e:
        print(f"❌ Błąd składni XML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Błąd XML: {e}")
        sys.exit(1)


def save_json_file(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"✅ Zapisano jako JSON: {path}")
    except Exception as e:
        print(f"❌ Błąd zapisu JSON: {e}")
        sys.exit(1)


def save_yaml_file(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, sort_keys=False, allow_unicode=True)
            print(f"✅ Zapisano jako YAML: {path}")
    except Exception as e:
        print(f"❌ Błąd zapisu YAML: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file, output_file = parse_arguments()

    # Wczytanie danych
    if input_file.endswith(".json"):
        data = load_json_file(input_file)
    elif input_file.endswith((".yml", ".yaml")):
        data = load_yaml_file(input_file)
    elif input_file.endswith(".xml"):
        data = load_xml_file(input_file)
    else:
        print("❌ Format wejściowy nieobsługiwany.")
        sys.exit(1)

    # Zapis danych (na razie tylko JSON/YAML)
    if output_file.endswith(".json"):
        save_json_file(output_file, data)
    elif output_file.endswith((".yml", ".yaml")):
        save_yaml_file(output_file, data)
    else:
        print("❌ Ten typ pliku wyjściowego nie jest jeszcze obsługiwany.")
        sys.exit(1)
