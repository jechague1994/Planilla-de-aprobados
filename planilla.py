import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Configuración de página
st.set_page_config(page_title="Planilla Compartida", layout="wide")

st.title("Planilla de Aprobados")
st.markdown("---")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Se conecta usando la URL que pusiste en .streamlit/secrets.toml
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)
    # Limpiar filas vacías que pueda tener el Excel
    df = df.dropna(how='all')
except Exception as e:
    st.error("Error de conexión. Revisa el link en secrets.toml y que la hoja sea pública como 'Editor'.")
    st.stop()

# --- FORMULARIO DE CARGA ---
with st.expander("Cargar Nuevo Registro", expanded=True):
    with st.form("registro_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            cliente = st.text_input("Nombre del Cliente")
            vendedor = st.text_input("Vendedor")
        with c2:
            nro = st.text_input("N° Presupuesto")
            monto = st.number_input("Monto ($)", min_value=0.0)
        with c3:
            f_crea = st.date_input("Fecha Creación", date.today())
            f_aprob = st.date_input("Fecha Aprobación", date.today())
            corp = st.checkbox("¿Cliente Corporativo?")
        
        btn_guardar = st.form_submit_button("Guardar Registro")

        if btn_guardar:
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
                
                df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                conn.update(data=df_actualizado)
                
                st.success("¡Registro guardado con éxito!")
                st.rerun()
            else:
                st.error("Completa Cliente y N° de Presupuesto.")

st.markdown("---")

# --- BUSCADOR ---
busqueda = st.text_input("Buscar en la planilla...")

if not df.empty:
    mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
    df_filtrado = df[mask]
    
    st.dataframe(df_filtrado, use_container_width=True)

    # --- BOTÓN PARA BORRAR EL ÚLTIMO ---
    if st.button("Borrar último registro cargado"):
        df_final = df.drop(df.index[-1])
        conn.update(data=df_final)
        st.warning("Último registro eliminado.")
        st.rerun()
else:
    st.info("La planilla está vacía.")