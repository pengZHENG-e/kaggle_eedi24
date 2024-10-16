import pandas as pd
import numpy as np
from groq import Groq
from textwrap import dedent
import os

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

seens = misconception_mapping[misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()
unseen = misconception_mapping[~misconception_mapping['MisconceptionId'].isin(all_unique_misconceptions)]['MisconceptionName'].tolist()

print(len(seens))
print(seens[0])

print(len(unseen))
print(unseen[0])




import os
from mistralai import Mistral
import time
from textwrap import dedent

api_key = "Gmz1zmSIpYmIIwQ54YaaxNfizPdw9LeE"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)


with open('unseens_mistral.txt', 'a') as f:
    for i, mis in enumerate(unseen):
        if i<=20:
            continue
        print(i, " - ", len(unseen))
        prompt_user = dedent(
            f"""
Give a math question with Construct, with a correct answer and an incorrect answer with given misconception in following format.

<Construct>...</Construct>
<Question>...</Question>
<Correct Answer>...</Correct Answer>
<Incorrect Answer>...</Incorrect Answer>
<Misconception>{mis}</Misconception>

Ensure that:
1. The misconception matches exactly what I provide.
2. The incorrect answer is directly caused by the given misconception.
3. Your response contains only the formatted data, with no additional text.
4. The question is clear and relevant to the given Construct.
5. Both the correct and incorrect answers are plausible within the context of the question.

Here is an response example:
<Construct>Identify questions involving a 2D right-angled triangle that require the use of the Tangent (tan) ratio</Construct>
<Question>Which ratio would you use to find the value of \( p \) ? ![A right-angled triangle with the angle labelled 32 degrees, the side adjacent to this is 6cm and the side opposite is p.]()</Question>
<Correct Answer>Tan</Correct Answer>
<Incorrect Answer>Cos</Incorrect Answer>
<Misconception>Uses sin when tan is required</Misconception>
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

