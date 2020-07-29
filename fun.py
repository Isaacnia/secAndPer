import subprocess
import os
err = []

os.system("clear")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def run(command):
    status, out = subprocess.getstatusoutput(command)
    if status == 0:
        okPrint("Adjustment enabled successfully")
    else:
        global err
        failedPrint("Error occurred:")
        err.append(command)
        print(out)
def runEx(command):
    os.system(command)

def infPrint(x):
    print(bcolors.OKBLUE +bcolors.BOLD+"\n[i] "+x+ bcolors.ENDC+ bcolors.ENDC)

def okPrint(x):
    print(bcolors.OKGREEN +bcolors.BOLD+"\n[Ok] "+x+ bcolors.ENDC+ bcolors.ENDC)

def failedPrint(x):
    print(bcolors.FAIL +bcolors.BOLD+"\n[Failed] "+x+ bcolors.ENDC+ bcolors.ENDC)

def performance():
    infPrint("you select performance package")

    infPrint("Stop Apache Server")
    run("sudo systemctl stop apache2")

    infPrint("Stop php5.6 module")
    run("sudo a2dismod php5.6")

    infPrint("Stop mpm_prefork module")
    run("sudo a2dismod mpm_prefork")

    infPrint("Install php5.6-fpm")
    run("sudo apt install php-fpm")

    infPrint("Install fcgi module")
    run("sudo apt install libapache2-mod-fcgid")

    infPrint("Enable php-fpm")
    run("sudo a2enconf php5.6-fpm")

    infPrint("Enable http proxy module")
    run("sudo a2enmod proxy")

    infPrint("Enable FastCGI proxy module")
    run("sudo a2enmod proxy_fcgi")

    infPrint("Check Syntax ")
    run("sudo apachectl configtest")

    infPrint("Restart apache service ")
    run("sudo systemctl restart apache2")

    global err
    if len(err) == 0 :
        infPrint("Active mpm_event succsesful")
       # print(bcolors.OKBLUE +bcolors.BOLD+"\n[note] Please Read all [i] message to handle any errors"+ bcolors.ENDC+ bcolors.ENDC)
    else :
        numberofError = 1
        failedPrint(str(len(err)) + " Erorr have occurred!  Please Read all [i] message to handle any errors")
        for e in err :
            failedPrint(str(numberofError)+": "+e)
            numberofError=numberofError+1
    

