import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su Excel-stiliaus filtru ant 'Ekspeditorius'")

# 1) Bendri ir dienų stulpeliai
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
    "Laikas iki", "Vieta",
    "Atsakingas", "Tušti km",
    "Krauti km", "Kelių išlaidos",
    "Frachtas"
]

# 2) Pavyzdiniai vilkikai
trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321",2,24),
]

# 3) Surenkame duomenis DataFrame formatui
rows = []
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    for phase in ["Iškrovimas", "Pakrovimas"]:
        row = {
            "Transporto grupė": tr_grp,
            "Ekspedicijos grupės nr.": exp_grp,
            "Vilkiko nr.": truck,
            "Ekspeditorius": eksp,
            "Trans. vadybininkas": tvad,
            "Priekabos nr.": prk,
            "Vair. sk.": v_sk,
            "Savaitinė atstova": atst,
            "Fazė": phase
        }
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

# 4) Konfigūruojame AgGrid su filtru „Ekspeditorius“
gb = GridOptionsBuilder.from_dataframe(df)
# Įjungiame bendrus filtrus visiems stulpeliams (Excel stilius)
gb.configure_default_column(
    filter="agMultiColumnFilter",
    floatingFilter=True,
    sortable=True,
    resizable=True
)
# Papildomai užtikriname, kad 'Ekspeditorius' turėtų teksto filtro dropdown
gb.configure_column(
    "Ekspeditorius",
    filter="agSetColumnFilter",
    sortable=True,
    floatingFilter=True
)
grid_options = gb.build()

# 5) Atvaizduojame interaktyvią lentelę
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    theme="streamlit"
)
