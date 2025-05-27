import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su Excel-stiliaus filtrais ir separatoriais")

# ─── 1) Bendri ir dienų antraštės ────────────────────────────────────────────
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

# ─── 2) Datos (10 d.) horizontaliai ────────────────────────────────────────────
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

# ─── 4) Filtrai (Excel-stiliaus multiselect) ─────────────────────────────────
all_trucks = [t[2] for t in trucks_info]
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", options=all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   options=all_dates,  default=all_dates)

# ─── 5) CSS stiliai separatoriams ─────────────────────────────────────────────
st.markdown("""
<style>
  table {border-collapse: collapse; width: 100%; margin-top: 10px;}
  th, td {border: 1px solid #ccc; padding: 4px; text-align: center;}
  th {background: #f5f5f5; position: sticky; top: 0; z-index: 2;}

  /* horizontalus separator tarp vilkikų blokų */
  tr.truck-divider td {
    border-top: 3px solid #000 !important;
  }

  /* vertikalūs separatoriai po Savaitinė atstova ir po kiekvienos dienos Frachtas */
  th.sep, td.sep {
    border-left: 3px solid #000 !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── 6) Generuojame HTML lentelę ──────────────────────────────────────────────
html = "<table><tr>"

# bendros antraštės
for h in common_headers:
    html += f"<th>{h}</th>"

# poreikio tvarka: pridėsim separatoriaus klasę į STULPELĮ po „Savaitinė atstova“
html += '<th class="sep"></th>'  # dummy, kad „Savaitinė atstova“ grupė baigtųsi

# dienų antraštės tik užfiltruotoms datoms – su separator klase po Frachtas
for d in sel_dates:
    for dh in day_headers:
        cls = "sep" if dh == "Frachtas" else ""
        html += f'<th class="{cls}">{d}<br>– {dh}</th>'
html += "</tr>"

first = True
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if truck not in sel_trucks:
        continue

    # horizontalus separator klasė
    row_cls = "" if first else "truck-divider"
    first = False

    # a) IŠKROVIMAS
    html += f'<tr class="{row_cls}">'
    # suliejame bendrus per 2 eilutes
    for val in [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]:
        html += f'<td rowspan="2">{val}</td>'
    # „Savaitinė atstova“ baigiasi – antras separator langeliui
    html += '<td></td>'
    # kiekvienos datos stulpeliai
    for d in sel_dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Riga","Poznan","Klaipėda","Tallinn"])
        html += (
            "<td></td>"  # B. darbo laikas
            "<td></td>"  # L. darbo laikas
            f"<td>{t}</td>"
            "<td></td><td></td>"
            f'<td>{city}</td>'
            "<td></td><td></td><td></td><td></td>"
            "<td></td>"  # Frachtas tuščias – bet seka separator klasė žemiau
        )
    html += "</tr>"

    # b) PAKROVIMAS
    html += f'<tr class="{row_cls}">'
    html += "<td></td>" * (len(common_headers) + 1)  # +1 dėl STULPELIO po Savaitinė atstova
    for d in sel_dates:
        t1   = f"{random.randint(7,9)}:00"
        t2   = f"{random.randint(15,17)}:00"
        cty  = random.choice(["Vilnius","Kaunas","Berlin","Warsaw"])
        km_t = random.randint(20,120)
        km_k = random.randint(400,900)
        cost = round(km_t*0.2,2)
        fr   = round(km_k*random.uniform(1.0,2.5),2)
        # paskutinis laukas – Frachtas su separator klase
        html += (
            f"<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>{t2}</td>"
            f"<td>{cty}</td><td>{tvad}</td><td>{km_t}</td><td>{km_k}</td><td>{cost}</td>"
            f'<td class="sep">{fr}</td>'
        )
    html += "</tr>"

html += "</table>"

# ─── 7) Atvaizduojame HTML ───────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
