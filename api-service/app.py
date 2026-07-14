import asyncio
import contextlib
import os
from datetime import datetime

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from metrics_repository import MetricsRepository
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
    allow_origins=["http://localhost:8080", "http://localhost:5000", "http://web-server:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

monitor = ServerMonitor()
metrics_repository = MetricsRepository(os.getenv("DB_PATH", "/app/data/metrics.db"))
snapshot_task = None


async def snapshot_worker() -> None:
    interval_seconds = int(os.getenv("SNAPSHOT_INTERVAL_SECONDS", "30"))
    while True:
        status = monitor.get_full_status()
        metrics_repository.save_snapshot(status)
        await asyncio.sleep(interval_seconds)


@app.on_event("startup")
async def on_startup() -> None:
    global snapshot_task
    snapshot_task = asyncio.create_task(snapshot_worker())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if snapshot_task is not None:
        snapshot_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await snapshot_task

# ====== ENDPOINTS PRINCIPALES ======

@app.get("/health")
async def health_check():
    """Healthcheck para Docker"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Información de la API"""
    return {
        "service": "MC Infrastructure Monitor API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/status", "/cpu", "/memory",
            "/disk", "/network", "/services", "/history"
        ]
    }

@app.get("/status")
async def get_status():
    """Estado completo del servidor - Endpoint principal"""
    status = monitor.get_full_status()
    metrics_repository.save_snapshot(status)
    return status

@app.get("/cpu")
async def get_cpu_info():
    """Información de CPU"""
    return monitor.get_cpu_info()

@app.get("/memory")
async def get_memory_info():
    """Información de memoria"""
    return monitor.get_memory_info()

@app.get("/disk")
async def get_disk_info():
    """Información de discos"""
    return monitor.get_disk_info()

@app.get("/network")
async def get_network_info():
    """Información de red"""
    return monitor.get_network_info()

@app.get("/services")
async def get_services_info(limit: int = Query(default=10, ge=1, le=50)):
    """Información de servicios/processes"""
    return monitor.get_process_info(limit=limit)


@app.get("/history")
async def get_history(limit: int = Query(default=50, ge=1, le=1000)):
    """Obtiene historial persistente de métricas"""
    items = metrics_repository.get_history(limit)
    return {
        "count": len(items),
        "items": items,
    }

# ====== ENDPOINTS DE COMPATIBILIDAD ======

@app.get("/api/status")
async def get_status_alt():
    """Alias para /status (compatibilidad)"""
    return await get_status()

@app.get("/api/cpu")
async def get_cpu_alt():
    """Alias para /cpu (compatibilidad)"""
    return await get_cpu_info()

@app.get("/api/memory")
async def get_memory_alt():
    """Alias para /memory (compatibilidad)"""
    return await get_memory_info()

@app.get("/api/disk")
async def get_disk_alt():
    """Alias para /disk (compatibilidad)"""
    return await get_disk_info()

@app.get("/api/network")
async def get_network_alt():
    """Alias para /network (compatibilidad)"""
    return await get_network_info()

@app.get("/api/processes")
async def get_processes_alt(limit: int = Query(default=10, le=50)):
    """Alias para /services (compatibilidad)"""
    return await get_services_info(limit=limit)


@app.get("/api/history")
async def get_history_alt(limit: int = Query(default=50, ge=1, le=1000)):
    """Alias para /history (compatibilidad)"""
    return await get_history(limit=limit)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)