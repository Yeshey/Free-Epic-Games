

from multiprocessing.connection import wait
from queue import Empty
import subprocess
from tkinter.messagebox import NO
import webbrowser
import pyautogui
import os
import time
import pyperclip
import clipboard
import lxml.html, pyotp, re, sys, time, traceback
import tempfile
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
#import keyboard

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

#while keyboard.is_pressed('q') == False:
while True:
    img = pyautogui.locateCenterOnScreen('./../imgs/FREENOW.png', grayscale=True, confidence=0.7)
    if img is not None:
        #pyautogui.click(img)
        print("found")
    else:
        print("not found")
