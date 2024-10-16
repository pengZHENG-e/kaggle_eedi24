def inver_json2lsts(path):
    import json
    # Load the JSON structure from the file
    with open(path, 'r') as file:
        json_data = json.load(file)

    # Extract the queries and contexts
    queries_dict = json_data["queries"]
    contexts_dict = json_data["corpus"]

    # Convert the dictionaries back to lists
    queries = list(queries_dict.values())
    MISs = list(contexts_dict.values())

    # Print the queries and contexts lists
    # print("Queries:", queries)
    # print("Contexts:", contexts)
    print(len(queries))
    print(len(MISs))
    
    return queries, MISs

queries_1, MISs_1 = inver_json2lsts('merge/mix_data_17673.json')


########################################################################
# UNSEEN
########################################################################
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

queries_2 = []
MISs_2 = []

queries_2.extend(queries_groq)
queries_2.extend(queries_gemini)
queries_2.extend(queries_mistral)
MISs_2.extend(queries_groq)
MISs_2.extend(queries_gemini)
MISs_2.extend(MISs_mistral)



########################################################################
# SEEN
########################################################################
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

queries_3 = []
MISs_3 = []

queries_3.extend(queries_o)
queries_3.extend(queries_mistral)
MISs_3.extend(MISs_o)
MISs_3.extend(MISs_mistral)


########################################################################
# MERGE
########################################################################
queries = []
MISs = []

queries.extend(queries_1)
queries.extend(queries_2)
queries.extend(queries_3)

MISs.extend(MISs_1)
MISs.extend(MISs_2)
MISs.extend(MISs_3)

print(len(queries))
print(queries[0])
print(len(MISs))
print(MISs[-1])


########################################################################
# TO JSON
########################################################################
import uuid
import json

# Create UUIDs for each query and context
queries_dict = {str(uuid.uuid4()): query for query in queries}
contexts_dict = {str(uuid.uuid4()): context for context in MISs}

# Create relevant_docs dictionary with one-to-one mapping
relevant_docs = {}
query_ids = list(queries_dict.keys())
context_ids = list(contexts_dict.keys())

for i, query_id in enumerate(query_ids):
    relevant_docs[query_id] = [context_ids[i]]

# Create the final JSON structure
json_structure = {
    "queries": queries_dict,
    "corpus": contexts_dict,
    "relevant_docs": relevant_docs,
    "mode": "text"
}

# Save JSON to a file
with open('mix_data_29101.json', 'w') as file:
    json.dump(json_structure, file, indent=4)

