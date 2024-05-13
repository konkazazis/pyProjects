import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re

import tkinter
import customtkinter
import platform


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app=customtkinter.CTk()
app.geometry("500x500")
app.title("Hardware Info")

# UI Elements
title = customtkinter.CTkLabel(app, text="Hardware Info", font=("Arial", 20))
title.pack(padx=10,pady=10)


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

def System_information():
    # System Information
    
    uname = platform.uname()
    system = customtkinter.CTkLabel(app, text="System: "+uname.system)
    node = customtkinter.CTkLabel(app, text="Node Name: "+uname.node)
    release = customtkinter.CTkLabel(app, text="Release: "+uname.release)
    version = customtkinter.CTkLabel(app, text="Version: "+uname.version)
    machine = customtkinter.CTkLabel(app, text="Machine: "+uname.machine)
    processor = customtkinter.CTkLabel(app, text=f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
    ip = customtkinter.CTkLabel(app, text=f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
    mac = customtkinter.CTkLabel(app, text=f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")


    system.pack()
    node.pack()
    release.pack()
    version.pack()
    machine.pack()
    processor.pack()
    ip.pack()
    mac.pack()


    # Boot Time
    
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    boot_time = customtkinter.CTkLabel(app, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    boot_time.pack()

    # number of cores
    physical_cores = customtkinter.CTkLabel(app, text=f"Physical cores: {psutil.cpu_count(logical=False)}")
    total_cores = customtkinter.CTkLabel(app, text=f"Total cores: {psutil.cpu_count(logical=True)}")
    physical_cores.pack()
    total_cores.pack()
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpu_frequency = customtkinter.CTkLabel(app, text=f"Max Frequency: {cpufreq.max:.2f}Mhz")
    cpu_min_frequency = customtkinter.CTkLabel(app, text=f"Min Frequency: {cpufreq.min:.2f}Mhz")
    cpu_current_frequency = customtkinter.CTkLabel(app, text=f"Current Frequency: {cpufreq.current:.2f}Mhz")
    cpu_frequency.pack()
    cpu_min_frequency.pack()
    cpu_current_frequency.pack()
    
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")


    # Memory Information
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")



    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")



    # Disk Information
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")

    ## Network information
    print("="*40, "Network Information", "="*40)
    ## get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    ##get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")


if __name__ == "__main__":

    System_information()

app.mainloop()