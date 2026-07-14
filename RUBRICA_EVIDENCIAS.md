# Rubrica de Evidencias - Proyecto Parcial 2

## Instrucciones de uso

- Completar columna "Resultado obtenido" durante la demostracion.
- Adjuntar capturas de pantalla de comandos y dashboard.
- Marcar si cumple o no cumple cada criterio.

## Tabla de evaluacion

| # | Criterio evaluado | Evidencia requerida | Comando o accion | Resultado obtenido | Puntaje max |
|---|-------------------|---------------------|------------------|--------------------|-------------|
| 1 | Separacion en 2 servicios | Existen dos contenedores en ejecucion | docker compose ps | | 10 |
| 2 | API REST funcional | Respuesta JSON valida | curl http://localhost:8000/ (o docs en Swagger) | | 10 |
| 3 | Dashboard Web funcional | Vista web cargada correctamente | Abrir http://localhost:5000 | | 10 |
| 4 | Comunicacion por red Bridge personalizada | Ambos servicios conectados a monitor-net | docker network inspect monitor-net | | 15 |
| 5 | Resolucion DNS entre contenedores | Dashboard consulta por nombre api-service | docker compose exec dashboard-service python -c "import requests; print(requests.get('http://api-service:8000/api/system', timeout=5).status_code)" | | 15 |
| 6 | Administracion de recursos | Limites de CPU/memoria visibles en compose | docker compose config | | 10 |
| 7 | Healthchecks y disponibilidad | Estado healthy en servicios | docker compose ps | | 10 |
| 8 | Persistencia historica en BD | Tabla metrics_history con registros | docker compose exec api-service python -c "import sqlite3; c=sqlite3.connect('/app/data/metrics.db'); print(c.execute('select count(*) from metrics_history').fetchone()[0])" | | 15 |
| 9 | Endpoint de historial | API devuelve historial | Abrir http://localhost:8000/api/history?limit=10 | | 5 |

## Puntaje total sugerido

- Total: 100 puntos
- Aprobacion sugerida: 70 puntos

## Checklist de capturas recomendadas

- Captura 1: salida de docker compose ps mostrando ambos contenedores Up/Healthy.
- Captura 2: salida de docker network inspect monitor-net con ambos contenedores.
- Captura 3: dashboard cargado en el navegador.
- Captura 4: endpoint /api/history devolviendo datos.
- Captura 5: consulta SQLite con conteo de registros historicos.

## Observaciones del evaluador

- Fortalezas:
- Aspectos a mejorar:
- Recomendaciones finales:
