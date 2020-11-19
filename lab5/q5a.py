import ipaddress

ip = ipaddress.IPv4Address("223.1.17.0")
my_ip = ipaddress.IPv4Address("174.3.61.7")
print("IP is global: ", ip.is_global)
print("My Ip is gobal: ", my_ip.is_global)
print("My Ip is private: ", my_ip.is_private)
print(ipaddress.IPv4Address("192.168.1.1").is_global)
