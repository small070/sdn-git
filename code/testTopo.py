#!/usr/bin/python

# a network topo with swithces arranged in a n*n grid, 
# with two host in the far top-left and  bottom-right corner of the topology, respectively. 


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import Link, TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
import os
from subprocess import Popen, PIPE
import time

class GridTopo(Topo):
    Swithes = []
    Hosts   = []

    def __init__(self, k):
        self.grid_width = k

        Topo.__init__(self)
    
    def create_init(self):
        self.create_topo()
        self.create_links()
        
    def create_topo(self):
        self.Hosts.append(self.addHost('h01',ip='10.0.0.1/24',defaultRoute='h01-eth0'))
        self.Hosts.append(self.addHost('h02',ip='10.0.2.1/24',defaultRoute='h02-eth0'))

        switch_num = 0
        for i in range(0, self.grid_width):
            for j in range(0, self.grid_width):
                if(switch_num<10):
                    self.Swithes.append(self.addSwitch('s100'+str(switch_num)))
                else:
                    self.Swithes.append(self.addSwitch('s10'+str(switch_num)))
                switch_num = switch_num + 1
    def create_links(self):
        for i in range(0, self.grid_width):
            for j in range(0, self.grid_width-1):
                # Horizontal Links
                self.addLink(self.Swithes[i*self.grid_width+j],self.Swithes[i*self.grid_width+j+1])
                # Vertical Links
                self.addLink(self.Swithes[i+self.grid_width*j],self.Swithes[i+self.grid_width*(j+1)])
        
        # Add links to hosts
        self.addLink(self.Hosts[0], self.Swithes[0], intfName1='h01-eth0')
        self.addLink(self.Hosts[0], self.Swithes[self.grid_width], intfName1='h01-eth1')
        self.addLink(self.Hosts[1], self.Swithes[self.grid_width*self.grid_width-1], intfName1='h02-eth0')
        self.addLink(self.Hosts[1], self.Swithes[self.grid_width*self.grid_width-1-self.grid_width], intfName1='h02-eth1')




def topology(width):
    Swithes = []
    Hosts   = []

    # Add controller hosts
    net = Mininet(link=TCLink, controller=RemoteController)
    print("Add controller...")
    net.addController('controller', controller=RemoteController, ip="127.0.0.1", port=6653)	

    Hosts.append(net.addHost('h01', ip='10.0.1.1/24'))
    Hosts.append(net.addHost('h02', ip='10.0.3.1/24'))
    
    # Create topology
    switch_num = 0
    for i in range(0, width):
        for j in range(0, width):
            if(switch_num<10):
                Swithes.append(net.addSwitch('s100'+str(switch_num)))
            else:
                Swithes.append(net.addSwitch('s10'+str(switch_num)))
            switch_num = switch_num + 1

    # Create grid links
    print("Add links")
    for i in range(0, width):
        for j in range(0, width-1):
            # Horizontal Links
            net.addLink(Swithes[i*width+j],Swithes[i*width+j+1])
            # Vertical Links
            net.addLink(Swithes[i+width*j],Swithes[i+width*(j+1)])

    # Add links to hosts
    print("Add links to hosts")
    # net.addLink(Hosts[0], Swithes[0])
    # net.addLink(Hosts[0], Swithes[width])
    # net.addLink(Hosts[1], Swithes[width*width-1])
    # net.addLink(Hosts[1], Swithes[width*width-1-width])
    Link(Hosts[0], Swithes[0], intfName1='h01-eth0')
    Link(Hosts[0], Swithes[width], intfName1='h01-eth1')
    Link(Hosts[1], Swithes[width*width-1], intfName1='h02-eth0')
    Link(Hosts[1], Swithes[width*width-1-width], intfName1='h02-eth1')

    Hosts[0].cmd("ifconfig h01-eth1 10.0.2.1 netmask 255.255.255.0")
    Hosts[1].cmd("ifconfig h02-eth1 10.0.4.1 netmask 255.255.255.0")


    
    net.build()
    net.start()
    print("Wait 20 secs...")
    time.sleep(20)
    CLI(net)
    net.stop()
    
def teststart(width):
    "Crerate network and run simple performance test"
    topo = GridTopo(width)
    print("Create topo...")
    topo.create_init() #create topology
    net = Mininet(topo=topo, link=TCLink, controller=None)
    print("Add controller...")
    net.addController('controller', controller=RemoteController, ip="192.168.100.101", port=6633)	

    host1 = net.get("h01")
    host2 = net.get("h02")

	#host1.setIP('h01-eth0', '10.0.0.1/24')
    #host1.setIP('h01-eth1', '10.0.1.1/24')
    #host2.setIP('h02-eth0', '10.0.2.1/24')
    #host2.setIP('h02-eth1', '10.0.3.1/24')

    host1.cmd("ifconfig h01-eth1 10.0.1.1 netmask 255.255.255.0")
    host2.cmd("ifconfig h02-eth1 10.0.3.1 netmask 255.255.255.0")


    # host1.setDefaultRoute('h01-eth0')
    # host2.setDefaultRoute('h02-eth0')

    net.start() #start Mininet
    print("Wait 20 secs...")
    time.sleep(20)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Set log level
    # you can use 'info', 'warning', 'critical', 'error', 'debug', 'output'
    setLogLevel('info')
    print("Starting topology...")
    topology(3)
    teststart(3)
