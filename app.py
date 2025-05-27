import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("DISPO – Excel-stiliaus filtrai ir tikslūs separatoriai")

# 1) Stulpelių apibrėžimas
common_cols = [
    "Transporto grupė", "Ekspedicijos grupės nr.",
    "Vilkiko nr.", "Ekspeditorius",
    "Trans. vadybininkas", "Priekabos nr.",
    "Vair. sk.", "Savaitinė atstova"
]
# 10 dienų, bet rodysime 5 pavyzdžiui
start = datetime.today().date()
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
day_cols = ["B. darbo laikas", "L. darbo laikas", "Atvyk.", "Nuo", "Iki", "Vieta", "Frachtas"]

# 2) Sukuriame pavyzdinį DataFrame su „divider_before“ žyma
rows = []
divider_next = False
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in [
    ("1","2","ABC123","Tomas","Laura","PRK001",2,24),
    ("3","1","XYZ789","Greta","Jonas","PRK009",1,45),
    ("2","5","DEF456","Rasa","Tomas","PRK123",2,24),
]:
    # IŠKROVIMAS
    rec = dict(zip(common_cols, [tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst]))
    rec["_first"] = True
    rec["_divider_before"] = divider_next
    for d in dates:
        rec[f"{d} – Atvyk."] = datetime.now().strftime("%H:%M")
        rec[f"{d} – Vieta"]  = random.choice(["Vilnius","Kaunas","Riga"])
    rows.append(rec)
    divider_next = True

    # PAKROVIMAS
    rec2 = {c: "" for c in common_cols}
    rec2["_first"] = False
    rec2["_divider_before"] = False
    for d in dates:
        rec2[f"{d} – B. darbo laikas"] = random.randint(8,10)
        rec2[f"{d} – L. darbo laikas"] = random.randint(4,6)
        rec2[f"{d} – Atvyk."] = f"{random.randint(7,9)}:00"
        rec2[f"{d} – Nuo"]    = "08:00"
        rec2[f"{d} – Iki"]    = "16:00"
        rec2[f"{d} – Vieta"]  = random.choice(["Poznan","Tallinn"])
        rec2[f"{d} – Frachtas"] = round(random.randint(400,900)*1.5,2)
    rows.append(rec2)

df = pd.DataFrame(rows)

# 3) Konfigūruojame AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# a) Excel-stiliaus filtrai
gb.configure_default_column(
    filter="agMultiColumnFilter",
    floatingFilter=True,
    sortable=True,
    resizable=True
)

# b) RowSpan: sujungti common stulpelius per 2 eilutes
js_row_span = JsCode("function(params){ return params.data._first?2:0; }")
for c in common_cols:
    gb.configure_column(c, rowSpan=js_row_span, autoHeight=True)

# c) Vertikalus separatorius: piešiame storą liniją _prieš_ kiekvieną
#    stulpelį, kurio pavadinimas baigiasi "– B. darbo laikas"
col_defs = gb.build()["columnDefs"]
for cd in col_defs:
    fld = cd.get("field","")
    if fld.endswith("– B. darbo laikas"):
        style = cd.get("cellStyle",{})
        style["borderLeft"] = "3px solid black"
        cd["cellStyle"] = style
gb._grid_options["columnDefs"] = col_defs

# d) Horizontalus separatorius tarp blokų:
#    CSS klasė tr.truck-divider pritaikoma pirmai eilutei (_first==True)
gb.configure_grid_options(
    getRowClass=JsCode("""
function(params) {
  return params.data._divider_before? 'truck-divider':'';
}
""")
)

# pridėjam CSS taisyklę
st.markdown("""
<style>
  .truck-divider .ag-row {
    border-top: 3px solid black !important;
  }
</style>
""", unsafe_allow_html=True)

# 4) Rodome
AgGrid(
    df,
    gridOptions=gb.build(),
    enable_enterprise_modules=False,
    theme="streamlit",
    fit_columns_on_grid_load=True,
)
