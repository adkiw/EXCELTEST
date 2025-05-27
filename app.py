import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su filtrais ir atskyrimais")

# ─── 1) Bendri ir dienų antraštės ────────────────────────────────────────────
common_headers = [
    "Transporto grupė",
    "Ekspedicijos grupės nr.",
    "Vilkiko nr.",
    "Ekspeditorius",
    "Trans. vadybininkas",
    "Priekabos nr.",
    "Vair. sk.",
    "Savaitinė atstova"
]
day_headers = [
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

# ─── 2) Datos ─────────────────────────────────────────────────────────────────
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# ─── 3) Pavyzdiniai 5 vilkikai ────────────────────────────────────────────────
trucks_info = [
    ("1","2","ABC123","Tomas Mickus",   "Laura Juknevičienė","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė",  "Jonas Petrauskas",  "PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas Mickus",     "PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta Kairytė",     "PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa Mikalausk.","PRK321",2,24),
]

# ─── 4) Filtrai ───────────────────────────────────────────────────────────────
all_trucks = [t[2] for t in trucks_info]
sel_trucks = st.multiselect("🛻 Pasirink vilkikus", options=all_trucks, default=all_trucks)

all_dates = dates.copy()
sel_dates = st.multiselect("📅 Pasirink datas", options=all_dates, default=all_dates)

# ─── 5) Pradedame HTML lentelę ────────────────────────────────────────────────
html = """
<style>
  table {border-collapse: collapse; width: 100%;}
  th, td {border: 1px solid #ddd; padding: 4px; text-align: center;}
  th {background: #f0f0f0; position: sticky; top: 0; z-index: 1;}
  .truck-divider td {border-top: 3px solid #444 !important;}
  .date-divider th {border-left: 3px solid #0073e6 !important;}
</style>
<table>
  <tr>
"""
# bendros antraštės
for h in common_headers:
    html += f"<th>{h}</th>"

# dienų antraštės tik užfiltruotoms datoms
for d in sel_dates:
    for dh in day_headers:
        html += f'<th class="date-divider">{d}<br>– {dh}</th>'
html += "</tr>\n"

# ─── 6) Pildome eilutes su rowSpan ir atskyrimais ────────────────────────────
first = True
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if truck not in sel_trucks:
        continue

    # CSS klasė, kad prieš kiekvieną vilkiko grupę būtų storesnė juosta
    divider_cls = "truck-divider" if not first else ""
    first = False

    #  a) IŠKROVIMAS
    html += f'<tr class="{divider_cls}">'
    # suliejame bendrus stulpelius per dvi eilutes
    for val in [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]:
        html += f'<td rowspan="2">{val}</td>'
    # operacijos duomenys
    for d in sel_dates:
        t_arr = datetime.now().strftime("%H:%M")
        city = random.choice(["Riga","Poznan","Klaipėda","Tallinn"])
        html += (
            "<td></td>"  # Bendras darbo laikas
            "<td></td>"  # Likęs darbo laikas
            f"<td>{t_arr}</td>"  # Atvykimo laikas
            "<td></td><td></td>"  # Laikas nuo / iki tušti
            f"<td>{city}</td>"
            "<td></td><td></td><td></td><td></td><td></td>"
        )
    html += "</tr>\n"

    #  b) PAKROVIMAS
    html += f'<tr class="{divider_cls}">'
    html += "<td></td>" * len(common_headers)
    for d in sel_dates:
        t1 = f"{random.randint(7,9)}:00"
        t2 = f"{random.randint(15,17)}:00"
        cty = random.choice(["Vilnius","Kaunas","Berlin","Warsaw"])
        km_t = random.randint(20,120)
        km_k = random.randint(400,900)
        cost = round(km_t*0.2,2)
        fr = round(km_k*random.uniform(1.0,2.5),2)
        html += (
            f"<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>{t2}</td>"
            f"<td>{cty}</td><td>{tvad}</td>"
            f"<td>{km_t}</td><td>{km_k}</td><td>{cost}</td><td>{fr}</td>"
        )
    html += "</tr>\n"

html += "</table>"

# ─── 7) Atvaizduojame HTML ───────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
