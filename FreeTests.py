from multiprocessing.connection import wait
from pickle import TRUE
from queue import Empty
import subprocess
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
from src.screen import Screen # my class
from src.guiBrowser import GUIBrowser # my class

IMGS_FLDR = "src/imgs/"

if __name__ == '__main__':
    
    #imgCoords = Screen.find(IMGS_FLDR+"FREENOW.png",show=True)
    #if (imgCoords != None):
    #    pyautogui.click(imgCoords[0],imgCoords[1])

    #ourBrowser = GUIBrowser("firefox")
    #ourBrowser.go_to_url("https://store.epicgames.com/en-US/p/rogue-legacy")

    #ourBrowser.waitForSiteToLoad()

    #ourBrowser.open_console()

    #results = ourBrowser.clickTextCoords("get")
    
    color = (0, 120, 242)
    s = pyautogui.screenshot()
    for x, y in ((w1, w2) for w1 in range(s.width) for w2 in range(int(s.height/2), s.height)):
        if s.getpixel((x, y)) == color:
            pyautogui.move(x+5, y+5) 
            time.sleep(1)
            pyautogui.click(x+5, y+5) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.click()
            pyautogui.click(x+10, y+10)
            break
