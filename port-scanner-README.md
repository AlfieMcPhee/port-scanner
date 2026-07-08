# Python Port Scanner

A fast, multithreaded TCP port scanner built with Python's standard library. Give it a target host and a range of ports, and it reports which ports are open — using concurrency so a full scan takes seconds rather than minutes.

## Features

- Scans a single host across a configurable range of ports
- Multithreaded using `ThreadPoolExecutor` for fast scanning
- Configurable connection timeout
- Resolves common service names for open ports (e.g. 22 → SSH, 80 → HTTP)
- Clean command-line interface built with `argparse`
- Graceful error handling for invalid hosts and interrupted scans

## Requirements

- Python 3.8+
- No external dependencies — uses only the standard library (`socket`, `argparse`, `concurrent.futures`)

## Installation

```bash
git clone https://github.com/[your-username]/port-scanner.git
cd port-scanner
```

## Usage

```bash
python scanner.py <host> [options]
```

**Examples**

Scan the default port range on a host:

```bash
python scanner.py 192.168.1.1
```

Scan a specific range with a custom timeout and thread count:

```bash
python scanner.py scanme.nmap.org --start 1 --end 1024 --timeout 0.5 --threads 100
```

**Options**

| Flag | Description | Default |
|------|-------------|---------|
| `--start` | First port to scan | 1 |
| `--end` | Last port to scan | 1024 |
| `--timeout` | Socket timeout in seconds | 1.0 |
| `--threads` | Number of concurrent threads | 100 |

## Example output

```
Scanning 192.168.1.1 (ports 1-1024)...
[OPEN]  22   SSH
[OPEN]  80   HTTP
[OPEN]  443  HTTPS
Scan complete: 3 open ports found in 2.1s
```

*(Replace with a screenshot or real output from your build.)*

## How it works

For each port, the scanner attempts a TCP connection using a socket. If the connection succeeds, the port is open; if it's refused or times out, it's treated as closed. Rather than checking ports one at a time, a thread pool runs many connection attempts in parallel, which is where the speed comes from.

## Disclaimer

Only scan systems you own or have explicit permission to test. Unauthorised port scanning may be illegal in your jurisdiction. `scanme.nmap.org` is provided by the Nmap project specifically for testing.

## Possible improvements

- UDP scanning support
- Banner grabbing to identify service versions
- Export results to JSON or CSV
- Scan multiple hosts or a subnet in one run

## Concepts demonstrated

TCP sockets, concurrency with thread pools, CLI design, and safe error handling.
