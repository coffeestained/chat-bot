#!/bin/bash

# List of allowed ports
ALLOWED_PORTS=(22 80 443 3000)

# Flush existing rules
iptables -F
iptables -X

# Set default policies to drop all traffic
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow traffic on the loopback interface
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections (important for SSH and existing connections)
iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# Allow traffic on allowed ports
for PORT in "${ALLOWED_PORTS[@]}"; do
    iptables -A INPUT -p tcp --dport $PORT -j ACCEPT
    iptables -A OUTPUT -p tcp --sport $PORT -j ACCEPT
done

# Allow DNS traffic (for apt package installations)
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --sport 53 -j ACCEPT

# Allow HTTP and HTTPS traffic for apt-get
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --sport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --sport 443 -j ACCEPT

# Allow MongoDB traffic only from localhost
iptables -A INPUT -p tcp -s 127.0.0.1 --dport 27017 -j ACCEPT
iptables -A OUTPUT -p tcp -d 127.0.0.1 --sport 27017 -j ACCEPT

# Save the iptables rules
iptables-save > /etc/iptables/rules.v4

echo "Firewall rules updated. Only the following ports are allowed: ${ALLOWED_PORTS[@]}"