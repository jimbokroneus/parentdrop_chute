#!/bin/bash

# Redirect HTTP traffic to the proxy.
iptables -A PREROUTING -t nat -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
echo " Redirect HTTP traffic to the proxy -> COMPLETE " > ~/progress.log

# Required for forwarding everything else (e.g. DNS).
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
echo " Forwarding everything else -> COMPLETE " > ~/progress.log

# Start the proxy.
service privoxy force-reload
service dansguardian start
echo " Start the proxy -> COMPLETE " > ~/progress.log

while true; do
    sleep 5
done
echo " Sleep -> COMPLETE " > ~/progress.log

# Make the python script executable in the background
chmod +x /usr/local/bin/parser/parser.py
echo " Make the python script executable in the background -> COMPLETE " > ~/progress.log

# Execute the code required for dansguardian application
echo " Execute the python code -> PENDING " > ~/progress.log
python /usr/local/bin/parser/parser.py &

# If execution reaches this point, the chute will stop running.
exit 0
