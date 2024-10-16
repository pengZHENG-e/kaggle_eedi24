import pandas as pd
import numpy as np
from groq import Groq
from textwrap import dedent
import os

with open('GENERATE_SEEN/qco.txt', 'r') as file:
    content = file.read()

# Split the content into separate entries based on the <Construct> tag
entries = content.split('<Construct>')[1:]  # Ignore the first split part

json_data = []

# Iterate through each entry and extract the relevant fields
for entry in entries:
    # Extract the different fields
    construct = entry.split('</Construct>')[0].strip()
    subject = entry.split('<Subject>')[1].split('</Subject>')[0].strip()
    question = entry.split('<Question>')[1].split('</Question>')[0].strip()
    answer = entry.split('<Answer>')[1].split('</Answer>')[0].strip()
    misconception = entry.split('<Misconception>')[1].split('</Misconception>')[0].strip()
    
    # Create a dictionary for the JSON object
    data_dict = {
        "Construct": construct,
        "Subject": subject,
        "Question": question,
        "Answer": answer,
        "Misconception": misconception
    }
    
    json_data.append(data_dict)

print(len(json_data))
print(json_data[-1])

html_lst = []
for each in json_data:
    html_lst.append(f"""
<Construct>{each["Construct"]}</Construct>
<Subject>{each["Subject"]}</Subject>
<Question>
{each["Question"]}
</Question>
<Answer>{each["Answer"]}</Answer>
<Misconception>{each["Misconception"]}</Misconception>
""")
    
print(html_lst[0])





import time

client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key="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",
    # api_key="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",
    # api_key = "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"
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

with open('GENERATE_SEEN/unseens_groq_llama90b.txt', 'a') as f:
    for i, example in enumerate(html_lst[:3]):
        # if i <= 368:
        #     continue
        print(i, " - ", len(html_lst))
        prompt_user = dedent(
            f"""
Provide a similar example (note that the answer should be incorrect and the misconception should explain why the answer is given.):

{example}

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

        time.sleep(3)
