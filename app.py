import streamlit as st
from datetime import datetime, timedelta
import random
import hashlib

# Streamlit konfigūracija
st.set_page_config(layout="wide")
st.title("DISPO – 5 savaičių intervalas su rezerviniais stulpeliais")

# 1) Bendri header'iai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova", "Pastabos"
]

# 2) Dienos sub-header'iai
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Atsakingas",       "Tušti km",
    "Krauti km",        "Kelių išlaidos",
    "Frachtas"
]

# 3) Apskaičiuojame penkių savaičių intervalą
today  = datetime.today().date()
monday = today - timedelta(days=today.weekday())
start  = monday - timedelta(weeks=2)
# sukuriame sąrašą savaičių, kiekviena savaitei – 7 datas
weeks = []
for w in range(5):
    week_start = start + timedelta(weeks=w)
    weeks.append([week_start + timedelta(days=d) for d in range(7)])

# 4) Testiniai duomenys
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

# 6) Paprasta CSS lentelės stiliui
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
</style>
""", unsafe_allow_html=True)

# 7) Deterministinis Random pagal truck+data
def get_rnd(truck: str, day: str) -> random.Random:
    seed = int(hashlib.md5(f"{truck}-{day}".encode()).hexdigest(), 16)
    return random.Random(seed)

# 8) Skaičiuojame stulpelių kiekius
total_common   = len(common_headers)                # 9
per_week_cols  = len(day_headers)*7 + 10            # 7 dienos x sub-headers + 10 rezervinių
total_day_cols = per_week_cols * len(weeks)
total_cols     = total_common + total_day_cols

# 9) Pradedame kurti lentelės HTML
html = "<table>\n"

# 9.1) Numeracijos eilutė
html += "<tr><th></th>"
for i in range(1, total_cols+1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 9.2) Savaitinių grupių eilutė (tikslios datos intervalai)
html += "<tr><th></th>"
html += f'<th colspan="{total_common}"></th>'
for idx, week in enumerate(weeks, start=1):
    week_label = f"S{idx}: {week[0].strftime('%Y-%m-%d')}–{week[-1].strftime('%Y-%m-%d')}"
    html += f'<th colspan="{per_week_cols}">{week_label}</th>'
html += "</tr>\n"

# 9.3) Antroji header eilutė: bendri + po savaitėms datų ir po jų 10 tuščių
html += "<tr><th>#</th>"
for h in common_headers:
    html += f"<th>{h}</th>"
for week in weeks:
    # dienos
    for day in week:
        html += f"<th>{day.strftime('%Y-%m-%d')}</th>"
    # po savaitės 10 rezervinių
    html += "<th></th>" * 10
html += "</tr>\n"

# 10) Pildome lentelės duomenis
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    # rowspan iki kito krovimo
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"  # Pastabos

    for week in weeks:
        for day in week:
            rnd = get_rnd(truck, day.isoformat())
            atvykimo = f"{rnd.randint(0,23):02d}:{rnd.randint(0,59):02d}"
            city     = rnd.choice(["Vilnius","Kaunas","Berlin"])
            html += (
                "<td></td><td></td>"
                f"<td>{atvykimo}</td>"
                "<td></td><td></td>"
                f"<td>{city}</td>"
                "<td></td><td></td><td></td><td></td><td></td>"
            )
        # 10 rezervinių
        html += "<td></td>" * 10

    html += "</tr>\n"

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>" * total_common
    for week in weeks:
        for day in week:
            rnd = get_rnd(truck, day.isoformat())
            t1    = f"{rnd.randint(7,9):02d}:00"
            kms   = rnd.randint(20,120)
            fr    = round(rnd.uniform(800,1200),2)
            city2 = rnd.choice(["Riga","Poznan"])
            html += (
                "<td>9</td><td>6</td>"
                f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
                f"<td>{city2}</td>"
                "<td></td>"
                f"<td>{kms}</td><td>{kms*5}</td>"
                "<td></td>"
                f"<td>{fr}</td>"
            )
        html += "<td></td>" * 10
    html += "</tr>\n"
    row_num += 2

html += "</table>"

# 11) Atvaizduojame lentelę
st.markdown(html, unsafe_allow_html=True)
