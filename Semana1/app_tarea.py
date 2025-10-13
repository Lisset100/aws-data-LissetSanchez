
# Importación de Librerías
import boto3              # Para conectarse a Amazon S3
import pandas as pd       # Para trabajar con datos (tablas)
import json               # Para leer los archivos JSON
import streamlit as st    # Para crear el dashboard web
import plotly.express as px  # Para crear gráficas
import io    #Para manejar flujos de datos en memoria



# Configuración de Streamlit
st.set_page_config(
    page_title="Dashboard Simple",  # Título en la pestaña del navegador
    page_icon="🖥️",                
    layout="wide"                  # Significa que usa todo el ancho de la pantalla
)


# Crear conexión con S3
s3 = boto3.client("s3")  # Puerta para acceder a S3



def cargar_datos_desde_s3():
    bucket = "xideralaws-curso-lisset"
    key = "processed/data_procesada.csv"

    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()
    df = pd.read_csv(io.BytesIO(body))
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df



# Título principal
st.title("🖥️ Dashboard de Monitoreo")



# Barra lateral (sidebar) 
with st.sidebar:
    
    # Título de la barra lateral
    st.header("Controles y Filtros")
    
    # Crea un botón
    # Si el usuario hace click, esto devuelve True
    if st.button("🔄 Actualizar Datos"):
        # Limpiar la memoria caché
        st.cache_data.clear()
        # Recargar la página completa
        st.rerun()
    
 

# Carga de datos
# Muestra un mensaje mientras carga
with st.spinner("Cargando datos desde S3..."):
    df = cargar_datos_desde_s3()

# Se muestra mensaje de éxito
st.success(f" Se cargaron {len(df)} registros correctamente")


# Muestra los indicadores por estados (KPIs)
st.subheader("📊KPIs-Estados")

# Contar cuántos registros hay de cada estado
#El len() significa “length” y sirve para contar cuántos elementos hay

total_ok = len(df[df['status'] == 'OK'])        
total_warn = len(df[df['status'] == 'WARN'])   
total_error = len(df[df['status'] == 'ERROR'])  

# Crea 3 columnas para mostrar los números
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🟢 Estados OK",      # Título
        value=total_ok               # Número grande
    )

with col2:
    st.metric(
        label="🟠 Estados WARN",
        value=total_warn
    )

with col3:
    st.metric(
        label="🔴 Estados ERROR",
        value=total_error
    )

st.markdown("---")


# Filtro de estado
with st.sidebar:
    st.markdown("---")  # Línea divisoria
    st.header("🔍 Filtros")
    
    # Crear menú desplegable para elegir el estado
    filtro_estado = st.selectbox(
        "Filtrar por Estado:",                    # Etiqueta del filtro
        options=["Todos", "OK", "WARN", "ERROR"], # Opciones del menú
        index=0                                   # "Todos" seleccionado por defecto
    )

# Aplicación de el filtro por estado
# Crea una copia de los datos para no manipular el df real
df_filtrado = df.copy()

# Si el usuario elige algo diferente de "Todos" se filtra
if filtro_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['status'] == filtro_estado]

# Filtro por servidor
with st.sidebar:
    # Obtiene y ordena la lista de servidores únicos que existen
    lista_servidores = df['server_id'].unique()
    lista_servidores = sorted(lista_servidores)
    
    # Crea selector múltiple
    filtro_servidores = st.multiselect(
        "Filtrar por Servidor(es):",  # Etiqueta del filtro
        options=lista_servidores,     # Lista de servidores disponibles
        default=[]                    # Por defecto ninguno seleccionado
    )

# Aplicación del filtro de servidores
# Si el usuario seleccionó al menos un servidor
if len(filtro_servidores) > 0:
    df_filtrado = df_filtrado[df_filtrado['server_id'].isin(filtro_servidores)]



# Gráfica 1 Estados por servidor
st.subheader("📈 Estados por Servidor")

# Contar cuántos estados hay por cada servidor
# groupby = agrupar, size = contar
if len(df_filtrado) == 0:
    st.warning("⚠️ No hay datos con estos filtros")
else:
    conteo = df_filtrado.groupby(['server_id', 'status']).size().reset_index(name='cantidad')

# Crea una gráfica de barras
grafica_barras = px.bar(
    conteo,                          # Datos a graficar
    x='server_id',                   # Eje horizontal (X)
    y='cantidad',                    # Eje vertical (Y)
    color='status',                  # Color diferente por estado
    barmode='group',                 # Barras una al lado de la otra
    color_discrete_map={             # Define colores específicos
        'OK': 'green',
        'WARN': 'orange',
        'ERROR': 'red'
    },
    labels={                         # Etiquetas personalizadas
        'server_id': 'Servidor',
        'cantidad': 'Cantidad',
        'status': 'Estado'
    }
)

# Muestra la gráfica en Streamlit
st.plotly_chart(grafica_barras, use_container_width=True)

st.markdown("---")


# Gráfica 2 - Uso de CPU en el tiempo
st.subheader("📉 Uso de CPU en el Tiempo")

if len(df_filtrado) == 0:
    st.warning("⚠️ No hay datos con estos filtros")
    # Ordenar los datos por fecha (del más antiguo al más nuevo)
else:
    df_ordenado = df_filtrado.sort_values('timestamp')


# Crear gráfica de línea
grafica_linea = px.line(
    df_ordenado,                     # Datos ordenados
    x='timestamp',                   # Eje X: tiempo
    y='cpu_usage',                   # Eje Y: uso de CPU
    color='server_id',               # Color diferente por servidor
    labels={
        'timestamp': 'Tiempo',
        'cpu_usage': 'Uso de CPU (%)',
        'server_id': 'Servidor'
    }
)

# Mostrar la gráfica
st.plotly_chart(grafica_linea, use_container_width=True)

st.markdown("---")


#Tabla con los datos
st.subheader("📋 Tabla de Datos")

# Seleccionar solo las columnas que se quieren mostrar
columnas_importantes = [
    'timestamp',      # Fecha y hora
    'server_id',      # Nombre del servidor
    'cpu_usage',      # Uso de CPU
    'memory_usage',   # Uso de memoria
    'status',         # Estado (OK, WARN, ERROR)
    'region'          # Región geográfica
]

# Crea una nueva tabla solo con esas columnas
df_mostrar = df_filtrado[columnas_importantes]

# Ordenar por fecha (más recientes primero)
df_mostrar = df_mostrar.sort_values('timestamp', ascending=False)

# Mostrar la tabla interactiva
st.dataframe(
    df_mostrar,                      # Datos a mostrar
    use_container_width=True,        # Usar todo el ancho
    height=400                       # Altura de 400 píxeles
)


