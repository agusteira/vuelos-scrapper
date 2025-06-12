# Imagen base más liviana
FROM python:3.12.5-slim

# Previene que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Desactiva el buffer de salida (útil para logs en Railway)
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos solo requirements primero (mejor cache)
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

RUN playwright install

# Ejecutamos el script principal
CMD ["python", "main.py"]
