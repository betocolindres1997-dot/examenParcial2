from flask import Flask, render_template, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# URL de la API - usando el nombre del servicio en Docker
API_BASE_URL = os.getenv('API_URL', 'http://api-server:5000')

def get_api_data(endpoint):
    """Obtiene datos de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Error {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "No se puede conectar con la API"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('index.html')

@app.route('/api/proxy/status')
def proxy_status():
    """Proxy para /status"""
    return jsonify(get_api_data('/status'))

@app.route('/api/proxy/cpu')
def proxy_cpu():
    """Proxy para /cpu"""
    return jsonify(get_api_data('/cpu'))

@app.route('/api/proxy/memory')
def proxy_memory():
    """Proxy para /memory"""
    return jsonify(get_api_data('/memory'))

@app.route('/api/proxy/disk')
def proxy_disk():
    """Proxy para /disk"""
    return jsonify(get_api_data('/disk'))

@app.route('/api/proxy/network')
def proxy_network():
    """Proxy para /network"""
    return jsonify(get_api_data('/network'))

@app.route('/api/proxy/services')
def proxy_services():
    """Proxy para /services (procesos)"""
    limit = request.args.get('limit', 10)
    return jsonify(get_api_data(f'/services?limit={limit}'))


@app.route('/api/proxy/history')
def proxy_history():
    """Proxy para /history"""
    limit = request.args.get('limit', 20)
    return jsonify(get_api_data(f'/history?limit={limit}'))

# Mantener compatibilidad con endpoints antiguos
@app.route('/api/proxy/processes')
def proxy_processes_alt():
    """Alias para compatibilidad"""
    return proxy_services()

@app.route('/health')
def health():
    """Healthcheck para el dashboard"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)