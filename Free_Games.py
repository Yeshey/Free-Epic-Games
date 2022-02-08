from queue import Empty
import webbrowser
import pyautogui
import os
import time
import sys          
import subprocess
import pyperclip
import lxml.html, pyotp, re, sys, time, traceback
from datetime import datetime

from os import getenv
from dotenv import load_dotenv
load_dotenv()
a = [getenv("EPIC_EMAIL").split(","), getenv("EPIC_PASSWORD").split(","), getenv("EPIC_TFA_TOKEN").split(",")]
credentialslist = [[a[j if len(str(j)) > 0 else None][i if len(str(i)) > 0 else None] for j in range(len(a))] for i in range(len(a[0]))]

# wait for a page to load: https://stackoverflow.com/questions/49807107/how-to-wait-for-the-page-to-fully-load-using-webbrowser-method

epic_home_url = "https://www.epicgames.com/site/en-US/home"
epic_store_url = "https://www.epicgames.com/store/en-US/?lang=en-US"
epic_login_url = "https://www.epicgames.com/id/login/epic"
epic_logout_url = 'https://www.epicgames.com/id/logout'

def open_browser(url, whichBrowser=Empty):
    '''
    if (whichBrowser == Empty):
        if sys.platform=='win32':
            subprocess.Popen(['start', url], shell= True)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
    
    if (whichBrowser == "firefox"):
        if sys.platform=='win32':
            subprocess.Popen(['start', url], shell= True)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            os.system("firefox --private-window " + url)
    '''
    if (whichBrowser == Empty):
        webbrowser.get().open(url)
    else:
        webbrowser.get(whichBrowser).open(url)

    #pyautogui.hotkey('ctrl', 'shift', 'n')
    time.sleep(2)
    pyautogui.press('F11')

def wait_to_see(rec_img, moveMouse = True, timeout=15):
    if (moveMouse == True):
        pyautogui.moveTo(1,1)
    print("looking for",rec_img, end="")
    start_time = datetime.now()
    while True:
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() >= timeout:
            print("time limit exceeded")
            return -1
        print(".", end="")
        img = pyautogui.locateCenterOnScreen('imgs/'+rec_img, grayscale=True, confidence=.7)
        if img is not None:
            break 
    return img

def go_to_url(url):
    pyautogui.hotkey('ctrl', 'l')
    for letter in url:    
        pyperclip.copy(letter)
        pyautogui.hotkey('ctrl', 'v')
    pyautogui.press ('enter')

def log_into_account(email, password, two_fa_key=None):
    time.sleep(1)
    wait_to_see('LanguageGlobe.png')
    
    # Log out if need be
    img = pyautogui.locateCenterOnScreen('imgs/LogedIn.png', grayscale=True, confidence=.7) 
    if (img is not None):
        go_to_url(epic_logout_url)
        '''
        pyautogui.moveTo(img)
        img = wait_to_see('SignOut.png', False)
        pyautogui.click(img)
        time.sleep(2)
        wait_to_see('LanguageGlobe.png')
        '''
    else:
        img = pyautogui.locateCenterOnScreen('imgs/signIn.png', grayscale=True, confidence=.7)
        if img is not None:
            pyautogui.click(img)

    img = wait_to_see("signInWithEpic.png")
    pyautogui.click(img)

    img = wait_to_see("EmailAddress.png")
    pyautogui.click(img)

    for letter in email:
        if letter == '@':
            pyperclip.copy('@')
            pyautogui.hotkey('ctrl', 'v')
        else:
            pyautogui.write(letter)
    pyautogui.press('Tab')
    pyautogui.write(password)
    for i in range(0, 4):
        pyautogui.press('Tab')
    pyautogui.press ('enter')

    img = wait_to_see("EnterTheScurityCodeToContenue.png", True, 10)
    if (img != -1):
        for i in range(0, 2):
            pyautogui.press('Tab')
        pyautogui.write(pyotp.TOTP(two_fa_key).now())
        for i in range(0, 4):
            pyautogui.press('Tab')
        pyautogui.press ('enter')

    go_to_url(epic_store_url)

def claim_free_games():
    wait_to_see('LanguageGlobe.png')
    while True:
        pyautogui.press ('down')
        #for i in range(0,5):
        img = pyautogui.locateCenterOnScreen('imgs/FREENOW.png', grayscale=True, confidence=.7)
        if img is not None:
            break  
        #img = pyautogui.locateCenterOnScreen('imgs/present.png', grayscale=True, confidence=.7)
        #if img is not None:
        #    break
    pyautogui.click(img)


if __name__ == '__main__':
    for credentials in credentialslist:
        open_browser(epic_store_url,"firefox")
        log_into_account(*credentials)
        claim_free_games()