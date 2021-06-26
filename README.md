# Adin-Network-Backup

This program aims to automate network switch backups. Features of the program:<br />
-Taking backup of the device and sending it through FTP.<br />
-Sending mail if any error occures(FTP connection, Login to switch via ssh, Trying to connect to FTP multiple times in one day)<br />
-If error is not related to any of this, program creates a log file of what happened and keeps it locally.<br />
-Working on a schedule if crontab is used on "backup.sh"<br /><br />

This backup system supports this devices:<br />
-Aruba<br />
-Huawei<br />
-HP <br />
-Tplink<br />
-Alcatel<br /><br />

Use crontab on Ubuntu to schedule the program to work automatically.<br /><br />

If network device has old ssh ciphers change "~/.ssh/config".<br />
## USAGE

Change devices and customer names to your desire. I could get it from an xml but I was on short a time so just made it this way.<br />
Change mail info on backmail.py.
