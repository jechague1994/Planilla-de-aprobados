import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Planilla Aprobados", layout="wide")
st.title("Planilla de Aprobados")

# Conectamos con el link de los Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentamos leer la base actual
try:
    df = conn.read(ttl=0).dropna(how="all")
except:
    df = pd.DataFrame(columns=["Cliente", "Vendedor", "Nro_Presupuesto", "Monto", "Fecha_Creacion", "Fecha_Aprobacion", "Corporativo"])

# Formulario de carga
with st.form("nuevo_registro"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Cliente")
        vendedor = st.text_input("Vendedor")
        nro = st.text_input("Nro Presupuesto")
    with col2:
        monto = st.number_input("Monto", min_value=0.0)
        f_crea = st.date_input("Fecha Creación")
        f_aprob = st.date_input("Fecha Aprobación")
    
    corp = st.checkbox("¿Es Corporativo?")
    enviar = st.form_submit_button("Guardar en Google Sheets")

    if enviar:
        if cliente and nro:
            nueva_fila = pd.DataFrame([{
                "Cliente": cliente,
                "Vendedor": vendedor,
                "Nro_Presupuesto": nro,
                "Monto": monto,
                "Fecha_Creacion": str(f_crea),
                "Fecha_Aprobacion": str(f_aprob),
                "Corporativo": "SI" if corp else "NO"
            }])
            # Sumamos la fila al Excel
            actualizado = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(data=actualizado)
            st.success("¡Datos guardados correctamente!")
            st.rerun()
        else:
            st.warning("Por favor completa Cliente y Nro de Presupuesto")

# Mostramos lo que hay en el Excel
st.write("### Datos Actuales")
st.dataframe(df, use_container_width=True)