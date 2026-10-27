# This is the install file that downloads all dependencies and libraries needed to run the program 

import os
import shutil
import subprocess
import sys
import sysconfig

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(HERE, "venv")


def in_virtual_env():
    return sys.prefix != sys.base_prefix


def externally_managed():
    # Debian marks its system Python with this file (PEP 668) and refuses "pip install" on it
    return os.path.exists(os.path.join(sysconfig.get_path("stdlib"), "EXTERNALLY-MANAGED"))


def venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def create_venv():
    print("This Python is externally managed (Debian), so creating a virtual environment in ./venv ...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    except subprocess.CalledProcessError:
        shutil.rmtree(VENV_DIR, ignore_errors=True)  # remove a half-built venv
        print("\nCould not create the virtual environment.")
        print("On Debian run:  sudo apt install python3-venv   then run this install script again.")
        sys.exit(1)


def main():
    os.chdir(HERE)  # so requirements.txt is found no matter which folder this is run from
    print("Installing dependencies...")

    python = sys.executable
    if externally_managed() and not in_virtual_env():
        if not os.path.exists(venv_python()):
            create_venv()
        python = venv_python()

    subprocess.check_call([python, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\n Done. Run 'python3 main.py' to start the app.")


if __name__ == "__main__":
    main() 