# import psutil

# def get_cpu_info():
#     cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
#     cpu_times_per_core = psutil.cpu_times(percpu=True)
#     cpu_freq_per_core = psutil.cpu_freq(percpu=True)

#     for i, (percent, times, freq) in enumerate(zip(cpu_percent_per_core, cpu_times_per_core, cpu_freq_per_core)):
#         print(f"CPU 核心 {i}:")
#         print(f"  使用率: {percent}%")
#         print(f"  时间: {times}")
#         print(f"  频率: {freq.current} MHz")

# get_cpu_info()

# # GPU能耗
# import pynvml

# def get_gpu_power_usage():
#     pynvml.nvmlInit()
#     device_count = pynvml.nvmlDeviceGetCount()
#     for i in range(device_count):
#         handle = pynvml.nvmlDeviceGetHandleByIndex(i)
#         power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000  # 转换为瓦特
#         name = pynvml.nvmlDeviceGetName(handle)
#         print(f"GPU {i} ({name}): {power_usage} W")
#     pynvml.nvmlShutdown()

# get_gpu_power_usage()


# import pyRAPL

# pyRAPL.setup()

# # Create a meter to measure energy usage
# meter = pyRAPL.Measurement('example')

# # Start measuring
# meter.begin()

# # Run some code
# for i in range(1000000):
#     pass

# # Stop measuring
# meter.end()

# print(f'CPU Energy (joules): {meter.result.pkg}')
# print(f'DRAM Energy (joules): {meter.result.dram}')


# import subprocess

# def get_cpu_power_usage():
#     result = subprocess.run(['power_gadget', '-e', '1', '-d', '1', '-t', '1'], capture_output=True, text=True)
#     output = result.stdout
#     # 解析输出以提取能耗信息
#     lines = output.split('\n')
#     for line in lines:
#         if 'Processor Power' in line:
#             print(line)

# get_cpu_power_usage()

# import os

# def read_rapl_energy():
#     def read_energy(file_path):
#         with open(file_path) as f:
#             energy_uj = int(f.read())
#         return energy_uj / 1e6  # 转换为焦耳

#     base_path = '/sys/class/powercap/intel-rapl/'
#     try:
#         pkg_energy = read_energy(os.path.join(base_path, 'intel-rapl:0/energy_uj'))
#         print(f'Package Energy used: {pkg_energy} J')
#     except FileNotFoundError:
#         print("Package energy file not found")

#     # 查找其他可能存在的目录
#     for subdir in os.listdir(base_path):
#         subdir_path = os.path.join(base_path, subdir)
#         if os.path.isdir(subdir_path):
#             energy_file = os.path.join(subdir_path, 'energy_uj')
#             if os.path.exists(energy_file):
#                 try:
#                     energy = read_energy(energy_file)
#                     print(f'Energy used in {subdir}: {energy} J')
#                 except FileNotFoundError:
#                     print(f"Energy file not found in {subdir}")

# read_rapl_energy()
# # Package Energy used: 179626.50689 J
# # Energy used in intel-rapl:0: 179626.50689 J

import pynvml

def monitor_pcie_bandwidth():
    pynvml.nvmlInit()
    device_count = pynvml.nvmlDeviceGetCount()
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        pci_info = pynvml.nvmlDeviceGetPciInfo(handle)
        rx_throughput = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        tx_throughput = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
        print(f"Device {i}: RX Throughput: {rx_throughput} bytes/s, TX Throughput: {tx_throughput} bytes/s")
    pynvml.nvmlShutdown()

monitor_pcie_bandwidth()


