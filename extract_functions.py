import os
import json
import re
from tree_sitter_languages import get_language, get_parser

# Load the Julia language and initialize the parser
julia_language = get_language("julia")
parser = get_parser("julia")


def extract_functions(file_path):
    """Extracts functions from a Julia source file using Tree-sitter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node
    functions = []

    def traverse(node):
        if node.type == 'function_definition':
            func_code = code[node.start_byte:node.end_byte]
            functions.append(func_code)
        for child in node.children:
            traverse(child)

    traverse(root_node)
    return functions


def get_function_name(func_code):
    """Extracts the function name from the function code using regex."""
    match = re.search(r'function\s+([a-zA-Z0-9_]+)', func_code)
    return match.group(1) if match else None


# Directory containing the cloned repositories
repo_dir = 'julia_repos'

# Parse each Julia file in the `src` folder of each repository
all_functions = []
for repo in os.listdir(repo_dir):
    repo_path = os.path.join(repo_dir, repo)
    src_path = os.path.join(repo_path, 'src')  # Focus only on the `src` folder

    if os.path.isdir(src_path):
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith('.jl'):
                    file_path = os.path.join(root, file)
                    try:
                        functions = extract_functions(file_path)
                        all_functions.extend(functions)
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")

# Save the extracted functions to a JSON file for use in model training
output_file = 'extracted_julia_functions.json'
with open(output_file, 'w') as f:
    json.dump(all_functions, f)

print(f"Extracted {len(all_functions)} functions and saved them to {output_file}.")
