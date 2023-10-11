import os
import webbrowser
import json
from datetime import datetime
from time import sleep
import pygetwindow

def list_shortcuts_with_extension(folder, extension):
    shortcuts = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                shortcut_path = os.path.join(root, file)
                shortcuts.append(shortcut_path)
    return shortcuts

def generate_dict():
    data_dict = {}
    
    winstosearch = []
    setup_file_path = os.path.join(os.path.dirname(__file__), 'setup.txt')
    curr_dt = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

    if not os.path.exists(setup_file_path):
        log_file_path = os.path.join(os.path.dirname(__file__), f'log_{curr_dt}.txt')
        with open(log_file_path, 'w') as log_file:
            log_file.write("No setup.txt file found.")
    else:
        with open(setup_file_path, 'r') as file:
            winstosearch = [element.strip() for element in file.read().split(',')]
            
        for program in winstosearch:
            windows = pygetwindow.getWindowsWithTitle(program)
            
            if windows:
                window = windows[0]
                
                all_users_start_menu = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu')
    
                current_user_start_menu = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu')
    
                all_users_shortcuts = list_shortcuts_with_extension(all_users_start_menu, ".lnk")
                current_user_shortcuts = list_shortcuts_with_extension(current_user_start_menu, ".lnk")
    
                all_shortcuts = all_users_shortcuts + current_user_shortcuts
    
                for shortcut in all_shortcuts:
                    if shortcut.endswith(f"{program}.lnk"):
                        shortcut_path = shortcut
                        data_dict[program] = [window.title, window.left, window.top, window.width, window.height, shortcut_path]
        with open(os.path.join(os.path.dirname(__file__), 'init.txt'), 'w') as file:
            json.dump(data_dict, file)
        os.remove(setup_file_path)
def execontent(data_dict):
    all_window_names = list(data_dict.keys())
    window_number = len(all_window_names)
    
    for program in all_window_names:
        program_url = f"file://{data_dict[program][-1].replace('\\', '/')}"
        webbrowser.open(program_url)
        sleep(0.2)
    
    sleep(8)
    
    while True:
        try:
            for i in range(window_number):
                window_title = all_window_names[i]
                windows = pygetwindow.getWindowsWithTitle(window_title)
                
                if windows:
                    window = windows[0]
                    window.restore()
                    window.left = data_dict[window_title][1]
                    window.top = data_dict[window_title][2]
                    window.width = data_dict[window_title][3]
                    window.height = data_dict[window_title][4]
        except Exception as e:
            sleep(0.2)
            continue
        else:
            break
    sleep(3)

def main():
    setup_file_path = os.path.join(os.path.dirname(__file__), 'setup.txt')
    init_file_path = os.path.join(os.path.dirname(__file__), 'init.txt')
    
    if not os.path.exists(setup_file_path) and not os.path.exists(init_file_path):
        curr_dt = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        log_file_path = os.path.join(os.path.dirname(__file__), f'log_{curr_dt}.txt')
        with open(log_file_path, "w") as log_file:
            log_file.write("No setup.txt or init.exe file found.")
            
    elif os.path.exists(setup_file_path):
        generate_dict()
    
    elif os.path.exists(init_file_path):
        with open(os.path.join(init_file_path), 'r') as file:
            data_dict = json.load(file)
        execontent(data_dict)
    
    else:
        open("log.txt", "w+")
        curr_dt = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        log_file_path = os.path.join(os.path.dirname(__file__), f'log_{curr_dt}.txt')
        with open(log_file_path, "w+") as log_file:
            log_file.write("Both init.txt and setup.txt file found. Remove one and re-run.")

if __name__ == '__main__':
    main()
