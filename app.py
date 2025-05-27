import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su interaktyviu filtru „Ekspeditorius“")

# ─── 1) Duomenų generavimas ────────────────────────────────────────────────────
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Atsakingas",      "Tušti km",
    "Krauti km",       "Kelių išlaidos",
    "Frachtas"
]

trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321",2,24),
]

rows = []
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    for phase in ["Iškrovimas", "Pakrovimas"]:
        row = {h: "" for h in common_headers}
        if phase == "Iškrovimas":
            vals = [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]
            for h, v in zip(common_headers, vals):
                row[h] = v
        # pasilaukiam fazės rodymui
        row["Fazė"] = phase
        for d in dates:
            for h in day_headers:
                col = f"{d} – {h}"
                if phase == "Iškrovimas":
                    if h == "Atvykimo laikas":
                        row[col] = datetime.now().strftime("%H:%M")
                    elif h == "Vieta":
                        row[col] = random.choice(["Vilnius","Kaunas"])
                    else:
                        row[col] = ""
                else:
                    if h == "B. darbo laikas":
                        row[col] = random.randint(8,10)
                    elif h == "L. darbo laikas":
                        row[col] = random.randint(4,6)
                    elif h == "Atvykimo laikas":
                        row[col] = f"{random.randint(7,9)}:00"
                    elif h == "Laikas nuo":
                        row[col] = "08:00"
                    elif h == "Laikas iki":
                        row[col] = "16:00"
                    elif h == "Vieta":
                        row[col] = random.choice(["Poznan","Riga"])
                    elif h == "Frachtas":
                        row[col] = round(random.uniform(800,1200),2)
                    else:
                        row[col] = ""
        rows.append(row)

df = pd.DataFrame(rows)

# ─── 2) Filtras „Ekspeditorius“ ───────────────────────────────────────────────
eksp_list = sorted(set(df["Ekspeditorius"]))
selected_eksp = st.multiselect(
    "Filtruok pagal ekspeditorių",
    options=eksp_list,
    default=eksp_list
)
filtered_df = df[df["Ekspeditorius"].isin(selected_eksp)]

# ─── 3) Lentelės atvaizdavimas ────────────────────────────────────────────────
st.dataframe(filtered_df, use_container_width=True)
