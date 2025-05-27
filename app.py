# 6) HTML lentelės pradžia
html = "<table>\n"

# 6.1) Numeracijos eilutė (1,2,3…)
html += "<tr><th></th>"
for i in range(1, len(cols) + 1):
    html += f"<th>{i}</th>"
html += "</tr>\n"

# 6.2) Datų eilutė su „Pastabos“ stulpeliu
html += "<tr><th></th>"
# 9 bendri stulpeliai (8 headeriai + dummy) – pavadiname “Pastabos”
html += '<th colspan="9">Pastabos</th>'
# po viena susijungusi celdė kiekvienai datai
for d in dates:
    html += f'<th colspan="11">{d}</th>'
html += "</tr>\n"

# 6.3) Antroji headerių eilutė (#, Transporto grupė, Eksp. grupės nr. …)
html += "<tr><th>#</th>"
for h in cols:
    html += f"<th>{h}</th>"
html += "</tr>\n"

# 7) Pildome rows, tik pasirinkti ekspeditoriai
row_num = 1
for tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst in trucks_info:
    if eksp not in sel_eksp:
        continue

    # IŠKROVIMAS
    html += f"<tr><td>{row_num}</td>"
    for val in (tr_grp, exp_grp, truck, eksp, tvad, prk, v_sk, atst):
        html += f'<td rowspan="2">{val}</td>'
    html += "<td></td>"
    for d in dates:
        t = datetime.now().strftime("%H:%M")
        city = random.choice(["Vilnius","Kaunas","Berlin"])
        html += (
            "<td></td><td></td>"
            f"<td>{t}</td>"
            "<td></td><td></td>"
            f"<td>{city}</td>"
            "<td></td><td></td><td></td>"
            "<td></td><td></td>"
        )
    html += "</tr>\n"

    # PAKROVIMAS
    html += f"<tr><td>{row_num+1}</td>"
    html += "<td></td>"*(len(common_headers)+1)
    for d in dates:
        t1   = f"{random.randint(7,9)}:00"
        kms  = random.randint(20,120)
        fr   = round(random.uniform(800,1200),2)
        html += (
            "<td>9</td><td>6</td>"
            f"<td>{t1}</td><td>{t1}</td><td>16:00</td>"
            f"<td>{random.choice(['Riga','Poznan'])}</td>"
            "<td></td>"
            f"<td>{kms}</td><td>{kms*5}</td>"
            "<td></td>"
            f"<td>{fr}</td>"
        )
    html += "</tr>\n"
    row_num += 2

html += "</table>"

# 8) Atvaizdavimas
st.markdown(html, unsafe_allow_html=True)
