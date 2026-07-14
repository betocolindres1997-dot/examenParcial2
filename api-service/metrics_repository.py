import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List


class MetricsRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self) -> None:
        directory = os.path.dirname(self.db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS metrics_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    hostname TEXT,
                    cpu_usage_percent REAL,
                    memory_percent REAL,
                    memory_used_gb REAL,
                    memory_total_gb REAL,
                    disk_used_percent REAL,
                    bytes_sent_gb REAL,
                    bytes_received_gb REAL,
                    total_processes INTEGER,
                    raw_status_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics_history(timestamp)"
            )

    def save_snapshot(self, status: Dict[str, Any]) -> None:
        disks = status.get("disk", {}).get("partitions", [])
        disk_used_percent = max((disk.get("percent", 0) for disk in disks), default=0)

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO metrics_history (
                    timestamp,
                    hostname,
                    cpu_usage_percent,
                    memory_percent,
                    memory_used_gb,
                    memory_total_gb,
                    disk_used_percent,
                    bytes_sent_gb,
                    bytes_received_gb,
                    total_processes,
                    raw_status_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    status.get("timestamp", datetime.utcnow().isoformat()),
                    status.get("system", {}).get("hostname"),
                    status.get("cpu", {}).get("cpu_usage_percent"),
                    status.get("memory", {}).get("memory_percent"),
                    status.get("memory", {}).get("memory_used_gb"),
                    status.get("memory", {}).get("memory_total_gb"),
                    disk_used_percent,
                    status.get("network", {}).get("bytes_sent_gb"),
                    status.get("network", {}).get("bytes_received_gb"),
                    status.get("processes", {}).get("total_processes"),
                    json.dumps(status),
                ),
            )

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    hostname,
                    cpu_usage_percent,
                    memory_percent,
                    memory_used_gb,
                    memory_total_gb,
                    disk_used_percent,
                    bytes_sent_gb,
                    bytes_received_gb,
                    total_processes
                FROM metrics_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        items = [dict(row) for row in rows]
        items.reverse()
        return items
