"""
port-scanner.py

A multithreaded TCP port scanner.
Usage: python port-scanner.py <host> [--start PORT] [--end PORT] [--timeout SECS] [--threads N]
"""

import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# ── Helpers ──────────────────────────────────────────────────────────────────

def resolve_host(host):
    """Turn a hostname into an IP address. Raises SystemExit if it can't."""
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        print(f"[ERROR] Could not resolve host: {host}")
        raise SystemExit(1)


def get_service_name(port):
    """Try to look up the service name for a port (e.g. 80 -> http)."""
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


# ── Core scanning logic ───────────────────────────────────────────────────────

def scan_port(ip, port, timeout):
    """
    Attempt a TCP connection to ip:port.
    Returns the port number if open, None if closed/filtered.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))  # returns 0 if connection succeeded
            if result == 0:
                return port
    except socket.error:
        pass
    return None


def scan_range(ip, start_port, end_port, timeout, max_threads):
    """
    Scan a range of ports concurrently using a thread pool.
    Returns a sorted list of open ports.
    """
    open_ports = []
    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all port scans at once; each runs in its own thread
        futures = {executor.submit(scan_port, ip, port, timeout): port for port in ports}

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                open_ports.append(result)
                print(f"  [OPEN]  {result:<6} {get_service_name(result)}")

    return sorted(open_ports)


# ── Output ────────────────────────────────────────────────────────────────────

def print_summary(open_ports, elapsed):
    """Print a tidy summary at the end of the scan."""
    print("-" * 40)
    if open_ports:
        print(f"Found {len(open_ports)} open port(s) in {elapsed:.1f}s")
    else:
        print(f"No open ports found ({elapsed:.1f}s)")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple multithreaded TCP port scanner."
    )
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("--start",   type=int, default=1,    help="First port to scan (default: 1)")
    parser.add_argument("--end",     type=int, default=1024, help="Last port to scan (default: 1024)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--threads", type=int, default=100,  help="Number of threads (default: 100)")
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Validate port range
    if not (1 <= args.start <= 65535) or not (1 <= args.end <= 65535):
        print("[ERROR] Ports must be between 1 and 65535.")
        raise SystemExit(1)
    if args.start > args.end:
        print("[ERROR] Start port must be less than or equal to end port.")
        raise SystemExit(1)

    ip = resolve_host(args.host)

    print(f"\nScanning {args.host} ({ip})")
    print(f"Ports {args.start}–{args.end}  |  timeout {args.timeout}s  |  {args.threads} threads\n")

    start_time = time.time()

    try:
        open_ports = scan_range(ip, args.start, args.end, args.timeout, args.threads)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        raise SystemExit(0)

    elapsed = time.time() - start_time
    print_summary(open_ports, elapsed)


if __name__ == "__main__":
    main()