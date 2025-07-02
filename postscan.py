import pandas as pd

df1 = pd.read_csv('enriched_collection.csv') # current full collection
df2 = pd.read_csv('new_uploads.csv') # new uploads from prescan

df1['Status'] = 'Old'
df2['Status'] = 'Newly Added'

combined_df = pd.concat([df1, df2], ignore_index=True)

print(combined_df.head(25))

print(len(combined_df)) # this is a check

combined_df.to_csv('up_to_date_collection.csv', index=False) # this is the new current collection