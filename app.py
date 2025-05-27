import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("DISPO – blokų apibrėžimas storesniu rėmeliu")

# ─── 1) Iš pradžių – baziniai apibrėžimai ───────────────────────────────────
common_headers = [
    "Transporto grupė","Ekspedicijos grupės nr.","Vilkiko nr.",
    "Ekspeditorius","Trans. vadybininkas","Priekabos nr.",
    "Vair. sk.","Savaitinė atstova"
]
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
day_headers = [
    "B. darbo laikas","L. darbo laikas","Atvykimo laikas",
    "Laikas nuo","Laikas iki","Vieta","Atsakingas",
    "Tušti km","Krauti km","Kelių išlaidos","Frachtas"
]
trucks = [
    ("1","2","ABC123","Tomas","Laura","PRK001",2,24),
    ("1","3","XYZ789","Greta","Jonas","PRK009",1,45),
    ("2","1","DEF456","Rasa","Tomas","PRK123",2,24),
    ("3","4","GHI321","Laura","Greta","PRK555",1,45),
    ("2","5","JKL654","Jonas","Rasa","PRK321",2,24),
]

# ─── 2) Filtrai ───────────────────────────────────────────────────────────────
all_trucks = [t[2] for t in trucks]
all_dates  = dates.copy()
sel_trucks = st.multiselect("🛻 Filtruok vilkikus", all_trucks, default=all_trucks)
sel_dates  = st.multiselect("📅 Filtruok datas",   all_dates,  default=all_dates)

# ─── 3) CSS: bazinis + blokų rėmeliai ────────────────────────────────────────
st.markdown("""
<style>
  table {border-collapse: collapse; width:100%; margin-top:10px;}
  th, td {border:1px solid #ccc; padding:4px; text-align:center;}
  th {background:#f5f5f5; position:sticky; top:0; z-index:1;}
  /* storesnis rėmelis blokų kraštuose */
  .block-left    {border-left:3px solid #000 !important;}
  .block-right   {border-right:3px solid #000 !important;}
  .block-top     {border-top:3px solid #000 !important;}
  .block-bottom  {border-bottom:3px solid #000 !important;}
</style>
""", unsafe_allow_html=True)

# ─── 4) Sukuriame stulpelių sąrašą ir paruošiame html pradžią ────────────────
# bendri + dummy po "Savaitinė atstova"
cols = common_headers + [""]
# dienų blokai po 11 stulpelių
for d in sel_dates:
    cols += [f"{d} – {h}" for h in day_headers]

# Header: stulpelių numeriai
html = "<table>\n<tr><th></th>"
for i in range(1, len(cols)+1):
    html += f"<th>{i}</th>"
html += "</tr>\n<tr><th>#</th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>\n"

# ─── 5) Eilutės su blokų apibrėžimu ──────────────────────────────────────────
row_idx = 1
for tr in trucks:
    tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst = tr
    if truck not in sel_trucks:
        continue

    # iteruojam kiekvienai datai – čia blokų horiz. pozicijos
    block_width = len(day_headers)
    # paskaičiuojam kiek stulpelių iki pirmo dienų bloko:
    offset = len(common_headers) + 1

    # a) IŠKROVIMAS
    html += f"<tr><td>{row_idx}</td>"
    # bendri stulpeliai su rowspan per 2 eilutes
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2" class="block-left block-top block-bottom">{val}</td>'
    # dummy langelis
    html += '<td class="block-left block-top block-bottom"></td>'
    # dienų blokai
    for di, d in enumerate(sel_dates):
        for j, h in enumerate(day_headers):
            # apskaičiuojam bendrą stulpelio indeksą (1-based):
            col_idx = offset + di*block_width + j
            classes = []
            # kairinis kraštas
            if j == 0: classes.append("block-left")
            # dešinis kraštas
            if j == block_width-1: classes.append("block-right")
            # viršus (pirmoje eilutėje)
            classes.append("block-top")
            # suformuojam class string
            cls = " ".join(classes)
            # vertė
            if h == "Atvykimo laikas":
                val = datetime.now().strftime("%H:%M")
            elif h == "Vieta":
                val = random.choice(["Vilnius","Kaunas"])
            else:
                val = ""
            html += f'<td class="{cls}">{val}</td>'
    html += "</tr>\n"

    # b) PAKROVIMAS
    row_idx += 1
    html += f"<tr><td>{row_idx}</td>"
    # tušti bendri
    html += '<td></td>' * (len(common_headers)+1)
    # dienų blokai
    for di, d in enumerate(sel_dates):
        for j, h in enumerate(day_headers):
            col_idx = offset + di*block_width + j
            classes = []
            if j == 0: classes.append("block-left")
            if j == block_width-1: classes.append("block-right")
            classes.append("block-bottom")
            cls = " ".join(classes)
            # vertė
            if h == "B. darbo laikas":
                val = random.randint(8,10)
            elif h == "L. darbo laikas":
                val = random.randint(4,6)
            elif h == "Atvykimo laikas":
                val = f"{random.randint(7,9)}:00"
            elif h == "Nuo":
                val = "08:00"
            elif h == "Iki":
                val = "16:00"
            elif h == "Vieta":
                val = random.choice(["Riga","Poznan"])
            elif h == "Frachtas":
                val = round(random.uniform(500,1200),2)
            else:
                val = ""
            html += f'<td class="{cls}">{val}</td>'
    html += "</tr>\n"

    row_idx += 1

html += "</table>"

# ─── 6) Atvaizduojame lentelę ─────────────────────────────────────────────────
st.markdown(html, unsafe_allow_html=True)
