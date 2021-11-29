#!/bin/bash

#echo "Previous routing table:"
#netstat -rn -f inet

function log {
# not working in zsh#
#	echo -e "\e[92m$1\e[0m"
	echo $1
}
function err {
	echo -e "\e[31m$1\e[0m"
}

## F5 creates a default route to send everything via VPN!
## The goal is to remove the F5 default route, route only 10.0.0.0/8 to VPN and route 172.22.4.0/24 to vboxnet
## Update: Not working anymore the F5 agent immediately recreates the default route as soon at it gets deleted.

log "Removing default gateway - 1dc"
sudo route -n delete default
# default route gets recreated automatically, probably by the F5 client or the WSS agent :(
log "Restore gateway - default WIFI gateway"
sudo route -n add default 192.168.8.1

# 1DC IPs

# find utun1 IP
vpn_ip=$(ifconfig | grep utun2 -A 1 | grep inet | awk '{print $2}')

log "Add 1dc route for 10.0.0.0/8"
sudo route -n add 10.0.0.0/8 $vpn_ip

log "Restore VirtualBox routes"
sudo route -n delete 172.22.4.0
sudo route -n add 172.22.4.0/24 -interface vboxnet2

log "Current Routing table:"
netstat -rn -f inet
