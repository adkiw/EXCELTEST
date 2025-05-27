import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su HTML ir CSS separatoriais")

# ─── 1) Duomenų apibrėžimai ───────────────────────────────────────────────────
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.", "Vilkiko nr.",
    "Ekspeditorius", "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
# 10 dienų horizontaliai
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
# Pavyzdiniai vilkikai po 2 eilutes kiekvienam
trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321",2,24),
]

# ─── 2) Filtrai multiselect ───────────────────────────────────────────────────
all_trucks = [t[2] for t in trucks_info]
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", options=all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   options=all_dates,  default=all_dates)

# ─── 3) CSS pagrindui ir separatoriams ────────────────────────────────────────
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:2;}
  /* Kiekvieno naujo vilkiko FIRST row: juodas border-top */
  tr.divider-row td {border-top:3px solid #000 !important;}
  /* Vert. separatoriai: po Savaitinė atstova ir po kiekvienos dienos Frachtas */
  th.sep, td.sep {border-left:3px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# ─── 4) Statome HTML lentelę ─────────────────────────────────────────────────
html = "<table>\n  <tr>"
# a) bendri headeriai
for h in common_headers:
    html += f"<th>{h}</th>"
# b) įterpiame sep klasę po „Savaitinė atstova“
html += '<th class="sep"></th>'
# c) dienų headeriai – tik ta data, kuri atrinkta
for d in sel_dates:
    for dh in day_headers:
        cls = "sep" if dh == "Frachtas" else ""
        html += f'<th class="{cls}">{d}<br>– {dh}</th>'
html += "</tr>\n"

# ─── 5) Pildome eiles su rowspan ir horizontal separator flag’u ──────────────
first = True
for (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst) in trucks_info:
    if truck not in sel_trucks:
        continue

    # markuojame šią eilutę kaip separator-row, jei ne pirmas vilkikas
    row_cls = "" if first else "divider-row"
    first = False

    # ► IŠKROVIMAS (ROWSPAN)
    html += f'  <tr class="{row_cls}">'
    # sugebiname bendrus per 2 eilutes
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    # dummy sep cell po Savaitinė atstova
    html += "<td></td>"
    # kiekvienos dienos duomenys (tik laikas + vieta)
    for d in sel_dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin","Warsaw"])
        html += (
            "<td></td><td></td>"         # B. darbo laikas, L. darbo laikas
            f"<td>{t}</td>"              # Atvykimo laikas
            "<td></td><td></td>"         # Laikas nuo, Laikas iki
            f"<td>{city}</td>"           # Vieta
            "<td></td><td></td><td></td>"# Atsakingas, Tušti km, Krauti km
            "<td></td>"                  # Kelių išlaidos
            "<td class='sep'>"           # Frachtas su sep klasu
            f"{round(random.uniform(500,900),2)}</td>"
        )
    html += "</tr>\n"

    # ► PAKROVIMAS
    html += f'  <tr class="{row_cls}">'
    # tušti bendri + dummy sep
    html += "<td></td>"*(len(common_headers)+1)
    for d in sel_dates:
        t1   = f"{random.randint(7,9)}:00"
        kms  = random.randint(20,120)
        fra  = round(random.uniform(800,1200),2)
        html += (
            f"<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{random.choice(['Riga','Poznan','Tallinn'])}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{kms*random.randint(3,8)}</td>"
            "<td></td>"
            f"<td class='sep'>{fra}</td>"
        )
    html += "</tr>\n"

html += "</table>"

# ─── 6) Atvaizduojame ─────────────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
