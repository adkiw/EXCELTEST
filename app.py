import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("DISPO – Paprasta interaktyvi lentelė be separatorių")

# 1) Baziniai nustatymai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Frachtas"
]
trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("3","1","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","5","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
]

# 2) Renkame duomenis
rows = []
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    for phase in ["Iškrovimas", "Pakrovimas"]:
        row = {}
        # Bendri laukai
        if phase == "Iškrovimas":
            values = [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]
            for h, val in zip(common_headers, values):
                row[h] = val
        else:
            for h in common_headers:
                row[h] = ""
        # Papildoma fazė stulpelis
        row["Fazė"] = phase
        # Datos laukai
        for d in dates:
            for h in day_headers:
                col = f"{d} – {h}"
                if phase == "Iškrovimas":
                    if h == "Atvykimo laikas":
                        row[col] = datetime.now().strftime("%H:%M")
                    elif h == "Vieta":
                        row[col] = random.choice(["Vilnius", "Kaunas", "Riga"])
                    else:
                        row[col] = ""
                else:
                    if h == "B. darbo laikas":
                        row[col] = random.randint(8, 10)
                    elif h == "L. darbo laikas":
                        row[col] = random.randint(4, 6)
                    elif h == "Atvykimo laikas":
                        row[col] = f"{random.randint(7, 9)}:00"
                    elif h == "Laikas nuo":
                        row[col] = "08:00"
                    elif h == "Laikas iki":
                        row[col] = "16:00"
                    elif h == "Vieta":
                        row[col] = random.choice(["Poznan", "Tallinn"])
                    elif h == "Frachtas":
                        row[col] = round(random.uniform(800, 1200), 2)
                    else:
                        row[col] = ""
        rows.append(row)

df = pd.DataFrame(rows)

# 3) Atvaizduojame lentelę be jokių specialių linijų
st.dataframe(df, use_container_width=True)
