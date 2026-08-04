# File: main.py

import os
import sys

# Memastikan Python mengenali folder root agar 'src' bisa diimpor dengan aman
# (Sabuk pengaman agar tidak error di berbagai terminal/OS)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.cli.menu_utama import MenuCLI

if __name__ == "__main__":
    app = MenuCLI()
    app.menu_utama()