
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

queries, MISs = inver_json2lsts('merge/mix_data_17673.json')