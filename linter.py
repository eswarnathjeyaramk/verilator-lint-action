import os
import sys
import json
import subprocess

files_str = os.environ.get('INPUT_FILES', '')
files = files_str.split()
severity = os.environ.get('INPUT_SEVERITY', 'warning')

# This is the magical file GitHub provides for us to pass data back to the workflow
output_file = os.environ.get('GITHUB_OUTPUT')

results = {}

# Set flags based on severity input
flags = ['-Wall']
if severity == 'warning':
    flags.append('-Wno-fatal')

for f in files:
    if not os.path.exists(f):
        results[f] = "file_not_found"
        continue

    cmd = ['verilator', '--lint-only'] + flags + [f]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results[f] = "pass"
    except subprocess.CalledProcessError:
        results[f] = "fail"

json_results = json.dumps(results)

# Write the output in the exact format GitHub Actions requires: key=value
with open(output_file, 'a') as f:
    f.write(f"results={json_results}\n")

print(f"Linting completed. Output: {json_results}")
