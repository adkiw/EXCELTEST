import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")

st.title("DISPO – Planavimo lentelė (HTML su rowspan)")

# 1) Apibrėžiame bendrus laukus ir dienų laukus
common_cols = [
    ("Transporto grupė", "1"), 
    ("Ekspedicijos grupės nr.", "2"),
    ("Vilkiko nr.", "ABC123"),
    ("Ekspeditorius", "Tomas Mickus"),
    ("Trans. vadybininkas", "Laura Juknevičienė"),
    ("Priekabos nr.", "PRK001"),
    ("Vair. sk.", "2"),
    ("Savaitinė atstova", "24")
]

day_cols = [
    "Bendras darbo laikas", "Likęs darbo laikas atvykus",
    "Atvykimo laikas", "Laikas nuo", "Laikas iki",
    "Vieta", "Atsakingas", "Tušti km", "Krauti km",
    "Kelių išlaidos (EUR)", "Frachtas (EUR)"
]

# 2) Sukuriame 10 datų horizontaliai
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

# 3) Pradedame statyti HTML lentelę
html = """
<style>
  table {border-collapse: collapse; width: 100%;}
  th, td {border: 1px solid #ddd; padding: 4px; text-align: center;}
  th {background: #f0f0f0;}
</style>
<table>
  <tr>
    <!-- headerai -->
    <th>Transporto grupė</th><th>Ekspedicijos grupės nr.</th>
    <th>Vilkiko nr.</th><th>Ekspeditorius</th><th>Trans. vadybininkas</th>
    <th>Priekabos nr.</th><th>Vair. sk.</th><th>Savaitinė atstova</th>
"""
# pridėti kiekvienos dienos dienų antraštės
for d in dates:
    for dc in day_cols:
        html += f"<th>{d}<br>– {dc}</th>"
html += "</tr>\n"

# 4) Pirmas vilkikas: dvi eilutės
#   a) IŠKROVIMAS (bendri stulpeliai rowspan=2)
html += "<tr>"
for name, val in common_cols:
    html += f'<td rowspan="2">{val}</td>'
# Iškrovimo stulpeliai – tik laikas/vieta
for _ in dates:
    t = datetime.now().strftime("%H:%M")
    city = random.choice(["Riga", "Poznan", "Klaipėda"])
    # įrašome laikas atvykimo/Tušti kiti laukai tušti
    html += f"<td></td><td></td><td>{t}</td>"
    html += "<td></td><td></td>"
    html += f"<td>{city}</td>"
    html += "<td></td><td></td><td></td><td></td><td></td>"
html += "</tr>\n"

#   b) PAKROVIMAS (bendri stulpeliai tušti)
html += "<tr>"
html += "<td></td>" * len(common_cols)
for _ in dates:
    t1 = f"{random.randint(8,9)}:00"
    t2 = f"{random.randint(15,16)}:00"
    city = random.choice(["Vilnius","Kaunas","Berlin"])
    kms_t = random.randint(20,120)
    kms_k = random.randint(400,900)
    cost = round(kms_t*0.2,2)
    fr = round(kms_k*random.uniform(1.0,2.0),2)
    html += f"<td>9</td><td>6</td><td>{t1}</td><td>{t1}</td><td>{t2}</td>"
    html += f"<td>{city}</td><td>Laura</td><td>{kms_t}</td><td>{kms_k}</td><td>{cost}</td><td>{fr}</td>"
html += "</tr>\n"

# 5) Antras vilkikas (analoginė struktūra)
# Pakeisk common_cols reikšmes arba kopijuok aukščiau ir sukeisk reikšmes kaip nori
common2 = [("1","3"),("Eksp. grupės nr.","1"),("XYZ789","Greta"),("","Jonas"),("","PRK009"),("","1"),("","45"),("","")]
html += "<tr>"
for _, val in common_cols: html += '<td rowspan="2"></td>'
# ... generuok analogiškai ...
html += "</tr>\n<tr></tr>\n"

html += "</table>"

# 6) Rodome kaip HTML
st.markdown(html, unsafe_allow_html=True)
