src_mac='10.0.0.1'
dst_mac='10.0.0.3'
pkt_arpsrc_ip='10.0.0.3'
pkt_arpdst_ip='10.0.0.3'
port='2'

print(('｜ARP Reply｜').center(50, '-'))
print(('｜src_mac: ' + src_mac + '|').center(50, '-'))
print(('｜dst_mac: ' + dst_mac + '|').center(50, '-'))
print(('｜pkt_arp.src_ip: ' + pkt_arpsrc_ip + '|').center(50, '-'))
print(('｜pkt_arp.dst_ip: ' + pkt_arpdst_ip + '|').center(50, '-'))
print(('｜port: ' + port + '|').center(50, '-'))
print(('||').center(50, '-'))