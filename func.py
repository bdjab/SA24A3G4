import json

# Load the JSON file
with open('extracted_julia_functions.json', 'r') as f:
    functions = json.load(f)

# Print the number of functions and the first few entries
print(f"Total functions extracted: {len(functions)}")
for i, func in enumerate(functions[:5]):  # Print first 5 functions
    print(f"\nFunction {i + 1}:\n{func}")

