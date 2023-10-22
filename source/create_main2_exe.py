import os
import shutil
import subprocess
import os.path

path = os.path.join(os.path.dirname(__file__))
main_exe = os.path.join(f"{path}", 'main2.exe')
main_spec = os.path.join(f"{path}", 'main2.spec')
dist_path = os.path.join(f"{path}", 'dist')
build_path = os.path.join(f"{path}", 'build')
ready_exe_path = os.path.join(f"{path}", 'AutoWindowArranger.exe')

if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
if os.path.exists(build_path):
    shutil.rmtree(build_path)
if os.path.isfile(main_spec):
    os.remove(main_spec)
if os.path.isfile(ready_exe_path):
    os.remove(ready_exe_path)
    
subprocess.run(["pyinstaller", "--onefile", "--icon", "AutoWindowArranger.ico", "main2.py"])

shutil.move(os.path.join(f"{dist_path}","main2.exe"), f"{main_exe}")

os.rename(f"{main_exe}", f"{ready_exe_path}")

shutil.rmtree(dist_path)
shutil.rmtree(build_path)
os.remove(main_spec)