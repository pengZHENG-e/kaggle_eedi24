import pandas as pd

def parse_txt(path):
    with open(path, 'r') as file:
        content = file.read()

    # Split the content into separate entries based on the <Construct> tag
    entries = content.split('<Construct>')[1:]  # Ignore the first split part

    json_data = []

    # Iterate through each entry and extract the relevant fields
    for entry in entries:
        try:
            # Extract the different fields
            construct = entry.split('</Construct>')[0].strip()
            question = entry.split('<Question>')[1].split('</Question>')[0].strip()
            correct = entry.split('<Correct Answer>')[1].split('</Correct Answer>')[0].strip()
            incorrect = entry.split('<Incorrect Answer>')[1].split('</Incorrect Answer>')[0].strip()
            misconception = entry.split('<Misconception>')[1].split('</Misconception>')[0].strip()
            
            # Create a dictionary for the JSON object
            data_dict = {
                "ConstructName": construct,
                "CorrectAnswer": "A",
                "QuestionText": question,
                "AnswerAText": correct,
                "AnswerBText": incorrect,
                "MisconceptionName": misconception
            }
            
            json_data.append(data_dict)
        except IndexError as e:
            print(f"Error parsing entry: {entry}\nError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(json_data)
    
    return df


mapping_df = pd.read_csv("data/misconception_mapping.csv")
train_df = pd.read_csv("data/train.csv")

path_mistral = 'unseens_mistral.txt'
path_gemini = 'unseens_gemini.txt'
path_groq = 'unseens_groq_llama90b.txt'
paths = [path_mistral, path_gemini, path_groq]

def modify_df(path_mistral,outname):
    df_mistral = parse_txt(path_mistral)
    df_mistral = df_mistral.merge(mapping_df,on="MisconceptionName", how="left")
    df_mistral.rename(columns={'MisconceptionId': 'MisconceptionBId'}, inplace=True)

    train_add_mistral = pd.concat([train_df, df_mistral], ignore_index=True, sort=False)
    train_add_mistral.to_csv(outname)

# modify_df(path_groq,"train_add_groq.csv")


def add_all(paths,outname):
    merged_dfs = []
    for path in paths:
        df = parse_txt(path)
        df = df.merge(mapping_df,on="MisconceptionName", how="left")
        df.rename(columns={'MisconceptionId': 'MisconceptionBId'}, inplace=True)
        merged_dfs.append(df)

    merged_df = pd.concat(merged_dfs, axis=0, ignore_index=True)

    train_add_merged = pd.concat([train_df, merged_df], ignore_index=True, sort=False)
    train_add_merged.to_csv(outname)

add_all(paths,"train_add_all.csv")
