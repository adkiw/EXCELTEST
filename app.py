import streamlit as st
from datetime import datetime, timedelta
import random, hashlib

# … (ankstesnės definicijos) …

# Prieš lentelės braižymą:
def get_rnd(truck: str, day: str):
    # hash -> 128 bit, pavertiam į int
    seed = int(hashlib.md5(f"{truck}-{day}".encode()).hexdigest(), 16)
    return random.Random(seed)

# … st.set_page_config, CSS, filtras … 

# Braižom lentelę
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp: continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    # … rowspan bendri duomenys …
    html += "<td></td>"  # Pastabos
    for d in dates:
        rnd = get_rnd(truck, d)
        # generuojam
        t_h = rnd.randint(7,23)
        t_m = rnd.randint(0,59)
        atvykimo = f"{t_h:02d}:{t_m:02d}"
        city = rnd.choice(["Vilnius","Kaunas","Berlin"])
        # atvaizdavimui:
        html += (
            "<td></td><td></td>"
            f"<td>{atvykimo}</td>"
            "<td></td><td></td>"
            f"<td>{city}</td>"
            # … likę td …
        )
    html += "</tr>\n"

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>" * total_common
    for d in dates:
        rnd = get_rnd(truck, d)
        t1   = f"{rnd.randint(7,9)}:02d:00"
        kms  = rnd.randint(20,120)
        fr   = round(rnd.uniform(800,1200),2)
        html += (
            "<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{rnd.choice(['Riga','Poznan'])}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{kms*5}</td>"
            "<td></td>"
            f"<td>{fr}</td>"
        )
    html += "</tr>\n"
    row_num += 2
