import socket
import re
import os # Libraries Imported, self explanatory


ip_add_pattern = re.compile("^(?:[0-9]){1,3}\. [0-9]{1,3}$") # Checks against IPV4 Address
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

port_min = 0
port_max = 65535 # Initialise port range and list to store ports

open_ports = []

while True:
    ip_add_entered = input("Enter IP you would like to use")
    if ip_add_pattern.search(ip_add_entered):
        print(f"{ip_add_entered} is a valid IP address")
        break # Simple loop until valid IP address is entered

while True:
    print("Please enter the range of ports you would like to scan, eg 60-100")
    port_range = input("Enter range of ports")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1)) # Regex split
        port_max = int(port_range_valid.group(2))
        break # Loops until valid port range is entered

for port in range(port_min, port_max +1 ): # Creates a TCP socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            set.settimeout(0.5)
            s.connect((ip_add_entered, port))
            open_port.append(port)
    except:
        pass # Loops through ports

    for port in open_ports:
        print(f"Port {port} is open on {ip_add_entered}")

filename = f"scan_results_{ip_add_entered}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, 'w') as f:
    f.write(f"Port Scan Results\n")
    f.write(f"Target IP: {ip_add_entered}\n")
    f.write(f"Port Range: {port_min}-{port_max}\n")
    f.write(f"Scan Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total Open Ports: {len(open_ports)}\n")
    f.write("=" * 50 + "\n")
    if open_ports:
        for port in open_ports:
            f.write(f"Port {port} is open\n")
    else:
        f.write("No open ports found\n")

print(f"\nResults saved to {filename}")
