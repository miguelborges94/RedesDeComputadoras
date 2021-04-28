import ipaddress

NETWORKS = [
    '10.9.0.0/24',
    '',
]

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print('{!r}'.format(net))
    for i, ip in zip(range(3), net):
        print(ip)
    print()
