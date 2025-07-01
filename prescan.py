import pandas as pd

print("hello world")

df1 = pd.read_csv('enriched_collection.csv')
df2 = pd.read_csv(r"C:\Users\Corey\Downloads\ManaBox_Collection71.csv")

merged_df = pd.merge(df1, df2, on='Scryfall ID', how='inner', suffixes=('_df1', '_df2'))

unique_to_df2 = df2[~df2['Scryfall ID'].isin(df1['Scryfall ID'])]

unique_to_df2.to_csv('new_uploads.csv', index=False)


print(len(df1))
print(len(df2))

print(len(unique_to_df2))


