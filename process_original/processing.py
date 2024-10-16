import pandas as pd

# Load the datasets
train = pd.read_csv("data/train.csv")
misconception_mapping = pd.read_csv("data/misconception_mapping.csv")

# Define the misconception columns to merge
misconception_columns = ["MisconceptionAId", "MisconceptionBId", "MisconceptionCId", "MisconceptionDId"]

# Loop through each misconception column and merge with the misconception_mapping
for col in misconception_columns:
    text_col = col.replace("Id", "text")  # Generate corresponding text column name
    train = pd.merge(train, 
                     misconception_mapping[['MisconceptionId', 'MisconceptionName']], 
                     left_on=col, 
                     right_on="MisconceptionId", 
                     how="left")
    
    # Rename the merged MisconceptionName to corresponding text column
    train.rename(columns={"MisconceptionName": text_col}, inplace=True)
    
    # Drop the MisconceptionId column after the merge
    train.drop(columns=["MisconceptionId"], inplace=True)

# Convert all values in 'MisconceptionAtext' to strings using apply
train["MisconceptionAtext"] = train["MisconceptionAtext"].apply(str)
train["MisconceptionBtext"] = train["MisconceptionBtext"].apply(str)
train["MisconceptionCtext"] = train["MisconceptionCtext"].apply(str)
train["MisconceptionDtext"] = train["MisconceptionDtext"].apply(str)
train.drop(columns=["QuestionId"], inplace=True)
train.drop(columns=["ConstructId"], inplace=True)
train.drop(columns=["SubjectId"], inplace=True)
train.drop(columns=["MisconceptionAId"], inplace=True)
train.drop(columns=["MisconceptionBId"], inplace=True)
train.drop(columns=["MisconceptionCId"], inplace=True)
train.drop(columns=["MisconceptionDId"], inplace=True)

print(train.columns)
train.to_csv("processed_train.csv")