import streamlit as st
from datetime import datetime, timedelta
import random
import hashlib  # jei naudosite deterministinį seed’ą

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su merged cells ir ekspeditoriaus filtru")

# 1) Bendri header’iai
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova",
    "Pastabos"   # 9-asis stulpelis
]

# 2) Datos – per 10 dienų nuo šiandien
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# 3) Dienos sub-header’iai
day_headers = [
    "B. darbo laikas", "L. darbo laikas", "Atvykimo laikas",
    "Laikas nuo",       "Laikas iki",       "Vieta",
    "Atsakingas",       "Tušti km",         "Krauti km",
    "Kelių išlaidos",   "Frachtas"
]

# 4) **TRUCKS_INFO turi būti čia, **prieš** for-ciklą!**
trucks_info = [
    ("1", "2", "ABC123", "Tomas Mickus",     "Laura", "PRK001", 2, 24),
    ("1", "3", "XYZ789", "Greta Kairytė",    "Jonas", "PRK009", 1, 45),
    ("2", "1", "DEF456", "Rasa Mikalausk.",  "Tomas", "PRK123", 2, 24),
    ("3", "4", "GHI321", "Laura Juknevič.",  "Greta", "PRK555", 1, 45),
    ("2", "5", "JKL654", "Jonas Petrauskas", "Rasa",  "PRK321", 2, 24),
]

# 5) Filtras pagal ekspeditorius
all_eksp = sorted({t[3] for t in trucks_info})
sel_eksp = st.multiselect("Filtruok pagal ekspeditorius", options=all_eksp, default=all_eksp)

# 6) CSS stilius
st.markdown("""<style>…</style>""", unsafe_allow_html=True)

# 7) Sudarome cols sąrašą
cols = common_headers[:]  # dabar jau įskaičiuota “Pastabos”
for d in dates:
    cols += day_headers

# 8) Čia jau “for … in trucks_info” – kintamasis egzistuoja ir klaidos nebėra
html = "<table>…"
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    # …
