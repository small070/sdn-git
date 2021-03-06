import pandas as pd
import numpy as np
import networkx as nx

# 顯示所有的行
pd.set_option('display.max_columns', None)
# 顯示所有的列
pd.set_option('display.max_rows', None)
# 顯示長度 ＝ 100 ,預設50
pd.set_option('max_colwidth',100)


arr = []
ev_msg_body = [429,1,2,429,1,2,3,429,1,2]
df = pd.DataFrame(columns=['switch_id', 'live_port', 'hw_addr'])
edges = pd.DataFrame({'source' : [0, 1],
                      'target' : [1, 2],
                      'weight' : [100, 50]})


a = pd.Series(1)
b = pd.Series(2)
c=[1,2,3]
d=[4,5,6]
i= 1

# df=df.append({'switch_id':1}, ignore_index=True)
# df=df.append({'live_port':4294967}, ignore_index=True)
# df=df.append({'hw_addr':'2e:f2:9f:aa:62:4d:'}, ignore_index=True)
# df=df.append({'live_port':1, 'hw_addr':'e2:64:98:d2:8b:d7'}, ignore_index=True)
# df=df.append({'live_port':2, 'hw_addr':'d2:03:07:ee:ad:a4:'}, ignore_index=True)
# df=df.append({'switch_id':3}, ignore_index=True)

df=df.append({'switch_id':1, 'live_port':4294967, 'hw_addr':'2e:f2:9f:aa:62:4d:'}, ignore_index=True)
df=df.append({'switch_id':1, 'live_port':1, 'hw_addr':'e2:64:98:d2:8b:d7'}, ignore_index=True)
df=df.append({'switch_id':1, 'live_port':2, 'hw_addr':'d2:03:07:ee:ad:a4:'}, ignore_index=True)

df=df.append({'switch_id':2, 'live_port':4294967, 'hw_addr':'de:7e:b4:a7:f0:42'}, ignore_index=True)
df=df.append({'live_port':1, 'hw_addr':'26:50:fb:81:1f:df'}, ignore_index=True)
df=df.append({'live_port':2, 'hw_addr':'56:7c:81:82:c1:07'}, ignore_index=True)
# df=df.append({'live_port':3, 'hw_addr':'12:fb:02:12:67:77'}, ignore_index=True)
# df=df.append({'live_port':4, 'hw_addr':'6a:ec:db:25:c0:f1'}, ignore_index=True)

# df=df.append({'switch_id':3, 'live_port':4294967, 'hw_addr':'7a:5f:99:46:04:4d'}, ignore_index=True)
# df=df.append({'live_port':1, 'hw_addr':'ee:fe:46:c4:29:01'}, ignore_index=True)
# df=df.append({'live_port':4, 'hw_addr':'8a:6d:2f:7e:a1:ac'}, ignore_index=True)
# df=df.append({'live_port':2, 'hw_addr':'9a:4c:7e:21:31:38'}, ignore_index=True)
# df=df.append({'live_port':3, 'hw_addr':'ae:1a:9b:8f:72:99'}, ignore_index=True)

# print(df)
# print(df.isnull().any(axis = 0))
df['switch_id'] = df['switch_id'].fillna(method='ffill')

# print(df[df['hw_addr'].isnull() & df['live_port'].notnull()])
df1 = df[df['hw_addr'].isnull() & df['live_port'].notnull()]
# print(df[df['hw_addr'].notnull() & df['live_port'].isnull()])
df2 = df[df['hw_addr'].notnull() & df['live_port'].isnull()]

df1.set_index(df2.index, inplace=True)
# print(df1)
# print(df1.index)
# print(df2)
# print(df2.index)

df2 = df2.combine_first(df1)
# print(df2.combine_first(df1))
df = df.combine_first(df2)
# print(df)
df = df.dropna(axis=0).reset_index().drop(columns='index')
# print(df)


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

# print(edges)

import networkx as nx
net = nx.DiGraph()

src_dpid = 1
dst_dpid = 3
port = 2

links=[(src_dpid, dst_dpid, {'port': port})]
net.add_edges_from(links)

net.add_node('aa:bb:cc')
net.add_edge(1, 'aa:bb:cc', attr_dict={'port': 3})
net.add_edge('aa:bb:cc', 1)

# self.network.add_node(src)
# self.network.add_edge(dpid, src, attr_dict={'port': in_port})
# self.network.add_edge(src, dpid)
# print(net.edges)


tmp2_df = pd.DataFrame(columns=['request_sid', 'request_port', 'receive_sid', 'receive_port'])
tmp2_df=tmp2_df.append({'request_sid': 1, 'request_port': 2, 'receive_sid': 2, 'receive_port': 2}, ignore_index=True)
tmp2_df=tmp2_df.append({'request_sid': 2, 'request_port': 2, 'receive_sid': 1, 'receive_port': 2}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 3, 'request_port': 2, 'receive_sid': 2, 'receive_port': 2}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 3, 'request_port': 1, 'receive_sid': 1, 'receive_port': 3}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 2, 'request_port': 1, 'receive_sid': 1, 'receive_port': 2}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 3, 'request_port': 3, 'receive_sid': 4, 'receive_port': 4}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 1, 'request_port': 4, 'receive_sid': 4, 'receive_port': 3}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 3, 'request_port': 4, 'receive_sid': 5, 'receive_port': 3}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 2, 'request_port': 3, 'receive_sid': 5, 'receive_port': 2}, ignore_index=True)
# tmp2_df=tmp2_df.append({'request_sid': 4, 'request_port': 5, 'receive_sid': 5, 'receive_port': 4}, ignore_index=True)

