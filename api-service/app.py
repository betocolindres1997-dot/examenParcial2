import asyncio
import contextlib
import os

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
    allow_origins=["*"],
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
    status = monitor.get_full_status()
    metrics_repository.save_snapshot(status)
    return status

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


@app.get("/api/history")
async def get_history(limit: int = Query(default=50, ge=1, le=1000)):
    """Obtiene historial persistente de métricas"""
    items = metrics_repository.get_history(limit)
    return {
        "count": len(items),
        "items": items,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)