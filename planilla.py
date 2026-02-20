import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Planilla Aprobados", layout="wide")
st.title("Planilla de Aprobados")

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos actuales
df = conn.read(ttl=0).dropna(how="all")

# Formulario
with st.form("registro"):
    c1, c2, c3 = st.columns(3)
    cliente = c1.text_input("Cliente")
    vendedor = c1.text_input("Vendedor")
    nro = c2.text_input("Nro Presupuesto")
    monto = c2.number_input("Monto", min_value=0.0)
    f_crea = c3.date_input("Fecha Creacion")
    f_aprob = c3.date_input("Fecha Aprobacion")
    corp = c3.checkbox("Corporativo")
    
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
            # Intentar actualizar
            conn.update(data=df_final)
            st.success("¡Datos guardados!")
            st.rerun()

# Mostrar tabla
st.dataframe(df, use_container_width=True)