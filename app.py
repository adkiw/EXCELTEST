import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ─── Duomenų bazės prisijungimas ───────────────────────────────────────────────
conn = sqlite3.connect('dispo_new.db', check_same_thread=False)
c = conn.cursor()

# ─── Modulių pasirinkimas ────────────────────────────────────────────────────
modulis = st.sidebar.radio("📂 Pasirink modulį", ["DISPO"])

# ─── DISPO ────────────────────────────────────────────────────────────────────
if modulis == "DISPO":
    st.title("DISPO – Planavimo lentelė")

    # 1) Bendri stulpeliai (suliejami per 2 eilutes)
    common_columns = [
        "Transporto grupė",
        "Ekspedicijos grupės nr.",
        "Vilkiko nr.",
        "Ekspeditorius",
        "Trans. vadybininkas",
        "Priekabos nr.",
        "Vair. sk.",
        "Savaitinė atstova"
    ]

    # 2) Dienos stulpeliai (kartojasi kiekvienai datai)
    day_columns = [
        "Bendras darbo laikas",
        "Likęs darbo laikas atvykus",
        "Atvykimo laikas",
        "Laikas nuo",
        "Laikas iki",
        "Vieta",
        "Atsakingas",
        "Tušti km",
        "Krauti km",
        "Kelių išlaidos (EUR)",
        "Frachtas (EUR)"
    ]

    # 3) Sukuriame 10 datų
    start_date = datetime.today().date()
    dienos = [start_date + timedelta(days=i) for i in range(10)]

    # 4) Finalūs stulpeliai: bendri + kiekvienos dienos blocʼas
    final_columns = common_columns.copy()
    for diena in dienos:
        ds = diena.strftime("%Y-%m-%d")
        final_columns += [f"{ds} – {col}" for col in day_columns]

    # 5) Pavyzdiniai vilkikai (8 bendri laukai):
    #    (transporto_grupė, eksp_grupės_nr, vilkiko_nr, ekspeditorius,
    #     transporto_vadyb, priekaba_nr, vair_sk, savaite_atstova)
    vilkikai_info = [
        ("1", "2", "ABC123", "Tomas Mickus",   "Laura Juknevičienė", "PRK001", 2, 24),
        ("3", "1", "XYZ789", "Greta Kairytė",  "Jonas Petrauskas",   "PRK009", 1, 45),
    ]

    rows = []
    for tr_grp, exp_grp, vilk_nr, eksp, tvad, prk, v_sk, atst in vilkikai_info:
        #  a) IŠKROVIMAS – bendri laukai + minimalūs duomenys
        base_unload = [tr_grp, exp_grp, vilk_nr, eksp, tvad, prk, v_sk, atst]
        row_unload = base_unload.copy()
        for _ in dienos:
            # tik laikas ir vieta: kiti laukai tušti
            laikas = datetime.now().strftime("%H:%M")
            row_unload += [
                "",  # Bendras darbo laikas
                "",  # Likęs darbo laikas atvykus
                laikas,
                "",  # Laikas nuo
                "",  # Laikas iki
                random.choice(["Riga", "Poznan", "Klaipėda"]),
                "",  # Atsakingas
                "",  # Tušti km
                "",  # Krauti km
                "",  # Kelių išlaidos
                ""   # Frachtas
            ]
        rows.append(row_unload)

        #  b) PAKROVIMAS – bendri laukai tušti + visa info
        base_load = [""] * len(common_columns)
        row_load = base_load.copy()
        for _ in dienos:
            laikas = datetime.now().strftime("%H:%M")
            kms_tusti  = random.randint(20, 120)
            kms_krauti = random.randint(400, 900)
            fracht     = round(kms_krauti * random.uniform(1.0, 2.5), 2)
            row_load += [
                9,                # Bendras darbo laikas
                6,                # Likęs darbo laikas atvykus
                laikas,           # Atvykimo laikas
                "08:00",          # Laikas nuo
                "16:00",          # Laikas iki
                random.choice(["Vilnius", "Kaunas", "Berlin"]),
                tvad,             # Atsakingas = transporto vadybininkas
                kms_tusti,        # Tušti km
                kms_krauti,       # Krauti km
                round(kms_tusti*0.2,2),  # Kelių išlaidos
                fracht            # Frachtas
            ]
        rows.append(row_load)

    # 6) Sukuriame DataFrame ir atvaizduojame
    df_dispo = pd.DataFrame(rows, columns=final_columns)
    st.dataframe(df_dispo, use_container_width=True)
