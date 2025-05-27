import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – planavimas su separatoriais")

# 1) Bendri ir dienų antraštės
common_headers = [
    "Transporto grupė",
    "Ekspedicijos grupės nr.",
    "Vilkiko nr.",
    "Ekspeditorius",
    "Trans. vadybininkas",
    "Priekabos nr.",
    "Vair. sk.",
    "Savaitinė atstova",
]
day_headers = [
    "B. darbo laikas",
    "L. darbo laikas",
    "Atvykimo laikas",
    "Laikas nuo",
    "Laikas iki",
    "Vieta",
    "Atsakingas",
    "Tušti km",
    "Krauti km",
    "Kelių išlaidos",
    "Frachtas",
]

# 2) Datos
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# 3) Vilkikų duomenys
trucks_info = [
    ("1","2","ABC123","Tomas Mickus",   "Laura Juknevičienė","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė",  "Jonas Petrauskas",  "PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas Mickus",     "PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta Kairytė",     "PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa Mikalausk.","PRK321",2,24),
]

# 4) Filtrai
all_trucks = [t[2] for t in trucks_info]
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", options=all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   options=all_dates, default=all_dates)

# 5) CSS: storos linijos
st.markdown("""
<style>
  table {border-collapse: collapse; width: 100%; margin-top: 10px;}
  th, td {border: 1px solid #ccc; padding: 4px; text-align: center;}
  th {background: #f5f5f5; position: sticky; top: 0; z-index: 2;}

  /* vertical separator before each new date-block */
  th.date-divider, td.date-divider {
    border-left: 3px solid #0073e6 !important;
  }

  /* horizontal separator before each new truck-block */
  tr.truck-divider td {
    border-top: 3px solid #d00 !important;
  }
</style>
""", unsafe_allow_html=True)

# 6) Generuojame HTML lentelę
html = "<table><tr>"

# bendros antraštės
for h in common_headers:
    html += f"<th>{h}</th>"

# dienų antraštės tik užfiltruotoms datoms
for d in sel_dates:
    for dh in day_headers:
        html += f'<th class="date-divider">{d}<br>– {dh}</th>'
html += "</tr>"

first_truck = True
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if truck not in sel_trucks:
        continue

    # nustatom klasę horizontal. separator
    row_cls = "" if first_truck else "truck-divider"
    first_truck = False

    # a) IŠKROVIMAS
    html += f'<tr class="{row_cls}">'
    # suliejam bendrus langelius per 2 eilutes
    for val in [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]:
        html += f'<td rowspan="2">{val}</td>'
    # kiekvienos datos tik laikas/vieta
    for d in sel_dates:
        t_arr = datetime.now().strftime("%H:%M")
        city  = random.choice(["Riga","Poznan","Klaipėda","Tallinn"])
        html += (
            "<td></td>"  # B. darbo laikas
            "<td></td>"  # L. darbo laikas
            f"<td>{t_arr}</td>"
            "<td></td><td></td>"
            f'<td class="date-divider">{city}</td>'
            "<td></td><td></td><td></td><td></td><td></td>"
        )
    html += "</tr>"

    # b) PAKROVIMAS
    html += f'<tr class="{row_cls}">'
    html += "<td></td>" * len(common_headers)
    for d in sel_dates:
        t1   = f"{random.randint(7,9)}:00"
        t2   = f"{random.randint(15,17)}:00"
        cty  = random.choice(["Vilnius","Kaunas","Berlin","Warsaw"])
        km_t = random.randint(20,120)
        km_k = random.randint(400,900)
        cost = round(km_t*0.2,2)
        fr   = round(km_k*random.uniform(1.0,2.5),2)
        html += (
            f"<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>{t2}</td>"
            f'<td class="date-divider">{cty}</td>'
            f"<td>{tvad}</td><td>{km_t}</td><td>{km_k}</td><td>{cost}</td><td>{fr}</td>"
        )
    html += "</tr>"

html += "</table>"

# 7) Atvaizduojame
st.markdown(html, unsafe_allow_html=True)
