# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia del archivo de requerimientos y el código fuente
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias desde el archivo de requerimientos
RUN pip install -r requirements.txt

# Comando para ejecutar el codigo
CMD ["python", "expansionLlaves.py"]
