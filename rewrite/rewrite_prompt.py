import pandas as pd
import os
from groq import Groq

pd.set_option('display.max_colwidth', None)

# Data Loading
train = pd.read_csv("data/train.csv")
misconception_mapping = pd.read_csv("data/misconception_mapping_updated.csv")

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

length = len(misconception_mapping["MisconceptionName"])

# Open a single file to write all responses
with open("all_responses_0_240.txt", "a") as response_file:

    # Start the loop from misconception 240
    for idx in range(0, 240):
        mis = misconception_mapping["MisconceptionName"][idx]
        print(f"Processing misconception {idx}/{length}: {mis}")
        
        prompt = f"""
A Diagnostic Question is a multiple-choice question with four options: one correct answer and three distractors (incorrect answers). Each distractor is carefully crafted to capture a specific misconception.  

For example: 5*4+6/2 = ? 

A. 23 

B. 13 

C. 25 

D. 35 

If a student selects the distractor "13," they may have the misconception "Carries out operations from left to right regardless of priority order." 

Tagging distractors with appropriate misconceptions is essential but time-consuming, and it is difficult to maintain consistency across multiple human labellers. Misconceptions vary significantly in terms of description granularity, and new misconceptions are often discovered as human labellers tag distractors in new topic areas. 

Based on the context provided, please expand the following misconception to make it more complete and applicable to various distractors. Answer only with the augmented misconception and nothing else.  

The misconception to be expanded is: {mis} 
"""

        chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.1-70b-versatile",
                )

        response_content = chat_completion.choices[0].message.content

        # Write the response to the file
        response_file.write(f"Misconception {idx}: {mis}\n")
        response_file.write(f"Expanded misconception:\n{response_content}\n\n")

        misconception_mapping.at[idx, "MisconceptionName_rewrite_1"] = response_content

# Save the updated DataFrame
misconception_mapping.to_csv("data/misconception_mapping_updated_0_240.csv", index=False)

print("All responses have been written to all_responses.txt")
