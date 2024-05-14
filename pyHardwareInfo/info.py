import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import tkinter as tk
from tkinter import ttk
import customtkinter

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def system_information(frame):
    # System Information
    uname = platform.uname()
    system_label = customtkinter.CTkLabel(frame, text="System: "+uname.system)
    system_label.grid(row=0, column=0, sticky="w")
    node_label = customtkinter.CTkLabel(frame, text="Node Name: "+uname.node)
    node_label.grid(row=1, column=0, sticky="w")
    release_label = customtkinter.CTkLabel(frame, text="Release: "+uname.release)
    release_label.grid(row=2, column=0, sticky="w")
    version_label = customtkinter.CTkLabel(frame, text="Version: "+uname.version)
    version_label.grid(row=3, column=0, sticky="w")
    machine_label = customtkinter.CTkLabel(frame, text="Machine: "+uname.machine)
    machine_label.grid(row=4, column=0, sticky="w")
    processor_label = customtkinter.CTkLabel(frame, text=f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
    processor_label.grid(row=5, column=0, sticky="w")
    ip_label = customtkinter.CTkLabel(frame, text=f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
    ip_label.grid(row=6, column=0, sticky="w")
    mac_label = customtkinter.CTkLabel(frame, text=f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
    mac_label.grid(row=7, column=0, sticky="w")

def boot_time(frame):
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    boot_time_label = customtkinter.CTkLabel(frame, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    boot_time_label.grid(row=2, column=0, sticky="w")

def cpu_information(frame):
    # CPU Cores
    physical_cores_label = customtkinter.CTkLabel(frame, text=f"Physical cores: {psutil.cpu_count(logical=False)}")
    physical_cores_label.grid(row=9, column=0, sticky="w")
    total_cores_label = customtkinter.CTkLabel(frame, text=f"Total cores: {psutil.cpu_count(logical=True)}")
    total_cores_label.grid(row=1, column=1, sticky="w")

    # CPU Frequencies
    cpufreq = psutil.cpu_freq()
    cpu_frequency_label = customtkinter.CTkLabel(frame, text=f"Max Frequency: {cpufreq.max:.2f}Mhz")
    cpu_frequency_label.grid(row=11, column=0, sticky="w")
    cpu_min_frequency_label = customtkinter.CTkLabel(frame, text=f"Min Frequency: {cpufreq.min:.2f}Mhz")
    cpu_min_frequency_label.grid(row=12, column=0, sticky="w")
    cpu_current_frequency_label = customtkinter.CTkLabel(frame, text=f"Current Frequency: {cpufreq.current:.2f}Mhz")
    cpu_current_frequency_label.grid(row=13, column=0, sticky="w")

    # CPU Usage
    cpu_usage_label = customtkinter.CTkLabel(frame, text="CPU Usage Per Core:")
    cpu_usage_label.grid(row=14, column=0, sticky="w")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_core_label = customtkinter.CTkLabel(frame, text=f"Core {i}: {percentage}%")
        cpu_core_label.grid(row=15+i, column=0, sticky="w")
    total_cpu_usage_label = customtkinter.CTkLabel(frame, text=f"Total CPU Usage: {psutil.cpu_percent()}%")
    total_cpu_usage_label.grid(row=15+len(psutil.cpu_percent(percpu=True)), column=0, sticky="w")

def memory_information(frame):
    # Memory Information
    svmem = psutil.virtual_memory()
    memory_label = customtkinter.CTkLabel(frame, text=f"Memory Information: Total: {get_size(svmem.total)}, Available: {get_size(svmem.available)}, Used: {get_size(svmem.used)}, Percentage: {svmem.percent}%")
    memory_label.grid(row=1+len(psutil.cpu_percent(percpu=True)), column=0, sticky="w")

    # SWAP Information
    swap = psutil.swap_memory()
    swap_label = customtkinter.CTkLabel(frame, text=f"Swap Information: Total: {get_size(swap.total)}, Free: {get_size(swap.free)}, Used: {get_size(swap.used)}, Percentage: {swap.percent}%")
    swap_label.grid(row=2+len(psutil.cpu_percent(percpu=True)), column=0, sticky="w")

    # Disk Information
    partitions = psutil.disk_partitions()
    for i, partition in enumerate(partitions):
        disk_info_frame = customtkinter.CTkFrame(frame)
        disk_info_frame.grid(row=18+len(psutil.cpu_percent(percpu=True))+i, column=0, padx=10, pady=5, sticky="nsew")
        disk_info_label = customtkinter.CTkLabel(disk_info_frame, text=f"Disk {i+1} Information")
        disk_info_label.grid(row=0, column=0, sticky="w")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_usage_label = customtkinter.CTkLabel(disk_info_frame, text=f"Total Size: {get_size(partition_usage.total)}, Used: {get_size(partition_usage.used)}, Free: {get_size(partition_usage.free)}, Percentage: {partition_usage.percent}%")
            partition_usage_label.grid(row=1, column=0, sticky="w")
        except PermissionError:
            continue
    disk_io = psutil.disk_io_counters()
    disk_io_label = customtkinter.CTkLabel(frame, text=f"Total read: {get_size(disk_io.read_bytes)}, Total write: {get_size(disk_io.write_bytes)}")
    disk_io_label.grid(row=3+len(psutil.cpu_percent(percpu=True))+len(partitions), column=0, sticky="w")

def network_information(frame):
    partitions = psutil.disk_partitions()
    # Network Information
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        network_info_frame = customtkinter.CTkFrame(frame)
        network_info_frame.grid(row=19+len(psutil.cpu_percent(percpu=True))+len(partitions)+len(if_addrs), column=0, padx=10, pady=5, sticky="nsew")
        network_info_label = customtkinter.CTkLabel(network_info_frame, text=f"Network Interface: {interface_name}")
        network_info_label.grid(row=0, column=0, sticky="w")
        for j, address in enumerate(interface_addresses):
            if str(address.family) == 'AddressFamily.AF_INET':
                ip_label = customtkinter.CTkLabel(network_info_frame, text=f"IP Address: {address.address}, Netmask: {address.netmask}, Broadcast IP: {address.broadcast}")
                ip_label.grid(row=j+1, column=0, sticky="w")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                mac_label = customtkinter.CTkLabel(network_info_frame, text=f"MAC Address: {address.address}, Netmask: {address.netmask}, Broadcast MAC: {address.broadcast}")
                mac_label.grid(row=j+1, column=0, sticky="w")
    net_io = psutil.net_io_counters()
    net_io_label = customtkinter.CTkLabel(frame, text=f"Total Bytes Sent: {get_size(net_io.bytes_sent)}, Total Bytes Received: {get_size(net_io.bytes_recv)}")
    net_io_label.grid(row=19+len(psutil.cpu_percent(percpu=True))+len(partitions)+len(if_addrs)+1, column=0, sticky="w")

def main():
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.title("Hardware Info")
    root.geometry("900x500")
    
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(expand=True, fill="both")

    title_label = customtkinter.CTkLabel(main_frame, text="Hardware Info", font=("Arial", 20))
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    # Add Scrollbar
    canvas = customtkinter.CTkCanvas(main_frame)
    scrollbar = customtkinter.CTkScrollbar(main_frame, command=canvas.yview)
    scrollable_frame = customtkinter.CTkFrame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid layout for canvas and scrollbar
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    # Configure row and column weights to make the canvas expand
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # Column1
    column1_frame = customtkinter.CTkFrame(scrollable_frame)
    column1_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    system_information(column1_frame)
    boot_time(column1_frame)

    column1_frame2 = customtkinter.CTkFrame(scrollable_frame)
    column1_frame2.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    memory_information(column1_frame2)

    # column2
    column2_frame = customtkinter.CTkFrame(scrollable_frame)
    column2_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
    cpu_information(column2_frame)

    # column3
    column3_frame = customtkinter.CTkFrame(scrollable_frame)
    column3_frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
    network_information(column3_frame)

    root.mainloop()

if __name__ == "__main__":
    main()


