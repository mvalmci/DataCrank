import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px

def load_data(path="Tadej_trainings/2016_12_14_08_58_06.csv"):

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