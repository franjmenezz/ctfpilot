FROM python:3.11-slim

LABEL maintainer="franjmenezz"
LABEL description="CTFPilot - Your co-pilot for CTFs and HackTheBox machines"

# Instalar Nmap y dependencias del sistema
RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo
COPY . .

# Instalar CTFPilot
RUN pip install --no-cache-dir -e .

# Volumen para persistir la base de datos y reportes
VOLUME ["/app/db", "/root/Desktop/CTFPilot"]

# Comando por defecto
ENTRYPOINT ["ctfpilot"]
CMD ["--help"]