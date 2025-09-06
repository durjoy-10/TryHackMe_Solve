<img width="1490" height="289" alt="image" src="https://github.com/user-attachments/assets/8f4a8c45-3361-45e6-b384-2660f6d01948" />  
<img width="1508" height="832" alt="image" src="https://github.com/user-attachments/assets/f4d61269-b5b2-4da4-8874-9cea4be09203" />

## First Connect the target machine using ssh --> TASK_1.1
<img width="859" height="371" alt="image" src="https://github.com/user-attachments/assets/a56201ad-4e8a-4ab0-a9e4-cb4581e0a06b" />

<img width="1434" height="140" alt="image" src="https://github.com/user-attachments/assets/8c310ba0-48bf-49c6-bf37-85530f9556e6" />

## Now find id of the use --> Task_1.2

<img width="1097" height="42" alt="image" src="https://github.com/user-attachments/assets/9dc6cdb5-88c2-4e6b-a198-06e97c415dee" />

<img width="1456" height="846" alt="image" src="https://github.com/user-attachments/assets/b3ce6f1d-9420-4397-9907-54ffa9e4e0fb" />
<img width="1433" height="356" alt="image" src="https://github.com/user-attachments/assets/3eaa289d-138e-4bd3-8a23-39844d908f00" />

## Here i have to get root user permission by using readable permission of users of /etc/shadow file 

### First check the permission 
<img width="994" height="43" alt="image" src="https://github.com/user-attachments/assets/e2a7e3d3-875a-4bcd-921d-75e8680247da" />

#### Here i have read and write permission..Now first work on read permission. By using this read permission how can i get the root user permission. 


<img width="1308" height="500" alt="image" src="https://github.com/user-attachments/assets/40b10db9-7987-4e32-bb88-6cebc3838d0c" />

#### Read the /etc/shadow ...Here i get the root user password hashes .. Copy the hash and crack the hash using john the ripper 

<img width="1308" height="389" alt="image" src="https://github.com/user-attachments/assets/defd9386-5b34-4cf4-aca4-9ca03400e04a" />

#### Here I get the root password that is <b> password123 <b> and the hash was encrypted by <b> sha512crypt <b>

<img width="481" height="87" alt="image" src="https://github.com/user-attachments/assets/a09f6283-26a1-4203-aa6d-6efa26a7f626" />

#### Login as root 


<img width="1474" height="707" alt="image" src="https://github.com/user-attachments/assets/4d90bf1d-1c66-47dd-b0da-4f85a8b3119c" />

## Now here I describe when I have r & w permission of /etc/shadow file but assume in the previous escalation method by read file is not work (root password can't be cracked) or the file /etc/shadow have only w permission .. For this situation I can get permission of root for only having the write permission of /etc/shadow file 

<img width="711" height="44" alt="image" src="https://github.com/user-attachments/assets/ec32a829-3352-4273-9211-4ac8a83506e5" />

#### Here i have create a netcat listening port ..If anyone connect to the machine the he get the /etc/shadow file  

<img width="1438" height="552" alt="image" src="https://github.com/user-attachments/assets/6cfe6d8a-4196-4656-9446-fb659bcb685b" />

#### Here i get the file on my local machine .. Now I have to update the root password .. 

<img width="1438" height="222" alt="image" src="https://github.com/user-attachments/assets/05560066-1b34-4300-b5ae-5a1f91bc66b5" />

#### Now I created a sha256 hash of durjoy..


<img width="1438" height="245" alt="image" src="https://github.com/user-attachments/assets/c92ecdb6-1d0e-4c0e-b536-fc39d9ca69e8" />

#### Now change the root hash to my crated hash ..And save the file .. 

<img width="1435" height="62" alt="image" src="https://github.com/user-attachments/assets/5326e9c0-b1d3-4bfd-ac29-d235939ed629" /> 

#### Transfer the updated shadow file to the remote machine and interchange /etc/shadow to shadow 

<img width="707" height="67" alt="image" src="https://github.com/user-attachments/assets/8ef9b622-a282-4db7-8690-d5f287ef150e" />

#### netcat listener to the remote machine..Here now /etc/shadow file is updated ..Now I can login as root using the password of durjoy which i created 

<img width="707" height="67" alt="image" src="https://github.com/user-attachments/assets/2d9b4ae2-7e05-4929-bc6c-589e7267ac21" /> 

#### Task-4 Completed 

