# Usa una imagen oficial de Python 3.13.3
FROM python:3.13.3-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero los requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el resto de archivos de la aplicación
COPY . .

# Expone el puerto que usará tu app Flask
EXPOSE 5000

# Comando que ejecuta tu app
CMD ["python", "app.py"]
