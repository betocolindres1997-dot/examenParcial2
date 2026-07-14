# MC Infrastructure Monitor

Sistema distribuido de monitoreo de servidores basado en contenedores Docker.

## 🏗️ Arquitectura

El sistema está compuesto por dos microservicios:

1. **API REST (FastAPI)**: Genera información del estado del servidor
2. **Dashboard Web (Flask)**: Visualiza la información en tiempo real

Los servicios se comunican a través de una red Bridge personalizada de Docker.

## 📋 Requisitos Previos

- Docker 20.10+
- Docker Compose 2.0+
- Git

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <url-repositorio>
cd mc-infrastructure-monitor