import subprocess
import sys
import os

py_path = sys.executable
w_path = os.getcwd()

print("Generating valid accounts....")
subprocess.call([py_path, os.path.join(w_path, "main.py")])

print("Validating...")
subprocess.call([py_path, os.path.join(w_path, "checker.py")])

print("Cleaning up...")

# os.remove(os.path.join(w_path, "possibilities.out.txt")) # (Deprecated)
os.remove(os.path.join(w_path, "valid_possibilities.out.txt"))

print("Done.")
