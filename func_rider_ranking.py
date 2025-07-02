import pandas as pd
import json
import streamlit as st
import numpy as np
import calculate_statistics
import power_curve

def get_sorted_riders_by_elevation(riders):
    def parse_hm(rider):
        try:
            return int(rider.get("total_hm", 0) or 0)
        except (ValueError, TypeError):
            return 0

    sorted_riders = sorted(riders, key=parse_hm, reverse=True)
    return sorted_riders

def get_best_sprinter(riders):
    def parse_30s(rider):
        try:
            return float(rider.get("30", 0) or 0)
        except (ValueError, TypeError):
            return 0

    sorted_riders = sorted(riders, key=parse_30s, reverse=True)
    return sorted_riders



if __name__ == "__main__":

    # with open("rider_db.json", "r", encoding="utf-8") as file:
    #     riders = json.load(file)

    # statistik = get_sorted_riders_by_elevation(riders)

    # # Erster Fahrer hat die meisten Höhenmeter
    # print(statistik)
    # bester_fahrer = statistik[1]
    # print(f"Fahrer mit den meisten Höhenmetern: {bester_fahrer['firstname']} {bester_fahrer['lastname']} ({bester_fahrer['total_hm']} hm)")


    folder_path = "cycling_data_tadej.json"
  
    df_best = power_curve.aggregate_best_efforts_from_json(folder_path, "cycling_data_tadej.json")

