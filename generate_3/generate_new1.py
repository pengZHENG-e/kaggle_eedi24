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


import os
from groq import Groq


# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

length = len(train)

with open("whole_QAs_2.txt", "a") as response_file:
    for idx, row in train.iterrows():
        if idx < 1004:
            continue

        question = row["QuestionText"]
        print(f"Processing misconception {idx}/{length}: {question}")
        prompt = f"""
    Please provide another example of the following question while maintaining the same format and misconceptions.

    ###
    ConstructName: {row["ConstructName"]}
    ###
    Subject: {row["SubjectName"]}
    ###
    Question: {row["QuestionText"]}

    ###
    Answer A: {row["AnswerAText"]}
    Answer A Misconception: {row["MisconceptionAtext"]}
    Answer B: {row["AnswerBText"]}
    Answer B Misconception: {row["MisconceptionBtext"]}
    Answer C: {row["AnswerCText"]}
    Answer C Misconception: {row["MisconceptionCtext"]}
    Answer D: {row["AnswerDText"]}
    Answer D Misconception: {row["MisconceptionDtext"]}

    ###
    Correct Answer: {row["CorrectAnswer"]}

    Generate another example based on the same misconception for each answer provided (do not alter the misconception or add anything after it).

    The expected output format is JSON:
    [
        {{
            "question": {{
                "ConstructName": "{row["ConstructName"]}",
                "Subject": "{row["SubjectName"]}",
                "Question": "{row["QuestionText"]}"
            }},
            "answers": {{
                "Answer_A": {{
                    "Answer_text": "{row["AnswerAText"]}",
                    "Misconception": "{row["MisconceptionAtext"]}"
                }},
                "Answer_B": {{
                    "Answer_text": "{row["AnswerBText"]}",
                    "Misconception": "{row["MisconceptionBtext"]}"
                }},
                "Answer_C": {{
                    "Answer_text": "{row["AnswerCText"]}",
                    "Misconception": "{row["MisconceptionCtext"]}"
                }},
                "Answer_D": {{
                    "Answer_text": "{row["AnswerDText"]}",
                    "Misconception": "{row["MisconceptionDtext"]}"
                }}
            }},
            "Correct_Answer": "{row["CorrectAnswer"]}"
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

        response_file.write(f"Misconception {idx}/{length}:\n{response_content}\n\n")

print("All response contents saved to responses.txt")