import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Configuracion basica
st.set_page_config(page_title="Planilla Compartida", layout="wide")
st.title("Planilla de Aprobados")

# Conexion a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)
    df = df.dropna(how='all')
except Exception as e:
    st.error("Error de conexion. Verifica el archivo secrets y que la hoja sea publica.")
    st.stop()

# Formulario
with st.expander("Cargar Nuevo Registro", expanded=True):
    with st.form("form_registro", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("Cliente")
            vendedor = st.text_input("Vendedor")
        with col2:
            nro = st.text_input("Nro Presupuesto")
            monto = st.number_input("Monto", min_value=0.0)
        with col3:
            f_crea = st.date_input("Fecha Creacion", date.today())
            f_aprob = st.date_input("Fecha Aprobacion", date.today())
            corp = st.checkbox("Corporativo")
        
        if st.form_submit_button("Guardar"):
            if cliente and nro:
                nueva_fila = pd.DataFrame([{
                    "Cliente": cliente,
                    "Vendedor": vendedor,
                    "Nro_Presupuesto": nro,
                    "Fecha_Creacion": str(f_crea),
                    "Fecha_Aprobacion": str(f_aprob),
                    "Monto": monto,
                    "Corporativo": "SI" if corp else "NO"
                }])
                df_final = pd.concat([df, nueva_fila], ignore_index=True)
                conn.update(data=df_final)
                st.success("Guardado!")
                st.rerun()

# Tabla y Busqueda
busqueda = st.text_input("Buscar...")
if not df.empty:
    mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
    st.dataframe(df[mask], use_container_width=True)