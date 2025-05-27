import streamlit as st
import pandas as pd

st.set_page_config(page_title="Užsakymų valdymas", layout="wide")
st.title("Užsakymų valdymo įrankis")

# 1) Failo įkėlimas
uploaded_file = st.file_uploader("Įkelkite Excel failą (Order Management)", type="xlsx")
if not uploaded_file:
    st.info("Prašome įkelti savo Excel failą, kad galėčiau parodyti duomenis.")
    st.stop()

# 2) Perskaitome darbalapį ORDERS su multilevel-header (eilutės 1 ir 2)
df_raw = pd.read_excel(
    uploaded_file,
    sheet_name="ORDERS",
    header=[1, 2]  # pirmas header eilučių lygis – grupės, antrasis – konkretūs stulpeliai
)

# 3) „Flatteniname“ stulpelių pavadinimus
new_cols = []
for lvl0, lvl1 in df_raw.columns:
    parts = []
    if pd.notna(lvl0):
        parts.append(str(lvl0).strip())
    if pd.notna(lvl1):
        parts.append(str(lvl1).strip())
    new_cols.append(" ".join(parts))
df_raw.columns = new_cols

# 4) Išvalome pradines eiles (pvz., kur pirmame stulpelyje – INSERT)
df = df_raw[df_raw.iloc[:, 0] != "INSERT"].copy()

# 5) Rodyti visą lentelę
st.subheader("Visi užsakymai (ORDERS)")
st.dataframe(df, use_container_width=True)

# 6) Filtravimas pagal Pakrovimo datą
if "Pakrovimas (data)" in df.columns:
    df["Pakrovimas (data)"] = pd.to_datetime(df["Pakrovimas (data)"], errors="coerce")
    min_date = df["Pakrovimas (data)"].min().date()
    max_date = df["Pakrovimas (data)"].max().date()
    date_range = st.date_input(
        "Filtruokite užsakymus pagal pakrovimo datą",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    mask = (
        (df["Pakrovimas (data)"].dt.date >= date_range[0]) &
        (df["Pakrovimas (data)"].dt.date <= date_range[1])
    )
    st.subheader(f"Pakrovimo datos nuo {date_range[0]} iki {date_range[1]}")
    st.dataframe(df.loc[mask], use_container_width=True)
else:
    st.warning("Stulpelis “Pakrovimas (data)” nerastas – negalima taikyti datos filtro.")
