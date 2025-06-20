#Funktion welche über die Datensätze iteriert und checkt ob es sich um eine Fahrrad Aktivität handelt oder nicht.
#wenn es sich nicht um eine Fahrrad Aktivität handelt, dann wird der Eintrag übersprungen.

import pandas as pd
import json
import os

def save_cycling_data(df, filename, output_file=input("Wie soll die neue Json Datei heißen?")+ ".json"):
    """Speichert einen DataFrame als JSON-Eintrag, wenn 'power' > 0 vorkommt."""
    entry = {
        "source_file": filename,
        "data": df.to_dict(orient="records")
    }

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(filename)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)

def process_training_file(df: pd.DataFrame, filename: str):
    """Überprüft, ob ein Wert in 'power' > 0 ist – wenn ja, speichern."""
    if "power" not in df.columns:
        print(f"Datei {filename} hat keine 'power'-Spalte.")
        return

    if df["power"].fillna(0).gt(0).any():
        save_cycling_data(df, filename)
        print(f"Cycling-Training erkannt & gespeichert: {filename}")
    else:
        print(f"Kein Cycling-Training in Datei: {filename}")

# Beispielverwendung
def get_csv_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]

if __name__ == "__main__":
    folder = input("Gib den Pfad zum Ordner mit den CSV-Dateien ein: ")
    if not os.path.isdir(folder):
        print("❌ Ungültiger Ordnerpfad.")
        exit(1)

    csv_files = get_csv_files(folder)

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            process_training_file(df, file)
        except Exception as e:
            print(f"❌ Fehler bei Datei {file}: {e}")

