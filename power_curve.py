#power_curve generieren und plotten
#müde power curve z.B.: 1500kJ verbraucht
#sehr müde power curve z.B.: 3000kJ verbraucht
#über gesamten Datensatz drübergehen und Energieverbrauch in Json hinzufügen

import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px
import json
import os

def load_data(path="Pogacar_Tadej/2016_12_14_08_58_06.csv"):

    df = pd.read_csv(path)

    t_end = len(df)
    time = np.arange(0, t_end)
    df["Time/s"] = time

    return df

def find_best_effort(series, windows=[30, 60, 180, 300, 600, 1800, 2000]):
    
    best_efforts = {}
    
    for window in windows:
        max_average = series.rolling(window).mean()
        list_max_avg = max_average.max()
        best_efforts[window] = list_max_avg
    
    df2 = pd.DataFrame.from_dict(best_efforts, orient='index', columns=['Best Effort'])
    df2 = df2.reset_index().rename(columns={'index': 'Time/s'})

    return df2

def plot_power_curve(df2):
    figure = px.line(
        df2,
        x="Time/s",
        y="Best Effort",
        title="Powercurve",
        markers=True
    )
    return figure

def average_power_per_minute(df):
    if "power" not in df.columns:
        raise ValueError("DataFrame must contain 'power' column.")
    
    average_power = df["power"].rolling(window=60, min_periods=60).mean()
    average_power = average_power.dropna().reset_index(drop=True)

    power_per_full_minutes = average_power.iloc[59::60].reset_index(drop=True)

    return power_per_full_minutes

def used_energy_per_minute(power_per_full_minutes):
    if power_per_full_minutes.empty:
        return 0
    
    energy_per_minute = power_per_full_minutes * 60  # Convert from Watts to Joules (1 W = 1 J/s)

    df = pd.DataFrame(energy_per_minute, columns=["Energy (Joules)"])

    return energy_per_minute

    

def fatigue_indices(energy_per_minute, tired_limit=1500000, very_tired_limit=3000000):
    summe = 0
    fresh_index = None
    tired_index = None
    very_tired_index = None

    for idx, wert in enumerate(energy_per_minute):
        summe += wert
        if tired_index is None and summe > tired_limit:
            tired_index = idx
        if very_tired_index is None and summe > very_tired_limit:
            very_tired_index = idx
        if tired_index is None and very_tired_index is  None:
            fresh_index = idx

    return fresh_index, tired_index, very_tired_index





def aggregate_best_efforts_from_json(json_path, folder_with_csvs, windows=[30, 60, 180, 300, 600, 1800, 2000]):
    # 1. JSON einlesen und Dateinamen extrahieren
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    csv_files = data['csv_files']  # Passe ggf. den Key an

    # 2. Dictionary für alle besten Werte initialisieren
    best_overall = {window: float('-inf') for window in windows}
    # 3. Iteriere über alle Dateien
    for csv_file in csv_files:
        full_path = csv_file
        df = pd.read_csv(full_path)
        if "power" not in df.columns:
            continue  # Datei überspringen, falls keine Power-Spalte vorhanden
        df_efforts = find_best_effort(df["power"], windows)
        for i, row in df_efforts.iterrows():
            window = row['Time/s']
            value = row['Best Effort']
            if pd.notnull(value) and value > best_overall[window]:
                best_overall[window] = value

    # 4. Ergebnis-DataFrame bauen
    result_df = pd.DataFrame({
        'Time/s': list(best_overall.keys()),
        'Best Effort': list(best_overall.values())
    })

    return result_df



# def aggregate_best_efforts_from_json_with_fatigue(json_path, windows, fatigue_filter="Frisch", tired_limit=1500000, very_tired_limit=3000000):
#     # 1. JSON einlesen und Dateinamen extrahieren
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     csv_files = data['csv_files']

#     best_overall = {window: float('-inf') for window in windows}

#     for csv_file in csv_files:
#         df = pd.read_csv(csv_file)
#         if "power" not in df.columns:
#             continue

#         # Ermüdungsfilter anwenden
#         if "energy_per_minute" in df.columns:
#             energy_list = df["energy_per_minute"].fillna(0).tolist()
#         else:
#             # Alternativ: Energie selbst berechnen aus Power (z. B. df["power"].rolling(60).sum()*1)
#             energy_list = df["power"].fillna(0).tolist()  # Dummy

#         fresh_index, tired_index, very_tired_index = fatigue_indices(
#             energy_list, tired_limit, very_tired_limit
#         )

#         if fatigue_filter == "Frisch":
#             start_index = fresh_index or 0
#         elif fatigue_filter == "Ermüdet":
#             start_index = tired_index or 0
#         elif fatigue_filter == "Sehr müde":
#             start_index = very_tired_index or 0
#         else:
#             start_index = 0

#         # DataFrame ab Filter-Index verwenden
#         df_filtered = df.iloc[start_index:].reset_index(drop=True)
#         df_efforts = find_best_effort(df_filtered["power"], windows)
#         for i, row in df_efforts.iterrows():
#             window = row['Time/s']
#             value = row['Best Effort']
#             if pd.notnull(value) and value > best_overall[window]:
#                 best_overall[window] = value

#     # Ergebnis-DataFrame bauen
#     result_df = pd.DataFrame({
#         'Time/s': list(best_overall.keys()),
#         'Best Effort': list(best_overall.values())
#     })

#     return result_df

if __name__ == "__main__":

    #training_data = load_data()
    #avg_power = average_power_per_minute(training_data)
    #print(avg_power)
    #used_energy_per_minute = used_energy_per_minute(avg_power)
    #print(f"Used energy per minute: {used_energy_per_minute}")

    #fresh_index, tired_index, very_tired_index = fatigue_indices(used_energy_per_minute)
    #print(f"Fresh index: {fresh_index}")
    #print(f"Tired index: {tired_index}")
    #print(f"Very tired index: {very_tired_index}")

    df_best = aggregate_best_efforts_from_json(
    "cycling_data_tadej.json",
    "Pogacar_Tadej"
        )
    print(df_best)