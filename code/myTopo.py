from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

class MyTopo(Topo):
    # simple Topo
    host = []
    switch = []

    def __init__(self, h, s):
        # create topology

        # Initialize topology
        Topo.__init__(self)
        self.num_host = h
        self.num_sw = s
        print('Totally Host and Switch')
        print(self.num_host, self.num_sw)

    def create_host(self):
        # h = number of host

        # Add host
        for i in range(0, self.num_host, 1):
            self.host.append(self.addHost('h'+str(i)))
        print('Adding Hosts...')
        print(self.host)


    def create_switch(self):
        # num_sw = number of switch

        # Add switch
        for i in range(0, self.num_sw, 1):
            self.switch.append(self.addSwitch('s'+str(i)))
        print('Adding Switches...')
        print(self.switch)

    def create_link(self):

        # Add lines
        # host to switch

        self.addLink(self.host[0], self.switch[0])
        self.addLink(self.host[1], self.switch[2])
        self.addLink(self.host[2], self.switch[2])
        self.addLink(self.host[3], self.switch[4])
        self.addLink(self.host[4], self.switch[6])

        # switch to switch

        self.addLink(self.switch[0], self.switch[1])
        self.addLink(self.switch[0], self.switch[2])
        self.addLink(self.switch[0], self.switch[4])
        self.addLink(self.switch[0], self.switch[7])
        self.addLink(self.switch[1], self.switch[6])
        self.addLink(self.switch[2], self.switch[3])
        self.addLink(self.switch[3], self.switch[4])
        self.addLink(self.switch[4], self.switch[5])
        self.addLink(self.switch[5], self.switch[6])
        self.addLink(self.switch[6], self.switch[7])

        print('Adding Links...')

#   topology gui

#                h0
#                |
#                s0
#          /            \
#         /              \
#       s1                s7
#      /                    \
#     /                      \
#    s2                      s6 --------h4
#    |\                      /
#    | \                    /
#    |  s3                s5
#    |    \              /
#    |     \            /
#    |      \          /
#    |           s4
#    |\             ＼
#    | \               ＼
#    |  \                 ＼
#   h1   h2                 h3


def creater():
    test = MyTopo(5, 8)     # host & switch
    test.create_host()
    test.create_switch()
    test.create_link()
    net = Mininet(topo = test, link = TCLink, controller = None)
    net.addController('controller1', controller = RemoteController, ip = '127.0.0.1', port = 6653)
    net.start()
    CLI(net)

if __name__ == '__main__':
    creater()
