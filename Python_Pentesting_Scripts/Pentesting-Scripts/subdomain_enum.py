#!/usr/bin/env python3
"""
Subdomain Enumeration Tool
Python for Pentesters - Task 2

Reads potential subdomain names from a wordlist, prepends each one
to a target domain, and tests for valid responses via HTTP.

Usage:
    python3 subdomain_enum.py <domain> <wordlist>

Example:
    python3 subdomain_enum.py example.com subdomains.txt
"""

import requests
import sys


def load_wordlist(filepath):
    """Read a wordlist file and return a list of stripped lines."""
    try:
        with open(filepath, "r") as f:
            words = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(words)} entries from {filepath}")
        return words
    except FileNotFoundError:
        print(f"[!] Error: '{filepath}' not found.")
        return []


def enumerate_subdomains(domain, wordlist):
    """Test each subdomain candidate against the target domain."""
    found = []

    for sub in wordlist:
        url = f"http://{sub}.{domain}"
        try:
            requests.get(url, timeout=3)
            print(f"[+] Found: {url}")
            found.append(url)
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass

    return found


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <domain> <wordlist>")
        print(f"Example: python3 {sys.argv[0]} example.com subdomains.txt")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist_path = sys.argv[2]

    print(f"[*] Starting subdomain enumeration for {domain}")
    wordlist = load_wordlist(wordlist_path)

    if not wordlist:
        print("[!] No words to test. Exiting.")
        sys.exit(1)

    results = enumerate_subdomains(domain, wordlist)
    print(f"\n[*] Enumeration complete. Found {len(results)} subdomain(s).")


main()