print(df)
print(tmp2_df)
# print(df.info())
# print(tmp2_df.info())
# for row in tmp2_df.itertuples():
#     print(getattr(row, 'request_sid'))
    # if (df['switch_id'] == getattr(row, 'request_sid')) & (df['live_port'] == getattr(row, 'request_port')):
    # if (df.iloc[0] == getattr(row, 'request_sid')) & (df.iloc[1] == getattr(row, 'request_port')):
    # if (df.loc['switch_id'] == 1):
    #     print('test')
# print(tmp2_df.request_sid)
# print(tmp2_df[tmp2_df['request_sid'] == 1])
df3 = df.copy()
# for i, o in tmp2_df.request_sid, tmp2_df.request_port:
#     print(i, o)
#     print(df3[(df3['switch_id'] == i) & (df3['live_port'] == o)])

for i in range(0, len(tmp2_df), 1):
    print(df3[(df3['switch_id'] == tmp2_df.at[i, 'request_sid']) & (df3['live_port'] == tmp2_df.at[i, 'request_port'])])
    request_index = df3[(df3['switch_id'] == tmp2_df.at[i, 'request_sid']) & (df3['live_port'] == tmp2_df.at[i, 'request_port'])].index
    receive_index = df3[(df3['switch_id'] == tmp2_df.at[i, 'receive_sid']) & (df3['live_port'] == tmp2_df.at[i, 'receive_port'])].index
    controller_index = df3[(df3['live_port'] > 429)].index
    # print(type(index))
    df3.drop(index=request_index, inplace=True)
    df3.drop(index=receive_index, inplace=True)
    df3.drop(index=controller_index, inplace=True)
    df3.reset_index(drop=True, inplace=True)
print(df3)


# print(df[(df['switch_id'] == tmp2_df['request_sid'])])
# print(df.loc[(df['switch_id'] == 1) & (df['live_port'] == 1)])
# print(pd.concat([df, tmp2_df], axis=0))


# tmp  = dict({3: {3: [3], 1: [3, 1], 5: [3, 5], 4: [3, 4], 2: [3, 2]}, 1: {1: [1], 3: [1, 3], 4: [1, 4], 2: [1, 2], 5: [1, 3, 5]}, 5: {5: [5], 3: [5, 3], 4: [5, 4], 2: [5, 2], 1: [5, 3, 1]}, 4: {4: [4], 3: [4, 3], 5: [4, 5], 1: [4, 1], 2: [4, 3, 2]}, 2: {2: [2], 1: [2, 1], 3: [2, 3], 5: [2, 5], 4: [2, 1, 4]}}
# )
# print('原始networkx所有資料: ', tmp)
# print('資料的所有key: ', tmp.keys())
# print('資料的所有values: ', tmp.values())
# print('資料key = 3的所有 資料: ', tmp[3])
# print('資料key = 3的所有key: ', tmp[3].keys())
# print('資料key = 3的所有資料', tmp[3].values())

# tmp_df = pd.DataFrame(tmp[3].values())
# print(tmp_df)
# tmp_df = pd.DataFrame(tmp)
# print('原始資料塞進dataframe: \n', tmp_df)
# print(tmp_df.loc[3])
# for m in tmp_df.index:
#     for i in tmp_df.loc[m]:
#         if len(i) == 2:
#             print(type(i), i[0], i[1])
#             # print(tmp2_df[(tmp2_df['request_sid'] == i[0]) & (tmp2_df['receive_sid'] == i[1]) |
#             #      (tmp2_df['request_sid'] == i[1]) & (tmp2_df['receive_sid'] == i[0])].iloc[0, 1])
#             # print(tmp2_df[(tmp2_df['request_sid'] == i[0]) & (tmp2_df['receive_sid'] == i[1]) |
#             #               (tmp2_df['request_sid'] == i[1]) & (tmp2_df['receive_sid'] == i[0])].iloc[0, 3])
#         if len(i) == 3:
#             print(type(i), i[0], i[1], i[2])
#         #     print(tmp2_df[(tmp2_df['request_sid'] == i[0]) & (tmp2_df['receive_sid'] == i[1]) |
#         #          (tmp2_df['request_sid'] == i[1]) & (tmp2_df['receive_sid'] == i[0])].iloc[0, 3])

# print(tmp_df.loc[[3]])
# print(type(tmp_df.loc[3]), type(tmp_df.loc[[3]]))

# # 轉成上三角矩陣
# m,n = tmp_df.shape
# tmp_df[:] = np.where(np.arange(m)[:,None] >= np.arange(n),np.nan,tmp_df)
# # 轉成完整矩陣
# tmp_df = tmp_df.stack().reset_index()
# tmp_df.columns = ['start_sid', 'end_sid', 'link']
# print(tmp_df)
#
# for i in range(0, len(tmp_df), 1):
#     test = tmp_df.loc[i, 'link']
#     print('第一個for: ', tmp_df.loc[i, 'link'])
#     # print(test[n:n+2])
#     n = 2
#     for link in [test[i:i + n] for i in range(0, len(test), 1)]:
#         if len(link)%2 == 0:
#             print('第二個for: ', link)
#             print('第二個for: ', link[0], link[1])


