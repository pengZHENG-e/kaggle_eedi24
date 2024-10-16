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





import time

client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    # api_key="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",
    # api_key="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",
    api_key = "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"
)

from textwrap import dedent

prompt_sys = """
Provide a similar example to the one below (note that the answer must be incorrect and the misconception should explain why that answer is given. The construct focuses on how to respond to the question):

<Construct>...</Construct>  
<Subject>...</Subject>  
<Question>  
...
</Question>  
<Answer>...</Answer>  
<Misconception>...</Misconception>           

Please base your response on the misconception provided by the user.

- Respond only with the example data and nothing else. REMEMBER: the answer should be incorrect and derived from the misconception.
"""

responses = []

with open('GENERATE_UNSEEN/unseens_groq_llama90b.txt', 'a') as f:
    for i, mis in enumerate(unseen):
        if i <= 368:
            continue
        print(i, " - ", len(unseen))
        prompt_user = dedent(
            f"""
Provide a similar example following this structure (note that the answer should be incorrect and the misconception should explain why the answer is given. The construct focuses on how to answer the question):

<Construct>...</Construct>  
<Subject>...</Subject>  
<Question>  
...
</Question>  
<Incorrect Answer>....</Incorrect Answer> 
<Misconception>{mis}</Misconception>

Make sure the misconception is the same as I gave you. Please respond with the data only and nothing else. Remember the answer should be incorrect and caused by the misconception.
"""
        )

        chat_completion = client.chat.completions.create(
            messages=[
                # {
                #     "role": "system",
                #     "content": prompt_sys
                # },
                {
                    "role": "user",
                    "content": prompt_user,
                }
            ],
            model="llama-3.2-90b-text-preview",
        )

        response_content = chat_completion.choices[0].message.content
        responses.append(response_content)
        
        f.write(response_content + '\n\n\n')  

        time.sleep(2)
