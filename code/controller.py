from ryu.base import app_manager
from ryu.topology import event
from ryu.topology.api import get_switch, get_link, get_host
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
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

        # req = ofp_parser.OFPPortStatsRequest(msg.datapath, 0, ofp.OFPP_ANY)
        req = ofp_parser.OFPPortDescStatsRequest(msg.datapath, 0, ofp.OFPP_ANY)
        msg.datapath.send_msg(req)

        # Append msg.datapath_id to df's 'switch_id' columns
        self.df = self.df.append({'switch_id': msg.datapath_id}, ignore_index=True)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser
        tmp = []

        # Append stat.port_no to df's 'live_port' columns
        for stat in ev.msg.body:
            tmp.append(stat.hw_addr)

            # Append ports(e.g. 1,2,3...) between switch and switch or host
            # Mate switch_id and ports to df
            if stat.port_no < ofproto_v1_3_parser.ofproto.OFPP_MAX:
                self.df = self.df.append({'live_port': stat.port_no}, ignore_index=True)
                self.df.at[len(self.df) - 1, 'switch_id'] = self.df.at[len(self.df) - 2, 'switch_id']

            # Append port(e.g. 4294967294) between switch and controller
            else:
                self.df.at[len(self.df) - 1, 'live_port'] = stat.port_no

        self.df['switch_id'] = self.df['switch_id'].astype('int')
        self.df['live_port'] = self.df['live_port'].astype('int')

        print('=============================================')
        print('|         port_stats_reply_handler          |')
        print('=============================================')
        # print('df長度', len(self.df))
        print('tmp內容', tmp)
        print('df內容', self.df)
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


