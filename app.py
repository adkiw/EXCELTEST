import streamlit as st
from datetime import datetime, timedelta
import random
import hashlib

# Streamlit konfiguracija
st.set_page_config(layout="wide")
st.title("DISPO – 5 savaičių intervalas su tuščiais stulpeliais po šeštadienio")

# 1) Bendri header’iai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova", "Pastabos"
]

# 2) Dienos sub-header’iai
day_headers = [
    "B. d. laikas", "L. d. laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki", "Vieta",
    "Atsakingas", "Tušti km",
    "Krauti km", "Kelių išlaidos",
    "Frachtas"
]

# 3) Sugeneruojam 5 savaičių intervalą (2 savaitės atgal, 2 į priekį, nuo pirmadienio iki sekmadienio)
today = datetime.today().date()
current_monday = today - timedelta(days=today.weekday())
start_date = current_monday - timedelta(weeks=2)
end_date   = current_monday + timedelta(weeks=2, days=6)

all_dates = []
d = start_date
while d <= end_date:
    all_dates.append(d)
    d += timedelta(days=1)

# 4) Įterpiam po kiekvieno šeštadienio 10 tuščių vietų
processed_dates = []
for d in all_dates:
    processed_dates.append(d)
    if d.weekday() == 5:  # 5 = šeštadienis
        processed_dates += [None] * 10

# 5) Testiniai duomenys apie vilkikus ir ekspeditorius
trucks_info = [
    ("1", "2", "ABC123", "Tomas Mickus",     "Laura", "PRK001", 2, 24),
    ("1", "3", "XYZ789", "Greta Kairytė",    "Jonas", "PRK009", 1, 45),
    ("2", "1", "DEF456", "Rasa Mikalausk.",  "Tomas", "PRK123", 2, 24),
    ("3", "4", "GHI321", "Laura Juknevič.",  "Greta", "PRK555", 1, 45),
    ("2", "5", "JKL654", "Jonas Petrauskas", "Rasa",  "PRK321", 2, 24),
]

# 6) Filtras pagal ekspeditorius
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect(
    "Filtruok pagal ekspeditorius",
    options=all_eksp,
    default=all_eksp
)

# 7) CSS stilius
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 8) Deterministinis Random pagal sunkvežimio nr. ir datą
def get_rnd(truck: str, day: str) -> random.Random:
    seed = int(hashlib.md5(f"{truck}-{day}".encode()).hexdigest(), 16)
    return random.Random(seed)

# 9) Sudarome visą cols sąrašą
cols = common_headers.copy()
for item in processed_dates:
    if item is None:
        # 10 tuščių stulpelių be datos
        cols += day_headers
    else:
        cols += [f"{item.strftime('%Y-%m-%d')} – {h}" for h in day_headers]

# 10) Apskaičiuojame bendrą stulpelių skaičių
total_cols = len(cols)

# 11) Pradedame kurti lentelę
html = "<table>\n"

# 11.1) Numeracijos eilutė
html += "<tr><th></th>"
for i in range(1, total_cols + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 11.2) Antroji eilutė: tuščias virš common+Pastabos, po to datos/tuščios grupės su colspan
html += "<tr><th></th>"
# common_headers ilgis = 9
html += f'<th colspan="{len(common_headers)}"></th>'
for item in processed_dates:
    if item is None:
        html += f'<th colspan="{len(day_headers)}"></th>'
    else:
        html += f'<th colspan="{len(day_headers)}">{item.strftime("%Y-%m-%d")}</th>'
html += "</tr>\n"

# 11.3) Trečioji eilutė: faktiniai header’iai be datos prefikso
html += "<tr><th>#</th>"
for h in common_headers:
    html += f"<th>{h}</th>"
for item in processed_dates:
    for hh in day_headers:
        html += f"<th>{hh}</th>"
html += "</tr>\n"

# 12) Užpildome eilutes
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"  # Pastabos
    for item in processed_dates:
        rnd = get_rnd(truck, str(item) if item else f"{truck}-empty")
        if item is None:
            # tušti langeliai
            html += ("<td></td>" * len(day_headers))
        else:
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

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>" * len(common_headers)  # Pastabos įskaičiuota
    for item in processed_dates:
        rnd = get_rnd(truck, str(item) if item else f"{truck}-empty2")
        if item is None:
            html += ("<td></td>" * len(day_headers))
        else:
            t1   = f"{rnd.randint(7,9):02d}:00"
            kms  = rnd.randint(20,120)
            costs= kms * 5
            fr   = round(rnd.uniform(800,1200), 2)
            city = rnd.choice(["Riga","Poznan"])
            html += (
                "<td>9</td><td>6</td>"
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

# 13) Atvaizduojame lentelę
st.markdown(html, unsafe_allow_html=True)
