import json

def load_rider_data():
    try:
        with open("rider_db.json") as file:
            rider_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        rider_data = []
    return rider_data

def find_rider_data_by_name(suchstring):

    person_data = load_rider_data()
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print(eintrag)
            return eintrag
    else:
        return {}

if __name__ == "__main__":
    rider_data = find_rider_data_by_name("Pogacar, Tadej")
    rider_data_2 = find_rider_data_by_name("Yates, Adam")


