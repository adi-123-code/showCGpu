from flask import render_template, jsonify, request
import requests
from app import app

node_addresses = ['http://localhost:5001','http://localhost:5002','http://localhost:5003']  # 子节点地址列表

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data')
def fetch_data():
    data = {}
    for node in node_addresses:
        response = requests.get(f"{node}/report")
        if response.status_code == 200:
            data[node] = response.json()
    return jsonify(data)
