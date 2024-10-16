import pandas as pd
import numpy as np

pd.set_option('display.max_colwidth', None)

# Data Loading
train = pd.read_csv("data/train.csv")
misconception_mapping = pd.read_csv("data/misconception_mapping.csv")

result_df_1 = train.groupby('SubjectName')['MisconceptionAId'].apply(list).reset_index()
result_df_2 = train.groupby('SubjectName')['MisconceptionBId'].apply(list).reset_index()
result_df_3 = train.groupby('SubjectName')['MisconceptionCId'].apply(list).reset_index()
result_df_4 = train.groupby('SubjectName')['MisconceptionDId'].apply(list).reset_index()

merged_df = result_df_1.merge(result_df_2, on='SubjectName', suffixes=('_A', '_B')) \
                         .merge(result_df_3, on='SubjectName', suffixes=('', '_C')) \
                         .merge(result_df_4, on='SubjectName', suffixes=('', '_D'))

unique_misconceptions_df = merged_df.copy()
unique_misconceptions_df['UniqueMisconceptions'] = unique_misconceptions_df.apply(
    lambda row: list(set(filter(pd.notna, row['MisconceptionAId'] + row['MisconceptionBId'] + 
                                 row['MisconceptionCId'] + row['MisconceptionDId']))), axis=1
)

final_df = unique_misconceptions_df[['SubjectName', 'UniqueMisconceptions']]
final_df["UniqueMisconceptions"] = final_df["UniqueMisconceptions"].apply(lambda x: [np.int64(i) for i in x])

all_unique_misconceptions = list(set(value for sublist in final_df['UniqueMisconceptions'] for value in sublist))
unique_count = len(all_unique_misconceptions)

# seens = misconception_mapping[misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()
# unseen = misconception_mapping[~misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()

# print(len(seens))
# print(seens[0])

# print(len(unseen))
# print(unseen[0])

# unseen_df = pd.DataFrame(unseen, columns=['unseens'])
# unseen_df.to_csv('unseens.csv', index=False)


seens = misconception_mapping[misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()
unseen = misconception_mapping[~misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()

# Print the lengths and first elements of the seen and unseen lists
print(len(seens))
print(seens[0])

print(len(unseen))
print(unseen[0])

# Create a DataFrame for unseen misconceptions
unseen_df = pd.DataFrame(unseen, columns=['unseens'])

# Get the MisconceptionId for unseen misconceptions
unseen_df['MisconceptionId'] = misconception_mapping[misconception_mapping['MisconceptionName'].isin(unseen)]['MisconceptionId'].values

# Save the unseen_df to a CSV file
unseen_df.to_csv('unseens1.csv', index=False)


# with open('unseens.txt', 'w') as file:
#     # Write each item on a new line
#     for item in unseen:
#         file.write(f"{item}\n\n")
