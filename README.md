# Free_Games.py Description

![](https://img.shields.io/github/stars/Yeshey/Free-Epic-Games)
![](https://img.shields.io/github/forks/Yeshey/Free-Epic-Games)
![](https://img.shields.io/github/license/Yeshey/Free-Epic-Games)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FYeshey%2FFree-Epic-Games)](https://twitter.com/Yeshey24726112)


Script that can be automatically ran via Windows Task Scheduler or Cron that logs into the Epic Games Store website and grabs the free games for the week. Tested on Linux, but there isn't any reason it wouldn't work on Windows as well. Just change the top line from `#! python3` (windows) to `#!/usr/bin/python3` (linux) and it should be fine. 

Inspiered by [Mason Stooksburys](https://github.com/MasonStooksbury)  [bots repository](https://github.com/MasonStooksbury/Free-Games), this version of the bot uses pyautogui to view the buttons it mut press on screen making it harder for the site to detect it is a bot. I wasn't able to use his bot due to captchas.

# Setup

## Requirements

First, clone this repo using `git clone https://github.com/Yeshey/Free-Epic-Games.git`. Then,  

Run `pip install -r requirements.txt` to automatically install dependencies

### Additionally

+ [Firefox](https://www.mozilla.org/firefox/new/) - You can technically do all of this with Chrome, there are some minor diferences, and the script isn't prepared for them yet
+ Enter the `EPIC_EMAIL` and `EPIC_PASSWORD` variables in the `.env` file to match your Epic Games Store account. Don't include any quotes here.
+ You may add multiple user accounts using comma separated values, e.g. `EPIC_EMAIL=a@a.com,b@b.com` `EPIC_PASSWORD=pass1,pass2`
+ While the scipt will technically work without 2FA enabled on your epic account, you will likely see many more captchas. In order to avoid this, follow the steps [here](###Two-factor-authentication) to enable 2FA on your account and configure the script to work with your 2FA secret. 

### Two-factor authentication

If you already have 2FA enabled on your account, you will be required to disable it temporarily. This is required to retrieve the key we need.

1. Go to [your Epic account settings](https://www.epicgames.com/account/password) and enable "**Authenticator App**".
1. Keep a copy of the "**Manual Entry Key**". This will be used later in the python script. Do not close the page yet.
1. On your phone, download [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en) or another similar application.
1. Using the application, scan the QR code visible on browser. Enter the code obtained from the application on the browser and click "**Activate**".
1. Keep a copy of the "**Rescue Codes**". This will come in handy to retrieve your account if you ever lose access to your Authentificator application (losing phone, etc.)
1. In the python script, input the "**Manual Entry Key**" retrieved earlier in the corresponding field, again leaving the single quotes as is.
1. Done!

### Finally

Now all you have to do is run `python Free_Games.py`, sit back & relax while your free games are being claimed (actually, you may have to complete a captcha upon signing in , but that's it).

# Setting up Windows Task Scheduler

These steps should help you get Windows Task Scheduler setup in such a way that it will wake your computer from sleep and grab your free games then go back to sleep. It will also be setup to run again if something goes wrong as well as kill itself if it goes haywire. I realize the first picture shows it being setup for Vista and Windows Server 2008, but this was the only way it would work on Windows 10 without doing some wonky BIOS setup that only worked for some people.

1. Fill out General:
    1. ![General](https://github.com/MasonStooksbury/Free-Games/blob/master/WTS_Setup/General.png)
2. Fill out Triggers:
    1. ![Triggers](https://github.com/MasonStooksbury/Free-Games/blob/master/WTS_Setup/Triggers.png)
3. Fill out Actions:
    1. ![Actions](https://github.com/MasonStooksbury/Free-Games/blob/master/WTS_Setup/Actions.png)
4. Fill out Conditions:
    1. ![Conditions](https://github.com/MasonStooksbury/Free-Games/blob/master/WTS_Setup/Conditions.png)
5. Fill out Settings:
    1. ![Settings](https://github.com/MasonStooksbury/Free-Games/blob/master/WTS_Setup/Settings.png)
