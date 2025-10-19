# Imagen base con Python
FROM python:3.11

# Instalar dependencias necesarias
RUN pip install --no-cache-dir  streamlit mysql-connector-python pandas  matplotlib seaborn dotenv

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código de la app
COPY music_analysis_dashboard.py /app/

# Exponer el puerto de Streamlit
EXPOSE 8152

# Comando para correr Streamlit
CMD ["streamlit", "run", "music_analysis_dashboard.py", "--server.port=8152", "--server.address=0.0.0.0"]
