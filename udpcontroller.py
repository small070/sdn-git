from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import *
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import *
from ryu.lib.packet import *
from ryu.lib import hub
from operator import attrgetter
from struct import *



class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        print("start...")
        
        #delete all entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                                                command=ofproto.OFPFC_DELETE, idle_timeout=0,
                                                hard_timeout=0, priority=2, instructions=inst, table_id=0)
        datapath.send_msg(mod)
        print("all delete...")
        
        #table miss entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print("table miss entry already add...")

        # SMF packet
        match = parser.OFPMatch(in_port=3,
                                ipv4_src="192.168.3.5",
                                eth_type=ether_types.ETH_TYPE_IP,
                                ip_proto=in_proto.IPPROTO_UDP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 1, match, actions)
        

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=0)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
        print("add flow entry success!")

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        print("------------------------")
        print("      packet in!!!      ")
        print("------------------------")
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        
        if arp_pkt:
            print(">> in arp")
            eth = pkt.get_protocols(ethernet.ethernet)[0]
            src = eth.src
            dst = eth.dst
            match = parser.OFPMatch(in_port=in_port,eth_type=ether_types.ETH_TYPE_ARP,eth_dst=dst)
            if (dst == 'ff:ff:ff:ff:ff:ff'):
                print("broadcast")
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                # self.add_flow(datapath, 2, match, actions, msg.buffer_id)
            else:
                print("else")
                if in_port == 2 and dst == '50:3e:aa:0f:a0:f1':
                    print("else and is 2 dst is n3iwf!")
                    actions = [parser.OFPActionOutput(1)]
                    # self.add_flow(datapath, 2, match, actions, msg.buffer_id)
                if in_port == 2 and dst == '50:3e:aa:0f:71:2e':
                    print("else and is 2 dst is smf!")
                    actions = [parser.OFPActionOutput(3)]
                    # self.add_flow(datapath, 2, match, actions, msg.buffer_id)
                if in_port == 1 or in_port == 3:
                    print("else and is 1 or 3!")
                    actions = [parser.OFPActionOutput(2)]
                    # self.add_flow(datapath, 2, match, actions, msg.buffer_id)
            #
            data = None
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                data = msg.data
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                in_port=in_port, actions=actions, data=data)
            print("...packet out...")
            datapath.send_msg(out)
            #
        elif ip_pkt:
            print(">> in ip_pkt")
            ip_src = ip_pkt.src
            ip_dst = ip_pkt.dst
            protocol = ip_pkt.proto
            print("ip_src = " + ip_src)
            print("ip_dst = " + ip_dst)

            if protocol == in_proto.IPPROTO_UDP:
                print(">> in UDP!!!")
                udp_pkt = pkt.protocols[2]
                # print(udp_pkt)

                if in_port == 2 and ip_src == "192.168.3.4" and ip_dst == "192.168.3.5":
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    actions = [parser.OFPActionOutput(3)]
                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                        in_port=in_port, actions=actions, data=data)
                    print("...packet out...")
                    datapath.send_msg(out)

                if in_port == 3 and ip_src == "192.168.3.5" and ip_dst == "192.168.3.4":
                    print("inport=3")
                    i=0
                    data = msg.data[58:]

                    while True:
                        if i==0:
                            i+=1
                        else:
                            i+=2
                        if data[i]==26:
                            print("in i=26")
                            print("data[i+ 3] = ", bytes([data[i+3]]))
                            print("data[i+ 4] = ", bytes([data[i+4]]))
                            print("data[i+ 5] = ", bytes([data[i+5]]))
                            print("data[i+ 6] = ", bytes([data[i+6]]))
                            print("data[i+ 7] = ", bytes([data[i+7]]))
                            UL_b = bytes([data[i+3]]) + bytes([data[i+4]]) + bytes([data[i+5]]) + bytes([data[i+6]]) + bytes([data[i+7]])
                            print("UL = ", UL_b)
                            UL = int.from_bytes(UL_b, byteorder='big')
                            print("UL = ", UL)
                            print("data[i+ 8] = ", bytes([data[i+8]]))
                            print("data[i+ 9] = ", bytes([data[i+9]]))
                            print("data[i+10] = ", bytes([data[i+10]]))
                            print("data[i+11] = ", bytes([data[i+11]]))
                            print("data[i+12] = ", bytes([data[i+12]]))
                            DL_b = bytes([data[i+8]]) + bytes([data[i+9]]) + bytes([data[i+10]]) + bytes([data[i+11]]) + bytes([data[i+12]])
                            print("DL = ", DL_b)
                            DL = int.from_bytes(DL_b, byteorder='big')
                            print("DL = ", DL)

                            bands = [parser.OFPMeterBandDrop(type_=ofproto.OFPMBT_DROP, len_=0, rate=UL, burst_size=0)]
                            req=parser.OFPMeterMod(datapath=datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_KBPS, meter_id=1, bands=bands)
                            datapath.send_msg(req)

                            bands = [parser.OFPMeterBandDrop(type_=ofproto.OFPMBT_DROP, len_=0, rate=3000, burst_size=0)]
                            req=parser.OFPMeterMod(datapath=datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_KBPS, meter_id=2, bands=bands)
                            datapath.send_msg(req)

                            bands = [parser.OFPMeterBandDrop(type_=ofproto.OFPMBT_DROP, len_=0, rate=5000, burst_size=0)]
                            req=parser.OFPMeterMod(datapath=datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_KBPS, meter_id=3, bands=bands)
                            datapath.send_msg(req)

                            bands = [parser.OFPMeterBandDrop(type_=ofproto.OFPMBT_DROP, len_=0, rate=10000, burst_size=0)]
                            req=parser.OFPMeterMod(datapath=datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_KBPS, meter_id=4, bands=bands)
                            datapath.send_msg(req)

                            bands = [parser.OFPMeterBandDrop(type_=ofproto.OFPMBT_DROP, len_=0, rate=30000, burst_size=0)]
                            req=parser.OFPMeterMod(datapath=datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_KBPS, meter_id=5, bands=bands)
                            datapath.send_msg(req)

                            data = None
                            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                                data = msg.data
                            actions = [parser.OFPActionOutput(2)]
                            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                                in_port=in_port, actions=actions, data=data)
                            print("...packet out...")
                            datapath.send_msg(out)
                            
                            break
                        else:
                            i+=2
                            i+=data[i]
                            
                    # ---------------udp_src=35784,udp_dst=2152
                    match = parser.OFPMatch(in_port=1,
                                            ipv4_src="192.168.3.3",
                                            ipv4_dst="192.168.3.4",
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol, 
                                            )
                    # , parser.OFPActionSetQueue(1)
                    actions = [parser.OFPActionOutput(2)]
                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] # , parser.OFPInstructionMeter(1,ofproto.OFPIT_METER)
                    mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                                                            command=ofproto.OFPFC_ADD, idle_timeout=0,
                                                            hard_timeout=0, priority=1, instructions=inst)
                    datapath.send_msg(mod)
                    # , udp_dst=35784    udp_src=2152

                    match = parser.OFPMatch(in_port=2,
                                            ipv4_src="192.168.3.4",
                                            ipv4_dst="192.168.3.3",
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol, 
                                            )
                    actions = [parser.OFPActionOutput(1)]
                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] # , parser.OFPInstructionMeter(1,ofproto.OFPIT_METER)
                    mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=1, 
                                            match=match, instructions=inst, table_id=0)
                    datapath.send_msg(mod)

                    # # --------------port = 22222----------
                    # match = parser.OFPMatch(in_port=1,
                    #                         ipv4_src="192.168.3.3",
                    #                         ipv4_dst="192.168.3.4",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=22222)
                    # # , parser.OFPActionSetQueue(1)
                    # actions = [parser.OFPActionOutput(2)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(2,ofproto.OFPIT_METER)]
                    # mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                    #                                         command=ofproto.OFPFC_ADD, idle_timeout=0,
                    #                                         hard_timeout=0, priority=1, instructions=inst)
                    # datapath.send_msg(mod)
                    # # , udp_dst=35784    udp_src=2152

                    # match = parser.OFPMatch(in_port=2,
                    #                         ipv4_src="192.168.3.4",
                    #                         ipv4_dst="192.168.3.3",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=22222)
                    # actions = [parser.OFPActionOutput(1)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(2,ofproto.OFPIT_METER)]
                    # mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=1, 
                    #                         match=match, instructions=inst, table_id=0)
                    # datapath.send_msg(mod)

                    # # --------------port = 33333----------
                    # match = parser.OFPMatch(in_port=1,
                    #                         ipv4_src="192.168.3.3",
                    #                         ipv4_dst="192.168.3.4",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst)
                    # # , parser.OFPActionSetQueue(1)
                    # actions = [parser.OFPActionOutput(2)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(3,ofproto.OFPIT_METER)]
                    # mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                    #                                         command=ofproto.OFPFC_ADD, idle_timeout=0,
                    #                                         hard_timeout=0, priority=1, instructions=inst)
                    # datapath.send_msg(mod)
                    # # , udp_dst=35784    udp_src=2152

                    # match = parser.OFPMatch(in_port=2,
                    #                         ipv4_src="192.168.3.4",
                    #                         ipv4_dst="192.168.3.3",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=33333)
                    # actions = [parser.OFPActionOutput(1)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(3,ofproto.OFPIT_METER)]
                    # mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=1, 
                    #                         match=match, instructions=inst, table_id=0)
                    # datapath.send_msg(mod)

                    # # --------------port = 44444----------
                    # match = parser.OFPMatch(in_port=1,
                    #                         ipv4_src="192.168.3.3",
                    #                         ipv4_dst="192.168.3.4",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=44444)
                    # # , parser.OFPActionSetQueue(1)
                    # actions = [parser.OFPActionOutput(2)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(4,ofproto.OFPIT_METER)]
                    # mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                    #                                         command=ofproto.OFPFC_ADD, idle_timeout=0,
                    #                                         hard_timeout=0, priority=1, instructions=inst)
                    # datapath.send_msg(mod)
                    # # , udp_dst=35784    udp_src=2152

                    # match = parser.OFPMatch(in_port=2,
                    #                         ipv4_src="192.168.3.4",
                    #                         ipv4_dst="192.168.3.3",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=44444)
                    # actions = [parser.OFPActionOutput(1)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(4,ofproto.OFPIT_METER)]
                    # mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=1, 
                    #                         match=match, instructions=inst, table_id=0)
                    # datapath.send_msg(mod)

                    # # --------------port = 55555----------
                    # match = parser.OFPMatch(in_port=1,
                    #                         ipv4_src="192.168.3.3",
                    #                         ipv4_dst="192.168.3.4",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=55555)
                    # # , parser.OFPActionSetQueue(1)
                    # actions = [parser.OFPActionOutput(2)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(5,ofproto.OFPIT_METER)]
                    # mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0, 
                    #                                         command=ofproto.OFPFC_ADD, idle_timeout=0,
                    #                                         hard_timeout=0, priority=1, instructions=inst)
                    # datapath.send_msg(mod)
                    # # , udp_dst=35784    udp_src=2152

                    # match = parser.OFPMatch(in_port=2,
                    #                         ipv4_src="192.168.3.4",
                    #                         ipv4_dst="192.168.3.3",
                    #                         eth_type=ether_types.ETH_TYPE_IP,
                    #                         ip_proto=protocol, 
                    #                         udp_dst=55555)
                    # actions = [parser.OFPActionOutput(1)]
                    # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(5,ofproto.OFPIT_METER)]
                    # mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=1, 
                    #                         match=match, instructions=inst, table_id=0)
                    # datapath.send_msg(mod)

                    # --------------------------------!!!

                    
            elif protocol == in_proto.IPPROTO_TCP:
                if ip_src == "192.168.3.3" and ip_dst == "192.168.1.65":
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    actions = [parser.OFPActionOutput(2)]
                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                            in_port=in_port, actions=actions, data=data)
                    print("...packet out...")
                    datapath.send_msg(out)
                elif ip_src == "192.168.1.65" and ip_dst == "192.168.3.3":
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    actions = [parser.OFPActionOutput(1)]
                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                            in_port=in_port, actions=actions, data=data)
                    print("...packet out...")
                    datapath.send_msg(out)
                    '''
                    match = parser.OFPMatch(in_port=3,
                                            ipv4_src=ip_src,
                                            ipv4_dst=ip_dst,
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol,
                                            udp_src=udp_pkt.src_port,
                                            udp_dst=udp_pkt.dst_port )
                    actions = [parser.OFPActionOutput(2)]
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id)

                    #
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                        in_port=in_port, actions=actions, data=data)
                    print("...packet out...")
                    datapath.send_msg(out)
                    #
                    
                    match = parser.OFPMatch(in_port=2,
                                            ipv4_src=ip_dst,
                                            ipv4_dst=ip_src,
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol,
                                            udp_src=udp_pkt.dst_port,
                                            udp_dst=udp_pkt.src_port )
                    actions = [parser.OFPActionOutput(3)]
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                    '''
                    '''
                    match = parser.OFPMatch(in_port=1,
                                            ipv4_src="192.168.3.3",
                                            ipv4_dst="192.168.3.4",
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol,
                                            udp_src=35784,
                                            udp_dst=2152)
                    actions = [parser.OFPActionOutput(2)]
                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(1,ofproto.OFPIT_METER)]
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id, inst)

                    match = parser.OFPMatch(in_port=2,
                                            ipv4_src="192.168.3.4",
                                            ipv4_dst="192.168.3.3",
                                            eth_type=ether_types.ETH_TYPE_IP,
                                            ip_proto=protocol,
                                            udp_src=2152,
                                            udp_dst=35784 )
                    actions = [parser.OFPActionOutput(1)]
                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions), parser.OFPInstructionMeter(1,ofproto.OFPIT_METER)]
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id, inst)
                    '''
        else:
            pass