import streamlit as st
import pandas as pd
from datetime import datetime

# Lista de modelos (cambia con los tuyos; para Sheets, cambia después)
modelos = ["Ana", "Sofia", "Valeria", "Luna", "María"]

servicios = ["Sexting", "Llamada", "Custom Video", "GFE"]
metodos = ["CashApp", "Venmo", "PayPal", "Zelle", "Throne", "Amazon Gift Card", "Crypto"]

# Datos en memoria (para Sheets, agrega gspread después)
if "ventas" not in st.session_state:
    st.session_state.ventas = pd.DataFrame(columns=["Fecha", "Modelo", "Monto USD", "Servicio", "Método"])

df = st.session_state.ventas

st.title("Ventas Modelos")

# Pantalla 1: Lista de modelos clickable
st.header("Modelos")
for modelo in modelos:
    if st.button(modelo, key=modelo):
        st.session_state.selected = modelo

# Pantalla 2: Formulario
if "selected" in st.session_state:
    st.header(f"Venta para {st.session_state.selected}")
    monto = st.number_input("Monto USD", min_value=0.0)
    servicio = st.selectbox("Servicio", servicios)
    metodo = st.selectbox("Método de Pago", metodos)
    if st.button("Guardar"):
        if monto > 0:
            nueva = pd.DataFrame({
                "Fecha": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
                "Modelo": [st.session_state.selected],
                "Monto USD": [monto],
                "Servicio": [servicio],
                "Método": [metodo]
            })
            st.session_state.ventas = pd.concat([df, nueva], ignore_index=True)
            st.success("Guardado!")
            del st.session_state.selected
        else:
            st.error("Monto inválido")

# Pantalla 3: Reporte
st.header("Reporte")
fecha_desde = st.date_input("Desde")
fecha_hasta = st.date_input("Hasta")
report_modelo = st.selectbox("Modelo", ["Todos"] + modelos)
if st.button("Ver Reporte"):
    df_temp = df.copy()
    df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format="%d/%m/%Y %H:%M:%S")
    mask = (df_temp['Fecha'] >= pd.to_datetime(fecha_desde)) & (df_temp['Fecha'] <= pd.to_datetime(fecha_hasta))
    report_df = df_temp[mask]
    if report_modelo != "Todos":
        report_df = report_df[report_df['Modelo'] == report_modelo]
    total = report_df['Monto USD'].sum()
    st.write(f"**Total USD: ${total:.2f}**")
    st.dataframe(report_df)
