# Room Link:  https://tryhackme.com/room/hfb1thegame

- It's a simple 5 min room which is made based on stegnograpy.. Here I simply use **strings** command with piping grep to catch the specif metadata which is hidden to a exe file 

* The command :
```
strings -n 8 Tetrix.exe | grep -i "thm{"
```
- Here -n means min length and in grep -i means it is not case sensitive

![i1](/Image/The%20Game/1.png)

![i2](/Image/The%20Game/2.png)