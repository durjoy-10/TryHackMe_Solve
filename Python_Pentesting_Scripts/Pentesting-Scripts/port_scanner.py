#!/usr/bin/env python3
"""
TCP Port Scanner
Python for Pentesters - Task 4

Scans a target host for open TCP ports using connect_ex() for efficiency.
Supports hostname resolution and maps common ports to service names.

Usage:
    python3 port_scanner.py <target> [max_port]

Example:
    python3 port_scanner.py 10.10.10.5 1024
"""

import socket
import sys


def probe_port(ip, port, timeout=0.5):
    """Attempt a TCP connection to ip:port. Return True if open, False otherwise."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def scan_ports(ip, port_range, timeout=0.5):
    """Scan a range of ports on the target IP and return a list of open ports."""
    open_ports = []

    for port in port_range:
        if probe_port(ip, port, timeout):
            print(f"[+] Port {port} is open")
            open_ports.append(port)

    return open_ports


def resolve_target(target):
    """Resolve a hostname to an IP address. Return the IP if already valid."""
    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            print(f"[*] Resolved {target} to {ip}")
        return ip
    except socket.gaierror:
        print(f"[!] Could not resolve {target}")
        return None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <target> [max_port]")
        print(f"Example: python3 {sys.argv[0]} MACHINE_IP 1024")
        sys.exit(1)

    target = sys.argv[1]
    max_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1024

    ip = resolve_target(target)
    if not ip:
        sys.exit(1)

    print(f"[*] Scanning {ip} (ports 1-{max_port})...\n")
    open_ports = scan_ports(ip, range(1, max_port + 1))

    if open_ports:
        print(f"\n[*] Scan complete. {len(open_ports)} open port(s) found:")
        print(f"{'Port':<10}{'Likely Service':<20}")
        print("-" * 30)

        common_services = {
            21: "FTP", 22: "SSH", 23: "Telnet",
            25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS",
            445: "SMB", 3306: "MySQL", 3389: "RDP",
            8080: "HTTP Proxy", 8443: "HTTPS Alt"
        }

        for port in sorted(open_ports):
            service = common_services.get(port, "Unknown")
            print(f"{port:<10}{service:<20}")
    else:
        print("\n[!] No open ports found.")


main()
