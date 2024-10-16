import re

def separate_file_content(file_path):
    pattern = r'Misconception (\d+)/1869'
    sections = []
    current_section = ""
    
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Find all separators
        separators = re.finditer(pattern, content)
        
        # Get the start positions of all separators
        separator_positions = [match.start() for match in separators if 0 <= int(match.group(1)) <= 1869]
        
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

# Example usage
file_path = 'generate_3/whole_QAs_1.txt'
separated_sections = separate_file_content(file_path)

print(f"Found {len(separated_sections)} sections:")
# for i, section in enumerate(separated_sections, 1):
#     print(f"Section {i}:")
#     print(section[:100] + "..." if len(section) > 100 else section)  # Print first 100 chars of each section
#     print()