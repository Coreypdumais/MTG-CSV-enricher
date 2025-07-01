import pandas as pd

print("hello world")

df1 = pd.read_csv('enriched_collection.csv') # old collection here
df2 = pd.read_csv(r"C:\Users\Corey\Downloads\ManaBox_Collection71.csv") # new collection here

merged_df = pd.merge(df1, df2, on='Scryfall ID', how='inner', suffixes=('_df1', '_df2'))

unique_to_df2 = df2[~df2['Scryfall ID'].isin(df1['Scryfall ID'])]

unique_to_df2.to_csv('new_uploads.csv', index=False) # this is the file to run in main file


print(len(df1))
print(len(df2))

print(len(unique_to_df2))


