import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė (HTML su rowspan, 5 vilkikai)")

# ─── 1) Bendri ir dienų stulpeliai ────────────────────────────────────────────
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

# ─── 2) Datos (10 d.) horizontaliai ────────────────────────────────────────────
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# ─── 3) Pavyzdiniai 5 vilkikai ────────────────────────────────────────────────
# kiekvienas įrašas: (tr_grp, exp_grp, truck_nr, eksp, tvad, prk, v_sk, atst)
trucks_info = [
    ("1","2","ABC123","Tomas Mickus",   "Laura Juknevičienė","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė",  "Jonas Petrauskas",  "PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas Mickus",     "PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta Kairytė",     "PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa Mikalausk.","PRK321",2,24),
]

# ─── 4) Kuriame HTML ───────────────────────────────────────────────────────────
html = """
<style>
  table {border-collapse: collapse; width: 100%;}
  th, td {border: 1px solid #ddd; padding: 4px; text-align: center;}
  th {background: #f0f0f0;}
</style>
<table>
  <tr>
"""
# antraštės
for h in common_headers:
    html += f"<th>{h}</th>"
for d in dates:
    for dh in day_headers:
        html += f"<th>{d}<br>– {dh}</th>"
html += "</tr>\n"

# ─── 5) Eilutės kiekvienam vilkikui ───────────────────────────────────────────
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    # IŠKROVIMAS (rowspan)
    html += "<tr>"
    for val in [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]:
        html += f'<td rowspan="2">{val}</td>'
    for _ in dates:
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
    # PAKROVIMAS
    html += "<tr>"
    html += "<td></td>" * len(common_headers)
    for _ in dates:
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

# ─── 6) Atvaizduojame ───────────────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
