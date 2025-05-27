import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("DISPO – su Excel-stiliaus filtrais ir separatoriais")

# ─── 1) Sukuriame pavyzdinius duomenis ────────────────────────────────────────
# bendri stulpeliai ir kelios dienos
common_cols = ["Transporto grupė", "Ekspedicijos grupės nr.", "Vilkiko nr.", "Ekspeditorius"]
dates = [(datetime.today().date() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
day_cols = ["B. darbo laikas", "L. darbo laikas", "Atvyk.", "Nuo", "Iki", "Vieta"]

# build DataFrame
rows = []
for tr_grp, exp_grp, truck, exp in [
    ("1","2","ABC123","Tomas Mickus"),
    ("3","1","XYZ789","Greta Kairytė"),
]:
    # iškrovimas
    rec = {"Transporto grupė":tr_grp, "Ekspedicijos grupės nr.":exp_grp,
           "Vilkiko nr.":truck, "Ekspeditorius":exp}
    rec["_isFirst"] = True
    for d in dates:
        rec[f"{d} – Atvyk."] = datetime.now().strftime("%H:%M")
        rec[f"{d} – Vieta"]  = random.choice(["Vilnius","Kaunas"])
    rows.append(rec)
    # pakrovimas
    rec2 = {c:"" for c in common_cols}
    rec2["_isFirst"] = False
    for d in dates:
        rec2[f"{d} – B. darbo laikas"] = random.randint(8,10)
        rec2[f"{d} – L. darbo laikas"] = random.randint(4,6)
        rec2[f"{d} – Atvyk."] = f"{random.randint(8,9)}:00"
        rec2[f"{d} – Nuo"]  = "08:00"
        rec2[f"{d} – Iki"]  = "16:00"
        rec2[f"{d} – Vieta"]  = random.choice(["Poznan","Riga"])
    rows.append(rec2)

df = pd.DataFrame(rows)

# ─── 2) Paruošiame AgGrid su filtrais, rowspan ir separatoriais ───────────────
gb = GridOptionsBuilder.from_dataframe(df)

# auto filtras Excel stiliumi
gb.configure_default_column(
    filter="agMultiColumnFilter",
    sortable=True,
    floatingFilter=True,
    resizable=True
)

# rowspan funk
js_row_span = JsCode("""
function(params) {
  return params.data._isFirst ? 2 : 0;
}
""")
for c in common_cols:
    gb.configure_column(c, rowSpan=js_row_span, autoHeight=True)

# stulpelių separatorius – vertikali linija prieš kiekvieną datos grupę
col_defs = gb.build()["columnDefs"]
new_defs = []
for cd in col_defs:
    field = cd.get("field","")
    # kiekvieną datą – jeigu laukas su " – " (data – X), tada kairinė linija
    if " – " in field:
        cd.setdefault("cellStyle", {})["borderLeft"] = "3px solid #0073e6"
    new_defs.append(cd)
gb._grid_options["columnDefs"] = new_defs

# eilutės separatorius – horizontali linija prieš antrą vilkiką
gb.configure_grid_options(
    getRowClass=JsCode("""
function(params) {
  return !params.data._isFirst ? 'truck-divider' : '';
}
""")
)

# pridėjam CSS klasę
grid_css = """
<style>
    .truck-divider .ag-cell {
        border-top: 3px solid #444 !important;
    }
</style>
"""
st.markdown(grid_css, unsafe_allow_html=True)

grid_options = gb.build()

# ─── 3) Atvaizduojame AgGrid ──────────────────────────────────────────────────
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    theme="streamlit"
)
