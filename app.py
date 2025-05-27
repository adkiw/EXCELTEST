import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("DISPO – Planavimo lentelė su rowSpan")

# ─── Sukuriame pavyzdinę lentelę ─────────────────────────────────────────────
# Bendri stulpeliai
common = ["Transporto grupė", "Ekspedicijos grupės nr.", "Vilkiko nr.", "Ekspeditorius"]

# Dienos stulpeliai (viena data, kad iliustruoti)
day_cols = ["Bendras darbo laikas", "Atvykimo laikas", "Laikas nuo", "Laikas iki", "Vieta"]

# Sukuriam dvi “vilkiko” grupes po dvi eilutes
rows = []
for grp, exp_grp, truck, exp in [
    ("1", "2", "ABC123", "Tomas Mickus"),
    ("3", "1", "XYZ789", "Greta Kairytė")
]:
    # Iškrovimas (pirmoji eilutė)
    rows.append({
        **{"Transporto grupė": grp, "Ekspedicijos grupės nr.": exp_grp,
           "Vilkiko nr.": truck, "Ekspeditorius": exp},
        **{col: (datetime.now().strftime("%H:%M") if col in ["Atvykimo laikas","Laikas nuo"] else "") for col in day_cols},
        "_isFirst": True
    })
    # Pakrovimas (antroji)
    rows.append({
        **{"Transporto grupė": grp, "Ekspedicijos grupės nr.": exp_grp,
           "Vilkiko nr.": truck, "Ekspeditorius": exp},
        **{col: (f"{random.randint(8,9)}:00" if col=="Laikas nuo"
                else f"{random.randint(15,16)}:00" if col=="Laikas iki"
                else random.choice(["Vilnius","Kaunas"]) if col=="Vieta"
                else random.randint(8,9) if col=="Bendras darbo laikas"
                else "") for col in day_cols},
        "_isFirst": False
    })

df = pd.DataFrame(rows)

# ─── Paruošiame AgGrid su rowSpan ────────────────────────────────────────────
gb = GridOptionsBuilder.from_dataframe(df)

# JS funkcija, kuri grąžina 2 (rowSpan) tik pirmai eilutei (_isFirst=True)
js_row_span = JsCode("""
function(params) {
    return params.data._isFirst ? 2 : 0;
}
""")

# Pridėsim rowSpan tik pirmajam bendro stulpelio stulpeliui “Transporto grupė”
gb.configure_column(
    "Transporto grupė",
    rowSpan=js_row_span,
    autoHeight=True
)
# Užtikslinkime, kad ir “Ekspedicijos grupės nr.” taip pat turi rowSpan
gb.configure_column(
    "Ekspedicijos grupės nr.",
    rowSpan=js_row_span,
    autoHeight=True
)

# Kiti bendri stulpeliai be rowSpan
for col in ["Vilkiko nr.", "Ekspeditorius"]:
    gb.configure_column(col, rowSpan=js_row_span, autoHeight=True)

# Dienos stulpeliai be rowSpan
for col in day_cols:
    gb.configure_column(col)

grid_opts = gb.build()

# ─── Rodome lentelę ─────────────────────────────────────────────────────────
AgGrid(
    df,
    gridOptions=grid_opts,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    theme="streamlit"  # ar "balham"
)
