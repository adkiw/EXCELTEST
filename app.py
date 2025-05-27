import streamlit as st
from datetime import date, datetime, timedelta
import random
import hashlib

# Streamlit konfiguracija
st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su datų intervalu ir deterministiniu random")

# 1) Pagalbinė funkcija – suranda pirmadienį duotai datai
def iso_monday(d: date) -> date:
    return d - timedelta(days=(d.isoweekday() - 1))

# 2) Numatytoji intervalo riba (−2 savaitės pirmadienis … +2 savaitės sekmadienis)
today = date.today()
this_monday = iso_monday(today)
start_default = this_monday - timedelta(weeks=2)
end_default   = this_monday + timedelta(weeks=2, days=6)

# 3) Streamlit datos intervalo pasirinkimas
start_sel, end_sel = st.date_input(
    "Pasirinkite datų intervalą:",
    value=(start_default, end_default),
    min_value=start_default - timedelta(weeks=4),
    max_value=end_default + timedelta(weeks=4)
)

# 4) Atskiriame datas ir generuojame sąrašą
if isinstance(start_sel, tuple):
    start_date, end_date = start_sel
else:
    start_date = end_date = start_sel

num_days = (end_date - start_date).days + 1
dates = [
    (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    for i in range(num_days)
]

st.write(f"Rodyti {num_days} dienų nuo {start_date} iki {end_date}.")

# 5) Bendri header’iai (įskaitant “Pastabos”)
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova", "Pastabos"
]

# 6) Dienos sub-header’iai
day_headers = [
    "B. d. laikas", "L. d. laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki", "Vieta",
    "Atsakingas", "Tušti km",
    "Krauti km", "Kelių išlaidos",
    "Frachtas"
]

# 7) Testiniai duomenys apie vilkikus ir ekspeditorius
trucks_info = [
    ("1", "2", "ABC123", "Tomas Mickus",     "Laura", "PRK001", 2, 24),
    ("1", "3", "XYZ789", "Greta Kairytė",    "Jonas", "PRK009", 1, 45),
    ("2", "1", "DEF456", "Rasa Mikalausk.",  "Tomas", "PRK123", 2, 24),
    ("3", "4", "GHI321", "Laura Juknevič.",  "Greta", "PRK555", 1, 45),
    ("2", "5", "JKL654", "Jonas Petrauskas", "Rasa",  "PRK321", 2, 24),
]

# 8) Filtras pagal ekspeditorių vardus
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect(
    "Filtruok pagal ekspeditorius",
    options=all_eksp,
    default=all_eksp
)

# 9) CSS stilius lentelės marginimui
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 10) Funkcija deterministiniam Random (kad filtravimas nekeistų skaičių)
def get_rnd(truck: str, day: str) -> random.Random:
    seed = int(hashlib.md5(f"{truck}-{day}".encode()).hexdigest(), 16)
    return random.Random(seed)

# 11) Skaičiuojame bendrą stulpelių skaičių
total_common = len(common_headers)            # 9
total_day_cols = len(dates) * len(day_headers)
total_cols = total_common + total_day_cols   # viso

# 12) Pradedame kurti lentelės HTML
html = "<table>\n"

# 12.1) Pirmoji eilutė: numeracija
html += "<tr><th></th>"
for i in range(1, total_cols + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 12.2) Antroji eilutė: tuščias blokas virš “common+Pastabos” + datos
html += "<tr><th></th>"
html += f'<th colspan="{total_common}"></th>'
for d in dates:
    html += f'<th colspan="{len(day_headers)}">{d}</th>'
html += "</tr>\n"

# 12.3) Trečioji eilutė: faktiniai header’iai be datos prefikso
html += "<tr><th>#</th>"
for h in common_headers:
    html += f"<th>{h}</th>"
for _ in dates:
    for hh in day_headers:
        html += f"<th>{hh}</th>"
html += "</tr>\n"

# 13) Užpildome lentelės eilutes
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # 13.1) IŠKROVIMAS (pirmoji eilutė)
    html += f"<tr><td>{row_num}</td>"
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"  # Pastabos
    for d in dates:
        rnd = get_rnd(truck, d)
        atvykimo = f"{rnd.randint(0,23):02d}:{rnd.randint(0,59):02d}"
        city     = rnd.choice(["Vilnius","Kaunas","Berlin"])
        html += (
            "<td></td><td></td>"
            f"<td>{atvykimo}</td>"
            "<td></td><td></td>"
            f"<td>{city}</td>"
            + "<td></td>" * 5
        )
    html += "</tr>\n"

    # 13.2) PAKROVIMAS (antroji eilutė)
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>" * total_common
    for d in dates:
        rnd    = get_rnd(truck, d)
        t1     = f"{rnd.randint(7,9):02d}:00"
        kms    = rnd.randint(20,120)
        costs  = kms * 5
        fr     = round(rnd.uniform(800,1200), 2)
        dest   = rnd.choice(["Riga","Poznan"])
        html += (
            "<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{dest}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{costs}</td>"
            "<td></td>"
            f"<td>{fr}</td>"
        )
    html += "</tr>\n"
    row_num += 2

html += "</table>"

# 14) Atvaizdavimas
st.markdown(html, unsafe_allow_html=True)
