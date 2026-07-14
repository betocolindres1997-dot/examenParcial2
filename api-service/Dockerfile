FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request as r, sys; urls=['http://localhost:5000/health','http://localhost:8000/health','http://localhost:5000/','http://localhost:8000/']; ok=False\nfor u in urls:\n    try:\n        r.urlopen(u, timeout=3); ok=True; break\n    except Exception:\n        pass\nsys.exit(0 if ok else 1)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]