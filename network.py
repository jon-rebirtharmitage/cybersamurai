import ipaddress
import socket
import subprocess
import platform
import scapy.all as scapy
from pymongo import MongoClient, database

c = MongoClient(
    'mongodb+srv://ceadministrator:B3urH8ffZakl96ew@nemesis.aswz80g.mongodb.net/?retryWrites=true&w=majority&appName=nemesis')

db = c.get_database("resources")
collection = db.get_collection("ouiLookup")


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
        return ip, subnet
    else:
        ip, subnet = get_ip_and_subnet_linux()
        return ip, subnet


def parse_network(ip, subnet):
    subnet_mask = sum(bin(int(x)).count('1') for x in subnet.split('.'))
    return ip + "/" + str(subnet_mask)
def network_discovery():
    ip, subnet = get_network()
    request = scapy.ARP()
    request.pdst = parse_network(ip, subnet)
    broadcast = scapy.Ether()
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'
    request_broadcast = broadcast / request
    clients = scapy.srp(request_broadcast, timeout=10, verbose=1)[0]
    for element in clients:
        e = "NULL"
        try:
            query = {element[1].hwsrc[0:8].upper(): {'$exists': 1}}
            a = collection.find_one(query)
            e = a[element[1].hwsrc[0:8].upper()]
        except:
            e = "N/A"
        print(element[1].psrc + "   -    " + e)
    c.close()

network_discovery()
