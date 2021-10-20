from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

net = Mininet(link=TCLink, controller=None)
h1 = net.addHost('h1')
h2 = net.addHost('h2')

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

net.addLink(h1, s1)
net.addLink(h2, s2)

net.addLink(s1, s2)

c1 = net.addController('controller1', controller = RemoteController, ip = '127.0.0.1', port = 6653)
c2 = net.addController('controller2', controller = RemoteController, ip = '127.0.0.2', port = 6633)

# controller_list = []
# controller_list.append(net.addController('controller1', controller=RemoteController, ip='127.0.0.1', port=6653))
# controller_list.append(net.addController('controller2', controller=RemoteController, ip='127.0.0.2', port=6633))

s1.start([c1, c2])
s2.start([c1, c2])

net.build()
net.start()
CLI(net)
