import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.colab import auth
from google.auth import default

# Autenticación con OAuth (no necesita JSON)
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Abre tu hoja (cambia el nombre si es diferente)
sh = gc.open("Ventas Modelos Simple")  # Pon el nombre exacto de tu Sheet

ws_modelos = sh.worksheet("Modelos")
ws_ventas = sh.worksheet("Registro")

# Cargar modelos automáticamente
modelos = ws_modelos.col_values(1)[1:]  # Desde A2

# Cargar ventas para reporte
ventas_data = ws_ventas.get_all_records()
df = pd.DataFrame(ventas_data)

st.title("Ventas Modelos")

# Lista de modelos clickable
st.header("Modelos")
for modelo in modelos:
    if st.button(modelo, key=modelo):
        st.session_state.selected_modelo = modelo

# Formulario
if "selected_modelo" in st.session_state:
    st.header(f"Venta para {st.session_state.selected_modelo}")
    monto = st.number_input("Monto USD", min_value=0.0, step=1.0)
    servicio = st.selectbox("Servicio", ["Sexting", "Llamada", "Custom Video", "GFE"])
    metodo = st.selectbox("Método de Pago", ["CashApp", "Venmo", "PayPal", "Zelle", "Throne", "Amazon Gift Card", "Crypto"])
    if st.button("Guardar Venta"):
        if monto > 0:
            nueva_venta = [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                st.session_state.selected_modelo,
                monto,
                servicio,
                metodo
            ]
            ws_ventas.append_row(nueva_venta)
            st.success("Guardado!")
            del st.session_state.selected_modelo
        else:
            st.error("Monto inválido")

# Reporte
st.header("Reporte")
fecha_desde = st.date_input("Desde")
fecha_hasta = st.date_input("Hasta")
report_modelo = st.selectbox("Modelo", ["Todos"] + modelos)
if st.button("Ver Reporte"):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d/%m/%Y %H:%M:%S")
    mask = (df['Fecha'] >= pd.to_datetime(fecha_desde)) & (df['Fecha'] <= pd.to_datetime(fecha_hasta))
    report_df = df[mask]
    if report_modelo != "Todos":
        report_df = report_df[report_df['Modelo'] == report_modelo]
    total = report_df['Monto USD'].sum()
    st.write(f"Total USD: ${total:.2f}")
    st.dataframe(report_df)
