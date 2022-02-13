#!/usr/bin/python
from multiprocessing.connection import wait
from queue import Empty
import webbrowser
import pyautogui
import os
import time
import sys          
import subprocess
import pyperclip
import clipboard
import lxml.html, pyotp, re, sys, time, traceback
import tempfile
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

load_dotenv()
a = [getenv("EPIC_EMAIL").split(","), getenv("EPIC_PASSWORD").split(","), getenv("EPIC_TFA_TOKEN").split(",")]
credentialslist = [[a[j if len(str(j)) > 0 else None][i if len(str(i)) > 0 else None] for j in range(len(a))] for i in range(len(a[0]))]

# wait for a page to load: https://stackoverflow.com/questions/49807107/how-to-wait-for-the-page-to-fully-load-using-webbrowser-method

epic_home_url = "https://www.epicgames.com/site/en-US/home"
epic_store_url = "https://www.epicgames.com/store/en-US/?lang=en-US"
epic_login_url = "https://www.epicgames.com/id/login/epic"
epic_logout_url = 'https://www.epicgames.com/id/logout'

def open_browser(whichBrowser=Empty):
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

    #document.body.requestFullscreen.call(document.body)

    freenow="imgs/FREENOW.png"

    if (whichBrowser == Empty):
        webbrowser.get().open(freenow)
    else:
        webbrowser.get(whichBrowser).open(freenow)

    # javascript that adds an eventlistner that once the page comes into focus, deletes itself and enables fullscreen
    # javaScriptFullScreen = 'document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler); document.body.requestFullscreen(); });'
    # WTF IS THIS TRASH FULLSCREEN?!? CANT EVEN USE CTRL+L

    # javascript that adds an eventlistner that once the page comes into focus, deletes itself and puts in the clipboard if the browser is or not in fullscreen
    javaScriptFullScreen2 = ' document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler);  if(!window.screenTop && !window.screenY){ str = "YES" } else { str = "NO" } navigator.clipboard.writeText(str); });    '
    pyperclip.copy(javaScriptFullScreen2)

    img = wait_to_see('FREENOW.png', True, 5)
    if img is not None:
        pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press ('enter')
        pyautogui.click(img) # because tab needs to be in focus to enter fullscrean
        pyautogui.press('F12')

        isFullScreen = clipboard.paste()
        if (isFullScreen == 'NO'):
            pyautogui.press('F11')
        elif (isFullScreen != 'YES'):
            print("Couldnt determine if fullscreen")
            exit()
    else:
        pyautogui.press('F11')
        time.sleep(1)

def wait_to_see(rec_img, moveMouse = True, timeout=20, rec_img2=Empty):
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
        if (rec_img2 != Empty): 
            img = pyautogui.locateCenterOnScreen('imgs/'+rec_img2, grayscale=True, confidence=.7)
            if img is not None:
                break 
    return img

def go_to_url(url):
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.1)
    pyperclip.copy(url)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.press ('enter')

def log_into_account(email, password, two_fa_key=None):
    a = 1
    while (a > 0):
        a-=1
        go_to_url(epic_store_url)
        img = wait_to_see('LanguageGlobe.png')
        if img is None:
            a+=1

    
    # Log out if need be
    img = pyautogui.locateCenterOnScreen('imgs/LogedIn.png', grayscale=True, confidence=.7) 
    if (img is not None):
        go_to_url(epic_logout_url)
    else:
        img = pyautogui.locateCenterOnScreen('imgs/signIn.png', grayscale=True, confidence=.7)
        if img is not None:
            pyautogui.click(img)

    img = wait_to_see("signInWithEpic.png")
    pyautogui.click(img)

    img = wait_to_see("EmailAddress.png")
    pyautogui.click(img)

    pyperclip.copy(email)
    pyautogui.hotkey('ctrl', 'v')

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

def claim_free_games():
    amount_of_free_games = -1

    while amount_of_free_games != 0:
        amount_of_free_games-=1
        go_to_url("file://" + ROOT_DIR + "/imgs/FREENOW.png")
        wait_to_see("FREENOW.png")
        go_to_url(epic_store_url)
        wait_to_see('LanguageGlobe.png')
        key_to_press = 'space'
        while True:
            img = pyautogui.locateCenterOnScreen('imgs/FREENOW.png', grayscale=True, confidence=.7)
            if img is not None:
                imgs_list = list(pyautogui.locateAllOnScreen('imgs/FREENOW.png', grayscale=True, confidence=0.95))
                if(len(imgs_list) == 0):
                    key_to_press = "up"
                else:
                    if (amount_of_free_games < 0): # only updates one time, then never again
                        amount_of_free_games = len(imgs_list)-1 # -1 because we're already in the first iteration
                    img = imgs_list[amount_of_free_games-1]
                    pyautogui.click(x=img.left+(img.width/2), y=img.top+(img.height/2))
                    break

            pyautogui.press (key_to_press)
            
        # wait to see in_library.png or get.png
        img = wait_to_see('get.png', True, 20, 'IN_LIBRARY.png')

        img = pyautogui.locateCenterOnScreen('imgs/get.png', grayscale=True, confidence=.7) 
        if img is not None:
            pyautogui.click(img)
            img = wait_to_see('PLACE_ORDER.png')
            if img is not None:
                pyautogui.click(img)
                img = wait_to_see('I_Agree.png')
                if img is not None:
                    pyautogui.click(img)
                    wait_to_see('Thank_u_for_buying.png',True, 7)
                    return
            
            print("Something changed!")
            exit()
        else:
            print("No free games here")
            return


if __name__ == '__main__':
    for credentials in credentialslist:
        open_browser("firefox")
        log_into_account(*credentials)
        claim_free_games()
        pyautogui.hotkey('ctrl', 'w')