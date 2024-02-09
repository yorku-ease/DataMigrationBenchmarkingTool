# Data

In this folder you're supposed to have all files specified in `config.ini` needed to run the experiment. 
In this example, you have 2 options. 
- Download the file from here [Ubuntu's website](https://ubuntu.com/download/desktop) and name it ubuntu.iso 
- Run this command to generate a 5gb file. 
```bash
dd if=/dev/zero of=ubuntu.iso bs=1M count=5000
```