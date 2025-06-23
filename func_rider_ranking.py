import pandas as pd
import json
import streamlit as st
import numpy as np
import calculate_statistics

def get_sorted_riders_by_elevation(riders):
    
    # Stelle sicher, dass total_hm als Zahl interpretiert wird (falls als String gespeichert)
    def parse_hm(rider):
        try:
            return int(rider.get("total_hm", 0))
        except ValueError:
            return 0

    # Sortierung nach Höhenmetern (absteigend)
    sorted_riders = sorted(riders, key=parse_hm, reverse=True)
    return sorted_riders

if __name__ == "__main__":

    with open("rider_db.json", "r", encoding="utf-8") as file:
        riders = json.load(file)

    statistik = get_sorted_riders_by_elevation(riders)

    # Erster Fahrer hat die meisten Höhenmeter
    print(statistik)
    bester_fahrer = statistik[1]
    print(f"Fahrer mit den meisten Höhenmetern: {bester_fahrer['firstname']} {bester_fahrer['lastname']} ({bester_fahrer['total_hm']} hm)")