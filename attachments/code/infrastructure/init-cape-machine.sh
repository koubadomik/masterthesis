#!/bin/bash

##################################
#          VARIABLES             #
##################################
#GENERAL
user="capecomp1"
home="/home/${user}"
iface="eno1"
ip4=$(/sbin/ip -o -4 addr list ${iface} | awk '{print $4}' | cut -d/ -f1)
cape_sh_script_name="cape2.sh"
qemu_sh_script_name="kvm-qemu.sh"
#FTP
ftp_user=""
ftp_password=""
ftp_server="X.X.X.X/config"
#SECURITY
pub_key="" # of master machine
ssh_port=903
sshd_config="/etc/ssh/sshd_config"
ports=(903 2042 8000) # ports which has to be open on each machine
#VIRTUALIZATION
vms_home="/data"
declare -a images_home=("win7" "win7_2" "win7_3" "win7_4")

declare -a chosen_images=("win7" "win72" "win73" "win74") #TESTED 6 machines and system was slow so I do not want analyses to be biased 
declare -a snapshot_names=("ezj" "frge" "erwr" "wefd")

#SANDBOX
declare -a config_files=("api.conf" "auxiliary.conf" "cuckoo.conf" "kvm.conf" "memory.conf" "processing.conf" "reporting.conf" "routing.conf" "vpn.conf" "web.conf")

##################################
#          FUNCTIONS             #
##################################

function helpfunc(){
    echo "Usage: $0 [--help] COMMANDS"
    echo "  --help  Help. Display this message and quit."
    echo "COMMANDS:"
    echo "  ssh - setup ssh on worker machine with master only access"
    echo "  ufw - install ufw and enable only listed ports"
    echo "  security - ssh, ufw and additional security tools"
    echo "  qemu - initialize qemu/kvm on worker machine"
    echo "  vms - copy listed images on worker machine and running snapshot"
    echo "  sandbox - init CAPEv2 sandbox on worker machine"
    echo "  update - update config from ftp server"
    echo "  collect - initialize collector script"
    echo "  empty - empty sandbox analyses and binaries"
    exit
}

function ssh_init(){
    apt install ssh -y
    if [ ! -f ${home}/.ssh/authorized_keys ]; then
        sudo -u ${user} touch authorized_keys
    fi
    grep -qxF "${pub_key}" ${home}/.ssh/authorized_keys || echo ${pub_key} >> ${home}/.ssh/authorized_keys
    sed -i "s/#\?\(Port\s*\).*$/\1 "${ssh_port}" /" "$sshd_config"
    sed -i "s/.*PermitRootLogin.*/PermitRootLogin no/g" "$sshd_config"
    sed -i "s/.*AddressFamily.*/AddressFamily inet/g" "$sshd_config"
    sed -i "s/#\?\(PubkeyAuthentication\s*\).*$/\1 yes/" "$sshd_config"
    sed -i "s/.*PermitEmptyPasswords.*/PermitEmptyPasswords no/g" "$sshd_config"
    sed -i "s/#\?\(PasswordAuthentication\s*\).*$/\1 no/" "$sshd_config"
    service sshd restart
}

function ufw_init(){
    apt install ufw -y   
    for port in "${ports[@]}"
    do
	    ufw allow $port 
    done
    ufw --force enable
    printf "\nFirewall listing:\n"
    ufw status numbered
}


function security() {
    #update
    apt update && apt upgrade -y
    #nowifi
    nmcli radio wifi off 
    #fail2ban
    apt install fail2ban -y
    cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
    service fail2ban restart
}

function qemu_init() {
    if [ ! -d "/opt/libguestfs/" ]; then #check that was not installed yet
        if [ ! -f $qemu_sh_script_name ]; then
	    wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/${qemu_sh_script_name} -O ${qemu_sh_script_name}
	fi
    	    chmod +x $qemu_sh_script_name
            echo "Installing QEMU"
            ./$qemu_sh_script_name all capecomp1
    fi
    #virsh has another default uri so we need to change it
    LINE="export LIBVIRT_DEFAULT_URI=\"qemu:///system\""
    FILE="${home}/.bashrc"
    sudo -u ${user} grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"
    echo "[+] PLEASE REBOOT and run qemu_post_init"
}



