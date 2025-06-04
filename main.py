import sys
import os

# Obsługiwane formaty
SUPPORTED_FORMATS = ['.json', '.xml', '.yml', '.yaml']

def parse_arguments():
    if len(sys.argv) != 3:
        print("Błąd: Należy podać dokładnie dwa argumenty: ścieżkę do pliku wejściowego i wyjściowego.")
        print("Przykład: program.exe input.json output.yaml")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Sprawdzenie czy rozszerzenia plików są obsługiwane
    _, input_ext = os.path.splitext(input_path)
    _, output_ext = os.path.splitext(output_path)

    if input_ext.lower() not in SUPPORTED_FORMATS:
        print(f"Błąd: Format wejściowy {input_ext} nie jest obsługiwany.")
        sys.exit(1)

    if output_ext.lower() not in SUPPORTED_FORMATS:
        print(f"Błąd: Format wyjściowy {output_ext} nie jest obsługiwany.")
        sys.exit(1)

    print("Argumenty poprawne:")
    print(f"   Plik wejściowy: {input_path}")
    print(f"   Plik wyjściowy: {output_path}")

    return input_path, output_path


if __name__ == "__main__":
    parse_arguments()
