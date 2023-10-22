import sys
import os
import json
import pygetwindow

SEARCH_PATH1 = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu')
SEARCH_PATH2 = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu')
   
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
    
    allblks = s1 + s2
    
    dict = {}
    
    for program in programs:
        for program_lnk in allblks:
            if program_lnk.endswith(f"{program}.lnk"):
                windows = pygetwindow.getWindowsWithTitle(program)
                window = windows[0]
                dict[program] = [window.title, window.left, window.top, window.width, window.height, program_lnk]
    
    data_str = '"' + str(dict) + '"'
    with open("init.txt", "w", encoding="utf-8") as f:
        f.write(data_str)  
        
if __name__ == '__main__':
    programs = sys.argv[1:]
    generate_dict(programs)