function vms_init(){
    if [ ! -d /data ]; then
    	mkdir /data
	mkdir /data/configs
    fi
    if [ ! -f /data/configs/netxml.xml ]; then
        wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/netxml.xml -O /data/configs/netxml.xml
      	virsh net-define ${vms_home}/configs/netxml.xml
	virsh net-start hostonly
    	virsh net-autostart hostonly
    fi
    for ((i=0;i<${#chosen_images[@]};++i)); do
        machine="${chosen_images[i]}"
        snap="${snapshot_names[i]}"
	
        if [ ! -d  /data/"${images_home[i]}" ];then
            mkdir /data/${images_home[i]}
            wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/${machine}.xml -O /data/configs/${machine}.xml
            wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/${machine}.qcow2 -O /data/${images_home[i]}/win7.qcow2
            virsh define ${vms_home}/configs/${machine}.xml
                virsh start ${machine}
                sleep 1m
                virsh snapshot-create-as --domain ${machine} --name ${snap}
                virsh shutdown ${machine} 
        fi
    done
}

function update_config(){
    for file in "${config_files[@]}";
    do
        rm /opt/CAPEv2/conf/${file}
	wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/${file} -O /opt/CAPEv2/conf/${file}
	chown cape:cape /opt/CAPEv2/conf/${file}
    done
    printf -v joined '%s,' "${chosen_images[@]}"
    sed -i "s/machines.*/machines="${joined%,}"/g" /opt/CAPEv2/conf/kvm.conf
    echo "[+] please reboot"
}


function sandbox_init(){
    if [ ! -f "./$cape_sh_script_name" ]; then
    	wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/${cape_sh_script_name} -O $cape_sh_script_name
        chmod +x $cape_sh_script_name
    fi
    sed -i "s/.*IFACE_IP.*/IFACE_IP=\"192.168.100.1\"/g" "$cape_sh_script_name"
    sed -i "s/.*NETWORK_IFACE.*/NETWORK_IFACE=virbr1/g" "$cape_sh_script_name"
    if [ ! -d "/opt/CAPEv2/" ]; then
        ./$cape_sh_script_name base cape
    fi
    update_config
    pip3 install flare-capa
    echo "[+] please reboot"
}

function collect(){
    if [ ! -f "/etc/collector/collect.py" ]; then
        mkdir /etc/collector
        wget --user ${ftp_user} --password ${ftp_password} ftp://${ftp_server}/collect.py -O /etc/collector/collect.py
    fi
    if ! crontab -l | grep -q '*/15 * * * * cd /etc/collector/'; then
        crontab -l | { cat; echo "*/15 * * * * cd /etc/collector/ && python3 /etc/collector/collect.py"; } | crontab -
    fi
}

function empty(){
    python3 /opt/CAPEv2/utils/cleaners.py --clean
}

##################################
#            RUN                 #
##################################

if [ "$EUID" -ne 0 ]; then
   echo 'This script must be run as root'
   exit 1
fi

COMMAND=$(echo "$1"|tr "[A-Z]" "[a-z]")

case $COMMAND in
    '--help')
        helpfunc
        exit 0;;
esac

case $COMMAND in
    'ssh')
        ssh_init
        ;;
    'ufw')
        ufw_init
        ;;
    'security')
        security 
        ufw_init
        ssh_init
        ;;
    'qemu')
        qemu_init
        ;;
    'vms')
        vms_init
        ;;
    'sandbox')
        sandbox_init
        ;;
    'update')
	    update_config
	    ;;	
    'collect')
        collect
        ;;
    'empty')
        empty
        ;;
    *)
        helpfunc
        ;;
esac