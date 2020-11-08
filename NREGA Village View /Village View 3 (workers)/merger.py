import os
import glob
import pandas as pd
 
os.chdir("/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/oop_data")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
print(len(all_filenames), 4675/25)
one = all_filenames[0:50]
two =  all_filenames[50:100]
three = all_filenames[100:150]
four =  all_filenames[150:]

df1 = pd.concat([pd.read_csv(f, low_memory=False) for f in one ])
df2 = pd.concat([pd.read_csv(f, low_memory=False) for f in two ])
df3 = pd.concat([pd.read_csv(f, low_memory=False) for f in three ])
df4 = pd.concat([pd.read_csv(f, low_memory=False) for f in four])

dfs = [df1, df2, df3, df4]
for d in dfs: 
    d = d.drop(df.columns[0], axis = 1)
    n = "/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/" + d + "final_mus.csv"
    d.to_csv(n, index=False, encoding='utf-8-sig')

