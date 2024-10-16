import pandas as pd
import numpy as np

pd.set_option('display.max_colwidth', None)

# Data Loading
train = pd.read_csv("data/train.csv")
misconception_mapping = pd.read_csv("data/misconception_mapping.csv")

print(type(misconception_mapping["MisconceptionId"].iloc[1]))
misconception_mapping

df = pd.DataFrame(train)

# Function to generate QuestionId_Answer excluding the correct answer
def generate_question_answer(row):
    answers = {
        'A': {'AnswerText': row['AnswerAText'], 'MisconceptionId': row['MisconceptionAId']},
        'B': {'AnswerText': row['AnswerBText'], 'MisconceptionId': row['MisconceptionBId']},
        'C': {'AnswerText': row['AnswerCText'], 'MisconceptionId': row['MisconceptionCId']},
        'D': {'AnswerText': row['AnswerDText'], 'MisconceptionId': row['MisconceptionDId']}
    }
    question_id_answer = []
    correctAnswer = answers[row['CorrectAnswer']]['AnswerText']

    # Now, add the incorrect answers to the list
    for answer_key, answer_data in answers.items():
        if answer_key != row['CorrectAnswer']:
            question_id_answer.append({
                'QuestionId_Answer': f"{row['QuestionId']}_{answer_key}",
                'IncorrectAnswerText': answer_data['AnswerText'],
                'MisconceptionId': answer_data['MisconceptionId'],
                "CorrectAnswerText": correctAnswer  # Set the correct answer directly
            })
    
    return question_id_answer

# Apply the function to create a list of dictionaries for each row
df['QuestionId_Answer_List'] = df.apply(generate_question_answer, axis=1)

# Explode the list into multiple rows
df_exploded = df.explode('QuestionId_Answer_List').reset_index(drop=True)

# Split the dictionary in 'QuestionId_Answer_List' into separate columns
df_exploded['QuestionId_Answer'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['QuestionId_Answer'])
df_exploded['IncorrectAnswerText'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['IncorrectAnswerText'])
df_exploded['MisconceptionId'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['MisconceptionId'])
df_exploded['CorrectAnswerText'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['CorrectAnswerText'])

# print(df_exploded)

# Drop the intermediate list column
df_exploded = df_exploded.drop(columns=['QuestionId_Answer_List'])

# Show the updated DataFrame
df_mine = df_exploded[['QuestionId', 'CorrectAnswer', 'QuestionId_Answer', 'QuestionText', 'ConstructName','CorrectAnswerText','IncorrectAnswerText', 'MisconceptionId', 'SubjectName']]
df_mine.loc[:, "context"] = "<Construct>" + df_mine["ConstructName"] + "</Construct>\n" + "<Subject>" + df_mine["SubjectName"] + "</Subject>\n" + "<Question>\n" + df_mine["QuestionText"] + "\n</Question>\n" + "<CorrectAnswer>" + df_mine["CorrectAnswerText"] + "</CorrectAnswer>\n" + "<IncorrectAnswer>" + df_mine["IncorrectAnswerText"] + "</IncorrectAnswer>\n"

def convert_to_int(x):
    if pd.isna(x):  # Check if the value is NaN
        return np.nan  # Return np.nan to keep it as NaN
    if isinstance(x, float) and x.is_integer():  # Check if it's a float and ends with ".0"
        return int(x)  # Convert to integer
    return x  # Return other values as is

# Apply the conversion function
df_mine["MisconceptionId"] = df_mine["MisconceptionId"].apply(convert_to_int)

# Convert column to numpy.int64, handling NaN values
df_mine["MisconceptionId"] = pd.to_numeric(df_mine["MisconceptionId"], errors='coerce').astype('Int64')


df_merged = df_mine.merge(misconception_mapping, on='MisconceptionId', how='left')


df_merged = df_merged.dropna(subset=['MisconceptionName'])
df_merged = df_merged[["context", "MisconceptionName"]]
df_merged

queries = list(df_merged["context"])
# print(queries[0])
# print(len(queries))


contexts = list(df_merged["MisconceptionName"])
# print(contexts[0])

alltogether = []
for idx,query in enumerate(queries):
    mis = contexts[idx]
    allto = query+"<Analysis>ADD TEXT HERE</Analysis><Misconception>"+mis+"</Misconception>"
    alltogether.append(allto)
print("*"*100)
print(alltogether[2])




import os
from mistralai import Mistral
import time
from textwrap import dedent

api_key = "Gmz1zmSIpYmIIwQ54YaaxNfizPdw9LeE"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)


with open('analysis_mistral.txt', 'a') as f:
    for i, mis in enumerate(alltogether):
        # if i<=20:
        #     continue
        print(i, " - ", len(alltogether))
        prompt_user = dedent(
            f"""
GIVEN A QUESTION, THE CORRECT ANSWER, AN INCORRECT ANSWER, AND THE UNDERLYING MISCONCEPTION, PROVIDE A CONCISE ANALYSIS OF HOW THE MISCONCEPTION CAN BE INFERRED BY COMPARING THE CORRECT AND INCORRECT ANSWERS.

Response only with this format:<Analysis>ADD TEXT HERE</Analysis>
{mis}
"""
        )

        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": prompt_user
                },
            ]
        )
        response = chat_response.choices[0].message.content
        
        f.write(response + '\n\n')  

        time.sleep(2)
