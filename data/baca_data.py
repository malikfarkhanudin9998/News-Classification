import pandas as pd

data = ('data_copy.csv')
baca = pd.read_csv(data)
itung = baca['Keterangan'].value_counts()
print(itung)
# kelist = baca.values.tolist()
# # kelist.sorted()
# def keysort(listbaru):
#     return listbaru[2]

# kelist.sort(key=keysort)

# hitung = baca['Keterangan'].value_counts()
# print(type(kelist))
# for i in kelist:
#     print(i)
# print(kelist)