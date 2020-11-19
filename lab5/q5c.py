import ipaddress
network4 = ipaddress.IPv4Network("223.1.17.192/28")
counter = 1
for ip in network4.hosts():
    print("Network {}: {}".format(counter,ip))
    counter+=1
print("Total count: {}".format(counter))
