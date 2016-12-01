#!/bin/bash

# Redirect HTTP traffic to the proxy.
iptables -A PREROUTING -t nat -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080

# Required for forwarding everything else (e.g. DNS).
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Start the proxy.
service privoxy force-reload
service dansguardian start

while true; do
    sleep 5
done

# Execute the code required for dansguardian application
python /usr/local/bin/parser/parser.py

# If execution reaches this point, the chute will stop running.
exit 0
