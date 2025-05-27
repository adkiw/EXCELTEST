import streamlit as st
from datetime import datetime, timedelta
import random

# Pagrindinės Streamlit nustatymas
st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su merged cells ir ekspeditoriaus filtru")

# 1) Bendri header’iai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]

# 2) Datos – per 10 dienų nuo šiandien
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# 3) Dienos sub-header’iai (jie kartosis po kiekvienos datos)
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Atsakingas",       "Tušti km",
    "Krauti km",        "Kelių išlaidos",
    "Frachtas"
]

# 4) Testiniai duomenys
trucks_info = [
    ("1", "2", "ABC123", "Tomas Mickus",     "Laura", "PRK001", 2, 24),
    ("1", "3", "XYZ789", "Greta Kairytė",    "Jonas", "PRK009", 1, 45),
    ("2", "1", "DEF456", "Rasa Mikalausk.",  "Tomas", "PRK123", 2, 24),
    ("3", "4", "GHI321", "Laura Juknevič.",  "Greta", "PRK555", 1, 45),
    ("2", "5", "JKL654", "Jonas Petrauskas", "Rasa",  "PRK321", 2, 24),
]

# 5) Filtras pagal ekspeditorius
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect(
    "Filtruok pagal ekspeditorius",
    options=all_eksp,
    default=all_eksp
)

# 6) Paprasta CSS lentelės stiliui
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 7) Kuriame HTML lentelę
html = "<table>\n"

# 7.1) Pirmoji eilutė: numeracijos stulpeliai
html += "<tr><th></th>"
# suskaičiuojam, kiek stulpelių turėsim: 8 common + 1 Pastabos + dates*len(day_headers)
total_common = len(common_headers) + 1  
total_day_cols = len(dates) * len(day_headers)
total_cols = total_common + total_day_cols
for i in range(1, total_cols + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 7.2) Antroji eilutė: tuščias blokas virš pirmų 9 stulpelių + datos su colspan
html += "<tr><th></th>"
html += f'<th colspan="{total_common}"></th>'  # tuščias virš “common + Pastabos”
for d in dates:
    html += f'<th colspan="{len(day_headers)}">{d}</th>'
html += "</tr>\n"

# 7.3) Trečioji eilutė: # + realūs header’iai (be datos prefikso)
html += "<tr><th>#</th>"
# bendri header’iai + Pastabos
for h in common_headers + ["Pastabos"]:
    html += f"<th>{h}</th>"
# po to – sub-header’iai kiekvienai datai
for _ in dates:
    for hh in day_headers:
        html += f"<th>{hh}</th>"
html += "</tr>\n"

# 8) Užpildome eilutes pagal filtrą ir duomenis
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    # rowspan du cell’ai – bendri duomenys
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += '<td rowspan="2">{}</td>'.format(val)
    # į Pastabos kol įterpiam tuščią td
    html += "<td></td>"
    # toliau datos x sub-header’iai
    for _ in dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius", "Kaunas", "Berlin"])
        html += (
            "<td></td><td></td>"    # B. darbo, L. darbo
            f"<td>{t}</td>"          # Atvykimo laikas
            "<td></td><td></td>"     # Laikas nuo / iki
            f"<td>{city}</td>"       # Vieta
            "<td></td><td></td><td></td><td></td><td></td>"
        )
    html += "</tr>\n"

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    # pirmi 9 tušti
    html += "<td></td>" * total_common
    for _ in dates:
        t1  = f"{random.randint(7,9)}:00"
        kms = random.randint(20,120)
        fr  = round(random.uniform(800,1200), 2)
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

# 9) Atvaizduojame
st.markdown(html, unsafe_allow_html=True)
