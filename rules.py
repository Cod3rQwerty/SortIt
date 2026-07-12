import json
from pathlib import Path


def get_default_rubric(output:bool = False):

    config_path = Path(__file__).parent / "rules.json"

    with open(config_path, "r") as file:
        config_data = json.load(file)

    if output:
        print("Successfully loaded DEFAULT_RUBRIC:")
        print(config_data["default_rubric"])

    return config_data["default_rubric"]

# FORMAT OF RULES:
# {
#       "folder_name": "Images/Holidays",
#       "pattern": "regex"
#     },

def add_rule(folder:str, pattern:str, report:bool=True):
    # 1. Locate the rules file
    config_path = Path(__file__).parent / "rules.json"
    
    # 2. Load the existing data
    with open(config_path, "r") as file:
        config_data = json.load(file)
    
    # 3. Create the new rule object
    new_rule = {
        "folder_name": folder,
        "pattern": pattern
    }
    
    # 4. Append it to the custom_rules array
    config_data["custom_rules"].append(new_rule)
    
    # 5. Write the entire updated dictionary back to the JSON file
    with open(config_path, "w") as file:
        json.dump(config_data, file, indent=4)
        
    if report: print(f"[✔] Rule added successfully: Files matching '{pattern}' will go to '{folder}'")


def remove_rule(folder: str, report:bool=True):
    # 1. Locate the rules file
    config_path = Path(__file__).parent / "rules.json"
    
    # 2. Load the existing data
    with open(config_path, "r") as file:
        config_data = json.load(file)
        
    # Track the number of rules before filtering so we know if we actually deleted something
    initial_count = len(config_data["custom_rules"])
    
    # 3. Filter out any rule that matches the target folder name
    config_data["custom_rules"] = [
        rule for rule in config_data["custom_rules"] 
        if rule["folder_name"] != folder
    ]
    
    # 4. If a rule was successfully removed, save the changes
    if len(config_data["custom_rules"]) < initial_count:
        with open(config_path, "w") as file:
            json.dump(config_data, file, indent=4)
        if report: print(f"[✔] Successfully removed all rules routing to '{folder}'")
    else:
        if report: print(f"[!] No rules found that route to '{folder}'")

def get_rules(output:bool = False):
    # 1. Locate the rules file
    config_path = Path(__file__).parent / "rules.json"
    
    # 2. Load the existing data
    with open(config_path, "r") as file:
        config_data = json.load(file)

    rules = config_data["custom_rules"]

    if output:
        print(f"List of custom rules:")
        for rule in rules:
            print(f"Folder Name: {rule["folder_name"]}")
            print(f"Pattern: {rule["pattern"]}")
            print()
    
    return rules