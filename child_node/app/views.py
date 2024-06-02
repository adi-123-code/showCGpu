from flask import jsonify
from app import app
import psutil
import GPUtil

@app.route('/report')
def report():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent  # 获取内存使用率
    gpus = GPUtil.getGPUs()
    gpu_loads = [gpu.load * 100 for gpu in gpus]  # GPU 负载百分比
    gpu_memory_usage = [gpu.memoryUsed / gpu.memoryTotal * 100 for gpu in gpus]  # GPU 显存使用率
    return jsonify({
        'cpu_usage': cpu_percent,
        'memory_usage': memory_percent,
        'gpu_usage': gpu_loads,
        'gpu_memory_usage': gpu_memory_usage
    })



