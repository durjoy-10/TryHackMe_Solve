#!/usr/bin/env python3
"""
ARP Network Scanner
Python for Pentesters - Task 3

Discovers live hosts on a local network by broadcasting ARP requests
and collecting responses. Requires root privileges.

Usage:
    sudo python3 arp_scanner.py <ip_range> [interface]

Example:
    sudo python3 arp_scanner.py 10.10.10.0/24 eth0
"""

from scapy.all import *
import sys


def build_arp_packet(ip_range):
    """Construct an Ethernet/ARP broadcast packet for the target range."""
    broadcast_mac = "ff:ff:ff:ff:ff:ff"
    ether_layer = Ether(dst=broadcast_mac)
    arp_layer = ARP(pdst=ip_range)
    return ether_layer / arp_layer


def scan_network(ip_range, interface="eth0", timeout=2):
    """Send ARP requests and return a list of (IP, MAC) tuples for live hosts."""
    packet = build_arp_packet(ip_range)
    answered, unanswered = srp(packet, timeout=timeout, iface=interface, inter=0.1, verbose=False)

    hosts = []
    for sent, received in answered:
        ip = received[ARP].psrc
        mac = received[Ether].src
        hosts.append((ip, mac))

    return hosts


def main():
    if len(sys.argv) < 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <ip_range> [interface]")
        print(f"Example: sudo python3 {sys.argv[0]} 10.10.10.0/24 eth0")
        sys.exit(1)

    ip_range = sys.argv[1]
    interface = sys.argv[2] if len(sys.argv) > 2 else "eth0"

    print(f"[*] Scanning {ip_range} on interface {interface}...")
    hosts = scan_network(ip_range, interface)

    if hosts:
        print(f"\n[*] Found {len(hosts)} live host(s):\n")
        print(f"{'IP Address':<20}{'MAC Address':<20}")
        print("-" * 40)
        for ip, mac in hosts:
            print(f"{ip:<20}{mac:<20}")
    else:
        print("[!] No hosts found. Check your IP range and interface.")


main()
