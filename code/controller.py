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
from ryu.lib.packet import packet
import pandas as pd

class good_controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    lldp_topo = {}
    df = pd.DataFrame(columns=['switch_id', 'live_port', 'hw_addr'])

    def __init__(self, *args, **kwargs):
        super(good_controller, self).__init__(*args, **kwargs)

    @set_ev_cls(event.EventSwitchEnter)
    def get_switch(self, ev):

        # self.topo_raw_switches = get_switch(self, None)
        # self.topo_raw_links = get_link(self, None)
        # self.topo_raw_hosts = get_host(self, None)
        # # switches = [switch.dp.id for switch in self.topo_raw_switches]
        # # ports = [port.port_no for port in self.topo_raw_switches]
        # # print("switches: ", switches)
        # # print("ports: ", ports)
        #
        # print(" \t" + "Current Switches:")
        # for s in self.topo_raw_switches:
        #     print(" \t\t" + str(s))
        #     # print(" \t\t" + str(s.dp.id)) # print dpid
        # print(" \t" + "Current Links:")
        # for link in self.topo_raw_links:
        #     print(" \t\t" + str(link))
        # print(" \t" + "Current Hosts:")
        # for host in self.topo_raw_hosts:
        #     print(" \t\t" + str(host))

        switch_list = get_switch(self, None)
        switches = [switch.dp.id for switch in switch_list]
        links_list = get_link(self, None)
        links = [(link.src.dpid, link.dst.dpid, {'port': link.src.port_no}) for link in links_list]
        # print(links)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        # parser = datapath.ofproto_parser
        msg = ev.msg

        self.send_port_stats_request(msg)
        print('=============================================')
        print('|          switch_features_handler          |')
        print('=============================================')
        print('...')
        print('..')
        print('.')

    def send_port_stats_request(self, msg):
        ofp = msg.datapath.ofproto
        ofp_parser = msg.datapath.ofproto_parser

        req = ofp_parser.OFPPortDescStatsRequest(msg.datapath, 0, ofp.OFPP_ANY)
        msg.datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        tmp = []

        # LLDP packet to controller
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 0, match, actions)

        # Append stat.port_no to df's 'live_port' columns
        for stat in ev.msg.body:
            tmp.append(stat.hw_addr)

            # Append ports(e.g. 1,2,3...) between switch and switch or host
            if stat.port_no < ofproto_v1_3_parser.ofproto.OFPP_MAX:
                self.df = self.df.append({'switch_id':datapath.id, 'live_port': stat.port_no, 'hw_addr': stat.hw_addr}, ignore_index=True)
                self.send_lldp_packet(datapath, stat.port_no, stat.hw_addr)

            # Append port(e.g. 4294967294) between switch and controller
            else:

                # 'at' just use int or float
                # 'loc' can use int or float or string ......
                # But 'at' faster to 'loc'
                self.df = self.df.append({'switch_id': datapath.id, 'live_port': stat.port_no, 'hw_addr': stat.hw_addr},
                                         ignore_index=True)

        print('=============================================')
        print('|         port_stats_reply_handler          |')
        print('=============================================')
        # print('df??', len(self.df))
        # print('tmp??', tmp)
        # print('df??', self.df)
        print('...')
        print('..')
        print('.')

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

    def add_flow(self, datapath, priority, match, actions):
        ofp = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, command=ofp.OFPFC_ADD,
                               match=match, instructions=inst)
        datapath.send_msg(mod)

    def send_lldp_packet(self, datapath, live_port, hw_addr):
        ofp = datapath.ofproto

        # ????packet????ethernet type?lldp
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=ether_types.ETH_TYPE_LLDP,
                                           src=hw_addr, dst=lldp.LLDP_MAC_NEAREST_BRIDGE))

        # ????????????????str????ascii
        tlv_chassis_id = lldp.ChassisID(subtype=lldp.ChassisID.SUB_LOCALLY_ASSIGNED, chassis_id=str(datapath.id).encode('ascii'))
        tlv_live_port = lldp.PortID(subtype=lldp.PortID.SUB_LOCALLY_ASSIGNED, port_id=str(live_port).encode('ascii'))
        tlv_ttl = lldp.TTL(ttl=0)
        tlv_end = lldp.End()
        tlvs = (tlv_chassis_id, tlv_live_port, tlv_ttl, tlv_end)

        pkt.add_protocol(lldp.lldp(tlvs))
        pkt.serialize()

        # self.logger.info('packet_out %s', pkt)

        # ???????
        data = pkt.data
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(port=live_port)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofp.OFP_NO_BUFFER, in_port=ofp.OFPP_CONTROLLER,
                                  actions=actions, data=data)
        datapath.send_msg(out)

    # @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    # def packet_in_handler(self, ev):
    #     msg = ev.msg
    #     datapath = msg.datapath
    #     ofproto = datapath.ofproto
    #     parser = datapath.ofproto_parser
    #     pkt = packet.Packet(data=msg.data)
    #     dpid = datapath.id  # switch id which send the packetin
    #     in_port = msg.match['in_port']
    #     pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
    #     pkt_lldp = pkt.get_protocol(lldp.lldp)
    #     if not pkt_ethernet:
    #         return
    #     # print(pkt_lldp)
    #     if pkt_lldp:
    #         self.handle_lldp(dpid, in_port, pkt_lldp.tlvs[0].chassis_id, pkt_lldp.tlvs[1].port_id)
    #
    #
    # def switch_link(self, s_a, s_b):
    #     return s_a + '-->' + s_b
    #
    # def handle_lldp(self, dpid, in_port, lldp_dpid, lldp_in_port):
    #     switch_a = 'switch'+str(dpid) +', port'+str(in_port)
    #
    #     switch_b = 'switch'+lldp_dpid +', port'+lldp_in_port
    #     link = self.switch_link(switch_a, switch_b)  # Check the switch link is existed
    #     if not any(self.switch_link(switch_b, switch_a) == search for search in self.link):
    #         self.link.append(link)
    #         print(self.link)



    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto

        if msg.reason == ofp.OFPPR_ADD:
            print('Add')
            # reason = 'ADD'
        elif msg.reason == ofp.OFPPR_DELETE:
            print('Delete')
            # reason = 'DELETE'
        elif msg.reason == ofp.OFPPR_MODIFY:
            print('Modify')
            # reason = 'MODIFY'
        else:
            print('Unknown')
            # reason = 'unknown'

        # self.logger.debug('OFPPortStatus received: reason=%s desc=%s',
        #                   reason, msg.desc)