# This is the install file that downloads all dependencies and libraries needed to run the program 

import subprocess
import sys

def main():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\n Done. Run 'python main.py' to start the app.")


if __name__ == "__main__":
    main()