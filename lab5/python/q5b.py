import ipaddress
network5 = ipaddress.IPv4Network("128.119.40.64/26")
for net in network5.subnets(new_prefix=27):
    print("Subnet: {}".format(net))
    print("Mask: {}".format(net.netmask))
    print("Broadcast address: {}".format(net.broadcast_address))
    print("Number of addresses: {}".format(net.num_addresses))
