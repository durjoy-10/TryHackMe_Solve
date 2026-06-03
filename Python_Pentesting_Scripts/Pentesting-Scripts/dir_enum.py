#!/usr/bin/env python3
"""
Directory Enumeration Tool
Python for Pentesters - Task 2

Reads directory/file name candidates from a wordlist and tests each one
against a target URL by appending the candidate and a file extension.

Usage:
    python3 dir_enum.py <target_url> <wordlist> [extension]

Example:
    python3 dir_enum.py http://10.10.10.5 wordlist.txt .html
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


def enumerate_directories(target_url, wordlist, extension=".html"):
    """Test each directory/file candidate against the target URL."""
    found = []

    for entry in wordlist:
        url = f"{target_url}/{entry}{extension}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code != 404:
                print(f"[+] {r.status_code} - {url}")
                found.append(url)
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass

    return found


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <target_url> <wordlist> [extension]")
        print(f"Example: python3 {sys.argv[0]} http://10.10.10.5 wordlist.txt .html")
        sys.exit(1)

    target_url = sys.argv[1]
    wordlist_path = sys.argv[2]
    extension = sys.argv[3] if len(sys.argv) > 3 else ".html"

    print(f"[*] Starting directory enumeration for {target_url}")
    wordlist = load_wordlist(wordlist_path)

    if not wordlist:
        print("[!] No words to test. Exiting.")
        sys.exit(1)

    results = enumerate_directories(target_url, wordlist, extension)
    print(f"\n[*] Enumeration complete. Found {len(results)} valid path(s).")


main()
