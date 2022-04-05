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

# wait for a page to load: https://stackoverflow.com/questions/49807107/how-to-wait-for-the-page-to-fully-load-using-webbrowser-method

if __name__ == '__main__':
    # get credentials
    load_dotenv()
    a = [getenv("EPIC_EMAIL").split(","), getenv("EPIC_PASSWORD").split(","), getenv("EPIC_TFA_TOKEN").split(",")]
    credentialslist = [[a[j if len(str(j)) > 0 else None][i if len(str(i)) > 0 else None] for j in range(len(a))] for i in range(len(a[0]))]

    # for every account
    for credentials in credentialslist:
        #print (webbrowser._browsers)
        ourBrowser = GUIBrowser("firefox")
        ourBrowser.log_into_account(*credentials)
        ourBrowser.claim_free_games()
        pyautogui.hotkey('ctrl', 'w')
