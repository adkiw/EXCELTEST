import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su freezes ir ekspeditorių filtru")

# ─── 1) Duomenų paruošimas ────────────────────────────────────────────────────
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
trucks_info = [
    ("1","2","ABC123","Tomas Mickus","Laura","PRK001", 2,24),
    ("1","3","XYZ789","Greta Kairytė","Jonas","PRK009", 1,45),
    ("2","1","DEF456","Rasa Mikalausk.","Tomas","PRK123", 2,24),
    ("3","4","GHI321","Laura Juknevič.","Greta","PRK555", 1,45),
    ("2","5","JKL654","Jonas Petrauskas","Rasa","PRK321", 2,24),
]

# ─── 2) Filtras pagal ekspeditorius ───────────────────────────────────────────
all_exps = sorted({t[3] for t in trucks_info})
sel_exps = st.multiselect("🔍 Filtruok pagal ekspeditorių", options=all_exps, default=all_exps)

# ─── 3) CSS „freeze panes“ ───────────────────────────────────────────────────
cell_w = 120
st.markdown(f"""
<style>
  .tbl {{border-collapse: collapse; width:100%; overflow:auto;}}
  .tbl th, .tbl td {{border:1px solid #ccc; min-width:{cell_w}px; padding:4px; text-align:center;}}
  .tbl th {{position: sticky; top: 0; background:white; z-index:3;}}
  /* stick first 10 cols */
  {"".join(
    f".tbl th:nth-child({i}), .tbl td:nth-child({i}) {{position: sticky; left:{(i-1)*cell_w}px; background:white; z-index:{4 if i==1 else 2};}}\n"
    for i in range(1, 11)
  )}
</style>
""", unsafe_allow_html=True)

# ─── 4) Sudarome visų stulpelių sąrašą ───────────────────────────────────────
cols = common_headers + [""]  # dummy po „Savaitinė atstova“
for d in dates:
    for h in day_headers:
        cols.append(f"{d} – {h}")

# ─── 5) Pradedam generuoti lentelę ────────────────────────────────────────────
html = '<div style="overflow-x:auto"><table class="tbl">'

# a) Antraštės
html += "<tr><th></th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>"

# b) Duomenų eilutės su rowspan=2
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_exps:
        continue

    # IŠKROVIMAS
    html += "<tr>"
    html += f"<td>{row_num}</td>"
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"  # dummy

    for d in dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        html += "<td></td><td></td>"     # B., L. darbo laikas
        html += f"<td>{t}</td>"          # Atvykimo laikas
        html += "<td></td><td></td>"     # Laikas nuo, Laikas iki
        html += f"<td>{city}</td>"       # Vieta
        html += "<td></td><td></td><td></td><td></td><td></td>"
    html += "</tr>"

    # PAKROVIMAS
    html += "<tr>"
    html += f"<td>{row_num+1}</td>"
    html += "<td></td>"*(len(common_headers)+1)
    for d in dates:
        t1  = f"{random.randint(7,9)}:00"
        km  = random.randint(20,120)
        fr  = round(random.uniform(500,1000),2)
        html += f"<td>9</td><td>6</td><td>{t1}</td><td>{t1}</td><td>16:00</td>"
        html += f"<td>{random.choice(['Riga','Poznan'])}</td><td></td><td>{km}</td><td>{km*5}</td><td></td><td>{fr}</td>"
    html += "</tr>"

    row_num += 2

html += "</table></div>"

# ─── 6) Rodome HTML lentelę ──────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
