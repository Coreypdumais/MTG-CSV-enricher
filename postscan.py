import pandas as pd

df1 = pd.read_csv('enriched_collection.csv') # current full collection
df2 = pd.read_csv('new_uploads.csv') # new uploads from prescan

combined_df = pd.concat([df1, df2], ignore_index=True)

print(len(combined_df)) # this is a check

combined_df.to_csv('up_to_date_collection.csv', index=False) # this is the new current collection