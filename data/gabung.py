import pandas as pd

t1 = pd.read_csv('uji.csv')
t2 = pd.read_csv('tu2.csv')

# menyatukan file csv dengan concat
frames = [t1,t2]
result = pd.concat(frames).drop_duplicates().reset_index(drop=True)
result.to_csv(r'dataujiv2.csv',index=False)