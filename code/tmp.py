# import pandas as pd
# import numpy as np
# import datetime
#
# #   顯示所有columns
# pd.set_option('display.max_columns', None)
# #   顯示所有rows
# pd.set_option('display.max_rows', None)
# #   設定colwidth為100，預設為50
# pd.set_option('max_colwidth',100)
#
#
# host_df = pd.DataFrame(columns=('switch_id', 'live_port', 'ip', 'datapath'))
#
# host_df = host_df.append({'switch_id':3, 'live_port':1, 'ip':'02:bf:d1:f6:5b:4c', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77048>'}, ignore_index=True)
# host_df = host_df.append({'switch_id':3, 'live_port':2, 'ip':'9e:32:72:76:5d:49', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77048>'}, ignore_index=True)
# host_df = host_df.append({'switch_id':7, 'live_port':1, 'ip':'10.0.0.5', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd13cfb6588>'}, ignore_index=True)
# host_df = host_df.append({'switch_id':4, 'live_port':1, 'ip':'36:5f:9c:f7:91:f5', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77160>'}, ignore_index=True)
#
# index = host_df[host_df.switch_id == 3].index.values
# # test = host_df[host_df.ip == '10.0.0.4'].index.values
# # if test.size is 0:
# #     test = 2
# #     print('greger')
# # dst_sid = host_df.at[int(test), 'switch_id']
#
# # print(host_df)
# # print(index)
# # print(dst_sid)
# # print(test)
# # print(type(test))
#
#
# # path = [1, 6, 5, 7]
# #
# # for i in range(len(path)-1):
# #     # if i < len(path)-1:
# #     print(path[i], path[i+1])
#
# tm = datetime.datetime.now()
# tm2 = datetime.datetime.now()
# tm3 = tm2-tm
# # print(tm3)
#
#
#
# import os
# # print(os.getcwd())
#
# import random
# dataset = pd.DataFrame()
#
# for i in range(0, 100):
#     # delta = datetime.timedelta(seconds=1.0, microseconds=random.randint(1,2000))
#     # tmp_packet_time = tm3 + delta
#     # dataset = dataset.append({'packet_time': tmp_packet_time}, ignore_index=True)
#     dataset = dataset.append({'packet_time': random.uniform(0.000001,0.002501)}, ignore_index=True)
#
# dataset.to_csv('time.csv')
#
# print(dataset)
# # import sklearn
# # print("Sklearn verion is {}".format(sklearn.__version__))
#
#
#
# sfd = float(6.472222222222222)
# sw_num = int(7)
#
# spi = sfd/sw_num
#
# print(spi)
# # sfd:  <class 'float'>
# # sw_num:  <class 'int'> 7

# import vaex
#
#
# df = vaex.open('123.csv')
#
# print(df)


import random
from scipy.special import comb, perm
import numpy as np

dict = np.array([])
switch = 30

edges = perm((switch - 2), 2)
delta = random.uniform(0.1, 0.9)
k = delta * edges


for i in range(0, switch, 1):
    if i != (switch - 1):
        print(i, i + 1)     # link S1 - Sn
    dict = np.append(dict, [i, 0])

print('\n')
print('k: ', k)
print('\n')

for key, value in dict:
    st_end_link = random.randint(0, 3)
    mid_link = random.randint(0, 2)
    # print(key, value)

    if k >= 0:
        if key == 0:
            k = k-st_end_link
            dict[key] = dict[key]+st_end_link
            print('first: ', k, value, st_end_link)

        elif key == (switch-1):
            k = k-mid_link
            dict[key] = dict[key] + st_end_link
            print('end: ', k, value)

        elif (value+mid_link) <= 2:
            k = k-st_end_link
            dict[key] = dict[key] + mid_link
            print('middle: ', k, value)

print('k: ', k)
print(dict.values())

# print('keys: ', len(dict.keys()))
# print('k: ', '%.3f' % k)
# print('dict: ', dict)