def security():

    infPrint("You select security package")
    infPrint("Get a Backup of Config files")
    run('sudo cp -p /etc/apache2/apache2.conf /etc/apache2/apache2.conf.bak.$(date +%F_%H%M%S)')
   
    infPrint("Install resolvconf ")
    run("sudo apt install resolvconf")
    infPrint("Get a Backup of dns config")
    run('sudo cp -p /etc/resolvconf/resolv.conf.d/head /etc/resolvconf/resolv.conf.d/head.bak.$(date +%F_%H%M%S)')
    infPrint("Set Shecan dns server ")
    run("echo 'nameserver 178.22.122.100' |\
    sudo tee -a  /etc/resolvconf/resolv.conf.d/head")
    run("echo 'nameserver 185.51.200.2' |\
    sudo tee -a  /etc/resolvconf/resolv.conf.d/head")
    run("echo 'automatic off' |\
    sudo tee -a  /etc/resolvconf/resolv.conf.d/head")
    run("sudo service resolvconf restart")
    
    infPrint("Add apache repo ")
    runEx("sudo add-apt-repository ppa:ondrej/apache2")
    
    infPrint("Update Apache webserver ")
    run("sudo apt install apache2")
    
    infPrint("Update MYSQL ")
    run("wget https://repo.mysql.com//mysql-apt-config_0.8.10-1_all.deb")
    runEx("sudo dpkg -i mysql-apt-config_0.8.10-1_all.deb")
    runEx("sudo apt-get update")
    runEx("sudo apt-get install mysql-server")

    infPrint("Current Version Mysql")
    run("apt policy mysql-server")

    infPrint("Install Apache security modules")
    run('sudo apt install libapache2-mod-security2')

    infPrint("Install Apach QOS modules")
    run("sudo apt-get install -y libapache2-mod-qos")
    
    infPrint("Enabling Security Module ")
    run('a2enmod security2')

    infPrint("Enabling Header Module")
    run("sudo a2enmod headers")
    
    infPrint("Enabling request timeout modules")
    run("sudo a2enmod reqtimeout")

    infPrint("Restart Apache Service ")
    run('sudo systemctl restart apache2')

    infPrint("Check Syntax ")
    run("sudo apachectl configtest")

    infPrint("Get a Backup of Security Moudle")
    run('sudo cp -p /etc/apache2/mods-available/security2.conf /etc/apache2/mods-available/security2.conf.bak.$(date +%F_%H%M%S)')

    infPrint("Set Head file security2")
    run('echo "SecDataDir /var/cache/modsecurity \n"|sudo tee -a /etc/apache2/mods-available/security2.conf')

    
    infPrint("Set HSTS Header")
    run("sudo echo 'Header set X-Frame-Options DENY' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf")
    
    infPrint("Set X-XSS-Protection Header")
    runEx('sudo echo '+"'"+'Header set X-XSS-Protection "1; mode=block"'+"'"+' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf')
    
    infPrint("Set HSTS Header")
    runEx('sudo echo '+"'"+'Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains" '+"'"+' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf')
    
    infPrint("Set X-Frame-Options Header")
    runEx('echo '+"'"+'Header set X-Frame-Options: "SAMEORIGIN"'+"'"+' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf')
    
    infPrint("Disabling AutoIndex Module")
    run("sudo a2dismod --force autoindex")

    infPrint("Change Server Name in Header")
    run('echo '+'ServerTokens Full '+' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf')
    run('echo '+'SecServerSignature "IIS" '+' | \
     sudo tee -a \
    /etc/apache2/mods-available/security2.conf')

    infPrint("Config RequestTimeOut ")
    run('echo "<IfModule mod_reqtimeout.c> \n RequestReadTimeout header=20-40,MinRate=500 body=20-40,MinRate=500 \n</IfModule>"|sudo tee -a /etc/apache2/mods-available/security2.conf')
   
    infPrint("Config QOS")
    run('echo "<IfModule mod_qos.c> \n QS_ClientEntries 100000 \n QS_SrvMaxConnPerIP 50 \n MaxClients 256 \n QS_SrvMaxConnClose 180 \n QS_SrvMinDataRate 150 1200 \n</IfModule>"|sudo tee -a /etc/apache2/mods-available/security2.conf')

    infPrint("Set Tail file security2")
    run('echo "IncludeOptional /etc/modsecurity/*.conf"|sudo tee -a /etc/apache2/mods-available/security2.conf')

    infPrint("Active Rule WAF")
    run("sed 's/DetectionOnly/On/g' /etc/modsecurity/modsecurity.conf-recommended | sudo tee /etc/modsecurity/modsecurity.conf 1> /dev/null")

    infPrint("Get a Backup to WAF config")
    run('sudo cp -p /etc/modsecurity/modsecurity.conf /etc/modsecurity/modsecurity.conf.bak.$(date +%F_%H%M%S)')

    #infPrint("Add rule to WAF")
    #run("echo '"+ 'SecRule RESPONSE_STATUS "@streq 408" "phase:5,t:none,nolog,pass,\n  setvar:ip.slow_dos_counter=+1, expirevar:ip.slow_dos_counter=60, id:'+"'"+'1234123456'+"'"+'" ' + "'" + " | sudo tee -a /etc/modsecurity/modsecurity.conf")
    #run("echo '"+ 'SecRule IP:SLOW_DOS_COUNTER "@gt 5" "phase:1,t:none,log,drop,\n msg:'+'Client Connection Dropped due to high number of slow DoS alerts'+', id:'+"'"+'1234123457'+"'"+'" ' + "'" + " | sudo tee -a /etc/modsecurity/modsecurity.conf")

    infPrint("Restart Apache Service ")
    run('sudo systemctl restart apache2')

    infPrint("Check Syntax ")
    run("sudo apachectl configtest")

    global err
    if len(err) == 0 :
        infPrint("Upgrade Apache Security Successful!")
       # print(bcolors.OKBLUE +bcolors.BOLD+"\n[note] Please Read all [i] message to handle any errors"+ bcolors.ENDC+ bcolors.ENDC)
    else :
        numberofError = 1
        failedPrint(str(len(err)) + " Erorr have occurred!  Please Read all [i] message to handle any errors")
        for e in err :
            failedPrint(str(numberofError)+": "+e)
            numberofError=numberofError+1
        

