#power_curve generieren und plotten
#müde power curve z.B.: 1500kJ verbraucht
#sehr müde power curve z.B.: 3000kJ verbraucht
#über gesamten Datensatz drübergehen und Energieverbrauch in Json hinzufügen

import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px

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




if __name__ == "__main__":

    training_data = load_data()
    avg_power = average_power_per_minute(training_data)
    print(avg_power)
    used_energy_per_minute = used_energy_per_minute(avg_power)
    print(f"Used energy per minute: {used_energy_per_minute}")

    fresh_index, tired_index, very_tired_index = fatigue_indices(used_energy_per_minute)
    print(f"Fresh index: {fresh_index}")
    print(f"Tired index: {tired_index}")
    print(f"Very tired index: {very_tired_index}")


