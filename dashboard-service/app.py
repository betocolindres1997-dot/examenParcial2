from flask import Flask, render_template, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# URL de la API - usando el nombre del servicio en Docker
API_BASE_URL = os.getenv('API_URL', 'http://api-service:8000')

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
    """Proxy para obtener estado completo"""
    return jsonify(get_api_data('/api/status'))

@app.route('/api/proxy/system')
def proxy_system():
    """Proxy para obtener información del sistema"""
    return jsonify(get_api_data('/api/system'))

@app.route('/api/proxy/cpu')
def proxy_cpu():
    """Proxy para obtener información de CPU"""
    return jsonify(get_api_data('/api/cpu'))

@app.route('/api/proxy/memory')
def proxy_memory():
    """Proxy para obtener información de memoria"""
    return jsonify(get_api_data('/api/memory'))

@app.route('/api/proxy/disk')
def proxy_disk():
    """Proxy para obtener información de discos"""
    return jsonify(get_api_data('/api/disk'))

@app.route('/api/proxy/network')
def proxy_network():
    """Proxy para obtener información de red"""
    return jsonify(get_api_data('/api/network'))

@app.route('/api/proxy/processes')
def proxy_processes():
    """Proxy para obtener información de procesos"""
    limit = request.args.get('limit', 10)
    return jsonify(get_api_data(f'/api/processes?limit={limit}'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)