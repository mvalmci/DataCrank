# DataCrank 🚴‍♂️

![UAE Team Emirates Logo](pictures/logo-uae.png)

**Abschlussprojekt Programmierübung 2 von Simon Schwarzer & Marius Valenta**

---

## Überblick

**DataCrank** ist eine spezialisierte App für Trainingsleiter von Profi-Radsport-Teams. Mit DataCrank können Trainingsdaten von Fahrern analysiert, Fatigue-Phasen erkannt und die optimale Rennplanung durchgeführt werden. Besonderes Augenmerk liegt auf der datengetriebenen Unterstützung von Trainingsentscheidungen und der Visualisierung der Leistungsfähigkeit.

---

## Haupt-Features

- **Analyse von Trainingsdaten** für einzelne Fahrer oder Teams
- **Automatische Einteilung in Fatigue-Phasen** zur optimalen Belastungssteuerung
- **Visualisierung von Leistungsdaten** (z. B. Watt, Herzfrequenz, Distanz)
- **Planung und Anpassung von Trainings- und Rennkalendern**
- **Import und Verwaltung von Trainingsdaten** aus verschiedenen Quellen (JSON-Dateien)
- **Ranking und Statistikfunktionen** für Fahrer
- **Benutzerfreundliche Python-Module** zur Erweiterung und Anpassung

---

## Technologie-Stack

- **Sprache:** Python
- **Datenanalyse:** Pandas, NumPy
- **Visualisierung:** (optional) Matplotlib, Plotly
- **Datenformate:** JSON für Trainings- und Fahrerdaten

---

## Projektstruktur & wichtige Dateien

| Datei / Ordner           | Zweck/Beschreibung                                   |
|------------------------- |------------------------------------------------------|
| `main.py`                | Einstiegspunkt der App, zentrale Steuerung           |
| `add_new_rider.py`       | Hinzufügen neuer Fahrer                              |
| `add_new_training.py`    | Hinzufügen neuer Trainingseinträge                   |
| `calculate_statistics.py`| Statistiken & Auswertungen zu Trainingsdaten         |
| `func_rider_ranking.py`  | Fahrer-Rankings und Leistungsvergleich               |
| `power_curve.py`         | Analyse und Darstellung von Power Curves             |
| `sort_data.py`           | Sortierung und Filterung von Datensätzen             |
| `read_rider_data.py`     | Einlesen und Verarbeiten von Fahrerdaten             |
| `cycling_data_*.json`    | Beispielhafte Trainingsdaten einzelner Fahrer        |
| `rider_db.json`          | Datenbank der Fahrer                                |
| `pictures/`              | Bilder & Logos (z. B. UAE Team Emirates)            |
| `pages/`                 | (Optional) Zusätzliche Seiten/Funktionen             |
| Eigene Ordner je Fahrer  | z. B. `Pogacar_Tadej`, `Yates_Adams`                |

> **Hinweis:** Die vollständige Dateiansicht findest du [hier auf GitHub](https://github.com/mvalmci/DataCrank/tree/main).

---

## Installation & Erste Schritte

1. **Repository klonen:**
   ```bash
   git clone https://github.com/mvalmci/DataCrank.git
   ```

2. **Abhängigkeiten installieren:**  
   (mit pip und ggf. [PDM](https://pdm.fming.dev/))
   ```bash
   pip install -r requirements.txt
   # oder
   pdm install
   ```

3. **Anwendung starten:**  
   ```bash
   streamlit run main.py
   ```

4. **Weitere Infos:**  
   Lies die Dokumentation oder den Quellcode der Module für spezifische Anwendungsfälle.

---

## Screenshots & Visuals

Hier kannst du z.B. ein Team-Logo oder App-Screenshots einfügen:

![UAE Team Emirates Logo](pictures/uae_team_emirates_logo.png)

---

## Zielgruppe

- Trainingsleiter und sportliche Leiter von Profi-Radsport-Teams
- Datenaffine Coaches, die moderne Trainingssteuerung und -analyse einsetzen möchten

---

## Autoren

- Simon Schwarzer
- Marius Valenta

---

> Dieses Projekt befindet sich in der Entwicklung. Feedback & Anregungen sind willkommen!
