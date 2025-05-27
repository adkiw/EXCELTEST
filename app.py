import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – su eilučių ir stulpelių numeracija")

# 1) Apibrėžtinių stulpelių ir dienų antraštės
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.", "Vilkiko nr.",
    "Ekspeditorius", "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]
day_headers = [
    "B. darbo laikas", "L. darbo laikas", "Atvykimo laikas",
    "Laikas nuo", "Laikas iki", "Vieta", "Atsakingas",
    "Tušti km", "Krauti km", "Kelių išlaidos", "Frachtas"
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
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", options=all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   options=all_dates,  default=all_dates)

# 3) CSS separatoriams
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:2;}
  tr.divider-row td {border-top:3px solid #000 !important;}
  th.sep, td.sep {border-left:3px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# 4) Kuriame lentelės HTML su numeracija
# Suskaičiuojame bendrų stulpelių skaičių + dummy sep + datos*day_headers
cols = common_headers + [""]  # +1 dummy po "Savaitinė atstova"
for d in sel_dates:
    cols += [f"{d} – {dh}" for dh in day_headers]

# Header: eilutės numeriai: tuščias langelis + stulpelių indeksai
html = "<table>\n  <tr>"
html += "<th></th>"  # kairėje kam put numeracijos pavadinimas
for i in range(1, len(cols)+1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# Antroji header eilutė: realūs pavadinimai
html += "  <tr>"
html += "<th>#</th>"
for idx, h in enumerate(cols, start=1):
    cls = "sep" if h.endswith("Frachtas") or idx == len(common_headers)+1 else ""
    html += f'<th class="{cls}">{h}</th>'
html += "</tr>\n"

# 5) Duomenų eilutės su numeracija
row_num = 1
first = True
for tr in trucks_info:
    tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst = tr
    if truck not in sel_trucks:
        continue

    # IŠKROVIMAS su rowspan ir horizontal separator
    cls = "" if first else "divider-row"
    first = False
    html += f'  <tr class="{cls}">'
    html += f"<td>{row_num}</td>"
    # rowspan bendri
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"  # dummy sep po Savaitinė atstova
    # dienų duomenys
    for d in sel_dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        html += (    "<td></td><td></td>"    # B., L. darbo laikas
                     f"<td>{t}</td>"
                     "<td></td><td></td>"
                     f"<td>{city}</td>"
                     "<td></td><td></td><td></td>"
                     "<td></td>"
                     "<td class='sep'></td>")
    html += "</tr>\n"

    # PAKROVIMAS
    html += f'  <tr class="{cls}">'
    html += "<td></td>"*(len(common_headers)+1)
    for d in sel_dates:
        t1   = f"{random.randint(7,9)}:00"
        kms  = random.randint(10,100)
        fra  = round(random.uniform(500,1200),2)
        html += (f"<td>9</td><td>6</td>"
                 f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
                 f"<td>{random.choice(['Riga','Poznan'])}</td>"
                 "<td></td>"
                 f"<td>{kms}</td><td>{kms*5}</td><td></td>"
                 f"<td class='sep'>{fra}</td>")
    html += "</tr>\n"

    row_num += 2  # padidinam numerį dviem, nes dvi eilutės

html += "</table>"

# 6) Atvaizduojame
st.markdown(html, unsafe_allow_html=True)
