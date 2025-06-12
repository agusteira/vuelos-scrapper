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

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
 && rm -rf /var/lib/apt/lists/*


# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

RUN playwright install

# Ejecutamos el script principal
CMD ["python", "main.py"]
