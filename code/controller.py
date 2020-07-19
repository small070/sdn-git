from ryu.base import app_manager
from ryu.topology import event
from ryu.topology.api import get_switch, get_link, get_host
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import lldp
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
import time


#   顯示所有columns
pd.set_option('display.max_columns', None)
#   顯示所有rows
pd.set_option('display.max_rows', None)
#   設定colwidth為100，預設為50
pd.set_option('max_colwidth',100)


class good_controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    sw_dpid = dict()
    sw_port_to_sw_port = []
    live_port_index = 0

    df = pd.DataFrame(columns=['switch_id', 'live_port', 'hw_addr'])
    lldp_df = pd.DataFrame(columns=['request_sid', 'request_port', 'receive_sid', 'receive_port'])
    host_df = pd.DataFrame()
    path_df = pd.DataFrame()
    mac_to_port_df2 = pd.DataFrame()
    mac_to_port_df = dict()

    sw_num = 0

    def __init__(self, *args, **kwargs):
        super(good_controller, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.net = nx.DiGraph()


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        msg = ev.msg

        # Table-miss Flow Entry
        # Other packets Packet_Out controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # LLDP packets Packet_In controller
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 0, match, actions)

        self.send_port_stats_request(msg)
        # print('=============================================')
        # print('|          switch_features_handler          |')
        # print('=============================================')
        # print('...')
        # print('..')
        # print('.')



    def send_port_stats_request(self, msg):
        ofp = msg.datapath.ofproto
        ofp_parser = msg.datapath.ofproto_parser

        req = ofp_parser.OFPPortDescStatsRequest(msg.datapath, 0, ofp.OFPP_ANY)
        msg.datapath.send_msg(req)

    def add_flow(self, datapath, priority, match, actions):
        ofp = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, command=ofp.OFPFC_ADD,
                               match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        tmp = []

        print('ofp_event.EventOFPPortDescStatsReply')



        # Append stat.port_no to df's 'live_port' columns
        for stat in ev.msg.body:
            tmp.append(stat.hw_addr)

            # Append ports(e.g. 1,2,3...) between switch and switch or host
            if stat.port_no < ofproto_v1_3_parser.ofproto.OFPP_MAX:
                self.df = self.df.append({'datapath': datapath, 'switch_id': datapath.id, 'live_port': stat.port_no, 'hw_addr': stat.hw_addr}, ignore_index=True)
                self.send_lldp_packet(datapath, stat.port_no, stat.hw_addr)


            # Append port(e.g. 4294967294) between switch and controller
            else:

                # 'at' just use int or float
                # 'loc' can use int or float or string ......
                # But 'at' faster to 'loc'
                self.df = self.df.append({'datapath': datapath, 'switch_id': datapath.id, 'live_port': stat.port_no, 'hw_addr': stat.hw_addr},
                                         ignore_index=True)

            # Record switch_id to node
            if not self.net.has_node(datapath.id):
                # self.net.add_nodes_from(str(datapath.id))    # networkx   ['2', '1', '3']     for list
                self.net.add_node(datapath.id)    # networkx    [2, 1, 3]   for str
                # self.net.add_node(datapath.id, port=stat.port_no)    # networkx    [2, 1, 3]   for str
                # print('nodes: ', self.net.nodes)


        # print('=============================================')
        # print('|         port_stats_reply_handler          |')
        # print('=============================================')
        # # print('df長度', len(self.df))
        # # print('tmp內容', tmp)
        # print('df內容', self.df)
        # print('...')
        # print('..')
        # print('.')

        # -------------------------------------------------------------
        # Log Mode

        # from operator import attrgetter
        # body = ev.msg.body
        #
        # self.logger.info('datapath         port     '
        #                  'rx-pkts  rx-bytes rx-error '
        #                  'tx-pkts  tx-bytes tx-error')
        # self.logger.info('---------------- -------- '
        #                  '-------- -------- -------- '
        #                  '-------- -------- --------')
        # for stat2 in sorted(body, key=attrgetter('port_no')):
        #     self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
        #                      ev.msg.datapath.id, stat2.port_no,
        #                      stat2.rx_packets, stat2.rx_bytes, stat2.rx_errors,
        #                      stat2.tx_packets, stat2.tx_bytes, stat2.tx_errors)
        # -------------------------------------------------------------

    def send_lldp_packet(self, datapath, live_port, hw_addr):
        print('send_lldp_packet')
        # print('dpid: ', datapath.id)
        # print('port: ', live_port)
        ofp = datapath.ofproto

        # 產生一個packet然後加上ethernet type為lldp
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=ether_types.ETH_TYPE_LLDP,
                                           src=hw_addr, dst=lldp.LLDP_MAC_NEAREST_BRIDGE))
        tlv_chassis_id = lldp.ChassisID(subtype=lldp.ChassisID.SUB_LOCALLY_ASSIGNED, chassis_id=str(datapath.id).encode('ascii'))
        tlv_live_port = lldp.PortID(subtype=lldp.PortID.SUB_LOCALLY_ASSIGNED, port_id=str(live_port).encode('ascii'))
        tlv_ttl = lldp.TTL(ttl=0)
        tlv_end = lldp.End()
        tlvs = (tlv_chassis_id, tlv_live_port, tlv_ttl, tlv_end)
        pkt.add_protocol(lldp.lldp(tlvs))
        pkt.serialize()

        # self.logger.info('packet_out %s', pkt)

        # 製作完成後發送
        data = pkt.data
        parser = datapath.ofproto_parser
        # print('live_port: ', live_port)
        actions = [parser.OFPActionOutput(port=live_port)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofp.OFP_NO_BUFFER, in_port=ofp.OFPP_CONTROLLER,
                                  actions=actions, data=data)
        datapath.send_msg(out)

    def handle_lldp(self, datapath, port, pkt_ethernet, pkt_lldp, ev):

        # swp1我們紀錄封包是從哪個switch的哪個port發出
        # swp2我們紀錄封包是從哪個switch的哪個port收到
        # swp1 = ["s"+str(datapath.id), "port "+str(port)]
        # swp2 = ["s"+str(pkt_lldp.tlvs[0].chassis_id), "port "+str(pkt_lldp.tlvs[1].port_id)]
        # self.sw_port_to_sw_port.append([swp1, swp2])
        # print('LLDP結果: ', self.sw_port_to_sw_port)

        # print('pkt_lldp.tlvs[1]: ', pkt_lldp.tlvs[1])
        # print('\n pkt_lldp.tlvs[1] type: ', type(pkt_lldp.tlvs[1]))
        # print('\n pkt_lldp.tlvs[1].port_id type: ', type(pkt_lldp.tlvs[1].port_id))

        self.lldp_df = self.lldp_df.append({'request_sid': datapath.id,
                                            'request_port': port,
                                            'receive_sid': int(pkt_lldp.tlvs[0].chassis_id),
                                            'receive_port': int(pkt_lldp.tlvs[1].port_id)},
                                            ignore_index=True)

        # print('lldp_df: ', self.lldp_df)

        # Record request_sid, receive_sid, receive_port to edge
        # links = [(datapath.id, int(pkt_lldp.tlvs[0].chassis_id), {'port': int(pkt_lldp.tlvs[1].port_id)})]
        # self.net.add_edges_from(links)
        self.net.add_edge(datapath.id, int(pkt_lldp.tlvs[0].chassis_id))
        self.net.add_edge(int(pkt_lldp.tlvs[0].chassis_id), datapath.id)
        # print('net nodes: ', self.net.nodes)
        # print('net edges: ', self.net.edges)


        self.shortest_path(ev)

        # if self.net.has_node(1) & self.net.has_node(5):
        #     print(nx.has_path(self.net, 1, 5))
        # if self.net.has_node(1) & self.net.has_node(5):
            # nx.draw(self.net, with_labels=True)
            # plt.show()
            # print(nx.shortest_path(self.net, 1, 5))   # 單個最短路徑


        self.host_df = self.df.copy()
        self.host_df.rename(columns={"hw_addr": "ip"}, inplace=True)

        # print("lldp_df:\n", self.lldp_df)
        # print("host_df:\n", self.host_df)

        # df.drop(df[df.name=='a'].index,axis=0)
        arr = []
        for i in range(0, len(self.lldp_df), 1):
            request_index = self.df[(self.df['switch_id'] == self.lldp_df.at[i, 'request_sid']) & (
                        self.df['live_port'] == self.lldp_df.at[i, 'request_port'])].index.values
            receive_index = self.df[(self.df['switch_id'] == self.lldp_df.at[i, 'receive_sid']) & (
                        self.df['live_port'] == self.lldp_df.at[i, 'receive_port'])].index.values
            # controller_index = self.df[(self.df['live_port'] >= ofproto_v1_3_parser.ofproto.OFPP_MAX)].index

            arr.append(int(request_index))
            arr.append(int(receive_index))
        controller_index = self.df[(self.df['live_port'] >= 50)].index.values
        arr.extend(controller_index)
        arr2 = set(arr)
        for del_index in arr2:
            self.host_df.drop(index=del_index, inplace=True)

        self.host_df.reset_index(drop=True, inplace=True)
        #     print('request_index', request_index)
        #     print('receive_index', receive_index)
        #     print('controller_index', controller_index)
        # self.host_df.drop(index=arr2, inplace=True)
        #     self.host_df.drop(index=receive_index, inplace=True)
        # self.host_df.drop(index=controller_index, inplace=True)
        # self.host_df.reset_index(drop=True, inplace=True)
        # print("lldp_df:\n", self.lldp_df)



    # https: // blog.csdn.net / xuchenhuics / article / details / 44494249
    def shortest_path(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        self.path_df = pd.DataFrame(dict(nx.all_pairs_dijkstra_path(self.net)))  # 全部最短路徑
        # tmp = dict(nx.all_pairs_dijkstra_path(self.net))  # 全部最短路徑
        # print('tmp: \n', tmp)
        # print('path_df: \n', path_df)


        # 轉成上三角矩陣
        m, n = self.path_df.shape
        self.path_df[:] = np.where(np.arange(m)[:, None] >= np.arange(n), np.nan, self.path_df)

        # 轉成完整矩陣
        self.path_df = self.path_df.stack().reset_index()
        self.path_df.columns = ['start_sid', 'end_sid', 'links']
        # print('path_df: \n', self.path_df)



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match['in_port']
        pkt = packet.Packet(data=msg.data)

        eth = pkt.get_protocols(ethernet.ethernet)[0]
        # print('eth', eth)
        src_mac = eth.src
        dst_mac = eth.dst

        # self.logger.info("packet in %s %s %s %s", dpid, src_mac, dst_mac, in_port)
        #
        # self.mac_to_port_df.setdefault(dpid, {})
        # self.mac_to_port_df[dpid][src_mac] = in_port
        # self.mac_to_port_df2 = pd.DataFrame(self.mac_to_port_df)
        # self.mac_to_port_df2 = self.mac_to_port_df2.append({'dpid': dpid, 'src_mac': src_mac, 'in_port': in_port}, ignore_index=True)
        # print('mac_to_port: ', self.mac_to_port_df)

        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)

        if not pkt_ethernet:
            print('Not lldp packets')
            return

        pkt_lldp = pkt.get_protocol(lldp.lldp)      # pkt_test = pkt_ethernet.ethertype == 35020

        if pkt_lldp:
            self.sw_num = self.sw_num + 1
            print('Packet_in LLDP')
            self.handle_lldp(datapath, in_port, pkt_ethernet, pkt_lldp, ev)
            # nx.draw(self.net, with_labels=True)
            # plt.show()
            return

        # 功能還沒開發
        pkt_arp = pkt.get_protocol(arp.arp)
        if pkt_arp:
            print('Packet_in ARP')
            self.handle_arp(datapath, in_port, pkt_ethernet, pkt_arp, src_mac, dst_mac)
            return
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        if pkt_icmp:
            print('Packet_in ICMP')
            self.handle_icmp(datapath, in_port, pkt, pkt_ethernet, pkt_ipv4, pkt_icmp, src_mac, dst_mac)

        pkt_tcp = pkt.get_protocol(tcp.tcp)
        if pkt_tcp:
            print('Packet_in TCP')
            # self.handle_tcp(datapath, in_port, pkt, pkt_ethernet, pkt_ipv4, pkt_tcp, src_mac, dst_mac)

        # pkt_udp = pkt.get_protocol(udp.udp)
        # if pkt_udp:
        #     print('Packet_in UDP')

        # print('=============================================')
        # print('|            packet_in_handler              |')
        # print('=============================================')
        # # print('msg.match[in_port]: ', port)
        # # print('packet.Packet(data=msg.data)內容', pkt)
        # print('...')
        # print('..')
        # print('.')


    def handle_arp(self, datapath, port, pkt_ethernet, pkt_arp, src_mac, dst_mac):
        # self.host_df = self.df.copy()
        # self.host_df.rename(columns={"hw_addr": "ip"}, inplace=True)
        #
        #
        # # print("lldp_df:\n", self.lldp_df)
        # # print("host_df:\n", self.host_df)
        #
        # for i in range(0, len(self.lldp_df), 1):
        #     request_index = self.df[(self.df['switch_id'] == self.lldp_df.at[i, 'request_sid']) & (self.df['live_port'] == self.lldp_df.at[i, 'request_port'])].index
        #     receive_index = self.df[(self.df['switch_id'] == self.lldp_df.at[i, 'receive_sid']) & (self.df['live_port'] == self.lldp_df.at[i, 'receive_port'])].index
        #     controller_index = self.df[(self.df['live_port'] >= 50)].index
        #     # controller_index = self.df[(self.df['live_port'] >= ofproto_v1_3_parser.ofproto.OFPP_MAX)].index
        #     print('request_index', request_index)
        #     print('receive_index', receive_index)
        #     print('controller_index', controller_index)
        #     self.host_df.drop(index=request_index, inplace=True)
        #     self.host_df.drop(index=receive_index, inplace=True)
        # self.host_df.drop(index=controller_index, inplace=True)
        # self.host_df.reset_index(drop=True, inplace=True)
        # # print("host_df:\n", self.host_df)

        pkt = packet.Packet()
        parser = datapath.ofproto_parser



        if pkt_arp.opcode == arp.ARP_REQUEST:

            pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype, dst=pkt_ethernet.dst, src=pkt_ethernet.src))
            # pkt.add_protocol(arp.arp(opcode=arp.ARP_REQUEST, src_mac=self.hw_addr, src_ip=self.ip_addr, dst_mac=pkt_arp.dst_mac, dst_ip=pkt_arp.dst_ip))
            pkt.add_protocol(arp.arp(opcode=arp.ARP_REQUEST, src_mac=pkt_arp.src_mac, src_ip=pkt_arp.src_ip, dst_mac=pkt_arp.dst_mac, dst_ip=pkt_arp.dst_ip))


            for i in range(0, len(self.host_df), 1):
                # self.send_packet(datapath, self.host_df.at[i, 'live_port'], 0, pkt)
                self.send_packet(self.host_df.at[i, 'datapath'], self.host_df.at[i, 'live_port'], 0, pkt)
                # print('host的port: ', self.host_df.at[i, 'live_port'])
                # print('datapath id: ', self.host_df.at[i, 'datapath'].id)

                if (self.host_df.at[i, 'switch_id'] == datapath.id) & (self.host_df.at[i, 'live_port'] == port):
                    # print('ip: ', self.host_df.at[i, 'ip'])
                    self.host_df.at[i, 'ip'] = pkt_arp.src_ip

                print('=============================================')
                print('|               ARP Request                 |')
                print('=============================================')
                # print('src_mac: ', src_mac)
                # print('dst_mac: ', dst_mac)
                # print('pkt_arp.src_ip: ', pkt_arp.src_ip)
                # print('pkt_arp.dst_ip: ', pkt_arp.dst_ip)
                # print('output_port: ', self.host_df.at[i, 'live_port'])
                print('...')
                print('..')
                print('.')

            # return
        elif pkt_arp.opcode == arp.ARP_REPLY:
            for i in range(0, len(self.host_df), 1):
                # print(self.host_df.at[i, 'switch_id'])
                # print(datapath.id)
                # print(self.host_df.at[i, 'live_port'])
                # print(port)
                if (self.host_df.at[i, 'switch_id'] == datapath.id) & (self.host_df.at[i, 'live_port'] == port):
                    # print('ip: ', self.host_df.at[i, 'ip'])
                    self.host_df.at[i, 'ip'] = pkt_arp.src_ip

            print('=============================================')
            print('|                ARP Reply                  |')
            print('=============================================')
            print('src_mac: ', src_mac)
            print('dst_mac: ', dst_mac)
            print('pkt_arp.src_ip: ', pkt_arp.src_ip)
            print('pkt_arp.dst_ip: ', pkt_arp.dst_ip)
            print('...')
            print('..')
            print('.')

            print('host_df', self.host_df)
            pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype, dst=pkt_ethernet.dst, src=pkt_ethernet.src))
            pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY, src_mac=pkt_arp.src_mac, src_ip=pkt_arp.src_ip, dst_mac=pkt_arp.dst_mac, dst_ip=pkt_arp.dst_ip))

            arp_request_index = self.host_df[self.host_df.ip == pkt_arp.dst_ip].index.values
            arp_request_sid = self.host_df.at[int(arp_request_index), 'switch_id']
            arp_request_port = self.host_df.at[int(arp_request_index), 'live_port']
            arp_request_datapath = self.host_df.at[int(arp_request_index), 'datapath']
            self.send_packet(arp_request_datapath, arp_request_port, 0, pkt)
            print('arp_request_index: ', arp_request_index)
            print('arp_request_sid: ', arp_request_sid)

    def handle_icmp(self, datapath, port, pkt, pkt_ethernet, pkt_ipv4, pkt_icmp, src_mac, dst_mac):
        print('handle_icmp datapath_id: ', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        dst_index = self.host_df[self.host_df.ip == pkt_ipv4.dst].index.values
        # print('pkt_ipv4.dst: ', pkt_ipv4.dst)
        # print('dst_index: ', dst_index)
        while dst_index.size == 0:
            print('host_df_ip not match ipv4_dst_ip')
            return
        dst_sid = self.host_df.at[int(dst_index), 'switch_id']
        dst_sid_port = self.host_df.at[int(dst_index), 'live_port']


        if pkt_icmp.type == icmp.ICMP_ECHO_REQUEST:
            dst_dp = self.host_df.at[int(dst_index), 'datapath']
            self.send_packet(dst_dp, dst_sid_port, 0, pkt)

            print('=============================================')
            print('|              ICMP Request                 |')
            print('=============================================')
            print('send ICMP Request packets to switch= ', dst_dp.id, ' port= ', dst_sid_port)
            # print('datapath.id: ', datapath.id)
            # print('src_mac: ', src_mac)
            # print('dst_mac: ', dst_mac)
            # # print('pkt_ipv4: ', pkt_ipv4)
            # print('pkt_ipv4.src_ip', pkt_ipv4.src)
            # print('pkt_ipv4.dst_ip', pkt_ipv4.dst)
            # print('port: ', port)
            # print('host_df switch_id: ', dst_sid)
            # print('host_df live_port: ', dst_sid_port)
            # print('path: ', path)
            # print('path length: ', len(path))
            print('...')
            print('..')
            print('.')

        elif pkt_icmp.type == icmp.ICMP_ECHO_REPLY:
            print('=============================================')
            print('|               ICMP Reply                  |')
            print('=============================================')
            print('datapath.id: ', datapath.id)
            print('src_mac: ', src_mac)
            print('dst_mac: ', dst_mac)
            # print('pkt_ipv4: ', pkt_ipv4)
            print('pkt_ipv4.src_ip', pkt_ipv4.src)
            print('pkt_ipv4.dst_ip', pkt_ipv4.dst)
            print('port: ', port)
            print('dst_sid: ', dst_sid) # host_df switch_id
            print('dst_sid_port: ', dst_sid_port) # host_df live_port
            # print('path: ', path)
            # print('path length: ', len(path))
            print('...')
            print('..')
            print('.')



            dst_dp = self.host_df.at[int(dst_index), 'datapath']
            print('dst_dp.id: ', dst_dp.id)
            print('dst_sid_port:', dst_sid_port)
            self.send_packet(dst_dp, dst_sid_port, 0, pkt)

            links_index = self.path_df[
                ((self.path_df.start_sid == int(datapath.id)) & (self.path_df.end_sid == int(dst_sid)))].index.values
            print('first links_index: ', links_index)
            if links_index.size == 0:
                links_index = self.path_df[((self.path_df.start_sid == int(dst_sid)) & (
                        self.path_df.end_sid == int(datapath.id)))].index.values
                print('second links_index: ', links_index)
            while links_index.size == 0:
                print('cant not find shortest path in path_df')
                return
            path = self.path_df.at[int(links_index), 'links']


            # 3 up sw's link
            for i in range(len(path) - 1):
                if datapath.id == path[0]:
                    print('reverse path')
                    path.reverse()

                    # link_index = self.lldp_df[((self.lldp_df.request_sid == int(path[i])) & (self.lldp_df.receive_sid == int(path[i+1])))].index.values
                    # request_port = self.lldp_df.at[int(link_index), 'request_port']
                    # receive_port = self.lldp_df.at[int(link_index), 'receive_port']
                    # print('link_index: ', link_index)
                    # print('request sid & port: ', path[i], '&', request_port)
                    # print('receive sid & port: ', path[i+1], '&', receive_port)

                if datapath.id == path[-1]:
                    print('normal path')
                    link_index = self.lldp_df[((self.lldp_df.request_sid == int(path[-i - 1])) & (
                                self.lldp_df.receive_sid == int(path[-i - 2])))].index.values
                    request_port = self.lldp_df.at[int(link_index), 'request_port']
                    receive_port = self.lldp_df.at[int(link_index), 'receive_port']
                    # print('link_index: ', link_index)
                    # print('request sid & port: ', path[-i-1], '&', request_port)
                    # print('receive sid & port: ', path[-i-2], '&', receive_port)

                    # handle first sw
                    if i == 0:
                        test_index = self.df[
                            (self.df.switch_id == int(datapath.id)) & (self.df.live_port == int(port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=request_port)
                        actions = [parser.OFPActionOutput(port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[
                            (self.df.switch_id == int(datapath.id)) & (self.df.live_port == int(port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        tmp_receive_port = receive_port

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('start sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('test_datapath.id: ', test_datapath.id)
                        print('in_port: ', port)
                        print('out_port: ', request_port)
                        print('...')
                        print('..')
                        print('.')

                    # handle mid sw
                    elif i != 0:
                        test_index = self.df[(self.df.switch_id == int(path[-i - 1])) & (
                                    self.df.live_port == int(request_port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=tmp_receive_port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[(self.df.switch_id == int(path[-i - 1])) & (
                                    self.df.live_port == int(request_port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=request_port)
                        actions = [parser.OFPActionOutput(tmp_receive_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('mid sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('tmp_port: ', tmp_receive_port)
                        tmp_receive_port = receive_port

                    # handle end sw
                    elif (i == len(path) - 2):
                        test_index = self.df[(self.df.switch_id == int(path[-i - 2])) & (
                                    self.df.live_port == int(tmp_receive_port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=request_port)
                        actions = [parser.OFPActionOutput(tmp_receive_port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[(self.df.switch_id == int(path[-i - 2])) & (
                                    self.df.live_port == int(tmp_receive_port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=tmp_receive_port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('end sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('tmp_port: ', tmp_receive_port)



        # print('df: ', self.df)
        # print('host_df: ', self.host_df)
        print('path_df: ', self.path_df)
        # print('lldp_df: ', self.lldp_df)
        # print('shortest path: ', nx.dijkstra_path(self.net, 1, 3))

    def handle_tcp(self, datapath, port, pkt, pkt_ethernet, pkt_ipv4, pkt_tcp, src_mac, dst_mac):
        print('handle_tcp datapath_id: ', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        dst_index = self.host_df[self.host_df.ip == pkt_ipv4.dst].index.values
        # print('pkt_ipv4.dst: ', pkt_ipv4.dst)
        # print('dst_index: ', dst_index)
        while dst_index.size == 0:
            print('host_df_ip not match ipv4_dst_ip')
            return
        dst_sid = self.host_df.at[int(dst_index), 'switch_id']
        dst_sid_port = self.host_df.at[int(dst_index), 'live_port']


        if pkt_tcp.type == icmp.ICMP_ECHO_REQUEST:
            dst_dp = self.host_df.at[int(dst_index), 'datapath']
            self.send_packet(dst_dp, dst_sid_port, 0, pkt)

            print('=============================================')
            print('|              ICMP Request                 |')
            print('=============================================')
            print('send ICMP Request packets to switch= ', dst_dp.id, ' port= ', dst_sid_port)
            # print('datapath.id: ', datapath.id)
            # print('src_mac: ', src_mac)
            # print('dst_mac: ', dst_mac)
            # # print('pkt_ipv4: ', pkt_ipv4)
            # print('pkt_ipv4.src_ip', pkt_ipv4.src)
            # print('pkt_ipv4.dst_ip', pkt_ipv4.dst)
            # print('port: ', port)
            # print('host_df switch_id: ', dst_sid)
            # print('host_df live_port: ', dst_sid_port)
            # print('path: ', path)
            # print('path length: ', len(path))
            print('...')
            print('..')
            print('.')

        elif pkt_tcp.type == icmp.ICMP_ECHO_REPLY:
            print('=============================================')
            print('|               ICMP Reply                  |')
            print('=============================================')
            print('datapath.id: ', datapath.id)
            print('src_mac: ', src_mac)
            print('dst_mac: ', dst_mac)
            # print('pkt_ipv4: ', pkt_ipv4)
            print('pkt_ipv4.src_ip', pkt_ipv4.src)
            print('pkt_ipv4.dst_ip', pkt_ipv4.dst)
            print('port: ', port)
            print('dst_sid: ', dst_sid) # host_df switch_id
            print('dst_sid_port: ', dst_sid_port) # host_df live_port
            # print('path: ', path)
            # print('path length: ', len(path))
            print('...')
            print('..')
            print('.')



            dst_dp = self.host_df.at[int(dst_index), 'datapath']
            print('dst_dp.id: ', dst_dp.id)
            print('dst_sid_port:', dst_sid_port)
            self.send_packet(dst_dp, dst_sid_port, 0, pkt)

            links_index = self.path_df[
                ((self.path_df.start_sid == int(datapath.id)) & (self.path_df.end_sid == int(dst_sid)))].index.values
            print('first links_index: ', links_index)
            if links_index.size == 0:
                links_index = self.path_df[((self.path_df.start_sid == int(dst_sid)) & (
                        self.path_df.end_sid == int(datapath.id)))].index.values
                print('second links_index: ', links_index)
            while links_index.size == 0:
                print('cant not find shortest path in path_df')
                return
            path = self.path_df.at[int(links_index), 'links']

            for i in range(len(path) - 1):
                if datapath.id == path[0]:
                    print('reverse path')
                    path.reverse()

                    # link_index = self.lldp_df[((self.lldp_df.request_sid == int(path[i])) & (self.lldp_df.receive_sid == int(path[i+1])))].index.values
                    # request_port = self.lldp_df.at[int(link_index), 'request_port']
                    # receive_port = self.lldp_df.at[int(link_index), 'receive_port']
                    # print('link_index: ', link_index)
                    # print('request sid & port: ', path[i], '&', request_port)
                    # print('receive sid & port: ', path[i+1], '&', receive_port)

                if datapath.id == path[-1]:
                    print('normal path')
                    link_index = self.lldp_df[((self.lldp_df.request_sid == int(path[-i - 1])) & (
                                self.lldp_df.receive_sid == int(path[-i - 2])))].index.values
                    request_port = self.lldp_df.at[int(link_index), 'request_port']
                    receive_port = self.lldp_df.at[int(link_index), 'receive_port']
                    # print('link_index: ', link_index)
                    # print('request sid & port: ', path[-i-1], '&', request_port)
                    # print('receive sid & port: ', path[-i-2], '&', receive_port)

                    # handle first sw
                    if i == 0:
                        test_index = self.df[
                            (self.df.switch_id == int(datapath.id)) & (self.df.live_port == int(port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=request_port)
                        actions = [parser.OFPActionOutput(port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[
                            (self.df.switch_id == int(datapath.id)) & (self.df.live_port == int(port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        tmp_receive_port = receive_port

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('start sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('test_datapath.id: ', test_datapath.id)
                        print('in_port: ', port)
                        print('out_port: ', request_port)
                        print('...')
                        print('..')
                        print('.')

                    # handle mid sw
                    elif i != 0:
                        test_index = self.df[(self.df.switch_id == int(path[-i - 1])) & (
                                    self.df.live_port == int(request_port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=tmp_receive_port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[(self.df.switch_id == int(path[-i - 1])) & (
                                    self.df.live_port == int(request_port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=request_port)
                        actions = [parser.OFPActionOutput(tmp_receive_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('mid sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('tmp_port: ', tmp_receive_port)
                        tmp_receive_port = receive_port

                    # handle end sw
                    elif (i == len(path) - 2):
                        test_index = self.df[(self.df.switch_id == int(path[-i - 2])) & (
                                    self.df.live_port == int(tmp_receive_port))].index.values
                        test_datapath = self.df.at[int(test_index), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.dst,
                                                ipv4_dst=pkt_ipv4.src, in_port=request_port)
                        actions = [parser.OFPActionOutput(tmp_receive_port)]
                        self.add_flow(test_datapath, 1, match, actions)

                        test_index1 = self.df[(self.df.switch_id == int(path[-i - 2])) & (
                                    self.df.live_port == int(tmp_receive_port))].index.values
                        test_datapath1 = self.df.at[int(test_index1), 'datapath']
                        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=pkt_ipv4.src,
                                                ipv4_dst=pkt_ipv4.dst, in_port=tmp_receive_port)
                        actions = [parser.OFPActionOutput(request_port)]
                        self.add_flow(test_datapath1, 1, match, actions)

                        print('=============================================')
                        print('|             ADD Flow Entry                |')
                        print('=============================================')
                        print('end sw')
                        print('request sid & port: ', path[-i - 1], '&', request_port)
                        print('receive sid & port: ', path[-i - 2], '&', receive_port)
                        print('tmp_port: ', tmp_receive_port)



        # print('df: ', self.df)
        # print('host_df: ', self.host_df)
        print('path_df: ', self.path_df)
        # print('lldp_df: ', self.lldp_df)
        # print('shortest path: ', nx.dijkstra_path(self.net, 1, 3))

    def send_packet(self, datapath, output_port, input_port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        if input_port == 0:
            input_port = ofproto.OFPP_CONTROLLER
        pkt.serialize()
        data = pkt.data
        actions = [parser.OFPActionOutput(port=output_port)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=input_port, actions=actions, data=data)
        datapath.send_msg(out)
        print('send packet')


    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto

        # if msg.reason == ofp.OFPPR_ADD:
        #     print('Add')
        #     # reason = 'ADD'
        # elif msg.reason == ofp.OFPPR_DELETE:
        #     print('Delete')
        #     # reason = 'DELETE'
        # elif msg.reason == ofp.OFPPR_MODIFY:
        #     print('Modify')
        #     # reason = 'MODIFY'
        # else:
        #     print('Unknown')
        #     # reason = 'unknown'

        # self.logger.debug('OFPPortStatus received: reason=%s desc=%s',
        #                   reason, msg.desc)