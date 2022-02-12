from queue import Empty
import webbrowser
import pyautogui
import os
import time
import sys          
import subprocess
import pyperclip
import lxml.html, pyotp, re, sys, time, traceback
import tempfile
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
    isfullscreanurl = 'data:text/html,<title>FullScreen?</title><body><div class="answer"></div></body><style>body{background-color:white !important;} .answer{position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);height: 90vh;width: 90vw;display:grid;place-items: center;font-size: min(80vh,40vw);font-family:"Segoe UI", Tahoma, Geneva, Verdana, sans-serif;}</style><script>function updt() { if((window.fullScreen) || (window.innerWidth == screen.width && window.innerHeight == screen.height)) {str = "YES"} else {str = "NO"} document.querySelector(".answer").innerHTML=str } window.addEventListener("resize", () => { updt() }); updt()</script>'

    #https://www.kite.com/python/answers/how-to-write-to-an-html-file-in-python
    html = '<html> ...  generated html string ...</html>'
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)

    exit()

    if (whichBrowser == Empty):
        webbrowser.get().open(isfullscreanurl)
    else:
        webbrowser.get(whichBrowser).open(isfullscreanurl)

    

    #pyautogui.hotkey('ctrl', 'shift', 'n')
    img = wait_to_see('NO.png', True, 20, 'YES.png')
    if img is None:
        pyautogui.press('F11')
        img = wait_to_see('NO.png', True, 20, 'YES.png')
    img = pyautogui.locateCenterOnScreen('imgs/NO.png', grayscale=True, confidence=.7)
    if img is not None:
        pyautogui.press('F11')

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
    #pyautogui.hotkey('ctrl', 'l')
    #for letter in url:    
    #    pyperclip.copy(letter)
    #    pyautogui.hotkey('ctrl', 'v')
    #pyautogui.press ('enter')
    pyautogui.hotkey('ctrl', 'l')
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press ('enter')

def log_into_account(email, password, two_fa_key=None):
    time.sleep(1)
    wait_to_see('LanguageGlobe.png')
    
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

    go_to_url(epic_store_url)

def claim_free_games():
    wait_to_see('LanguageGlobe.png')
    while True:
        pyautogui.press ('down')
        #for i in range(0,5):
        img = pyautogui.locateCenterOnScreen('imgs/FREENOW.png', grayscale=True, confidence=.7)
        if img is not None:
            break  
    pyautogui.click(img)

    # wait to see in_library.png or get.png
    img = wait_to_see('get.png', True, 20, 'IN_LIBRARY.png')

    img = pyautogui.locateCenterOnScreen('imgs/get.png', grayscale=True, confidence=.7) 
    if img is not None:
        pyautogui.click(img)
        wait_to_see('PLACE_ORDER.png')
    else:
        return


if __name__ == '__main__':
    for credentials in credentialslist:
        open_browser(epic_store_url,"firefox")
        log_into_account(*credentials)
        claim_free_games()