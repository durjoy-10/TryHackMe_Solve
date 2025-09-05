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


