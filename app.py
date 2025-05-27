import streamlit as st
from datetime import datetime, timedelta
import random
import hashlib

# Streamlit konfiguracija
st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su deterministic random ir ekspeditoriaus filtru")

# 1) Bendri header’iai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova", "Pastabos"
]

# 2) Datos – per 10 dienų nuo šiandien
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# 3) Dienos sub-header’iai
day_headers = [
    "B. d. laikas", "L. d. laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki", "Vieta",
    "Atsakingas", "Tušti km",
    "Krauti km", "Kelių išlaidos",
    "Frachtas"
]

# 4) Testiniai duomenys apie vilkikus ir ekspeditorius
trucks_info = [
    ("1", "2", "ABC123", "Tomas Mickus",     "Laura", "PRK001", 2, 24),
    ("1", "3", "XYZ789", "Greta Kairytė",    "Jonas", "PRK009", 1, 45),
    ("2", "1", "DEF456", "Rasa Mikalausk.",  "Tomas", "PRK123", 2, 24),
    ("3", "4", "GHI321", "Laura Juknevič.",  "Greta", "PRK555", 1, 45),
    ("2", "5", "JKL654", "Jonas Petrauskas", "Rasa",  "PRK321", 2, 24),
]

# 5) Filtras pagal ekspeditorių vardus
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect(
    "Filtruok pagal ekspeditorius",
    options=all_eksp,
    default=all_eksp
)

# 6) CSS stilius lentelės marginimui
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 7) Funkcija deterministiniam Random
def get_rnd(truck: str, day: str) -> random.Random:
    # seed iš truck ir dienos
    hash_str = f"{truck}-{day}"
    seed = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
    return random.Random(seed)

# 8) Skaičiuojame bendrą stulpelių skaičių
total_common = len(common_headers)           # 9
total_day_cols = len(dates) * len(day_headers)
total_cols = total_common + total_day_cols  # viso

# 9) Pradedame kurti lentelės HTML
html = "<table>\n"

# 9.1) Numeracijos eilutė
html += "<tr><th></th>"
for i in range(1, total_cols + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 9.2) Antroji eilutė: tuščias blokas virš “common+Pastabos” + datos
html += "<tr><th></th>"
html += f'<th colspan="{total_common}"></th>'
for d in dates:
    html += f'<th colspan="{len(day_headers)}">{d}</th>'
html += "</tr>\n"

# 9.3) Trečioji eilutė: faktiniai header’iai be datos prefix
html += "<tr><th>#</th>"
# bendri
for h in common_headers:
    html += f"<th>{h}</th>"
# dienų sub-header’iai
for _ in dates:
    for hh in day_headers:
        html += f"<th>{hh}</th>"
html += "</tr>\n"

# 10) Pildome duomenis
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    # bendri stulpeliai su rowspan=2
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    # Pastabos
    html += "<td></td>"
    # datos su deterministiniu random
    for d in dates:
        rnd = get_rnd(truck, d)
        atvykimo = f"{rnd.randint(0,23):02d}:{rnd.randint(0,59):02d}"
        city     = rnd.choice(["Vilnius","Kaunas","Berlin"])
        html += (
            "<td></td><td></td>"      # B. d. laikas, L. d. laikas
            f"<td>{atvykimo}</td>"     # Atvykimo laikas
            "<td></td><td></td>"       # Laikas nuo / iki
            f"<td>{city}</td>"         # Vieta
            + "<td></td>" * 5          # Atsakingas, Tušti km, Krauti km, Kelių išlaidos, Frachtas
        )
    html += "</tr>\n"

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    # 9 tušti td
    html += "<td></td>" * total_common
    for d in dates:
        rnd = get_rnd(truck, d)
        t1   = f"{rnd.randint(7,9):02d}:00"
        kms  = rnd.randint(20,120)
        costs= kms * 5
        fr   = round(rnd.uniform(800,1200), 2)
        city = rnd.choice(["Riga","Poznan"])
        html += (
            "<td>9</td><td>6</td>"      # B. d. laikas, L. d. laikas
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{city}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{costs}</td>"
            "<td></td>"
            f"<td>{fr}</td>"
        )
    html += "</tr>\n"
    row_num += 2

html += "</table>"

# 11) Atvaizdavimas
st.markdown(html, unsafe_allow_html=True)
