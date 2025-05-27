# Pakartojame kodą DISPO moduliui su sumergintais bendrais laukais

import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Duomenų bazės prisijungimas
conn = sqlite3.connect('dispo_new.db', check_same_thread=False)
c = conn.cursor()

# Modulių pasirinkimas
modulis = st.sidebar.radio("📂 Pasirink modulį", ["DISPO"])

if modulis == "DISPO":
    st.title("DISPO – Planavimo lentelė")

    # Bendri stulpeliai
    common_columns = [
        "Transporto grupė", "Ekspedicijos grupės nr.",
        "Vilkiko nr.", "Ekspeditorius", "Trans. vadybininkas",
        "Priekabos nr.", "Vair. sk.", "Savaitinė atstova"
    ]
    # Dienos stulpeliai
    day_columns = [
        "Bendras darbo laikas", "Likęs darbo laikas atvykus", "Atvykimo laikas",
        "Laikas nuo", "Laikas iki", "Vieta", "Atsakingas",
        "Tušti km", "Krauti km", "Kelių išlaidos (EUR)", "Frachtas (EUR)"
    ]

    # Datos
    start_date = datetime.today().date()
    dienos = [start_date + timedelta(days=i) for i in range(10)]
    final_columns = common_columns.copy()
    for diena in dienos:
        data_str = diena.strftime("%Y-%m-%d")
        final_columns += [f"{data_str} – {col}" for col in day_columns]

    # Vilkikai
    vilkikai_info = [
        ("ABC123", "Tomas Mickus", "Laura Juknevičienė", "PRK001", 2, 24, "1", "2"),
        ("XYZ789", "Greta Kairytė", "Jonas Petrauskas", "PRK009", 1, 45, "1", "3")
    ]

    rows = []
    for vilk in vilkikai_info:
        # Iškrovimo eilutė
        row_unload = list(vilk)
        for _ in dienos:
            laikas = datetime.now().strftime("%H:%M")
            row_unload += [9, 6, laikas, "", "", random.choice(["Riga", "Poznan"]), "", "", "", "", ""]
        rows.append(row_unload)

        # Pakrovimo eilutė (bendri tušti)
        row_load = [""] * len(vilk)
        for _ in dienos:
            laikas = datetime.now().strftime("%H:%M")
            row_load += [9, 6, laikas, "08:00", "16:00", random.choice(["Vilnius", "Kaunas"]),
                         vilk[2], random.randint(30, 120), random.randint(400, 900),
                         20.0, random.randint(800, 2000)]
        rows.append(row_load)

    df_dispo = pd.DataFrame(rows, columns=final_columns)
    st.dataframe(df_dispo, use_container_width=True)
