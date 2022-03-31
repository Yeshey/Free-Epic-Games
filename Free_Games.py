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

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

load_dotenv()
a = [getenv("EPIC_EMAIL").split(","), getenv("EPIC_PASSWORD").split(","), getenv("EPIC_TFA_TOKEN").split(",")]
credentialslist = [[a[j if len(str(j)) > 0 else None][i if len(str(i)) > 0 else None] for j in range(len(a))] for i in range(len(a[0]))]

# wait for a page to load: https://stackoverflow.com/questions/49807107/how-to-wait-for-the-page-to-fully-load-using-webbrowser-method

epic_home_url = "https://www.epicgames.com/site/en-US/home"
epic_store_url = "https://www.epicgames.com/store/en-US/?lang=en-US"
epic_login_url = "https://www.epicgames.com/id/login/epic"
epic_logout_url = 'https://www.epicgames.com/id/logout'

def wait_to_see(rec_img, moveMouse = True, timeout=20, rec_img2=Empty):
    if (moveMouse == True):
        pyautogui.moveTo(1,1)

    print("looking for",rec_img, end="")
    start_time = datetime.now()

    while True:
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() >= timeout:
            print("time limit exceeded")
            return None

        print(".", end="")

        img = pyautogui.locateCenterOnScreen('./imgs/'+rec_img, grayscale=True, confidence=.8)
        if img is None:
            if (rec_img2 != Empty):
                img = pyautogui.locateCenterOnScreen('imgs/'+rec_img2, grayscale=True, confidence=.8)
        
        return img

class GUIBrowser:
    allow_pasting = False
    fullscreen = False
    bodyCoords_with_console = None
    computerHeight = 0
    computerWidth = 0

    # constructor
    def __init__(self, whichBrowser=Empty):
        #document.body.requestFullscreen.call(document.body)
        if (whichBrowser == Empty):
            webbrowser.get().open("imgs/FREENOW.png")
        else:
            if sys.platform=='win32':
                os.system("start firefox --private file://" + ROOT_DIR + "/imgs/FREENOW.png")
                #subprocess.Popen(['start', freenow], shell= True)
            elif sys.platform=='darwin':
                subprocess.Popen(['open', url])
            else:
                os.system("firefox --private file://" + ROOT_DIR + "/imgs/FREENOW.png &")
            #webbrowser.get(whichBrowser).open("imgs/FREENOW.png")

        while True:
            img = wait_to_see('FREENOW.png', True, 5)    
            if img is not None:
                break
            pyautogui.press('F11')
        self.bodyCoords_with_console = img
        if (self.run_javascript("IsFullscreen.js") == "NO"):
            pyautogui.press('F11')
        # set the true body Coords with console open:
        pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        self.bodyCoords_with_console = wait_to_see('FREENOW.png', True, 5)
        if img is None:
            print("something went wrong")
            exit()
        pyautogui.press('F12') # close console

        '''
        # javascript that adds an eventlistner that once the page comes into focus, deletes itself and puts in the clipboard if the browser is or not in fullscreen
        javaScriptFullScreen2 = ' document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler);  if(!window.screenTop && !window.screenY){ str = "YES" } else { str = "NO" } navigator.clipboard.writeText(str); });    '
        pyperclip.copy(javaScriptFullScreen2)
        img = wait_to_see('FREENOW.png', True, 5)
        if img is not None:
            
            
            pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
            time.sleep(0.3)
            pyautogui.write("allow pasting")
            pyautogui.press ('enter')
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
        '''

    def run_javascript(self, script_name):
        pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        time.sleep(0.3)
        if self.allow_pasting == False:
            pyautogui.write("allow pasting")
            self.allow_pasting = True
        pyautogui.press ('enter')
        # javascript that adds an eventlistner that once the page comes into focus, deletes itself and puts in the clipboard if the browser is or not in fullscreen
        pyperclip.copy('document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler); ')
        pyautogui.hotkey('ctrl', 'v')
        fo = open("./JSscripts/" + script_name, 'r').read() # opens script and pastes it
        pyperclip.copy(fo)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy('});')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press ('enter')
        pyautogui.click(self.bodyCoords_with_console) # because tab needs to be in focus to enter fullscrean
        pyautogui.press('F12')

        return clipboard.paste()


    def go_to_url(self, url):
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.1)
        pyperclip.copy(url)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.press ('enter')

    def log_into_account(self, email, password, two_fa_key=None):
        while (True):
            a = 1
            while (a > 0):
                a-=1
                self.go_to_url(epic_store_url)
                img = wait_to_see('LanguageGlobe.png')
                if img is None:
                    a+=1

            
            # Log out if need be
            img = pyautogui.locateCenterOnScreen('imgs/LogedIn.png', grayscale=True, confidence=.7) 
            if (img is not None):
                self.go_to_url(epic_logout_url)
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
            if (img is not None):  
                for i in range(0, 2):
                    pyautogui.press('Tab')
                pyautogui.write(pyotp.TOTP(two_fa_key).now())
                for i in range(0, 4):
                    pyautogui.press('Tab')
                pyautogui.press ('enter')

            while (True):
                self.go_to_url("file://" + ROOT_DIR + "/imgs/FREENOW.png")
                if (wait_to_see("FREENOW.png") is not None):
                    break

            self.go_to_url(epic_store_url)
            img = wait_to_see('LogedIn.png',True, 19)
            if (img is not None):
                break

    def claim_free_games(self):
        amount_of_free_games = -1

        while amount_of_free_games != 0:
            amount_of_free_games-=1
            self.go_to_url("file://" + ROOT_DIR + "/imgs/FREENOW.png")
            wait_to_see("FREENOW.png")
            self.go_to_url(epic_store_url)
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
        #print (webbrowser._browsers)
        ourBrowser = GUIBrowser("firefox")
        ourBrowser.log_into_account(*credentials)
        ourBrowser.claim_free_games()
        pyautogui.hotkey('ctrl', 'w')

        #open_browser("firefox")
        #log_into_account(*credentials)
        #claim_free_games()

'''
def run_javascript(script_name):
    pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
    time.sleep(0.3)
    pyautogui.write("allow pasting")
    pyautogui.press ('enter')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press ('enter')
    pyautogui.click(img) # because tab needs to be in focus to enter fullscrean
    pyautogui.press('F12') # close console
'''
