from ryu.base import app_manager
from ryu.topology import event
from ryu.topology.api import get_switch, get_link, get_host
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
import time
import pandas as pd

class good_controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    sw_dpid = dict()
    live_port_index = 0
    df = pd.DataFrame(columns=['switch_id', 'live_port'])

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
        # method 1 of send port_no
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        # parser = datapath.ofproto_parser
        #
        self.sw_dpid.setdefault('switch dpid', [])
        self.sw_dpid['switch dpid'].append(ev.msg.datapath_id)
        # req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        # datapath.send_msg(req)
        print('=============================================')
        print('|          switch_features_handler          |')
        print('=============================================')
        print("sw_dpid: ", self.sw_dpid)
        print('...')
        print('..')
        print('.')

    # method 2 of send port_no
        msg = ev.msg
    #     datapath = msg.datapath

        self.send_port_stats_request(msg)
    def send_port_stats_request(self, msg):
        ofp = msg.datapath.ofproto
        ofp_parser = msg.datapath.ofproto_parser

        req = ofp_parser.OFPPortStatsRequest(msg.datapath, 0, ofp.OFPP_ANY)
        msg.datapath.send_msg(req)
        print('dpid: ', msg.datapath_id)
        # self.df.append(msg.datapath_id, ignore_index='live_port')
        self.df = self.df.append({'switch_id': msg.datapath_id, 'live_port': -1}, ignore_index=True)
        self.live_port_index = self.live_port_index + 1
        print('df: ', self.df)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = ev.msg.datapath
        ofproto_parser = datapath.ofproto_parser
        arr = []
        live_port_index = 0

        for stat in ev.msg.body:
            arr.append(stat.port_no)

        self.df.loc[self.live_port_index-1, 'live_port'] = arr

        # self.df.loc['live_port'] = arr
        print('=============================================')
        print('|         port_stats_reply_handler          |')
        print('=============================================')
        print("arr: ", arr)
        print("df: ", self.df)
        print('...')
        print('..')
        print('.')
