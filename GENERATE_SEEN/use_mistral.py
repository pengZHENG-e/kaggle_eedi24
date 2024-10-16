from textwrap import dedent

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

from mistralai import Mistral

api_key = "Gmz1zmSIpYmIIwQ54YaaxNfizPdw9LeE"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

responses = []

with open('GENERATE_SEEN/seens_mistral.txt', 'a') as f:
    for i, example in enumerate(html_lst):
        if i < 4182:
            continue
        print(i, " - ", len(html_lst))
        prompt_user = dedent(
            f"""
Provide a similar example (note that the answer should be incorrect and the misconception should explain why the answer is given.):

{example}

Make sure the misconception is the same as I gave you. Please respond with the data only and nothing else. Remember the answer should be incorrect and caused by the misconception.
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
        responses.append(response)
        
        f.write(response + '\n\n')  

        time.sleep(2)
