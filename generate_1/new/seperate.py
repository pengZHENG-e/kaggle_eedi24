import re

def separate_file_content(file_path):
    pattern = r'Misconception (\d+)/2587'
    sections = []
    current_section = ""
    
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Find all separators
        separators = re.finditer(pattern, content)
        
        # Get the start positions of all separators
        separator_positions = [match.start() for match in separators if 0 <= int(match.group(1)) <= 2587]
        
        # Add the end of the file as the last position
        separator_positions.append(len(content))
        
        # Split the content based on separator positions
        for i in range(len(separator_positions)):
            if i == 0:
                # First section starts from the beginning of the file
                start = 0
            else:
                start = separator_positions[i-1]
            
            end = separator_positions[i]
            section = content[start:end].strip()
            
            if section:
                sections.append(section)
    
    return sections

# # Example usage
# file_paths = [
#     'generate_1/new/whole_QMs.txt',
#     # 'generate_1/new/whole_QMs_1.txt',
#     # 'generate_1/new/whole_QMs_2.txt'
#     ]

# separated_sections = []

# for file_path in file_paths:
#     separated_sections.extend(separate_file_content(file_path))

# print(f"Found {len(separated_sections)} sections:")
# for i, section in enumerate(separated_sections, 1):
#     print(f"Section {i}:")
#     print(section[:100] + "..." if len(section) > 100 else section)  # Print first 100 chars of each section
#     print()