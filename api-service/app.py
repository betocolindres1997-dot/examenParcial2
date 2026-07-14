from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from monitor import ServerMonitor
import uvicorn

app = FastAPI(
    title="MC Infrastructure Monitor API",
    description="API para monitoreo de servidores",
    version="1.0.0"
)

# Configurar CORS para permitir acceso desde el dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

monitor = ServerMonitor()

@app.get("/")
async def root():
    """Endpoint raíz - Información de la API"""
    return {
        "service": "MC Infrastructure Monitor API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/status")
async def get_status():
    """Obtiene estado completo del servidor"""
    return monitor.get_full_status()

@app.get("/api/system")
async def get_system_info():
    """Obtiene información del sistema"""
    return monitor.get_system_info()

@app.get("/api/cpu")
async def get_cpu_info():
    """Obtiene información de CPU"""
    return monitor.get_cpu_info()

@app.get("/api/memory")
async def get_memory_info():
    """Obtiene información de memoria"""
    return monitor.get_memory_info()

@app.get("/api/disk")
async def get_disk_info():
    """Obtiene información de discos"""
    return monitor.get_disk_info()

@app.get("/api/network")
async def get_network_info():
    """Obtiene información de red"""
    return monitor.get_network_info()

@app.get("/api/processes")
async def get_process_info(limit: int = Query(default=10, le=50)):
    """Obtiene información de procesos"""
    return monitor.get_process_info(limit)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)