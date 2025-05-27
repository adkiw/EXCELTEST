import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su merged cells ir ekspeditoriaus filtru")

# 1) Apibrėžimai
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

# 2) Vilkikų duomenys
trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321",2,24),
]

# 3) Filtras pagal ekspeditorių
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect("Filtruok pagal ekspeditorius", options=all_eksp, default=all_eksp)

# 4) Paprasta CSS
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 5) Stulpelių sąrašas
cols = common_headers + [""]  # dummy after "Savaitinė atstova"
for d in dates:
    cols += [f"{d} – {h}" for h in day_headers]

# 6) HTML lentelė
html = "<table>\n<tr><th></th>"
for i in range(1, len(cols)+1):
    html += f"<th>{i}</th>"
html += "</tr>\n<tr><th>#</th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>\n"

# 7) Pildome rows, tik pasirinkti ekspeditoriai
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"
    for d in dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        html += (
            "<td></td><td></td>"
            f"<td>{t}</td>"
            "<td></td><td></td>"
            f"<td>{city}</td>"
            "<td></td><td></td><td></td>"
            "<td></td><td></td>"
        )
    html += "</tr>\n"
    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>"*(len(common_headers)+1)
    for d in dates:
        t1   = f"{random.randint(7,9)}:00"
        kms  = random.randint(20,120)
        fr   = round(random.uniform(800,1200),2)
        html += (
            "<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{random.choice(['Riga','Poznan'])}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{kms*5}</td>"
            "<td></td>"
            f"<td>{fr}</td>"
        )
    html += "</tr>\n"
    row_num += 2

html += "</table>"

# 8) Atvaizdavimas
st.markdown(html, unsafe_allow_html=True)
