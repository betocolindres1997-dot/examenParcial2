import psutil
import platform
import socket
from datetime import datetime
from typing import Dict, Any

class ServerMonitor:
    def __init__(self):
        self.hostname = socket.gethostname()
        
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información general del sistema"""
        return {
            "hostname": self.hostname,
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """Obtiene información de CPU"""
        cpu_freq = psutil.cpu_freq()
        return {
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "cpu_frequency_current": cpu_freq.current if cpu_freq else None,
            "cpu_frequency_max": cpu_freq.max if cpu_freq else None,
            "cpu_times": {
                "user": psutil.cpu_times().user,
                "system": psutil.cpu_times().system,
                "idle": psutil.cpu_times().idle
            }
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Obtiene información de memoria"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_percent": memory.percent,
            "swap_total_gb": round(swap.total / (1024**3), 2),
            "swap_used_gb": round(swap.used / (1024**3), 2),
            "swap_percent": swap.percent
        }
    
    def get_disk_info(self) -> Dict[str, Any]:
        """Obtiene información de discos"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        
        return {"partitions": disks}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Obtiene información de red"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent_gb": round(net_io.bytes_sent / (1024**3), 2),
            "bytes_received_gb": round(net_io.bytes_recv / (1024**3), 2),
            "packets_sent": net_io.packets_sent,
            "packets_received": net_io.packets_recv,
            "error_in": net_io.errin,
            "error_out": net_io.errout
        }
    
    def get_process_info(self, limit: int = 10) -> Dict[str, Any]:
        """Obtiene información de los procesos más demandantes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Ordenar por CPU y limitar
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        top_processes = processes[:limit]
        
        return {
            "total_processes": len(processes),
            "top_processes": top_processes
        }
    
    def get_full_status(self) -> Dict[str, Any]:
        """Obtiene estado completo del servidor"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "processes": self.get_process_info()
        }