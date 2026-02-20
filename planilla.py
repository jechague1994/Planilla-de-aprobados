import streamlit as st
import pandas as pd
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Planilla de Aprobados", layout="wide")

# Estilo personalizado para el título
st.markdown("<h1 style='text-align: center; color: #1E40AF;'>Planilla de aprobados</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- PERSISTENCIA DE DATOS ---
# Usamos session_state para mantener los datos mientras la app esté abierta
if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=[
        "Cliente", "Vendedor", "N° Presupuesto", 
        "Fecha Creación", "Fecha Aprobación", "Monto", "Corporativo"
    ])

# --- FORMULARIO DE CARGA ---
with st.container():
    st.subheader("📝 Cargar Nuevo Registro")
    with st.form("form_registro", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cliente = st.text_input("Nombre del Cliente")
            vendedor = st.text_input("Vendedor")
        
        with col2:
            nro_ppto = st.text_input("N° de Presupuesto")
            monto = st.number_input("Monto ($)", min_value=0.0, format="%.2f")
            
        with col3:
            f_crea = st.date_input("Fecha Creación", date.today())
            f_aprob = st.date_input("Fecha Aprobación", date.today())
            es_corp = st.checkbox("¿Cliente Corporativo?")

        submit = st.form_submit_button("✅ Guardar en Planilla")

        if submit:
            if cliente and nro_ppto:
                nueva_fila = {
                    "Cliente": cliente, 
                    "Vendedor": vendedor, 
                    "N° Presupuesto": nro_ppto,
                    "Fecha Creación": str(f_crea), 
                    "Fecha Aprobación": str(f_aprob), 
                    "Monto": monto,
                    "Corporativo": "SI" if es_corp else "NO"
                }
                # Añadir a la tabla
                st.session_state.datos = pd.concat([st.session_state.datos, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success("¡Registro cargado!")
            else:
                st.error("Por favor, completa Cliente y N° de Presupuesto.")

st.markdown("---")

# --- SECCIÓN DE TABLA Y FILTROS ---
if not st.session_state.datos.empty:
    st.subheader("📊 Registros Actuales")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar por cliente, vendedor o número de presupuesto...")
    
    # Filtrar datos
    df_filtrado = st.session_state.datos.copy()
    if busqueda:
        # Busca en todas las columnas
        mask = df_filtrado.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        df_filtrado = df_filtrado[mask]

    # Mostrar Tabla
    st.dataframe(df_filtrado, use_container_width=True)

    # --- ACCIONES ---
    col_descarga, col_borrar = st.columns([1, 1])
    
    with col_descarga:
        # Descarga CSV
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar esta vista (CSV)",
            data=csv,
            file_name="planilla_aprobados.csv",
            mime="text/csv"
        )
    
    with col_borrar:
        # Borrado individual por selección
        seleccion = st.selectbox("Seleccione N° de Presupuesto para borrar:", df_filtrado["N° Presupuesto"].unique())
        if st.button("🗑️ Borrar Seleccionado"):
            st.session_state.datos = st.session_state.datos[st.session_state.datos["N° Presupuesto"] != seleccion]
            st.warning(f"Presupuesto {seleccion} eliminado.")
            st.rerun()
else:
    st.info("Aún no hay registros en la planilla.")