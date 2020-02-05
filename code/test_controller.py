import pandas as pd

arr = []
ev_msg_body = [429,1,2,429,1,2,3,429,1,2]
df = pd.DataFrame([[1,2]],columns=['switch_id', 'live_port'])
# print(len(arr))
# i = 0
# for stat in ev_msg_body:
#     if stat >= 50 and len(arr) > 0:
#         print('arr = ', arr)
#         # func = lambda i=0: i + 1
#         df.loc[i, 'live port'] = arr
#         arr.clear()
#         arr.append(stat)
#         i = i + 1
#     elif stat >= 50:
#         arr.append(stat)
#     elif stat <= 50:
#         arr.append(stat)
#         # if # end of arr

# print('df = ', df)

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
print('df: ', df)
c=[1,2,3]
df=df.append({'live_port':c}, ignore_index=True)
df=df.append({'switch_id':4, 'live_port':[1,5,3]}, ignore_index=True)

# df = df['switch_id'].append([2])
# df = df['switch_id'].append([3])
print('df: ', df)