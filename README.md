# Adin-Network-Backup

This program aims to automate network switch backups. Features of the program:<br />
-Taking backup of the device and sending it through FTP.<br />
-Sending mail if any error occures(FTP connection, Login to switch via ssh, Trying to connect to FTP multiple times in one day)
-If error is not related to any of this, program creates a log file of what happened and keeps it locally.
-Working on a schedule if crontab is used on "backup.sh"

This backup system supports this devices:
-Aruba
-Huawei
-HP 
-Tplink
-Alcatel

Use crontab on Ubuntu to schedule the program to work automatically.

If network device has old ssh ciphers change "~/.ssh/config".
## USAGE

Change devices and customer names to your desire. I could get it from an xml but I was on short a time so just made it this way.
Change mail info on backmail.py.
