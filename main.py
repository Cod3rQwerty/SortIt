from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from rules import get_default_rubric, add_rule, remove_rule, get_rules
from file_matching import match_file

DEFAULT_RUBRIC = get_default_rubric()

def user_add_rule():
    pattern = input("RegEx Pattern: ")
    folder_name = input("Folder: ")

    rule = {
        "folder_name": folder_name,
        "pattern": pattern
    }

    if rule in get_rules():
        print("This rule already exists.")
    else:
        add_rule(folder_name, pattern)

def user_remove_rule():
    folder = input("Folder to remove: ")

    remove_rule(folder, report=True)


def user_view_rules():
    rules = get_rules(output=False)
    
    if not rules:
        print("Your custom rules list is currently empty.")
    else:
        get_rules(output=True)

def user_get_folder_and_contents():
    folder = input("What folder would you like to sort? Type 'dialog' to pick from a dialog: ")

    if folder == 'dialog':
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        selected_folder = filedialog.askdirectory(title="Select Folder to SortIt")
        root.destroy()
            
        folder = selected_folder
        print(f"Selected: {folder}")

    folder_path = Path(folder)

    filenames = [f.name for f in folder_path.iterdir() if f.is_file()]

    return folder, filenames

def get_destinations(filenames: list):

    destinations = []

    for filename in filenames:
        destinations.append((filename, match_file(filename)))
    
    return destinations

def move_files(destinations, root_folder):
    for filename, destination in destinations:
        # 1. Clean up the destination subfolder name
        clean_destination = str(destination).lstrip("\\/")

        # 2. Get the full paths for the source file and target directory
        source_file_path: Path = Path(root_folder) / filename
        target_directory: Path = Path(root_folder) / clean_destination
        
        # 3. Combine target directory and filename to get the final file path
        final_file_path: Path = target_directory / filename

        # 4. Create the new folder safely if it doesn't exist yet
        target_directory.mkdir(parents=True, exist_ok=True)

        # 5. Move ze file! 
        # .rename() works instantly because it just updates the file system pointer
        source_file_path.rename(final_file_path)

        print(f"[➔] Moved: {filename} -> {clean_destination}/")



if __name__ == '__main__':
    print("\n--- SortIt CLI File Organizer ---")
    print("[a] Add Custom Rule")
    print("[r] Remove Custom Rule")
    print("[g] Get/View All Rules")
    print("[s] Sort a Folder")
    print("[q] Quit App")
    print("-----------------------------------")

    while True:
        try:
            c = input("Choice: ").strip().lower()
            
            if c == 'a':
                user_add_rule()
            elif c == 'r':
                user_remove_rule()
            elif c == 'g':
                user_view_rules()
            elif c == 's':
                root_folder, filenames = user_get_folder_and_contents()
                destinations = get_destinations(filenames)
                move_files(destinations, root_folder)
        except Exception as e:
            print(f"Error encountered: {e}")

        print()

            

