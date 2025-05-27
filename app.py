import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su naujais separatoriais")

# 1) Stulpelių ir dienų apibrėžimai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]  # 5 dienos pavyzdžiui
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki", "Vieta",
    "Atsakingas", "Tušti km",
    "Krauti km", "Kelių išlaidos", "Frachtas"
]

trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321",2,24),
]

# 2) Filtrai
all_trucks = [t[2] for t in trucks_info]
all_dates = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", all_trucks, default=all_trucks)
sel_dates = st.multiselect("📅 Filtruok datas", all_dates, default=all_dates)

# 3) CSS separatoriams
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:2;}
  /* horizontalios linijos po 2,4,6,... eilučių */
  tr.divider-row td {border-top:3px solid #000 !important;}
  /* vertikalios linijos po 9,20,31,42,53,... stulpelių */
  th.sep, td.sep {border-left:3px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# 4) Sudarome visų stulpelių pavadinimų sąrašą
cols = common_headers + [""]  # dummy po "Savaitinė atstova"
for d in sel_dates:
    cols += [f"{d} – {h}" for h in day_headers]

# 5) Apskaičiuojame vertikalių separatorių pozicijas (1-based)
sep_positions = []
offset = len(common_headers) + 1  # po šio stulpelio dummy
# pirmas po common+dummy = position offset+len(day_headers)=?
# bet user wants after col9,20,31,... so:
sep_positions = [9 + 11*k for k in range((len(cols)//11)+1)]

# 6) Header: stulpelių numeriai
html = "<table>\n<tr><th></th>"
for i in range(1, len(cols)+1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 7) Header: pavadinimai su sep klasėmis
html += "<tr><th>#</th>"
for idx, h in enumerate(cols, start=1):
    cls = "sep" if idx in sep_positions else ""
    html += f'<th class="{cls}">{h}</th>'
html += "</tr>\n"

# 8) Duomenų eilutės su horizont. separatoriais kas 2 eilutes
row_counter = 0
for tr in trucks_info:
    tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst = tr
    if truck not in sel_trucks:
        continue

    # IŠKROVIMAS
    row_counter += 1
    row_cls = "divider-row" if row_counter % 2 == 1 and row_counter > 1 else ""
    html += f'<tr class="{row_cls}"><td>{row_counter}</td>'
    # sujungti common stulpeliai per 2 eilutes
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    # dummy po Savaitinė atstova
    idx_dummy = len(common_headers)+1
    for idx, _ in enumerate(cols[len(common_headers):len(common_headers)+1], start=len(common_headers)+1):
        cls = "sep" if idx in sep_positions else ""
        html += f'<td class="{cls}"></td>'
    # dienų laukai
    for d in sel_dates:
        for j, h in enumerate(day_headers, start=1):
            idx_col = cols.index(f"{d} – {h}") + 1
            cls = "sep" if idx_col in sep_positions else ""
            if h == "Atvykimo laikas":
                val = datetime.now().strftime("%H:%M")
            elif h == "Vieta":
                val = random.choice(["Vilnius","Kaunas","Berlin"])
            else:
                val = ""
            html += f'<td class="{cls}">{val}</td>'
    html += "</tr>\n"

    # PAKROVIMAS
    row_counter += 1
    row_cls = "divider-row" if row_counter % 2 == 1 else ""
    html += f'<tr class="{row_cls}"><td>{row_counter}</td>'
    # tušti common stulpeliai
    for idx in range(len(common_headers)):
        html += "<td></td>"
    # dummy po Savaitinė atstova
    idx_dummy = len(common_headers)+1
    cls = "sep" if idx_dummy in sep_positions else ""
    html += f'<td class="{cls}"></td>'
    # dienų pakrovimo duomenys
    for d in sel_dates:
        for j, h in enumerate(day_headers, start=1):
            idx_col = cols.index(f"{d} – {h}") + 1
            cls = "sep" if idx_col in sep_positions else ""
            if h == "B. darbo laikas":
                val = random.randint(8,10)
            elif h == "L. darbo laikas":
                val = random.randint(4,6)
            elif h == "Atvyk. laikas":
                val = f"{random.randint(7,9)}:00"
            elif h == "Nuo":
                val = "08:00"
            elif h == "Iki":
                val = "16:00"
            elif h == "Vieta":
                val = random.choice(["Riga","Poznan"])
            elif h == "Frachtas":
                val = round(random.uniform(500,1200),2)
            else:
                val = ""
            html += f'<td class="{cls}">{val}</td>'
    html += "</tr>\n"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)

