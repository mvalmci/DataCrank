#power_curve generieren und plotten
#müde power curve z.B.: 1500kJ verbraucht
#sehr müde power curve z.B.: 3000kJ verbraucht
#über gesamten Datensatz drübergehen und Energieverbrauch in Json hinzufügen

import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px
import json

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
    
    energy_per_minute = power_per_full_minutes * 60  #von Watt zu joule

    df = pd.DataFrame(energy_per_minute, columns=["Energy (Joules)"])

    return energy_per_minute, df

    

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
    #json lesen
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    csv_files = data['csv_files']

    #dict
    best_overall = {window: float('-inf') for window in windows}
    #über csvs iterieren
    for csv_file in csv_files:
        full_path = csv_file
        df = pd.read_csv(full_path)
        if "power" not in df.columns:
            continue
        df_efforts = find_best_effort(df["power"], windows)
        for i, row in df_efforts.iterrows():
            window = row['Time/s']
            value = row['Best Effort']
            if pd.notnull(value) and value > best_overall[window]:
                best_overall[window] = value

    #df zum zurückgeben
    result_df = pd.DataFrame({
        'Time/s': list(best_overall.keys()),
        'Best Effort': list(best_overall.values())
    })

    return result_df



def fatigue_powercurves_from_json(
    json_path, 
    windows=[30, 60, 180, 300, 600, 1800, 2000], 
    tired_limit=150000, 
    very_tired_limit=300000
):
    #wie oben, json lesen
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    csv_files = data['csv_files']

    #seperate dicts
    tired_best = {window: float('-inf') for window in windows}
    very_tired_best = {window: float('-inf') for window in windows}

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        if "power" not in df.columns:
            continue

        #Fatigue indices ausrechnen
        avg_power = df["power"].rolling(window=60, min_periods=60).mean().dropna().reset_index(drop=True)
        power_per_minute = avg_power.iloc[59::60].reset_index(drop=True)
        energy_per_minute = power_per_minute * 60  #wieder in joule

        fresh_idx, tired_idx, very_tired_idx = fatigue_indices(energy_per_minute, tired_limit, very_tired_limit)

        
        tired_start = (tired_idx + 1) * 60 if tired_idx is not None else None
        very_tired_start = (very_tired_idx + 1) * 60 if very_tired_idx is not None else None
        n = len(df)

        #tired_start bis ende
        if tired_start is not None and very_tired_start is not None and tired_start < very_tired_start:
            tired_section = df["power"].iloc[tired_start:n].reset_index(drop=True)
            tired_efforts = find_best_effort(tired_section, windows)
            for i, row in tired_efforts.iterrows():
                window = row['Time/s']
                value = row['Best Effort']
                if pd.notnull(value) and value > tired_best[window]:
                    tired_best[window] = value

        #very_tired_start bis ende
        if very_tired_start is not None and very_tired_start < n:
            very_tired_section = df["power"].iloc[very_tired_start:].reset_index(drop=True)
            very_tired_efforts = find_best_effort(very_tired_section, windows)
            for i, row in very_tired_efforts.iterrows():
                window = row['Time/s']
                value = row['Best Effort']
                if pd.notnull(value) and value > very_tired_best[window]:
                    very_tired_best[window] = value

    #ergebnisse als ---_df
    tired_df = pd.DataFrame({
        'Time/s': list(tired_best.keys()),
        'Best Effort': list(tired_best.values())
    })
    very_tired_df = pd.DataFrame({
        'Time/s': list(very_tired_best.keys()),
        'Best Effort': list(very_tired_best.values())
    })

    return tired_df, very_tired_df

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


    tired_df, very_tired_df = fatigue_powercurves_from_json(
        "cycling_data_tadej.json",
        windows=[30, 60, 180, 300, 600, 1800, 2000],
        tired_limit=150000,
        very_tired_limit=300000    
    )   
    print(tired_df, very_tired_df)