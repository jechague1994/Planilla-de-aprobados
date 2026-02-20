import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Configuración de página
st.set_page_config(page_title="Planilla Compartida", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E40AF;'>Planilla de Aprobados Real-Time</h1>", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
# Lee la URL desde el archivo secrets.toml que creaste
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0) # ttl=0 para que los datos siempre sean los más recientes
except Exception as e:
    st.error("Error de conexión. Revisa que el link en secrets.toml sea correcto y la hoja sea pública.")
    st.stop()

# --- FORMULARIO DE CARGA ---
with st.expander("📝 Cargar Nuevo Registro", expanded=True):
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
        
        btn_guardar = st.form_submit_button("🚀 Guardar y Sincronizar")

        if btn_guardar:
            if cliente and nro:
                # Crear la nueva fila
                nueva_fila = pd.DataFrame([{
                    "Cliente": cliente,
                    "Vendedor": vendedor,
                    "Nro_Presupuesto": nro,
                    "Fecha_Creacion": str(f_crea),
                    "Fecha_Aprobacion": str(f_aprob),
                    "Monto": monto,
                    "Corporativo": "SI" if corp else "NO"
                }])
                
                # Unir con los datos viejos y subir a la nube
                df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                conn.update(data=df_actualizado)
                
                st.success("✅ ¡Guardado! Ahora todos pueden ver este registro.")
                st.rerun()
            else:
                st.error("Completa los campos obligatorios.")

st.markdown("---")

# --- BUSCADOR ---
busqueda = st.text_input("🔍 Buscar en la base de datos compartida...")

if not df.empty:
    # Filtro inteligente
    mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
    df_filtrado = df[mask]
    
    # Tabla visual
    st.dataframe(df_filtrado, use_container_width=True)

    # --- ACCIONES ---
    col_del, col_down = st.columns([1, 1])
    with col_del:
        if st.button("🗑️ Borrar ÚLTIMO registro"):
            df_final = df.drop(df.index[-1])
            conn.update(data=df_final)
            st.warning("Último registro eliminado de la nube.")
            st.rerun()
            
    with col_down:
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "planilla_nube.csv", "text/csv")
else:
    st.info("La base de datos está vacía. Empieza cargando un registro.")