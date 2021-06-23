from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController
import numpy as np
import random
from scipy.special import comb, perm


class MyTopo(Topo):
    # simple Topo

    def __init__(self, h, s):
        # create topology

        # Initialize topology
        Topo.__init__(self)
        self.num_host = h
        self.num_sw = s
        self.host = []
        self.switch = []
        self.arr = []
        self.arr2 = []
        print('Totally Host and Switch')
        print(self.num_host, self.num_sw)

    def create_host(self):
        # h = number of host

        # Add host
        for i in range(0, self.num_host, 1):
            self.host.append(self.addHost('h' + str(i + 1)))
        print('Adding Hosts...')
        print(self.host)

    def create_switch(self):
        # num_sw = number of switch

        # Add switch
        for i in range(0, self.num_sw, 1):
            self.switch.append(self.addSwitch('s' + str(i + 1)))
            self.arr = np.append(self.arr, ['s' + str(i + 1), 0])
        self.arr2 = np.array(self.arr).reshape(len(self.switch), 2)

        print('Adding Switches...')
        # print(self.switch)
        # print(self.arr)
        # print(self.arr2[0][0])
        # print(self.arr2[0][1])

    def create_link(self):

        # Add lines
        # host to switch
        for i in range(0, len(self.switch), 1):
            self.addLink(self.host[i], self.switch[i])
        # self.addLink(self.host[0], self.switch[0])
        # self.addLink(self.host[1], self.switch[2])
        # self.addLink(self.host[2], self.switch[2])
        # self.addLink(self.host[3], self.switch[3])
        # self.addLink(self.host[4], self.switch[6])

        # switch to switch

        edges = perm((len(self.switch) - 2), 2)
        delta = random.uniform(0.1, 0.9)
        k = delta * edges

        print('edges, delta, k: ', edges, delta, k)

        # link s1-sn
        for i in range(0, len(self.switch), 1):
            if i != (len(self.switch) - 1):
                self.addLink(self.switch[i], self.switch[i + 1])
            self.arr2[i][1] = 2     # (s1~sn)'s link
            self.arr2[0][1] = 1     # (s1~sn)'s link
            self.arr2[-1][1] = 1     # (s1~sn)'s link

        # distribute k(links) to each sw, if k<=0, distribute finished
        if k >= 0:
            for i in self.arr2:
                st_end_link = random.randint(0, 3)
                mid_link = random.randint(0, 2)

                # print('str(i): ', str(i[0]))
                # print('self.arr2[0][0]: ', self.arr2[0][0])
                # print('self.arr2[-1][0]: ', self.arr2[-1][0])

                if str(i[0]) == str(self.arr2[0][0]):
                    for link in range(1, st_end_link+1, 1):
                        if int(i[1]) >= 4:
                            break
                        sw = random.randint(2, len(self.switch))
                        self.addLink(self.switch[0], self.switch[sw-1])
                        k = k - 1
                        i[1] = int(i[1]) + 1
                        self.arr2[(sw - 1)][1] = int(self.arr2[(sw - 1)][1]) + 1
                    print('first: ', self.arr2)

                elif (str(i[0]) != str(self.arr2[0][0])) & (str(i[0]) != str(self.arr2[-1][0])):

                    for link in range(1, mid_link+1, 1):
                        if int(i[1]) >= 4:
                            break
                        sw = random.randint(3, len(self.switch))
                        sw_num = ''.join([x for x in str(i[0]) if x.isdigit()])
                        print('sw, sw_num: ', sw, sw_num)
                        if (int(sw) == int(sw_num)) | (int(sw) == (int(sw_num)+1)) | (int(sw) == (int(sw_num)-1)):
                            break
                        self.addLink(self.switch[int(sw_num)-1], self.switch[sw - 1])
                        k = k - 1
                        i[1] = int(i[1]) + 1
                        self.arr2[(sw - 1)][1] = int(self.arr2[(sw - 1)][1]) + 1

                    print('middle: ', self.arr2)

                elif str(i[0]) == str(self.arr2[-1][0]):
                    k = k - st_end_link

                    for link in range(1, st_end_link+1, 1):
                        if int(i[1]) >= 4:
                            break
                        i[1] = int(i[1]) + 1
                    print('end: ', self.arr2)




        print('Adding Links...')

        # self.addLink(self.switch[0], self.switch[1])
        # self.addLink(self.switch[0], self.switch[2])
        # self.addLink(self.switch[0], self.switch[5])
        # self.addLink(self.switch[1], self.switch[2])
        # self.addLink(self.switch[1], self.switch[4])
        # self.addLink(self.switch[2], self.switch[3])
        # self.addLink(self.switch[2], self.switch[5])
        # self.addLink(self.switch[3], self.switch[4])
        # self.addLink(self.switch[3], self.switch[6])
        # self.addLink(self.switch[4], self.switch[5])

        print('Adding Links...')


#   topology gui

#       h1
#        \
#         \
#         s1----------s6
#         /|         / \
#        / |       /    \
#       s2-|-----/------s5
#        \ |    /       /
#         \|  /        /
#         s3----------s4----s7
#         / \          \     \
#        /   \          \     \
#       h2   h3          h4    h5


def creater():
    test = MyTopo(7, 7)  # host & switch
    test.create_host()
    test.create_switch()
    test.create_link()
    net = Mininet(topo=test, link=TCLink, controller=None)
    net.addController('controller1', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()
    CLI(net)


if __name__ == '__main__':
    creater()
