import pandas as pd

arr = []
ev_msg_body = [429,1,2,429,1,2,3,429,1,2]
df = pd.DataFrame(columns=['switch_id', 'live_port'])
# df = pd.DataFrame()


testarr = [429,1,2]
testarr2 = [429,1,2,3]
# testdict = dict()
# testdict.setdefault('test',[])
# testdict['test'].append(testarr)
# testdict['test'].append(testarr2)
#
# df.loc[0, 'live port'] = testarr
# df.loc[1, 'live port'] = testarr2
# df.loc[0, 'test'] = 'success!!!'
# # df=df.append(testarr,ignore_index='live port')
# print('df = ', df)
# print('live port 0 = ', df.loc[0,'live port'])
# print('dict = ', testdict)

# ser = pd.Series([testarr])
# print('ser: ', ser)
# df = df['live_port'].append(ser)
a = pd.Series(1)
b = pd.Series(2)
c=[1,2,3]
d=[4,5,6]
i= 1

df=df.append({'switch_id':4, 'live_port':[1,5,3]}, ignore_index=True)
df=df.append({'switch_id':5}, ignore_index=True)
df=df.append({'switch_id':6, 'live_port':[7,8,9]}, ignore_index=True)
# df.iloc[-1,-1] = 666
# df.ix[:, 'live_port'] = 456
print('df.loc[0,live_port]: ', df.loc[0,'live_port'])
print('原本的dataframe: ')
print(df)

if df.isnull().loc[1, 'live_port']:
    print('isnull: ', df.isnull().loc[1, 'live_port'])
    # df.loc[2,'live_port'] = [frozenset(c)] # frozenset()存不可變序列
    # df._set_value(1,'live_port', c) # 存可變序列
    df.loc[i, 'live_port'] = c
    df.loc[2, 'live_port'] = d

# df = df['switch_id'].append([2])
# df = df['switch_id'].append([3])

print('後來的dataframe: ')
print(df)