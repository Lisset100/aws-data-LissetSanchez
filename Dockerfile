# Imagen base con Python
FROM python:3.11

# Instalar dependencias necesarias
RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    boto3 \
    plotly \
    python-dotenv

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código de la app
COPY music_analysis_dashboard.py /app/

# Exponer el puerto de Streamlit
EXPOSE 8502

# Comando para correr Streamlit
CMD ["streamlit", "run", "music_analysis_dashboard.py", "--server.port=8502", "--server.address=0.0.0.0"]
