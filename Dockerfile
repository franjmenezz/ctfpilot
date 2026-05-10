FROM python:3.11-slim

LABEL maintainer="franjmenezz"
LABEL description="CTFPilot - Your co-pilot for CTFs and HackTheBox machines"

RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Instalar sin modo editable, copiando directamente al path
RUN pip install --no-cache-dir hatchling && \
    python -m hatchling build -t wheel && \
    pip install --no-cache-dir dist/*.whl

VOLUME ["/app/db", "/root/Desktop/CTFPilot"]

ENTRYPOINT ["ctfpilot"]
CMD ["--help"]