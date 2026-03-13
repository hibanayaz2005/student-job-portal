
import re
import sys

def resolve_conflicts(content):
    # This pattern matches standard git conflict markers
    # It tries to keep the HEAD version (top part)
    pattern = r'<<<<<<< HEAD\n([\s\S]*?)\n=======\n[\s\S]*?\n>>>>>>> [a-f0-9]+\n'
    resolved = re.sub(pattern, r'\1\n', content)
    return resolved

file_path = r'c:\internship\student-job-portal\CAREERBRIDGE\backend\dashboard\templates\dashboard\student-portal.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = resolve_conflicts(content)
    
    # Check if there are still markers left
    if '<<<<<<< HEAD' in new_content:
        print("Still markers left. Manual intervention might be needed.")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Resolved conflicts in student-portal.html")
except Exception as e:
    print(f"Error: {e}")
