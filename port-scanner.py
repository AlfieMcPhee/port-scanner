import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Importing Libraries Above

def resolve_host(host):
    # Converts a hostname into an IP address
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        print(f"[ERROR] Could not resolve host: {host}")
        raise SystemExit(1)



def  get_service_name(port):
    #Looks up a service name per port
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"

