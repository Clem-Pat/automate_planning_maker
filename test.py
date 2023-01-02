import tkinter as tk
from tkinter import ttk
import os

def start(bool):
    if bool:
        print('start again')
        os.system('python test.py')
    else: print('no restart')

if __name__ == '__main__':
    start(True)
else:
    print('restart but from elsewhere')
