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
    
    for answer_key, answer_data in answers.items():
        if answer_key != row['CorrectAnswer']:  # Exclude the correct answer
            question_id_answer.append({
                'QuestionId_Answer': f"{row['QuestionId']}_{answer_key}",
                'AnswerText': answer_data['AnswerText'],
                'MisconceptionId': answer_data['MisconceptionId']
            })
    
    return question_id_answer

# Apply the function to create a list of dictionaries for each row
df['QuestionId_Answer_List'] = df.apply(generate_question_answer, axis=1)

# Explode the list into multiple rows
df_exploded = df.explode('QuestionId_Answer_List').reset_index(drop=True)

# Split the dictionary in 'QuestionId_Answer_List' into separate columns
df_exploded['QuestionId_Answer'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['QuestionId_Answer'])
df_exploded['AnswerText'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['AnswerText'])
df_exploded['MisconceptionId'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['MisconceptionId'])

# Drop the intermediate list column
df_exploded = df_exploded.drop(columns=['QuestionId_Answer_List'])

# Show the updated DataFrame
df_mine = df_exploded[['QuestionId', 'CorrectAnswer', 'QuestionId_Answer', 'QuestionText', 'ConstructName', 'AnswerText', 'MisconceptionId']]
df_mine.loc[:, "context"] = "Question Text:\n" + df_mine["QuestionText"] + "\n\n" + "Construct Name:\n" + df_mine["ConstructName"] + "\n\n" + "Answer Text:\n" + df_mine["AnswerText"] 

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
print(queries[0])


contexts = list(df_merged["MisconceptionName"])
print(contexts[0])

import os
from groq import Groq
import pandas as pd

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
with open("responses.txt", "a") as response_file:
    for idx, query in enumerate(queries):
        mis = contexts[idx]
        print(f"Processing misconception {idx}/{len(queries)}: {mis}")
        prompt = f"""
                    You are a good teacher, skilled at creating Diagnostic Questions (DQs), which are multiple-choice questions featuring one correct answer and three incorrect answers, known as distractors. Each question targets a specific *construct* (also referred to as a skill), representing the most granular level of knowledge relevant to the question. Each distractor is designed to correspond with a potential *misconception*.

                    Here is an example showing how Question-Construct-Answer triplets and misconceptions are related.
                    ***
                    Question-Construct-Answer：
                    {query}

                    Misconception:
                    {mis}
                    ***

                    I need you to give another example based on the same Misconception I gave you.(dont change the Misconception or add anything after it)

                    The expected output format in JSON:
                    [
                        {{
                            "question": {{
                                "text": "...",
                                "construct": "...",
                                "answer": "..."
                            }},
                            "misconception": "..."
                        }}
                    ]
                """
        
        chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-70b-8192",
            )

        response_content = chat_completion.choices[0].message.content

        response_file.write(f"Misconception {idx}/{len(queries)}:\n{response_content}\n\n")

print("All response contents saved to responses.txt")