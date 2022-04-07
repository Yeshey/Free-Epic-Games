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
    ourBrowser = GUIBrowser("firefox")
    ourBrowser.go_to_url("https://store.epicgames.com/en-US/p/rogue-legacy")

    ourBrowser.waitForSiteToLoad()

    ourBrowser.open_console()

    results = ourBrowser.clickTextCoords("get")
