from multiprocessing.connection import wait
from pickle import TRUE
from queue import Empty
import subprocess
import webbrowser
from xml.dom import minicompat
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
import config #my config

epic_home_url = "https://www.epicgames.com/site/en-US/home"
epic_store_url = "https://www.epicgames.com/store/en-US/?lang=en-US"
epic_login_url = "https://www.epicgames.com/id/login/epic"
epic_logout_url = 'https://www.epicgames.com/id/logout'

'''def wait_to_see(rec_img, moveMouse = True, timeout=20, rec_img2=Empty):
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
        img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+rec_img, grayscale=True, confidence=.8)
        if img is not None:
            break 
        if (rec_img2 != Empty): 
            img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+rec_img2, grayscale=True, confidence=.8)
            if img is not None:
                break 
    return img'''

class GUIBrowser:
    allow_pasting = False
    fullscreen = False
    bodyCoords_with_console = None
    computerHeight = 0
    computerWidth = 0
    console_open = False

    # constructor
    def __init__(self, whichBrowser=Empty):
        #document.body.requestFullscreen.call(document.body)
        if (whichBrowser == Empty):
            webbrowser.get().open(config.IMGS_FLDR+"FREENOW.png")
        else:
            if sys.platform=='win32':
                os.system("start firefox --private file://" + config.ROOT_DIR + "/imgs/FREENOW.png")
                #subprocess.Popen(['start', freenow], shell= True)
            elif sys.platform=='darwin':
                subprocess.Popen(['open', url])
            else:
                os.system("firefox --private file://" + config.ROOT_DIR + "/imgs/FREENOW.png &")

        while True:
            img = Screen.wait_to_see('FREENOW.png', moveMouse= True, timeout=5)    
            if img is not None:
                break
            pyautogui.press('F11')
        self.bodyCoords_with_console = img
        if (self.run_javascript("IsFullscreen.js") == "NO"):
            pyautogui.press('F11')
        # set the true body Coords with console open:
        pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        self.bodyCoords_with_console = Screen.wait_to_see('FREENOW.png', moveMouse = True, timeout=5)
        if img is None:
            print("something went wrong")
            exit()
        pyautogui.press('F12') # close console

    def run_javascript(self, script_name):
        if (not self.console_open):
            pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        time.sleep(0.3)
        if self.allow_pasting == False:
            pyautogui.write("allow pasting")
            self.allow_pasting = True
        pyautogui.press ('enter')
        # javascript that adds an eventlistner that once the page comes into focus, deletes itself and puts in the clipboard if the browser is or not in fullscreen
        pyperclip.copy('document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler); ')
        pyautogui.hotkey('ctrl', 'v')
        fo = open("./src/JSscripts/" + script_name, 'r').read() # opens script and pastes it
        pyperclip.copy(fo)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy('});')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press ('enter')
        pyautogui.click(self.bodyCoords_with_console) # because tab needs to be in focus to copy to clipboard
        if (not self.console_open):
            pyautogui.press('F12')

        return clipboard.paste()

    def findTextCoords(self, text, wordNumber=1):
        if (not self.console_open):
            pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox
        pyautogui.hotkey('ctrl', 'f')
        for i in range(1,wordNumber):
            pyautogui.press('enter')    
        pyautogui.write(text)
        pyautogui.press('esc')

        coords = self.run_javascript("getSelectionCoords.js")

        results = coords.split()
        results = list(map(float, results))

        if (not self.console_open):
            pyautogui.press('F12')

        return results


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
            self.go_to_url(epic_logout_url)
            '''
            self.go_to_url(epic_store_url)
            img = Screen.wait_to_see('LanguageGlobe.png')
            
            # Log out if need be
            img = Screen.find(config.IMGS_FLDR+'LogedIn.png')
            #img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+'LogedIn.png', grayscale=True, confidence=.7) 
            if (img is not None):
                self.go_to_url(epic_logout_url)
            else:
                img = Screen.find(config.IMGS_FLDR+'signIn.png')
                #img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+'signIn.png', grayscale=True, confidence=.7)
                if img is not None:
                    pyautogui.click(img)'''

            img = Screen.wait_to_see("signInWithEpic.png", minimumMatches=9)
            pyautogui.click(img)
            print(img)

            img = Screen.wait_to_see("EmailAddress.png")
            pyautogui.click(img)

            pyperclip.copy(email)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('Tab')
            pyautogui.write(password)
            for i in range(0, 4):
                pyautogui.press('Tab')
            pyautogui.press ('enter')

            #img = Screen.wait_to_see("EnterTheScurityCodeToContenue.png", moveMouse= True, timeout= 10, minimumMatches=9)
            time.sleep(4)
            if (img is not None):  
                for i in range(0, 2):
                    pyautogui.press('Tab')
                pyautogui.write(pyotp.TOTP(two_fa_key).now())
                for i in range(0, 4):
                    pyautogui.press('Tab')
                pyautogui.press ('enter')

            while (True):
                self.go_to_url("file://" + config.ROOT_DIR + "/imgs/FREENOW.png")
                if (Screen.wait_to_see("FREENOW.png") is not None):
                    break

            self.go_to_url(epic_store_url)
            img = Screen.wait_to_see('LogedIn.png',moveMouse=True, timeout=19)
            if (img is not None):
                break

    def claim_free_games(self):
        amount_of_free_games = -1

        while amount_of_free_games != 0:
            amount_of_free_games-=1
            self.go_to_url("file://" + config.ROOT_DIR + "/imgs/FREENOW.png")
            Screen.wait_to_see("FREENOW.png")
            self.go_to_url(epic_store_url)
            #Screen.wait_to_see('LanguageGlobe.png', timeout=10)

            time.sleep(8)

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.write("free now")
            pyautogui.press('esc')

            color = (0, 120, 242)
            s = pyautogui.screenshot()

            for x, y in ((w1, w2) for w1 in range(s.width) for w2 in range(s.height)):
                if s.getpixel((x, y)) == color:
                    pyautogui.click(x, y) 
                    break

            '''for x in range(s.width):
                for y in range(s.height):
                    if s.getpixel((x, y)) == color:
                        pyautogui.click(x, y)  # do something here
                        exit()'''
            '''
            key_to_press = 'space'
            start_time = datetime.now()
            timeout = 15
            while True:
                time_delta = datetime.now() - start_time
                if time_delta.total_seconds() >= timeout:
                    print("time limit exceeded")
                    start_time = datetime.now()
                    self.go_to_url(epic_store_url)
                    Screen.wait_to_see('LanguageGlobe.png', timeout=7)
                    timeout = 35
                    key_to_press="down"
                #img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+'FREENOW.png', grayscale=True, confidence=.7)
                img = Screen.find(config.IMGS_FLDR+'FREENOW.png',minimumMatches=5,show=False)
                if img is not None:
                    img = Screen.find(config.IMGS_FLDR+'FREENOW.png',minimumMatches=5,show=False)
                    if (img is not None):
                        pyautogui.click(img)
                        break
                    #imgs_list = list(pyautogui.locateAllOnScreen(config.IMGS_FLDR+'FREENOW.png', grayscale=True, confidence=0.95))
                pyautogui.press (key_to_press)
            '''

            time.sleep(5)

            self.console_open = True
            pyautogui.hotkey('ctrl', 'shift', 'k')

            coords = self.findTextCoords("GET")
            print(coords)
            pyautogui.click(coords)

            time.sleep(1)
            coords = self.findTextCoords("Place Order", 3)
            pyautogui.click(coords)

            time.sleep(1)
            coords = self.findTextCoords("I agree", 3)
            pyautogui.click(coords)

            return
            '''# wait to see in_library.png or get.png
            img = Screen.wait_to_see('get.png', 'IN_LIBRARY.png', moveMouse= True, timeout= 20, show=False)

            img = Screen.wait_to_see('get.png', 'IN_LIBRARY.png', moveMouse= True, timeout= 20, show = True)
            if img is not None:
                pyautogui.click(img)
                img = Screen.wait_to_see('PLACE_ORDER.png')
                if img is not None:
                    pyautogui.click(img)
                    img = Screen.wait_to_see('I_Agree.png')
                    if img is not None:
                        pyautogui.click(img)
                        Screen.wait_to_see('Thank_u_for_buying.png',moveMouse= True, timeout= 7)
                        return
                
                print("Something changed!")
                exit()
            else:
                print("No free games here")
                return'''