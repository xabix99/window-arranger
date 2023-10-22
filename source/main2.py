import os
import ast
import sys
import subprocess
import pygetwindow

INIT_PATH = os.path.join(os.path.dirname(__file__), 'init.txt')

def main(dict):
    programs = list(dict.keys())

    for program in programs:
        subprocess.run(["powershell.exe", "ii", f"'{dict[program][5]}'"])
        windows = pygetwindow.getWindowsWithTitle(program)
        if windows:
            window = windows[0]
            window.restore()
            window.left = dict[program][1]
            window.top = dict[program][2]
            window.width = dict[program][3]
            window.height = dict[program][4]

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
        subprocess.run(["powershell.exe", "Write-Output", "Error_parsing_the_dictionary_data:_{e}"])