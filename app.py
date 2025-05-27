import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – vieno bloko apibrėžimas")

# ─── 1) Bendri ir dienų antraštės ─────────────────────────────────────────────
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.", "Vilkiko nr.",
    "Ekspeditorius", "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
# datos
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Frachtas"
]

# ─── 2) Vilkikų pavyzdžiai ────────────────────────────────────────────────────
trucks_info = [
    ("1","2","ABC123","Tomas","Laura","PRK001",2,24),
    ("3","1","XYZ789","Greta","Jonas","PRK009",1,45),
    ("2","5","DEF456","Rasa","Tomas","PRK123",2,24),
]

# ─── 3) Multiselect filtrai ──────────────────────────────────────────────────
all_trucks = [t[2] for t in trucks_info]
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", options=all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   options=all_dates,  default=all_dates)

# ─── 4) CSS be jokių linijų, tik outline klases ──────────────────────────────
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:2;}
  .outline {border:2px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# ─── 5) Sudarome visų stulpelių sąrašą ───────────────────────────────────────
cols = common_headers + [""]  # dummy po "Savaitinė atstova"
for d in sel_dates:
    cols += [f"{d} – {h}" for h in day_headers]

# ─── 6) Header: numeracija + pavadinimai ─────────────────────────────────────
html = "<table>\n<tr><th></th>"
for i in range(1, len(cols)+1):
    html += f"<th>{i}</th>"
html += "</tr>\n<tr><th>#</th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>\n"

# ─── 7) Pildome eilutes su outline tik DEF456 ir 2025-05-27 ─────────────────
target_truck = "DEF456"
target_date  = "2025-05-27"

row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if truck not in sel_trucks:
        continue

    # IŠKROVIMAS
    html += "<tr>"
    html += f"<td>{row_num}</td>"
    # bendri su rowspan=2
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f"<td rowspan='2'>{val}</td>"
    html += "<td></td>"  # dummy

    for d in sel_dates:
        is_target = (truck == target_truck and d == target_date)
        cls = "outline" if is_target else ""
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        # B. darbo laikas
        html += f"<td class='{cls}'></td>"
        # L. darbo laikas
        html += f"<td class='{cls}'></td>"
        # Atvykimo laikas
        html += f"<td class='{cls}'>{t}</td>"
        # Laikas nuo
        html += f"<td class='{cls}'></td>"
        # Laikas iki
        html += f"<td class='{cls}'></td>"
        # Vieta
        html += f"<td class='{cls}'>{city}</td>"
        # Frachtas (tuščias šiame bloke)
        html += f"<td class='{cls}'></td>"
    html += "</tr>\n"

    # PAKROVIMAS
    html += "<tr>"
    html += f"<td>{row_num+1}</td>"
    html += "<td></td>" * (len(common_headers)+1)
    for d in sel_dates:
        is_target = (truck == target_truck and d == target_date)
        cls = "outline" if is_target else ""
        t1  = f"{random.randint(7,9)}:00"
        kms = random.randint(20,120)
        fr  = round(random.uniform(800,1200),2)
        html += f"<td class='{cls}'>9</td>"
        html += f"<td class='{cls}'>6</td>"
        html += f"<td class='{cls}'>{t1}</td>"
        html += f"<td class='{cls}'>{t1}</td>"
        html += f"<td class='{cls}'>16:00</td>"
        html += f"<td class='{cls}'>{city}</td>"
        html += f"<td class='{cls}'></td>"
        html += f"<td class='{cls}'>{kms}</td>"
        html += f"<td class='{cls}'>{kms*5}</td>"
        html += f"<td class='{cls}'></td>"
        html += f"<td class='{cls}'>{fr}</td>"
    html += "</tr>\n"

    row_num += 2

html += "</table>"

# ─── 8) Atvaizduojame ─────────────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
