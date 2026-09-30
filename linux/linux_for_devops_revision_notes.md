# Linux for DevOps – Detailed Revision Notes

> Source: "Train with Shubham" YouTube lecture series (Day 1 → Day 3 + Networking + awk/sed/grep + LVM/EBS).
> Commands are written as used in the lecture on an **Ubuntu EC2 instance**. Where the transcript was unclear, the standard command is given.

---

## Table of Contents
1. [How the Internet Works](#1-how-the-internet-works)
2. [Servers, Clients, Applications](#2-servers-clients-applications)
3. [Linux Fundamentals](#3-linux-fundamentals)
4. [Getting a Linux Machine (EC2 Setup)](#4-getting-a-linux-machine-ec2-setup)
5. [Basic Linux Commands](#5-basic-linux-commands)
6. [SSH & Remote Access](#6-ssh--remote-access)
7. [System / Monitoring Commands](#7-system--monitoring-commands)
8. [Package Management (apt)](#8-package-management-apt)
9. [User & Group Management](#9-user--group-management)
10. [File Permissions & Ownership](#10-file-permissions--ownership)
11. [Compression & Archiving](#11-compression--archiving)
12. [Remote File Transfer (scp, rsync)](#12-remote-file-transfer-scp-rsync)
13. [Networking Commands](#13-networking-commands)
14. [Text Processing: awk, sed, grep](#14-text-processing-awk-sed-grep)
15. [Storage: EBS, Volumes, LVM, Mounting](#15-storage-ebs-volumes-lvm-mounting)
16. [Interview Q&A Cheat-Sheet](#16-interview-qa-cheat-sheet)
17. [Master Command Table](#17-master-command-table)

---

## 1. How the Internet Works

- You (in Pune/Delhi etc.) watch a YouTube video whose servers may be in the USA. Data does **not** travel via satellite; it travels via **optical fibre cables laid under the sea**.
- **Data centre** = a large facility with many computers that **store** and **transmit** data.
- Cables are owned by companies (AT&T, Jio, Reliance, Airtel…). You pay them via **internet recharge / data pack**.
- **ISP (Internet Service Provider)** e.g. Airtel Xtreme, Jio gives your device internet access. Devices are identified using **IP addresses**.

**What happens when you type `youtube.com` in a browser**
1. Request goes to your **ISP** (checks you have internet access).
2. **Domain name** (`youtube.com`) must be converted to an **IP address**.
3. **DNS (Domain Name Server)** maps domain → IP address.
4. Request is forwarded (hop by hop through many servers) to the **application server** at that IP.
5. Server sends the **response** back to your **client** (browser/phone).

---

## 2. Servers, Clients, Applications

**Server** = a computer whose job is **to serve information**. Types:

| Server type | Purpose |
|---|---|
| Email server | serves emails |
| File server | stores/returns files |
| Database server | stores data (insert/query) |
| Application server | runs application logic (e.g. facebook.com, Django/NodeJS app) – **dynamic** data |
| Web server | serves **static** content (HTML, images) – e.g. **Nginx** |

**Client** = requests information from a server (phone, laptop, browser).

**Server vs Client (classic interview question):** server *serves* information; client *requests* information.

**Web server vs Application server:** Web server → static data (Nginx serving static pages). Application server → dynamic data with computation/logic (Django/NodeJS app).

**Types of applications**
- **Standalone** – needs no internet/DB/mail server (airport feedback kiosk, coin-operated machine).
- **Web application** – runs on the internet with supporting servers (email, DB, application servers, cache…), e.g. instagram.com, youtube.com.

A DevOps engineer must know which type they work on (web apps need DB, front-end, back-end, cloud connections).

**Application Support & Maintenance** – keeping applications healthy on their OS: checking crashes, connectivity (e.g. app's connection to the email server broke → emails not sent), giving "care and support".

---

## 3. Linux Fundamentals

### What is an OS?
A large program that lets applications run on your computer. ~90 % of desktop users use Windows, but **~90 % of servers/applications run on Linux**.

### Linux facts
- Created in **1991** by **Linus Torvalds**.
- **Open source** (free; community contributes), highly **secure**, no antivirus needed, multitasking.
- No forced auto-updates like Windows.
- Linux = free/open source; commercial variants exist (e.g. RHEL is paid; CentOS/Ubuntu free).
- Distros: Ubuntu, Kali, CentOS, Fedora, Arch, Red Hat, Gentoo…

### Windows vs Linux (points)
- Windows is commercial (licence); Linux is free.
- Windows needs an antivirus; Linux doesn't typically.
- Linux is CLI-centric, ideal for coding/servers.

### Ways to get Linux if you're on Windows
1. **WSL** (Windows Subsystem for Linux)
2. **VirtualBox** (VM inside Windows)
3. **Cloud VM** (AWS / Azure / GCP)
4. **Vagrant** (HashiCorp tool to run any OS as VM)

### Kernel, Shell, Bootloader
- **Kernel** – the "heart" of the OS; written in C; called the **Linux kernel**. Talks to hardware.
- **Shell** – interface/gateway between the **user and kernel**. You type **shell commands** (`mkdir`, `ls`…) in a **terminal**; the shell asks the kernel to do it.
- **Bootloader** – first process at boot; starts OS files/processes ("mom waking everyone up"). Linux bootloader: **GRUB** = **GR**and **U**nified **B**ootloader.

### System architecture (flow)
```
Applications (terminal, editors, utilities)
        ↓
      Shell
        ↓
      Kernel
        ↓
     Hardware (disk, RAM, CPU, printer, camera…)
```

### Hardware info commands
| Need | Command |
|---|---|
| CPU usage / processes | `top` |
| Disk usage | `df -h` |
| RAM usage | `free` / `free -h` |

(On macOS some differ.)

### Filesystem hierarchy – "everything starts from `/`" (root)
```
/           root
├── home    users' home dirs
├── usr     user programs
├── bin     binaries (commands)
├── etc     config files (e.g. /etc/passwd, /etc/group)
├── var     variable data (/var/log → logs)
├── tmp     temporary files
├── root    root user's home
├── dev     devices
├── mnt     mount points
└── proc    process/system info
```
- `cd /` goes to root. `cd /var/log` → logs. `cd /bin` → binaries.

### Processes
- Processes run in the background to keep the system running. **PID** = Process ID.
- The **first process launched by the boot loader has PID 1**.
- **Process states:** Running, Sleeping, Stopped, Terminated/Killed, **Zombie** (finished but still in the table).
- View with `top` (press `q` to quit).

---

## 4. Getting a Linux Machine (EC2 Setup)

1. Create an **AWS account** (Visa credit/debit card + OTP).
2. Go to **EC2** (Elastic Compute Cloud = virtual servers in the cloud).
3. **Launch instance:**
   - Name: e.g. `linux-for-devops`
   - OS/AMI: **Ubuntu** (free-tier eligible; don't pick Windows)
   - Instance type: **t2.micro** (free tier)
   - **Key pair:** create new (`.pem` file – private key downloaded; public key stays on the instance)
   - Network: allow **SSH (port 22)**
   - Storage: **8 GB minimum** (root volume; can't go lower)
4. Wait: *Pending → Running*. Select → **Connect**.
5. Connect via browser (EC2 Instance Connect) or SSH client (see §6).

> Note: public IP/DNS **changes after stop/start** → copy the new SSH command from the Connect tab.

---

## 5. Basic Linux Commands

### Terminal basics
```bash
date                 # current date/time (UTC on servers)
clear                # clear screen (Ctrl+L also)
Ctrl + R             # reverse-search command history
Up arrow             # previous commands
Ctrl + C             # stop running command
```

### Listing & navigating
```bash
ls                   # list files
ls -l                # long listing (permissions, owner, size, time)
ls -a                # include hidden files (start with .)
ls -la               # long + hidden
ls -ld folder        # info about the directory itself ('d' at start = directory)
pwd                  # print working directory
cd folder            # change directory
cd ..                # one level up (cd ../.. two levels)
cd /                 # root
cd /home/ubuntu      # absolute path
```
- Colours: blue = directory; green = executable; red = broken soft link.
- `ls -l` first char: `d` = directory, `-` = file, `l` = link.

### Create / delete
```bash
mkdir devops                 # make directory
touch new_file.txt           # create empty file
rm file.txt                  # remove file (permanent – no recycle bin)
rm -r folder                 # remove folder recursively
rmdir folder                 # remove empty directory
```
> `rm` on a directory fails without `-r` ("flag" = option starting with `-`).

### View content
```bash
cat file.txt                 # print file content
echo "Hello Dosto"           # print text
echo "Hello Dosto" > file.txt   # redirect output INTO a file (overwrites)
echo "more text" >> file.txt    # append
echo "This is my file" > myfile.txt   # creates the file if missing
zcat file.gz                 # view content of a compressed (gz) file
head file.txt                # first 10 lines
head -n 5 file.txt           # first 5 lines
tail file.txt                # last 10 lines
tail -n 5 file.txt           # last 5 lines
tail -f app.log              # follow file live (new lines appear); Ctrl+C to stop
less file.txt                # page-by-page viewer (q to quit)
more file.txt               # similar, paginated
```
**Real-life:** `tail -f logfile` while debugging live logs.

### Copy / move / rename
```bash
cp new_file.txt devops/              # copy file into folder
cp devops/devs_file.txt clouds/      # copy using path from outside
cp -r clouds devops/                 # copy folder recursively
mv new_file.txt clouds/              # move (source removed)
mv ../new_file.txt ../clouds/        # using relative paths
mv devops linux-for-devops           # RENAME = move to new name
```
- `cp` → copy exists at source **and** destination. `mv` → only at destination.

### Word count
```bash
wc myfile.txt        # lines  words  bytes
wc -l file           # lines only
```

### Links (shortcuts)
- **Hard link** – survives if the original file is deleted (points to same data).
- **Soft (symbolic) link** – breaks (turns red) if the original is deleted. Like a Windows shortcut.
```bash
ln /home/ubuntu/linux-for-devops/devs_file.txt hardlink_file     # hard link
ln -s /home/ubuntu/linux-for-devops/devs_file.txt softlink_file  # soft link
ls -l               # soft link shows ->  target
cat softlink_file
rm devs_file.txt    # after deleting source:
ls                  # softlink turns red (broken); hardlink still works
cat hardlink_file   # still prints content
```
Test: editing the original reflects through soft link; recreating the file at the same path revives the soft link.

### cut, tee, sort, diff
```bash
cat myfile.txt
cut -b 1 myfile.txt        # 1st byte
cut -b 1-4 myfile.txt      # bytes 1 to 4  ("This")

echo hello | tee hello.txt # show on screen AND write to file

sort file.txt              # sort lines alphabetically

diff hello.txt demo.txt    # differences between TWO files
wc a b c                   # word count works for many files
```

### Editors – vi / vim
```bash
vi demo.txt          # open (or vim demo.txt)
i                    # enter INSERT mode
Esc                  # leave insert mode
:wq                  # write & quit
:q!                  # quit without saving
```
> If the browser is zoomed, vi may display glitches – reset zoom.

### Hardware/disk quick view
```bash
df -h                # disk usage human readable (filesystem, size, used, avail, mount)
du .                 # disk usage of current dir tree
du -h .              # human readable
ls -a                # see hidden dirs like .cache
```

---

## 6. SSH & Remote Access

**Remote-access options:** RDP (Remote Desktop Protocol), **SSH (Secure Shell)**, AnyDesk. Servers use **port 22 for SSH**.

### Key concept (Rahul & Anjali analogy)
- **Public key** stays on the **server** (Anjali's public info).
- **Private key** stays with **you/client** (Rahul).
- Key pair is generated by **`ssh-keygen`** (AWS does this when you "create key pair"; `.pem` downloaded).

### Connect from local terminal
```bash
cd ~/Downloads
ls linux-for-devops-key.pem
chmod 400 linux-for-devops-key.pem      # make key not publicly viewable (required)

ssh -i linux-for-devops-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
# type: yes   (first-time host confirmation)
```
- Format: `ssh -i <path-to-private-key> <username>@<public-DNS-or-IP>`
- Default user on Ubuntu AMI: `ubuntu`.
- Windows: use **PuTTY**.
- If `ssh` prints usage text, SSH client is available.
- If permissions are wrong, use `sudo` or fix with `chmod 400`.

### Other basics on a system
```bash
uname                # OS platform (Linux / Darwin for macOS)
uptime               # how long system is up, users, load average
date
who                  # all logged-in users & login times
whoami               # current user only
which bash           # location of a command's binary (e.g. /usr/bin/bash)
which java           # check if java installed & its path
id                   # uid, gid, groups of current user
```
Use `which java` to verify the installed Java version location when an app needs Java 8.

---

## 7. System / Monitoring Commands

```bash
top                  # live processes (q to quit)
ps                   # processes in current shell
ps aux               # all processes
ps -ef               # all processes (full format)
free                 # RAM (total/used/free)
free -h              # human readable (e.g. ~949Mi total)
vmstat               # virtual memory statistics
vmstat -a            # active/inactive memory
df -h                # disk
du -h .              # directory sizes
fuser <file>         # which processes use a file/filesystem
kill <PID>           # kill a process (avoid unless necessary; needs permission)
watch <cmd>          # repeat a command every 2 s
watch -n 5 top       # repeat every 5 s
watch mtr train.com
```
**nohup** – run a command ignoring hangup and append output to a file:
```bash
nohup free -h > nohup.out      # (lecture: nohup + command; output → nohup.out)
cat nohup.out
head -n 5 nohup.out
tail -n 5 nohup.out
```
Useful for storing application logs in a file.

---

## 8. Package Management (apt)

Package managers by distro:

| Manager | Distro |
|---|---|
| **apt** | Ubuntu / Debian |
| **yum** | CentOS |
| **dnf** | Fedora |
| **rpm** | Red Hat |
| **pacman** | Arch |
| **portage (emerge)** | Gentoo |

```bash
sudo apt update                    # refresh package lists (do this first!)
sudo apt install docker.io         # install package (needs sudo)
sudo apt install zip unzip
sudo apt install net-tools
sudo apt install traceroute
sudo apt install jq
sudo apt install whois
sudo apt install ifplugd nmap wireless-tools

which docker                       # /usr/bin/docker
sudo apt remove docker.io          # uninstall
```
- Error "**Unable to locate package / no installation candidate**" → run `sudo apt update` first.
- Error "**Unable to acquire lock / permission denied**" → you're not root; use `sudo`.
- Tip: **Ctrl+R** to reuse an earlier command.
- Installing Docker also creates a **docker group** and a **docker0 network interface**.

---

## 9. User & Group Management

### Sudo concept ("Papa" analogy)
- **root** = superuser (Papa of the house; permission for everything).
- **sudo = "Super User DO"** – run a command with root privileges.
- Members of the **sudo group** are allowed to use sudo.
```bash
cd /root                 # Permission denied (normal user)
sudo su -                # become root (or: sudo -i)
sudo shutdown            # fails without sudo; with sudo it schedules power-off
sudo reboot              # restart system
```
(After shutdown/stop, restart from AWS console; **public IP may change**.)

### Users
```bash
sudo useradd -m jethalal          # create user + home dir (-m makes /home/jethalal)
sudo passwd jethalal              # set password (needs sudo)
su jethalal                       # switch user (asks for password)
whoami
id                                # uid/gid/groups
exit                              # go back to previous user
sudo userdel jethalal             # delete user
cat /etc/passwd                   # list of all users (last entries = newest)
```
- Without `sudo`: `useradd` → *Permission denied* (only Papa can add people).
- Ubuntu's first user `ubuntu` has **UID 1000**; next user typically **1001**.
- Newer user's shell prompt looks like `$` only (no full prompt) – cosmetic.

### Groups
```bash
sudo groupadd devops              # create group
sudo groupadd tester
cat /etc/group                    # list groups (or: less /etc/group)

sudo gpasswd -a jethalal devops           # add user to group
sudo gpasswd -a ubuntu devops
sudo gpasswd -M iyer,tappu,bhide tester   # add MULTIPLE users to group

sudo groupdel tester              # delete group (users remain, just not in that group)
id                                # shows current groups (re-login may be needed to refresh)
```
Scenario: Google-style company – DevOps engineers (ubuntu, jethalal) vs testers (iyer, tappu, bhide). Create groups, add users, assign permissions to **groups** not individuals.

---

## 10. File Permissions & Ownership

### Reading `ls -l`
```
drwxrwxr-x  2  ubuntu  ubuntu  4096  date  clouds
│└┬┘└┬┘└┬┘
│ │  │  └── OTHERS permissions
│ │  └───── GROUP permissions
│ └──────── USER (owner) permissions
└────────── type: d = directory, - = file, l = link
```
- **r = read (4), w = write (2), x = execute (1)**.
- **User** = owner; **Group** = collection of users; **Others** = everyone else.

### Numeric (octal) permissions
| Digit | Binary | Perm |
|---|---|---|
| 0 | 000 | `---` |
| 1 | 001 | `--x` |
| 2 | 010 | `-w-` |
| 3 | 011 | `-wx` |
| 4 | 100 | `r--` |
| 5 | 101 | `r-x` |
| 6 | 110 | `rw-` |
| 7 | 111 | `rwx` |

Examples:
- `775` = `rwxrwxr-x`
- `777` = `rwxrwxrwx` (open to all – file/folder turns colour highlighted)
- `664` = `rw-rw-r--`
- `700` = `rwx------` (only owner has everything)
- `400` = `r--------` (used for `.pem` keys)

### chmod / chown / chgrp
```bash
chmod 777 clouds                  # rwx for user, group, others
chmod 700 devs_file.txt           # only owner: rwx; file turns green (executable)
ls -l

sudo chown jethalal demo_file.txt         # change file OWNER
sudo chgrp devops demo_file.txt           # change file GROUP
ls -l demo_file.txt                       # owner: jethalal, group: devops
# chown user:group file   also works to set both
```

### umask
- **umask** = default permissions mask applied to newly created files.
```bash
umask               # e.g. 0022 (some systems) / 0002 (on this EC2)
```
- `0002` → user & group full access, others read/execute only (as explained in lecture).
- `0022` → group & others read/execute.
- Permanent change is done in shell config (e.g. `~/.bashrc`, `/etc/profile`).

---

## 11. Compression & Archiving

```bash
sudo apt install zip unzip

# ZIP
zip -r ldf.zip clouds            # -r recursive for folders
unzip ldf.zip                    # extract
gzip file / gunzip file.gz       # gz compress/extract (extension .gz)
```
Note: on Linux, `ldf.zip` is compress; `unzip` de-compress (make smaller / bigger).

### tar
```bash
tar -cvzf clouds.tar.gz clouds        # CREATE archive
tar -xvzf clouds.tar.gz               # EXTRACT
tar -xvzf clouds.tar.gz -C linux-for-devops   # extract into a directory
tar --help                            # all flags
```
Flag meaning:
| Flag | Meaning |
|---|---|
| `c` | create (compress/bundle) |
| `x` | extract |
| `v` | verbose (show progress) |
| `z` | gzip compression |
| `f` | specify file name (comes right before file name) |

Rule: **compress → `tar -cvzf`**, **extract → `tar -xvzf`**.

---

## 12. Remote File Transfer (scp, rsync)

### scp (Secure Copy) – uses the `.pem` key
```bash
# LOCAL → REMOTE
scp -i ~/Downloads/linux-for-devops.pem secret_file.txt ubuntu@<EC2-DNS>:/home/ubuntu

# REMOTE → LOCAL (folder → recursive -r)
scp -i ~/Downloads/linux-for-devops.pem -r ubuntu@<EC2-DNS>:/home/ubuntu/linux-for-devops .
```
- Format: `scp -i <key> <source> <destination>`; remote path = `user@host:/path`; `.` = current directory.
- First-time prompt: type **yes**.

### rsync (sync two directories – only differences transferred)
```bash
sudo apt install rsync
rsync -avz -e "ssh -i ~/Downloads/linux-for-devops.pem" \
      ubuntu@<EC2-DNS>:/home/ubuntu/linux-for-devops .
# reverse source & destination to sync the other way
```
- `-a` archive, `-v` verbose, `-z` compress, `-e` execute remote-shell command (ssh with key).
- Works both ways; just swap source/destination.

---

## 13. Networking Commands

Install tools first: `sudo apt install net-tools traceroute whois nmap wireless-tools ifplugd`

| Command | Purpose / Example |
|---|---|
| `ping train.com` | Checks connectivity: sends packets, reports transmitted/received/loss. Ctrl+C to stop. |
| `netstat` | Network statistics: **active internet connections**, protocol (TCP), local/foreign address, state (ESTABLISHED). |
| `ss` | Modern equivalent of netstat (same output). |
| `ifconfig` | Network interfaces (eth0, lo, docker0) with IPs. |
| `ip addr show` | Show all IP addresses / interfaces. |
| `iwconfig` | Wireless interface info (needs wireless-tools; "no wireless extensions" on EC2). |
| `traceroute youtube.com` | Shows **hops** (IPs) your request takes source → destination (up to 30 hops). |
| `tracepath youtube.com` | Similar, shows path in a friendlier way. |
| `mtr train.com` | **My Traceroute** – combines **ping + traceroute** live. |
| `nslookup train.com` | DNS lookup → resolves domain to IP. |
| `dig train.com` | Detailed DNS info of a domain. |
| `telnet train.com 80` | Test a specific **port** connectivity; `443` for HTTPS. |
| `whois train.com` | Domain registration details (registrar, dates). |
| `nc` / `netcat` | Networking utility (rarely used). |
| `arp` | **Address Resolution Protocol** – IP ↔ **MAC address** (hardware address). |
| `ifplugstatus` | Whether interfaces are plugged/working. |
| `ip route` / `route` | Routing table (default gateway 0.0.0.0 = internet gateway via eth0). |
| `sudo iptables -L` | Firewall rules / tables (needs root). |
| `nmap -v train.com` | Network/port scan – shows open ports (e.g., 80). |
| `curl` | Call API endpoints. |
| `wget` | Download files. |
| `watch` | Run a command repeatedly. |

**Important concepts**
- **HTTP → port 80**, **HTTPS → port 443**, **SSH → 22**.
- **TCP** = Transmission Control Protocol (used for most internet traffic).
- **NIC** = Network Interface Card; `eth0` = the EC2's Ethernet interface; **`lo`** = loopback interface.
- **Loopback / localhost = 127.0.0.1** – server talking to itself; apps run locally on `localhost:port`.
- **`docker0`** = network interface created by Docker.
- **Socket** = endpoint for a network connection (used in socket programming).
- `ping` can show **packet loss**; traceroute prints `* * *` (no reply) for hops that time out.
- Only scan sites you own / are authorised to (nmap).

### curl vs wget
```bash
# curl – API calls (GET)
curl -X GET https://dummy.restapiexample.com/api/v1/employees
curl -X GET <api-url> | jq          # prettify JSON with jq (sudo apt install jq)

# wget – download files
mkdir downloads && cd downloads
wget <file-url>                     # copy link address → paste
ls
```
**API analogy:** McDonald's – you don't enter the kitchen; the counter person (API) takes your order to the server (kitchen) and brings the response.

### Hotspot experiment (netstat)
Switching from Wi-Fi to phone hotspot changes the foreign/local address in `netstat` (old connection may linger in cache).

---

## 14. Text Processing: awk, sed, grep

Setup used in lecture:
```bash
mkdir day5 && cd day5
vi application.log        # paste a sample log (fields: date, time, level, ...)
head -n 2 application.log
```
Sample log columns: `$1` = date, `$2` = time, `$3`…= level/info/trace/event etc.

### awk (column-based; programming in a command)
Syntax: `awk 'PATTERN {ACTION}' file`

```bash
awk '{print}' application.log                 # print whole file
awk '{print $1}' application.log              # 1st column
awk '{print $1, $2}' application.log          # columns 1 and 2
awk '{print $1, $2, $4}' application.log      # skip column 3
awk '{print $1, $2, $3, $5}' application.log

# Filter lines that contain INFO
awk '/INFO/ {print $1, $2, $3, $4, $5}' application.log
awk '/INFO/ {print $1,$2,$3,$4,$5}' application.log > only_info.txt   # to a file
cat only_info.txt

# Count occurrences
awk '/INFO/ {count++} END {print count}' application.log
awk '/INFO/ {count++} END {print "The count of INFO is", count}' application.log   # → 16
awk '/<ip-address>/ {count++} END {print "The count of IP is", count}' application.log   # → 13

# Time range (column 2 = timestamp)
awk '$2 >= "08:53:00" && $2 <= "08:53:59" {print $1, $2, $3}' application.log

# Line range using NR (row number)
awk 'NR >= 2 && NR <= 10 {print NR, $0}' application.log

# Filter processes by user
ps aux | grep ubuntu
ps aux | awk '{print $2}'          # print PID column
```
**Requirement:** awk works best with **structured/formatted data** (CSV – comma separated, TSV – tab separated); column-by-column.

### sed (Stream EDitor; line-by-line, any data)
```bash
sed -n '/INFO/p' application.log            # -n = no auto-print; p = print matches
sed 's/INFO/LOG/g' application.log          # replace INFO → LOG globally (s = substitute, g = global)
sed -n '/INFO/=' application.log            # print LINE NUMBERS where INFO appears
sed -n -e '/INFO/=' -e '/INFO/p' application.log   # line number + the line

sed '1,10s/INFO/LOG/g' application.log      # replace only in lines 1–10
sed '1,15s/INFO/LOG/g;15q' application.log  # process lines 1–15 then quit (q)
```
- `-n` suppresses default output; without it INFO/TRACE/EVENT all print.
- `-e` = expression; multiple expressions allowed.
- Note: sed does **not edit the file** by default – add `-i` to edit in place.

### grep (**G**lobal **R**egular **E**xpression **P**attern)
```bash
grep INFO application.log          # lines matching INFO
grep -i info application.log       # -i = case-insensitive
grep -ic info application.log      # -c = count of matching lines → 16
ps aux | grep ubuntu               # filter another command's output (pipe)
```
Compare: counting INFO in awk needs `count++`, `END`, `print`; in grep it's just `grep -ic`.

### awk vs sed vs grep
| Tool | Works on | Best for |
|---|---|---|
| **awk** | structured, column-wise (CSV/TSV) | extracting columns, counts, conditions, ranges |
| **sed** | any data, **line by line** | find/replace, print line numbers/ranges, stream editing |
| **grep** | any text | quick pattern search, counting matches |

---

## 15. Storage: EBS, Volumes, LVM, Mounting

### Concepts
- **Block / Disk / Volume** – storage device (like C: / D: drive).
- **EBS = Elastic Block Store** – AWS service to create **volumes** and attach to EC2 (similar to EC2 creating servers). *Azure has no "EBS" by that name; this is the AWS way.*
- EC2 default root volume = **8 GB** (min); extra volumes can be attached when storage runs low.
- **Attach** = connect volume to instance (like plugging a USB). **Mount** = bind it to a directory so it's **usable**.
- **Snapshot** = backup of a volume (create volume from snapshot optional).
- Volume must be in the **same Availability Zone** as the instance.

### Lab plan
Create 3 volumes: **10 GB, 12 GB, 14 GB** → attach to EC2 (plus default 8 GB root).

**Steps**
1. Launch new Ubuntu t2.micro instance (`tws-volume-instance`), key pair, allow SSH, storage 8 GB.
2. SSH in (chmod 400 key, `ssh -i ...`).
3. AWS Console → **EC2 → Elastic Block Store → Volumes → Create volume**: General Purpose SSD, size 10 (then 12, 14), same AZ, no snapshot.
4. Select volume → **Actions → Attach volume** → choose instance → device name.
   - **Device names:** use **`/dev/sdf`, `/dev/sdg`, `/dev/sdh`** for data volumes. (`sda`/`sdb` are reserved for root → error "already in use".)
   - Inside Linux they show as **`/dev/xvdf`, `xvdg`, `xvdh`**. Root disk = `xvda` (partitions xvda1, 14, 15, 16).
5. Verify on the instance.

### Two key commands
```bash
lsblk        # list block devices (disks/volumes attached)
df -h        # mounted filesystems, size, used, avail, mount point
```
Attached ≠ mounted: new volumes appear in `lsblk` but **not** in `df -h` until mounted.

### LVM (Logical Volume Manager) – dynamic storage management
Hierarchy:
```
Physical Volumes (PV)  →  Volume Group (VG)  →  Logical Volumes (LV)
   xvdf (10G) + xvdg (12G)  = 22G VG        →  e.g. 10G LV (extendable)
```
- **Physical Volume**: a disk/volume prepared for LVM.
- **Volume Group**: pool combining several PVs (10 + 12 = ~22 GB).
- **Logical Volume**: "slice" carved from VG; can be **increased/reduced** anytime.
- LVM commands need root: `sudo su -` (or prefix `sudo`).

```bash
sudo su -                                   # become root
lvm                                         # opens LVM prompt (optional; same commands work outside)

# 1. Create Physical Volumes
pvcreate /dev/xvdf /dev/xvdg                # (in lvm prompt: pvcreate ...)
pvdisplay                                   # details of PVs

# 2. Create Volume Group
vgcreate tws-vg /dev/xvdf /dev/xvdg
vgs                                         # list VGs (size ~21.99G, free)
vgdisplay

# 3. Create Logical Volume
lvcreate -L 10G -n tws-lv tws-vg            # 10G LV named tws-lv from VG tws-vg
lvs                                         # list LVs
lvdisplay
```
(The third disk `xvdh` was left aside for direct-disk mounting demo.)

### Format and mount a Logical Volume
```bash
mkdir /mnt/tws-lv-mount                      # mount point (directory)

mkfs.ext4 /dev/tws-vg/tws-lv                 # create filesystem (format)
mount /dev/tws-vg/tws-lv /mnt/tws-lv-mount   # mount: mount <source> <destination>

df -h        # shows /dev/mapper/tws--vg-tws--lv mounted on /mnt/tws-lv-mount
```
Use it:
```bash
cd /mnt/tws-lv-mount
mkdir devops
cd devops
vi hello-dosto.txt
```
Unmount / remount:
```bash
umount /mnt/tws-lv-mount        # unmount
cat /mnt/tws-lv-mount/devops/hello-dosto.txt   # → No such file or directory (unmounted)
mount /dev/tws-vg/tws-lv /mnt/tws-lv-mount     # remount → files visible again
```

### Mount a raw disk directly (no LVM)
```bash
mkdir /mnt/tws-disk-mount
mkfs.xfs /dev/xvdh              # format disk (xfs); ext4 also works
#  (If it says the device contains an LVM member/filesystem – confirm only if you're sure)
mount /dev/xvdh /mnt/tws-disk-mount
df -h                           # both mounts visible
```
> `mkfs.xfs`/`mkfs.ext4` – filesystem creation. Formatting **erases** data.

### Extend a Logical Volume (dynamic storage)
```bash
df -h                                   # check current size
lvextend -L +5G /dev/tws-vg/tws-lv      # add 5 GB from VG (LV path, not VG name)
# result: "Size of logical volume changed from 10 GiB to 15 GiB"
lsblk                                   # LV shows larger; PVs xvdf/xvdg consumed accordingly
# (To make the filesystem itself grow you also run: resize2fs /dev/tws-vg/tws-lv  for ext4)
```
- Use path of the **LV** (`/dev/tws-vg/tws-lv`), not `tws-vg` – LV is already associated with its VG, which must have free space.
- Same LVM commands work **inside and outside** the `lvm` prompt (`lvs`, `lvdisplay`, etc.).
- LVM tooling originally came from the Linux community/Red Hat/Canonical ecosystem.

### Attach vs Mount (interview)
- **Attach:** adds a block/volume to the instance (hardware level).
- **Mount:** makes it usable by binding to a directory (filesystem level).

---

## 16. Interview Q&A Cheat-Sheet

| Question | Short answer |
|---|---|
| Server vs client? | Server serves info; client requests it. |
| Web server vs application server? | Web → static (Nginx); Application → dynamic logic (Django/NodeJS). |
| Standalone vs web app? | Standalone needs no internet/other servers; web app depends on DB, mail, app servers, internet. |
| What is a kernel / shell? | Kernel = heart of OS, talks to hardware; shell = interface between user and kernel. |
| Name a Linux bootloader | **GRUB** – GRand Unified Bootloader. |
| What is PID 1? | First process started by the bootloader/init. |
| Process states? | Running, Sleeping, Stopped, Terminated, Zombie. |
| Hard link vs soft link? | Hard link survives source deletion; soft link breaks. |
| `rm` vs `rmdir` vs `rm -r`? | Remove file / empty dir / directory recursively. |
| `cat` vs `zcat` | Show file / show gz-compressed file. |
| `head` / `tail` / `tail -f` | First lines / last lines / follow live logs. |
| `less` / `more` | Paginated viewing of big files. |
| `who` vs `whoami` | All logged-in users vs current user. |
| What is sudo? | Super User DO – run with root permissions. |
| File permission meaning of 755/644/777? | rwxr-xr-x / rw-r--r-- / rwxrwxrwx. |
| What is umask? | Default permission mask for new files. |
| `chown` / `chgrp` | Change owner / change group of a file. |
| `zip` vs `tar` | Both compress/archive; tar flags `-cvzf` create, `-xvzf` extract. |
| `scp` vs `rsync` | scp = copy over SSH; rsync = sync (only differences). |
| `curl` vs `wget` | curl = API calls; wget = download files. |
| ping vs traceroute vs mtr | Connectivity test / path of hops / both combined live. |
| Ports 22 / 80 / 443 | SSH / HTTP / HTTPS. |
| localhost IP? | 127.0.0.1 (loopback interface `lo`). |
| awk vs sed vs grep? | Column-based structured data / line-based editing / pattern search. |
| Attach vs mount? | Attach volume to instance / bind volume to a directory to use it. |
| PV / VG / LV? | Physical volume → Volume group → Logical volume. |
| `lsblk` vs `df -h` | Block devices attached vs mounted filesystems & usage. |
| Package managers? | apt (Ubuntu), yum (CentOS), dnf (Fedora), rpm (RedHat), pacman (Arch), portage (Gentoo). |

---

## 17. Master Command Table

| Category | Commands |
|---|---|
| Basics | `date`, `clear`, `pwd`, `ls`, `ls -l`, `ls -la`, `ls -ld`, `cd`, `cd ..` |
| Files/dirs | `touch`, `mkdir`, `rm`, `rm -r`, `rmdir`, `cp`, `cp -r`, `mv`, `ln`, `ln -s` |
| View/text | `cat`, `zcat`, `echo`, `head`, `tail`, `tail -f`, `less`, `more`, `wc`, `cut`, `tee`, `sort`, `diff`, `vi/vim` |
| System info | `uname`, `uptime`, `who`, `whoami`, `which`, `id`, `top`, `ps`, `free -h`, `vmstat`, `df -h`, `du`, `fuser`, `kill`, `nohup`, `watch` |
| Power | `sudo shutdown`, `sudo reboot` |
| Users/groups | `useradd`, `passwd`, `su`, `userdel`, `groupadd`, `groupdel`, `gpasswd -a`, `gpasswd -M`, `/etc/passwd`, `/etc/group` |
| Permissions | `chmod`, `chown`, `chgrp`, `umask` |
| Archive | `zip -r`, `unzip`, `gzip`, `gunzip`, `tar -cvzf`, `tar -xvzf` |
| Remote | `ssh -i key.pem user@host`, `scp -i key.pem`, `scp -r`, `rsync -avz -e "ssh -i key"` |
| Packages | `apt update`, `apt install`, `apt remove` |
| Network | `ping`, `netstat`, `ss`, `ifconfig`, `ip addr`, `iwconfig`, `traceroute`, `tracepath`, `mtr`, `nslookup`, `dig`, `telnet`, `whois`, `arp`, `ifplugstatus`, `route`, `iptables -L`, `nmap`, `curl`, `wget`, `jq` |
| Text tools | `awk`, `sed`, `grep` |
| Storage | `lsblk`, `df -h`, `pvcreate`, `pvdisplay`, `vgcreate`, `vgs`, `vgdisplay`, `lvcreate`, `lvs`, `lvdisplay`, `lvextend`, `mkfs.ext4`, `mkfs.xfs`, `mount`, `umount` |

---

### Practice tips from the lecture
- Practise every command yourself on an EC2 Ubuntu instance – break things, retry ("bleed more in practice, sweat less in war").
- Install missing tools when you hit "command not found" – that is part of learning.
- Take a real log file (sample from the internet) and practise `awk`, `sed`, `grep` on it.
- Stop/terminate EC2 instances and delete extra EBS volumes after practice to avoid charges.
