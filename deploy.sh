#!/bin/bash

echo "MC Infrastructure Monitor - Despliegue"
echo "====================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

# Verificar Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Docker Compose no está disponible${NC}"
    exit 1
fi

echo -e "${GREEN}Docker y Docker Compose encontrados${NC}"

# Detener servicios anteriores si existen
echo -e "${YELLOW}Deteniendo servicios anteriores...${NC}"
docker compose down 2>/dev/null

# Construir imágenes
echo -e "${YELLOW}Construyendo imágenes...${NC}"
docker compose build --no-cache

# Iniciar servicios
echo -e "${YELLOW}Iniciando servicios...${NC}"
docker compose up -d

# Esperar a que los servicios estén listos
echo -e "${YELLOW}Esperando que los servicios estén listos...${NC}"
sleep 12

# Verificar servicios
echo ""
echo "Verificando servicios..."

# Verificar Dashboard
if curl -sf http://localhost:8080/ > /dev/null; then
    echo -e "${GREEN}Dashboard Web: OK (http://localhost:8080)${NC}"
else
    echo -e "${RED}Dashboard Web: Error${NC}"
fi

# Verificar API desde host
if curl -sf http://localhost:8080/api/proxy/status > /dev/null; then
    echo -e "${GREEN}API Server (via dashboard): OK${NC}"
else
    echo -e "${RED}API Server: Error${NC}"
fi

# Verificar conectividad
if docker exec mc-web-server python -c "import requests; requests.get('http://api-server:5000/health', timeout=5); print('ok')" > /dev/null 2>&1; then
    echo -e "${GREEN}Conectividad entre servicios: OK${NC}"
else
    echo -e "${RED}Conectividad entre servicios: Error${NC}"
fi

echo ""
echo "====================================="
echo -e "${GREEN}Despliegue completado${NC}"
echo ""
echo "📊 Dashboard: http://localhost:8080"
echo "📖 API (proxy): http://localhost:8080/api/proxy/status"
echo ""
echo "Comandos útiles:"
echo "  Ver logs: docker compose logs -f"
echo "  Detener: docker compose down"
echo "  Reiniciar: docker compose restart"
echo "  Ver estado: docker compose ps"
echo "====================================="