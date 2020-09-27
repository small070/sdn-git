import pandas as pd
import numpy as np
import datetime

#   顯示所有columns
pd.set_option('display.max_columns', None)
#   顯示所有rows
pd.set_option('display.max_rows', None)
#   設定colwidth為100，預設為50
pd.set_option('max_colwidth',100)


host_df = pd.DataFrame(columns=('switch_id', 'live_port', 'ip', 'datapath'))

host_df = host_df.append({'switch_id':3, 'live_port':1, 'ip':'02:bf:d1:f6:5b:4c', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77048>'}, ignore_index=True)
host_df = host_df.append({'switch_id':3, 'live_port':2, 'ip':'9e:32:72:76:5d:49', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77048>'}, ignore_index=True)
host_df = host_df.append({'switch_id':7, 'live_port':1, 'ip':'10.0.0.5', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd13cfb6588>'}, ignore_index=True)
host_df = host_df.append({'switch_id':4, 'live_port':1, 'ip':'36:5f:9c:f7:91:f5', 'datapath':'<ryu.controller.controller.Datapath object at 0x7fd165b77160>'}, ignore_index=True)

index = host_df[host_df.switch_id == 3].index.values
# test = host_df[host_df.ip == '10.0.0.4'].index.values
# if test.size is 0:
#     test = 2
#     print('greger')
# dst_sid = host_df.at[int(test), 'switch_id']

# print(host_df)
# print(index)
# print(dst_sid)
# print(test)
# print(type(test))


# path = [1, 6, 5, 7]
#
# for i in range(len(path)-1):
#     # if i < len(path)-1:
#     print(path[i], path[i+1])

tm = datetime.datetime.now()
tm2 = datetime.datetime.now()
tm3 = tm2-tm
# print(tm3)



import os
# print(os.getcwd())

import random
dataset = pd.DataFrame()

for i in range(0, 100):
    # delta = datetime.timedelta(seconds=1.0, microseconds=random.randint(1,2000))
    # tmp_packet_time = tm3 + delta
    # dataset = dataset.append({'packet_time': tmp_packet_time}, ignore_index=True)
    dataset = dataset.append({'packet_time': random.uniform(0.000001,0.002501)}, ignore_index=True)

dataset.to_csv('time.csv')

print(dataset)
# import sklearn
# print("Sklearn verion is {}".format(sklearn.__version__))