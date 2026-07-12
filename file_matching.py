import re
from pathlib import Path

from rules import get_rules, get_default_rubric

DEFAULT_RUBRIC: dict = get_default_rubric()
RULES = get_rules()

def match_file(filename: str):
    for rule in RULES:
        pattern = rule["pattern"]

        try:
            pattern = pattern.encode().decode('unicode_escape')
        except ValueError:
            pass

        match = re.search(pattern, filename)

        if match:
            return rule["folder_name"]
        
    file_ext = Path(filename).suffix

    for folder, extensions in DEFAULT_RUBRIC.items():
        if file_ext in extensions:
            return folder
    
    return '/Others'

if __name__ == '__main__':
    while True:
        print(match_file(input("Match: ")))