import pandas as pd

arr = []
ev_msg_body = [429,1,2,429,1,2,3,429,1,2]
df = pd.DataFrame([[1,2]],columns=['switch_id', 'live_port'])


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
# df['switch_id'] = [1]
# df['switch_id'] = [2]

# df['switch_id'] = a
# df['switch_id'] = b
# print('df: ', df)
c=[1,2,3]

df=df.append({'switch_id':4, 'live_port':[1,5,3]}, ignore_index=True)
df=df.append({'switch_id':5}, ignore_index=True)
# df.iloc[-1,-1] = 666
# df.ix[:, 'live_port'] = 456
print(df.loc[2,'live_port'])
if df.isnull().loc[2, 'live_port']:
    print('isnull: ', df.isnull().loc[2, 'live_port'])
    # df.loc[2,'live_port'] = [frozenset(c)] # frozenset()存不可變序列
    df._set_value(2,'live_port', c) # 存可變序列

# df = df['switch_id'].append([2])
# df = df['switch_id'].append([3])
print('df: ', df)