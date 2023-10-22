import os
import shutil
import subprocess
import os.path

path = os.path.join(os.path.dirname(__file__))
main_exe = os.path.join(f"{path}", 'main.exe')
main_spec = os.path.join(f"{path}", 'main.spec')
dist_path = os.path.join(f"{path}", 'dist')
build_path = os.path.join(f"{path}", 'build')
ready_exe_path = os.path.join(f"{path}", 'GetWindowPosition.exe')

if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
if os.path.exists(build_path):
    shutil.rmtree(build_path)
if os.path.isfile(main_spec):
    os.remove(main_spec)
if os.path.isfile(ready_exe_path):
    os.remove(ready_exe_path)
    
subprocess.run(["pyinstaller", "--onefile", "--icon", "GetWindowPosition.ico", "main.py"])

shutil.move(os.path.join(f"{dist_path}","main.exe"), f"{main_exe}")

os.rename(f"{main_exe}", f"{ready_exe_path}")

shutil.rmtree(dist_path)
shutil.rmtree(build_path)
os.remove(main_spec)
