def parse_txt(path):
    with open(path, 'r') as file:
        content = file.read()

    # Split the content into separate entries based on the <Construct> tag
    entries = content.split('<Construct>')[1:]  # Ignore the first split part

    json_data = []

    # Iterate through each entry and extract the relevant fields
    for entry in entries:
        # Extract the different fields with checks
        construct = entry.split('</Construct>')[0].strip() if '<Construct>' in entry else None
        subject = entry.split('<Subject>')[1].split('</Subject>')[0].strip() if '<Subject>' in entry else None
        question = entry.split('<Question>')[1].split('</Question>')[0].strip() if '<Question>' in entry else None
        answer = entry.split('<Incorrect Answer>')[1].split('</Incorrect Answer>')[0].strip() if '<Incorrect Answer>' in entry else None
        misconception = entry.split('<Misconception>')[1].split('</Misconception>')[0].strip() if '<Misconception>' in entry else None
        
        # Create a dictionary for the JSON object
        data_dict = {
            "Construct": construct,
            "Subject": subject,
            "Question": question,
            "Answer": answer,
            "Misconception": misconception
        }
        
        json_data.append(data_dict)

    # Output the number of JSON objects and the last one's answer for verification
    print(len(json_data))
    print(json_data[-1]["Answer"])

    queries = []
    for each in json_data:
        queries.append(f"""{each["Question"]}
Incorrect Answer: {each["Answer"]}""")
        
    print(queries[0])
    print(len(queries))

    MISs = []
    for each in json_data:
        MISs.append(each["Misconception"])

    print(MISs[0])
    print(len(MISs))
    return queries, MISs


queries_groq, MISs_groq = parse_txt('GENERATE_UNSEEN/unseens_groq_llama90b.txt')
queries_gemini, MISs_gemini = parse_txt('GENERATE_UNSEEN/unseens_gemini.txt')
queries_mistral, MISs_mistral = parse_txt('GENERATE_UNSEEN/unseens_mistral.txt')

queries = []
MISs = []

queries.extend(queries_groq)
queries.extend(queries_gemini)
queries.extend(queries_mistral)
MISs.extend(queries_groq)
MISs.extend(queries_gemini)
MISs.extend(MISs_mistral)

print(len(queries))
print(queries[0])
print(len(MISs))
print(MISs[-1])