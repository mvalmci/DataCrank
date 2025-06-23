import pandas as pd
import os
import numpy as np

def max_hr(folder_path, hr_column='hr'):
  
    max_hr = np.nan
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                # Prüfen, ob die Spalte existiert
                if hr_column in df.columns:
                    current_max = pd.to_numeric(df[hr_column], errors='coerce').max()
                    if np.isnan(max_hr) or (not np.isnan(current_max) and current_max > max_hr):
                        max_hr = current_max
            except Exception as e:
                print(f"Fehler bei Datei {file}: {e}")
    return max_hr

def get_km_per_csv(df , distance_column='km'):
    km = df[distance_column].values
    km_per_csv = 0.0
    for i in range(1, len(km)):
        if not np.isnan(km[i]) and not np.isnan(km[i-1]):
            km_per_csv += km[i] - km[i-1]
    return km_per_csv

def total_km(folder_path, distance_column='km'):
    total_km = 0.0
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                km = get_km_per_csv(df, distance_column)
                total_km += km
            except Exception as e:
                print(f"Fehler bei Datei {file}: {e}")
    return total_km

def calculate_elevation_gain(df, altitude_column='alt'):

    altitudes = df[altitude_column].values
    elevation_gain = 0.0
    for i in range(1, len(altitudes)):
        diff = altitudes[i] - altitudes[i-1]
        if diff > 0:
            elevation_gain += diff
    return elevation_gain

def total_elevation_gain(folder_path, altitude_column='alt'):
   
    total_gain = 0.0
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                gain = calculate_elevation_gain(df, altitude_column)
                total_gain += gain
            except Exception as e:
                print(f"Fehler bei Datei {file}: {e}")

        
    return total_gain



if __name__ == "__main__":
    # Example usage
    df = pd.read_csv('Pogacar_Tadej\\2016_02_15_15_53_47.csv')
    elevation = calculate_elevation_gain(df)
    print(f"Total elevation gain: {elevation:.2f} m")
    folder = "Pogacar_Tadej"
    result = total_elevation_gain(folder)
    print(f"Gesamter Elevation Gain in {folder}: {result:.2f} m")

    
    hr_max = max_hr(folder)
    print(f"Höchste Herzfrequenz in {folder}: {hr_max}")

    km = get_km_per_csv(df)
    print(f"Kilometer in der CSV: {km:.2f} km")

    total_km_value = total_km(folder)
    print(f"Gesamte Kilometer in {folder}: {total_km_value:.2f} km")