<img width="1310" height="836" alt="image" src="https://github.com/user-attachments/assets/57faff68-60e0-49de-abe0-b2b4c423ee11" />

## Where I have write permission of /etc/passwd , I can use 3 techniques to escalate root privilege.. 

### Technique_1:  
##### N.B: It is not worked in all machine. But it good to check 
#### First check the /etc/passwd file permission 
<img width="513" height="57" alt="image" src="https://github.com/user-attachments/assets/98cc86ff-bdd8-4810-b6d4-7452c7f7a3a5" />
#### Here i have read and write permission .. 

#### Now simply read the file 
<img width="1203" height="147" alt="image" src="https://github.com/user-attachments/assets/89ce9220-69af-4824-a13b-39b5b2bc2ce4" />
#### Here Focus in any user..(root or others) .. I use root user .. Here in the root user hashes here have a x after root ..It means the root password is saved in shadow file .. 
#### Here After x , 0:0 defines userid(root) and groupid (root) 

#### Now remove the x which defines password in the shadow file as black password 
<img width="403" height="147" alt="image" src="https://github.com/user-attachments/assets/9dd4c8a8-c132-49b7-822a-f5b1e86955e4" />

#### Now try to login but failed..because in updated linux machine this method is not worked 
<img width="1203" height="87" alt="image" src="https://github.com/user-attachments/assets/b09d7daa-2f4c-4329-9a25-f6bb57f7b275" />


### Technique_2: give a hash password instead of x ..Then it is not check the shadow files..Automatically execute here 
<img width="732" height="153" alt="image" src="https://github.com/user-attachments/assets/a48e9a57-5499-48cf-a8ad-058bfc1c549d" />

#### Here i use hashes of durjoy 

#### NOw login as root giving the password durjoy 
<img width="1203" height="72" alt="image" src="https://github.com/user-attachments/assets/765ac3a3-c0aa-4d13-b2e4-6c81d6295fd4" />

### Technique_3 : Here i created a new user(Ddas), password(durjoy) with giving root permissions 
<img width="730" height="56" alt="image" src="https://github.com/user-attachments/assets/a99ca792-0be7-42c7-a1d4-596ce1021e1f" />

#### Now try to login as user Ddas and password durjoy and get the root privilege 
<img width="1203" height="72" alt="image" src="https://github.com/user-attachments/assets/caf1c988-78de-4f65-9481-1c8cccf2976e" />


## Extra: If a normal user have /etc/sudoers file permission then the process for escalate privilege 
#### It is not work in the latest linux machine .. 
### process : 
#### cmd:``` ls -la /etc/sudoers ```
###### It finds the permission of the /etc/sudoers file 

#### cmd:``` cat /etc/sudoers ```
###### Read the file 

#### cmd:``` vi /etc/sudoers ```
###### Edits the files ..Add this ! 
  ```
     #User Privilege Specification
root ALL=(All) ALL
user ALL=(ALL) ALL  --> Here I add these in these file
  ```
#### Now if the technique worked then i can run all the files or do what the root do using sudo privious the command .. 

#### cmd ```sudo bash``` 
###### Here I get the root bash it it worked ..But in this room the machine is up-to-date..Thats why i can't get access ..If it is not worked then it shows this type of message "sudo: /etc/sudoers is mode 0446, should be 0440..That's mean others userers don't have root permissions"


<img width="1314" height="770" alt="image" src="https://github.com/user-attachments/assets/6117d8b5-24ed-4eb3-90a5-6b466c5a8bae" />

## Sudo Misconfigure: 
### Technique_1: Idtended Functionality
<img width="1248" height="368" alt="Intended_1" src="https://github.com/user-attachments/assets/257ebc18-8a66-4259-ac75-4f263df5c258" />
<img width="1435" height="99" alt="Intended_2" src="https://github.com/user-attachments/assets/a9d9f3ca-4dff-4158-8b37-e2c80d7be37d" />

### Technique_2: Shell Escaping 

<img width="731" height="486" alt="shell_escaping_1" src="https://github.com/user-attachments/assets/e23257ce-bf1a-43b5-8695-56a6f4f1dc45" />
<img width="731" height="58" alt="shell_escaping_1_1" src="https://github.com/user-attachments/assets/fd772000-745c-42f9-96d4-a36f7ffe745c" />

<img width="1084" height="858" alt="image" src="https://github.com/user-attachments/assets/6fa09d63-c56b-4988-b135-85b9c9b6489b" />

<span style="color:red">Here I will give the note how to escalate privilege using environment variable </span>

