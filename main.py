import sys
import os
import json
import yaml
import xmltodict

SUPPORTED_FORMATS = ['.json', '.xml', '.yml', '.yaml']

def parse_arguments():
    if len(sys.argv) != 3:
        print("❌ Podaj dwa argumenty: plik wejściowy i wyjściowy.")
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
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_yaml_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def load_xml_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return xmltodict.parse(file.read())


def save_json_file(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"✅ Zapisano JSON: {path}")


def save_yaml_file(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, sort_keys=False, allow_unicode=True)
    print(f"✅ Zapisano YAML: {path}")


def save_xml_file(path, data):
    try:
        # Jeśli dane to dict i nie mają jednego głównego "roota", dodaj go
        if isinstance(data, dict) and len(data) == 1:
            xml_data = xmltodict.unparse(data, pretty=True)
        else:
            xml_data = xmltodict.unparse({'root': data}, pretty=True)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(xml_data)
        print(f"✅ Zapisano XML: {path}")
    except Exception as e:
        print(f"❌ Błąd zapisu XML: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file, output_file = parse_arguments()

    # Wczytaj dane
    if input_file.endswith(".json"):
        data = load_json_file(input_file)
    elif input_file.endswith((".yml", ".yaml")):
        data = load_yaml_file(input_file)
    elif input_file.endswith(".xml"):
        data = load_xml_file(input_file)
    else:
        print("❌ Format wejściowy nieobsługiwany.")
        sys.exit(1)

    # Zapisz dane
    if output_file.endswith(".json"):
        save_json_file(output_file, data)
    elif output_file.endswith((".yml", ".yaml")):
        save_yaml_file(output_file, data)
    elif output_file.endswith(".xml"):
        save_xml_file(output_file, data)
    else:
        print("❌ Format wyjściowy nieobsługiwany.")
        sys.exit(1)
