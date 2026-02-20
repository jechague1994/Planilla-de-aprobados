import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Planilla Aprobados", layout="wide")
st.title("Planilla de Aprobados")

# Conexión usando el bloque de secretos
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer base actual (sin caché para ver cambios al instante)
df = conn.read(ttl=0).dropna(how="all")

with st.form("form_nuevo"):
    c1, c2 = st.columns(2)
    cliente = c1.text_input("Cliente")
    vendedor = c1.text_input("Vendedor")
    nro = c2.text_input("Nro Presupuesto")
    monto = c2.number_input("Monto", min_value=0.0)
    
    if st.form_submit_button("Guardar Registro"):
        if cliente and nro:
            # Crear la nueva fila con los nombres exactos de tus columnas en Excel
            nueva_fila = pd.DataFrame([{
                "Cliente": cliente,
                "Vendedor": vendedor,
                "Nro_Presupuesto": nro,
                "Monto": monto,
                "Fecha_Creacion": "2026-02-20", # Puedes automatizarlo luego
                "Fecha_Aprobacion": "2026-02-20",
                "Corporativo": "SI"
            }])
            
            # Combinar y subir
            df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(spreadsheet=st.secrets["public_gsheets_url"], data=df_actualizado)
            
            st.success("¡Guardado con éxito en Google Sheets!")
            st.rerun()
        else:
            st.error("Faltan datos obligatorios.")

st.write("### Vista de la Planilla")
st.dataframe(df, use_container_width=True)