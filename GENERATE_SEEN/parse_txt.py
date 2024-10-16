def parse_txt(path):
    with open(path, 'r') as file:
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

    queries = []
    for each in json_data:
        queries.append(f"""{each["Construct"]}
    {each["Question"]}

    Incorrect Answer: {each["Answer"]}""")
        
    print(queries[0])
    print(len(queries))

    MISs = []
    for each in json_data:
        MISs.append(each["Misconception"])

    print(MISs[0])
    print(len(MISs))
    return queries, MISs

path_original = 'GENERATE_SEEN/qco.txt'
path_mistral = 'GENERATE_SEEN/seens_mistral.txt'

queries_o,MISs_o = parse_txt(path_original)
queries_mistral,MISs_mistral = parse_txt(path_mistral)

queries = []
MISs = []

queries.extend(queries_o)
queries.extend(queries_mistral)
MISs.extend(MISs_o)
MISs.extend(MISs_mistral)

print(len(queries))
print(queries[-1])
print(len(MISs))
print(MISs[-1])

