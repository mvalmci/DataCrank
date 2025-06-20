import pandas as pd


# Pfad zur JSON-Datei (z. B. vom Pogacar-Ordner)
json_path_tadej = "Pogacar_Tadej\{0031326c-e796-4f35-8f25-d3937edca90f}.json"
data_tadej = pd.read_json(json_path_tadej)

json_path_yates = "Yates_Adams\{000c6417-e1e4-497e-89e6-bb21e17ec355}.json"
data_yates = pd.read_json(json_path_yates)

json_path_deltoro = "Del Torro_Isaac\{000db8a2-a1f6-42bd-8228-fdfae659f476}.json"
data_deltoro = pd.read_json(json_path_deltoro)

if __name__ == "__main__":

    print("Daten für Tadej Pogacar:")
    print(data_tadej.head())

