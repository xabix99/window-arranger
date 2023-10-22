import os
import ast
import sys
import subprocess
import pygetwindow
import datetime

# Function to log errors to a file
def log_error(error_msg):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_filename = f"LOG{current_date}.txt"
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()}: {error_msg}\n")

INIT_PATH = os.path.join(os.path.dirname(__file__), 'init.txt')

def main(dict):
    programs = list(dict.keys())

    for program in programs:
        try:
            subprocess.run(["powershell.exe", "ii", f"'{dict[program][5]}'"])
            windows = pygetwindow.getWindowsWithTitle(program)
            if windows:
                window = windows[0]
                window.restore()
                window.left = dict[program][1]
                window.top = dict[program][2]
                window.width = dict[program][3]
                window.height = dict[program][4]
        except Exception as e:
            error_msg = f"Error while processing program '{program}': {str(e)}"
            log_error(error_msg)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    dict_string = sys.argv[1]

    try:
        data = ast.literal_eval(dict_string)
        
        if not isinstance(data, dict):
            raise ValueError("Input is not a dictionary.")
        main(data)
    except (ValueError, SyntaxError) as e:
        error_msg = f"Error parsing the dictionary data: {str(e)}"
        log_error(error_msg)
