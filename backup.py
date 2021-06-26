from netmiko import ConnectHandler
from ftplib import FTP
from datetime import date
import os
from backmail import send_mail

try:
    ##Establish FTP connection.
    ftp=FTP("x.x.x.x")
    ftp.login("username","password")
    ##Change Working Directory to Customers Folder
    ftp.cwd("/FTP_Directory")                            ####CHANGE####
except:
    send_mail("Customer name","-","FTP Hatası !")         ####CHANGE####
    exit()

try:
    ##Create Folder Based on Date
    ftp.mkd(str(date.today()))
except:
    send_mail("Customer name","-","1 Günde 2. Backup Denemesi !")     ####CHANGE####

##Change Working Directory to Dated Folder
ftp.cwd(str(date.today()))

##Info on devices.  ####CHANGE####
##     "ip_address":["device_type","username","password",(IF it is HP)"_cmdline password"]

liste={"192.168.2.11":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.12":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.13":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.14":["aruba_osswitch","admin","SWPASSWORD"],       
       "192.168.2.15":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.16":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.17":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.18":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.20":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.21":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.22":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.23":["aruba_osswitch","admin","SWPASSWORD"],
       "192.168.2.24":["aruba_osswitch","admin","SWPASSWORD"]
       }       
for i in liste:
    try:
        ##Set Device Type
        if liste[i][0]=="huawei" or liste[i][0]=="HP" or liste[i][0]=="alcatel":
            device_type="autodetect"
        else:
            device_type=liste[i][0]
        switch = {
                    "device_type": device_type,
                    "ip": i,
                    "username": liste[i][1],
                    "password": liste[i][2],
                }
        try:
            net_connect=ConnectHandler(**switch)
        except:
            send_mail("Customer name",i,"Cihaza bağlantı kurulamadı !")      ####CHANGE####
            continue

        ##If Aruba
        if liste[i][0]=="aruba_osswitch":
            command="show running-config"
            file_name_command="show running-config | include hostname"
            output = net_connect.send_command(command)
            file_name=net_connect.send_command(file_name_command).split()[1].replace('"',"")+"("+i.split(".")[2]+"."+i.split(".")[3]+")"+".txt"
        
        ##If Huawei
        elif liste[i][0]=="huawei":
            command="display current-configuration"
            file_name_command="display current-configuration | include sysname"
            output = net_connect.send_command(command)
            file_name=net_connect.send_command(file_name_command).split()[1].replace('"',"")+"("+i.split(".")[2]+"."+i.split(".")[3]+")"+".txt"

        ##If HP 19x series
        elif liste[i][0]=="HP":
            command="_cmdline-mode on \n Y\n"+liste[i][3]+"\nscreen-length disable \n display current-configuration"
            file_name_command="display current-configuration | include sysname"
            output = net_connect.send_command_timing(command)
            file_name=net_connect.send_command_timing(file_name_command).split()[1].replace('"',"")+"("+i.split(".")[2]+"."+i.split(".")[3]+")"+".txt"

        ##If Tp-Link
        elif liste[i][0]=="tplink_jetstream":
            command="show running-config"
            file_name_command="show running-config | include hostname"
            output = net_connect.send_command(command)
            file_name=net_connect.send_command(file_name_command).split()[2].replace('"',"")+"("+i.split(".")[2]+"."+i.split(".")[3]+")"+".txt"

        ##If Alcatel
        elif liste[i][0]=="alcatel":
            command="show configuration snapshot"
            output = net_connect.send_command_timing(command)
            for line in output.split("\n"):
                if "system name" in line:
                    file_name=line.split()[2]+"("+i.split(".")[2]+"."+i.split(".")[3]+")"+".txt"
                    break
        
        open(file_name,"w").write(output)
        with open(file_name,"rb") as file:
            ftp.storbinary(f"STOR {file_name}", file)
        os.remove(file_name)

    ##If any unkown error is occured. Create and send log file.
    except Exception as e:
        log_name=i+"ErrorLog.txt"
        open(log_name,"w").write(str(e))
        with open(log_name,"rb") as file:
            ftp.storbinary(f"STOR {log_name}", file)
        os.remove(log_name)
        send_mail("Customer name",i,"Log Dosyasını incele !")           ####CHANGE####
ftp.quit()
