import pandas as pd
from datetime import datetime, timedelta
import random
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Data preparation
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
    ("1","2","ABC123","Tomas","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas","Rasa","PRK321",2,24),
]

# Build DataFrame
rows = []
for tr in trucks_info:
    tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst = tr
    for phase in ["Iškrovimas", "Pakrovimas"]:
        row = dict(zip(common_headers, [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst])) if phase == "Iškrovimas" else {h: "" for h in common_headers}
        row["Fazė"] = phase
        for d in dates:
            for h in day_headers:
                col = f"{d} – {h}"
                if phase == "Iškrovimas":
                    if h == "Atvykimo laikas":
                        row[col] = datetime.now().strftime("%H:%M")
                    elif h == "Vieta":
                        row[col] = random.choice(["Vilnius","Kaunas","Riga"])
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
                        row[col] = random.choice(["Poznan","Tallinn"])
                    elif h == "Frachtas":
                        row[col] = round(random.uniform(800,1200),2)
                    else:
                        row[col] = ""
        rows.append(row)
df = pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("DISPO – Interaktyvi lentelė su freeze ir filtro 'Ekspeditorius'")

# AgGrid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter="agTextColumnFilter", sortable=True, resizable=True, floatingFilter=True)
# Freeze (pin) first 10 columns
for col in df.columns[:10]:
    gb.configure_column(col, pinned='left')
# Add filter on 'Ekspeditorius' explicitly
gb.configure_column("Ekspeditorius", filter="agTextColumnFilter", sortable=True)
grid_options = gb.build()
# Pin first data row to top
grid_options['pinnedTopRowData'] = [df.iloc[0].to_dict()]

# Display
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    theme="streamlit",
    fit_columns_on_grid_load=True
)
