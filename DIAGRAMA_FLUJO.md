# Diagrama de Flujo - MC Infrastructure Monitor

## Flujo general de la aplicacion

```mermaid
flowchart TD
    A[Usuario abre Dashboard<br/>http://localhost:8080] --> B[web-server Flask<br/>Ruta /]
    B --> C[Render index.html]

    C --> D[JavaScript ejecuta refreshAll()]
    D --> E[GET /api/proxy/status]
    E --> F[Flask proxy en web-server]
    F --> G[GET http://api-server:5000/status]

    G --> H[api-server FastAPI]
    H --> I[ServerMonitor recolecta metricas<br/>CPU, Memoria, Disco, Red, Procesos]
    I --> J[Respuesta JSON de estado]
    J --> F
    F --> D

    D --> K[Actualiza tarjetas y graficas en UI]

    D --> L[GET /api/proxy/history?limit=20]
    L --> M[Flask proxy /api/proxy/history]
    M --> N[GET http://api-server:5000/history]
    N --> O[FastAPI consulta SQLite<br/>/app/data/metrics.db]
    O --> P[Devuelve historial]
    P --> D
    D --> Q[Actualiza grafica historica]

    R[Boton Ver comunicacion] --> S[GET /api/proxy/connectivity]
    S --> T[Diagnostico DNS + HTTP<br/>entre web-server y api-server]
    T --> U[Panel de conectividad en dashboard]
```

## Flujo de persistencia de datos

```mermaid
flowchart LR
    S1[Worker periodico en FastAPI] --> S2[monitor.get_full_status()]
    S2 --> S3[metrics_repository.save_snapshot()]
    S3 --> S4[(SQLite metrics.db)]
    S4 --> S5[Endpoint /history]
    S5 --> S6[Dashboard /api/proxy/history]
    S6 --> S7[Grafica de historial CPU/Memoria]
```
