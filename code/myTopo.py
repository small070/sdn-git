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
            self.host.append(self.addHost('h'+str(i+1)))
        print('Adding Hosts...')
        print(self.host)


    def create_switch(self):
        # num_sw = number of switch

        # Add switch
        for i in range(0, self.num_sw, 1):
            self.switch.append(self.addSwitch('s'+str(i+1)))
        print('Adding Switches...')
        print(self.switch)

    def create_link(self):
        # Add lines
        # host to switch
        self.addLink(self.host[0], self.switch[0])

        self.addLink(self.host[1], self.switch[1])
        self.addLink(self.host[2], self.switch[1])

        self.addLink(self.host[3], self.switch[2])
        self.addLink(self.host[4], self.switch[2])
        self.addLink(self.host[5], self.switch[2])

        # self.addLink(self.host[6], self.switch[3])
        # self.addLink(self.host[7], self.switch[3])
        # self.addLink(self.host[8], self.switch[3])
        # self.addLink(self.host[9], self.switch[3])
        #
        # self.addLink(self.host[10], self.switch[4])
        # self.addLink(self.host[11], self.switch[4])
        # self.addLink(self.host[12], self.switch[4])
        # self.addLink(self.host[13], self.switch[4])
        # self.addLink(self.host[14], self.switch[4])
        #
        # self.addLink(self.host[15], self.switch[5])
        # self.addLink(self.host[16], self.switch[5])
        # self.addLink(self.host[17], self.switch[5])
        # self.addLink(self.host[18], self.switch[5])
        # self.addLink(self.host[19], self.switch[5])
        # self.addLink(self.host[20], self.switch[5])
        #
        # self.addLink(self.host[21], self.switch[6])
        # self.addLink(self.host[22], self.switch[6])
        # self.addLink(self.host[23], self.switch[6])
        # self.addLink(self.host[24], self.switch[6])
        # self.addLink(self.host[25], self.switch[6])
        # self.addLink(self.host[26], self.switch[6])
        # self.addLink(self.host[27], self.switch[6])

        # switch to switch
        self.addLink(self.switch[0], self.switch[1])
        self.addLink(self.switch[1], self.switch[2])
        # self.addLink(self.switch[2], self.switch[3])
        # self.addLink(self.switch[3], self.switch[4])
        # self.addLink(self.switch[4], self.switch[5])
        # self.addLink(self.switch[5], self.switch[6])

        print('Adding Links...')


def creater():
    test = MyTopo(6, 3)    # host & switch
    test.create_host()
    test.create_switch()
    test.create_link()
    net = Mininet(topo = test, link = TCLink, controller = None)
    net.addController('controller1', controller = RemoteController, ip = '127.0.0.1', port = 6633)
    net.start()
    CLI(net)

if __name__ == '__main__':
    creater()
