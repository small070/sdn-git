import pandas as pd
import numpy as np

arr = []
ev_msg_body = [429,1,2,429,1,2,3,429,1,2]
df = pd.DataFrame(columns=['switch_id', 'live_port', 'hw_addr'])

a = pd.Series(1)
b = pd.Series(2)
c=[1,2,3]
d=[4,5,6]
i= 1

df=df.append({'switch_id':1}, ignore_index=True)
df=df.append({'live_port':4294967}, ignore_index=True)
df=df.append({'hw_addr':'2e:f2:9f:aa:62:4d:'}, ignore_index=True)
df=df.append({'live_port':1, 'hw_addr':'e2:64:98:d2:8b:d7'}, ignore_index=True)
df=df.append({'live_port':2, 'hw_addr':'d2:03:07:ee:ad:a4:'}, ignore_index=True)
df=df.append({'switch_id':3}, ignore_index=True)
df=df.append({'live_port':4294967}, ignore_index=True)
df=df.append({'hw_addr':'de:7e:b4:a7:f0:42'}, ignore_index=True)
df=df.append({'live_port':4, 'hw_addr':'12:fb:02:12:67:77'}, ignore_index=True)
df=df.append({'live_port':1, 'hw_addr':'26:50:fb:81:1f:df'}, ignore_index=True)
df=df.append({'live_port':2, 'hw_addr':'56:7c:81:82:c1:07'}, ignore_index=True)
df=df.append({'live_port':3, 'hw_addr':'6a:ec:db:25:c0:f1'}, ignore_index=True)
df=df.append({'switch_id':2}, ignore_index=True)
df=df.append({'live_port':4294967}, ignore_index=True)
df=df.append({'hw_addr':'7a:5f:99:46:04:4d'}, ignore_index=True)
df=df.append({'live_port':1, 'hw_addr':'ee:fe:46:c4:29:01'}, ignore_index=True)
df=df.append({'live_port':4, 'hw_addr':'8a:6d:2f:7e:a1:ac'}, ignore_index=True)
df=df.append({'live_port':2, 'hw_addr':'9a:4c:7e:21:31:38'}, ignore_index=True)
df=df.append({'live_port':3, 'hw_addr':'ae:1a:9b:8f:72:99'}, ignore_index=True)

print(df)

# df=df.append({'switch_id':4, 'live_port':8}, ignore_index=True)
# df=df.append({'switch_id':5}, ignore_index=True)
# df=df.append({'switch_id':6, 'live_port':[7,8,9]}, ignore_index=True)
# df.iloc[-1,-1] = 666
# df.ix[:, 'live_port'] = 456
# print('df.loc[0,live_port]: ', df.loc[0,'live_port'])
# print('原本的dataframe: ')
# print(df)
#
# if df.isnull().loc[1, 'live_port']:
#     print('isnull: ', df.isnull().loc[1, 'live_port'])
#     # df.loc[2,'live_port'] = [frozenset(c)] # frozenset()存不可變序列
#     # df._set_value(1,'live_port', c) # 存可變序列
#     df.loc[i, 'live_port'] = [1,2,3]
#     df.loc[2, 'live_port'] = d
#
# # df = df['switch_id'].append([2])
# # df = df['switch_id'].append([3])
#
# print('後來的dataframe: ')
# print(df)