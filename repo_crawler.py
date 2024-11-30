import pandas as pd
import subprocess

# Load the CSV file
file_path ='test_result.gz'
df = pd.read_csv(file_path)

# Directory where repositories will be cloned
clone_directory = 'julia_repos'

# Create the directory if it doesn't exist
import os
os.makedirs(clone_directory, exist_ok=True)

# Loop through the repository names and clone each
for repo_name in df['name']:
    repo_url = f"https://github.com/{repo_name}.git"
    print(f"Cloning {repo_url}...")
    subprocess.run(['git', 'clone', '--depth', '1', repo_url, os.path.join(clone_directory, repo_name.split('/')[-1])])

print("Cloning complete.")
