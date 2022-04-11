from multiprocessing.connection import wait
from pickle import TRUE
from queue import Empty
from shutil import move
import subprocess
import webbrowser
from xml.dom import minicompat
#from aqt import TR
import pyautogui
import os
import time
import pyclip
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

        Screen.wait_to_see('FREENOW.png', moveMouse= True, timeout=5)    
        pyautogui.press('F11')
        if (self.run_javascript("IsFullscreen.js") == "NO"):
            pyautogui.press('F11')
        self.fullscreen = True

    def run_javascript(self, script_name):
        pyautogui.hotkey('ctrl', 'shift', 'k') # opens or focuses console in firefox
        time.sleep(1)
        if self.allow_pasting == False:
            pyautogui.write("allow pasting")
            self.allow_pasting = True
            pyautogui.press ('enter')
        # javascript that adds an eventlistner that once the page comes into focus, deletes itself and puts in the clipboard if the browser is or not in fullscreen
        pyclip.copy('document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler); ')
        pyautogui.hotkey('ctrl', 'v')
        fo = open("./src/JSscripts/" + script_name, 'r').read() # opens script and pastes it
        pyclip.copy(fo)
        pyautogui.hotkey('ctrl', 'v')
        pyclip.copy('});')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press ('enter')
        self.focus_site()
        if (not self.console_open):
            pyautogui.press('F12')
        
        time.sleep(0.1)

        result = str(pyclip.paste())[2:-1] # transforms <'NO'> in <NO>

        return result 

    def clickTextCoords(self, text, wordNumber=1):
        co = self.console_open
        self.open_console()

        time.sleep(2)
        print("Attention1")

        while (True):
            self.focus_site()

            time.sleep(1)
            print("Attention3")
            time.sleep(1)

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.write(text)

            time.sleep(2)
            print("Attention4")

            for i in range(0,wordNumber):
                pyautogui.press('enter')    
            pyautogui.press('esc')

            time.sleep(3)
            print("Attention5")

            # Run the code to get coords, and put it in a variable in the browser
            pyautogui.hotkey('ctrl', 'shift', 'k') # opens or focuses console in firefox
            time.sleep(1)
            if self.allow_pasting == False:
                pyautogui.write("allow pasting")
                self.allow_pasting = True
                pyautogui.press ('enter')
            fo = open("./src/JSscripts/getSelectionCoords.js", 'r').read()
            pyclip.copy(fo)
            pyautogui.hotkey('ctrl', 'v')

            time.sleep(2)
            print("Attention6")

            pyautogui.press ('enter')

            time.sleep(2)
            print("Attention7")

            #pyclip.copy('document.addEventListener("focus", function handler(e) { e.currentTarget.removeEventListener(e.type, handler); ')
            #pyautogui.hotkey('ctrl', 'v')

            #pyclip.copy(fo)
            #pyautogui.hotkey('ctrl', 'v')
            #pyclip.copy('});')
            #pyautogui.hotkey('ctrl', 'v')
            #pyautogui.press ('enter')
            #self.focus_site()

            coords = self.run_javascript("resultToClipboard.js")

            time.sleep(2)
            print("Attention8")

            #coords = self.run_javascript("getSelectionCoords.js")

            results = coords.split()

            try:
                results = list(map(float, results))
            except ValueError:
                print ("Not a float", end=" ")
                continue
            break

        if (results != [0, 0]):
            pyautogui.click(results)
        else:
            results = None

        if (not co):
            self.close_console()

        return results

    def go_to_url(self, url):
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.1)
        pyclip.copy(url)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.press ('enter')

    def waitForSiteToLoad(self):
        co = self.console_open
        self.open_console()
        time.sleep(4)
        while (True):
            time.sleep(1)
            if (self.run_javascript("isLoaded.js") == "loaded"):
                break
        if (not co):
            self.close_console()
        time.sleep(1)

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

            pyclip.copy(email)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('Tab')
            pyautogui.write(password)
            time.sleep(0.5)
            for i in range(0, 4):
                pyautogui.press('Tab')
            pyautogui.press ('enter')

            time.sleep(4)
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.hotkey('ctrl', 'c')
            result = str(pyclip.paste())[2:-1]
            if (result != "https://www.epicgames.com/account/personal"):

                # moves focuse back to webpage
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.hotkey('esc')

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
            self.waitForSiteToLoad()
            break
            #img = Screen.wait_to_see('LogedIn.png',moveMouse=True, timeout=19)
            #if (img is not None):
            #    break

    def open_console(self):
        if (self.console_open == False):
            pyautogui.hotkey('ctrl', 'shift', 'k') # open console in firefox and focuses it
            self.console_open = True

    def close_console(self):
        if (self.console_open == True):
            pyautogui.press('F12') # close console
            self.console_open = False

    def focus_console(self):
        pyautogui.hotkey('ctrl', 'shift', 'k')

    def focus_site(self):
        if (self.fullscreen == True):
            pyautogui.click(5, pyautogui.size()[1]/2)
        else:
            pyautogui.click(Screen.wait_to_see('FREENOW.png', moveMouse= True, timeout=5))

        #time.sleep(1)
        #pyautogui.click(self.bodyCoords_with_console, button='right')
        #time.sleep(1)
        #pyautogui.click(self.bodyCoords_with_console[0]-3, self.bodyCoords_with_console[1]-3) # because tab needs to be in focus to copy to clipboard
        #time.sleep(1)

    def claim_free_games(self):
        amount_of_free_games = -1

        while amount_of_free_games != 0:
            amount_of_free_games-=1
            #self.go_to_url("file://" + config.ROOT_DIR + "/imgs/FREENOW.png")
            #Screen.wait_to_see("FREENOW.png")
            #self.go_to_url(epic_store_url)
            #Screen.wait_to_see('LanguageGlobe.png', timeout=10)

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

            self.waitForSiteToLoad()

            #self.console_open = True
            #pyautogui.hotkey('ctrl', 'shift', 'k')

            coords = self.clickTextCoords("GET")
            if (coords == None):
                return
            #pyautogui.click(coords)

            time.sleep(4)
            color = (0, 120, 242)
            s = pyautogui.screenshot()

            for x, y in ((w1, w2) for w1 in range(s.width) for w2 in range(int(s.height/2), s.height)):
                if s.getpixel((x, y)) == color:
                    pyautogui.click(x+5, y+5) 
                    break

            time.sleep(4)
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

            #time.sleep(1)
            #print("CTRL Finf for place order")
            #coords = self.clickTextCoords("Place Order", 3)
            #pyautogui.click(coords)

            #time.sleep(1)
            #print("CTRL Finf I agree")
            #coords = self.clickTextCoords("I agree", 3)
            #pyautogui.click(coords)

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