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
