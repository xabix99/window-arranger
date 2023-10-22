import sys
import os
import json
import pygetwindow
import datetime

SEARCH_PATH1 = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu')
SEARCH_PATH2 = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu')

# Function to log errors to a file
def log_error(error_msg):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_filename = f"LOG{current_date}.txt"
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()}: {error_msg}\n")

def search_for_lnks(folder):
    shortcuts = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".lnk"):
                shortcut_path = os.path.join(root, file)
                shortcuts.append(shortcut_path)
    return shortcuts

def generate_dict(programs):
    s1 = search_for_lnks(SEARCH_PATH1)
    s2 = search_for_lnks(SEARCH_PATH2)

    all_links = s1 + s2

    program_dict = {}

    for program in programs:
        for program_lnk in all_links:
            if program_lnk.endswith(f"{program}.lnk"):
                try:
                    windows = pygetwindow.getWindowsWithTitle(program)
                    if windows:
                        window = windows[0]
                        program_dict[program] = [window.title, window.left, window.top, window.width, window.height, program_lnk]
                except Exception as e:
                    error_msg = f"Error while processing program '{program}': {str(e)}"
                    log_error(error_msg)

    data_str = json.dumps(program_dict)
    with open("init.txt", "w", encoding="utf-8") as f:
        f.write(data_str)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py program1 program2 ...")
        sys.exit(1)

    programs = sys.argv[1:]
    generate_dict(programs)
