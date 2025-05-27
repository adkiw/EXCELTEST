import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – su blokų rėmeliu")

# ─── 1) Baziniai apibrėžimai ──────────────────────────────────────────────────
common_headers = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova",
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
day_headers = [
    "B. darbo laikas", "L. darbo laikas",
    "Atvykimo laikas", "Laikas nuo",
    "Laikas iki",       "Vieta",
    "Frachtas",
]

trucks_info = [
    ("1","2","ABC123","Tomas","Laura","PRK001",2,24),
    ("3","1","XYZ789","Greta","Jonas","PRK009",1,45),
    ("2","5","DEF456","Rasa","Tomas","PRK123",2,24),
]

# ─── 2) Filtrai ───────────────────────────────────────────────────────────────
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", [t[2] for t in trucks_info],
                             default=[t[2] for t in trucks_info])
sel_dates  = st.multiselect("📅 Filtruok datas", dates, default=dates)

# ─── 3) CSS: bazinis + block-border ──────────────────────────────────────────
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:2;}
  .block-border {border:2px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# ─── 4) Sudarome visų stulpelių sąrašą ───────────────────────────────────────
cols = common_headers + [""]  # dummy po "Savaitinė atstova"
for d in sel_dates:
    cols += [f"{d} – {h}" for h in day_headers]

# ─── 5) Sukuriame lentelės HEADERS su numeracija ─────────────────────────────
html = "<table>\n<tr><th></th>"
for i in range(1, len(cols) + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

html += "<tr><th>#</th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>\n"

# ─── 6) Pildome eilutes su block-border klasėmis ────────────────────────────
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if truck not in sel_trucks:
        continue

    # ► IŠKROVIMAS
    html += "<tr>\n"
    html += f"<td class='block-border'>{row_num}</td>"
    # bendri stulpeliai su rowspan=2
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f"<td class='block-border' rowspan='2'>{val}</td>"
    html += "<td class='block-border'></td>"  # dummy

    # datos stulpeliai IŠKROVIMAS
    for d in sel_dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        # sukuriame po 3 stulpelius: laikas, tušti, vieta, frachtas
        # pagal day_headers: B., L., Atvykimo laikas, Nuo, Iki, Vieta, Frachtas
        html += "<td class='block-border'></td>"  # B. darbo laikas
        html += "<td class='block-border'></td>"  # L. darbo laikas
        html += f"<td class='block-border'>{t}</td>"
        html += "<td class='block-border'></td>"  # Laikas nuo
        html += "<td class='block-border'></td>"  # Laikas iki
        html += f"<td class='block-border'>{city}</td>"
        html += "<td class='block-border'></td>"  # Frachtas atskira eilutė → čia tuščias

    html += "\n</tr>\n"

    # ► PAKROVIMAS
    html += "<tr>\n"
    html += "<td class='block-border'></td>"
    html += "<td colspan='8'></td>"  # tušti bendri + dummy
    for d in sel_dates:
        t1  = f"{random.randint(7,9)}:00"
        kms = random.randint(20,120)
        fr  = round(random.uniform(800,1200),2)
        html += "<td class='block-border'>9</td>"
        html += "<td class='block-border'>6</td>"
        html += f"<td class='block-border'>{t1}</td>"
        html += f"<td class='block-border'>{t1}</td>"
        html += "<td class='block-border'>16:00</td>"
        html += f"<td class='block-border'>{city}</td>"
        html += "<td class='block-border'></td>"
        html += f"<td class='block-border'>{kms}</td>"
        html += f"<td class='block-border'>{kms*5}</td>"
        html += "<td class='block-border'></td>"
        html += f"<td class='block-border'>{fr}</td>"
    html += "\n</tr>\n"

    row_num += 2

html += "</table>"

# ─── 7) Atvaizduojame ─────────────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
