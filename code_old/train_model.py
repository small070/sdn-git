import pandas as pd

df = pd.read_csv('test2.csv')
# print(df)
x = pd.DataFrame(df, columns=['port_num', 'entry_num', 'packet_time', 'average_priority', 'average_hard_timeout', 'packet_ratio'])
# print(x)
y = df.label
# print(y.shape)


from GML.Ghalat_Machine_Learning import Ghalat_Machine_Learning

gml = Ghalat_Machine_Learning()
new_x,y = gml.Auto_Feature_Engineering(x,y,type_of_task='Regression',test_data=None,
                                                          splits=6,fill_na_='median',ratio_drop=0.2,
                                                          generate_features=True,feateng_steps=2)