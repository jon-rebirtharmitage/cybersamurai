import socket
import subprocess
import platform

def check_os():
    system_name = platform.system()
    if system_name == "Linux":
        return "Linux"
    elif system_name == "Windows":
        return "Windows"
    elif system_name == "Darwin":
        return "macOS"
    else:
        return f"Unknown system: {system_name}"


def get_ip_and_subnet_windows():
    # Get the IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Get the subnet mask using the `ipconfig` command
    process = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if ip_address in stdout.decode('utf-8'):
        lines = stdout.decode('utf-8').split('\n')
        for i in range(len(lines)):
            if ip_address in lines[i]:
                subnet_line = lines[i + 1].strip()
                subnet_mask = subnet_line.split(':')[-1].strip()
                return ip_address, subnet_mask
    return ip_address, None


def get_ip_and_subnet_linux():
    # Get the IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Get the subnet mask
    process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if ip_address in stdout.decode('utf-8'):
        for line in stdout.decode('utf-8').split('\n'):
            if ip_address in line:
                subnet_mask = line.strip().split()[-1]
                return ip_address, subnet_mask
    return ip_address, None
def get_network():
    ch = check_os()
    if ch == "Windows":
        ip, subnet = get_ip_and_subnet_windows()
        print(f"IP Address: {ip}")
        print(f"Subnet Mask: {subnet}")
    elif ch == "Linux":
        ip, subnet = get_ip_and_subnet_linux()
        print(f"IP Address: {ip}")
        print(f"Subnet Mask: {subnet}")
    else:
        print("Test")