# Setting Up On Windows
## Requirements
* The Ability To Follow Simple Instructions
* Python 3.6+ [Link](https://www.python.org/downloads/)
* MongoDB 3.2+ [Link](https://www.mongodb.com/download-center)
* A UTF-8 Compatible Text Editor [Notepad++](https://notepad-plus-plus.org/download/) or [Atom](https://atom.io/)
* Archive Extracting Software [7z](http://www.7-zip.org/download.html)
* Sigma's Master Branch Repository [Link](https://github.com/aurora-pro/apex-sigma/archive/master.zip)
*(Just download and extract this to the location of your choosing)*

## Installing Python 3.6
### Note
*This is actually just a courtesy, if you screw up, use Google, we won't really help you set up Python...*
### General Process
1. Download the installation package from the link above.
2. Start the installation.
3. At the bottom, there will be an **"Add Python 3.6 To PATH"** checkbox. Make sure it's **checked**.
4. Click **"Customize Installation"**.
5. We suggest leaving everything **checked**.
6. The next screen is **Advanced Options**, check the following.
  1. Install for all users
  2. Associate files with Python
  3. Add Python to environment variables
  4. Precompile standard library
7. Still at the **Advanced Options**, it's strongly suggested to change the install location to something easily accessible like `C:\Py36`
8. Hit the **Install** button and wait for it to finish.

### Testing The Installation
1. After the installation process has finished successfully, open your command prompt.
2. Type `python --version`
3. It should say `Python 3.6.X`
  1. If it does, congrats! You installed Python 3.6!
  2. If it gives a number starting with other than *3.6*, you have previous unremoved and interfering python installations.
  3. If it says that it is *not a recognized command* you have not added it to the *PATH* nor the *Environment Variable*
4. Type `pip --version`
5. It should say `pip 9.0.1`
  1. If it does, congrats! You installed Python 3.6!
  2. If the number lower, we recommend updating by using `pip install -U pip`
  3. If the number is higher, that's completely fine, at the time this was written, *9.0.1* was the latest.
  4. If it says that it is *not a recognized command* you have not added it to the *PATH* nor the *Environment Variable*

## Installing And Updating The Required PIP Modules
### Note
*Make sure your Python installation is properly functional with the test above.*
### installation
1. Navigate to the location of the sigma project directory that you unzipped earlier.
2. Open command prompt in it.
  1. One way is to open `cmd` and type `cd LOCATION_TO_SIGMA_PROJECT`, for example `cd "C:\Users\Alex\Desktop\apex-sigma-master"`
3. To install or update the required modules type `pip install -U -r requirements.txt`
4. Patiently wait for it to finish, Sigma has a lot of requirements.

## Setting Up MongoDB
### Note
*This is actually just a courtesy, if you screw up, use Google, we won't really help you set up MongoDB...*
### Installation
1. Really nothing special, just run of the mill casual *Hit next until it's done* installation, unless you want to set some things manually.
### Before Running
1. Go to `C:\`
2. Make a folder named `data`
3. Open `data`
4. Make a folder named `db`
### Starting MongoDB
1. Go to where MongoDB was installed. Most likely `C:\Program Files\MongoDB`
2. Go to `Server\3.X\bin`
3. Launch `mongod.exe`
*(Yes, it says mongod, short for mongo daemon)*
4. The window that pops up should stay up, if it doesn't, you probably didn't make the folders above.

## Configuring Sigma
### Making A New Discord Application
1. Go to the [Discord Dev Page](https://discordapp.com/developers/applications/me)
2. Click **New App**
3. Name it however you want and optionally give it a nice avatar if you wish to.
4. Hit **Create App**
5. At the new page that popped up, find the button that says **Create a Bot User**, hit it and confirm it's creation.
6. The page's *App Bot User* section now got expanded.
7. Keep this page open for now.

### Editing The config.py
*Initially the config.py file won't exist, make it by simply copying or renaming config_example.py*
1. Open `config.py` with a UTF-8 compatible editor of your choosing. This should **NEVER** be edited with the regular Notepad or Wordpad.
2. In `config.py` all variables look like `Something = getenv('Something') or ''`
3. What you want to do is edit the empty space in the quotation marks after the `or`
4. Find the `Token` variable, it'll probably look like
```python
Token = getenv('DiscordBotToken') or ''
```
5. On the page you left open in the instructions above, find where it says **Token** and *click to reveal*.
6. Click that to see your token. Remember, keep this token secretive and don't give it to anyone.
7. Copy that token and paste it between the quotation marks after the `or`, it should look like this.
```python
Token = getenv('DiscordBotToken') or 'CCB9oKas8asa4BRZlohs2as1nwMmWpw2c8bIsm'`
```
8. Save those changes if you didn't already.
9. You can now run the bot, just launch `run.py`.
*(Or open the command prompt and navigate to the project directory and type `python run.py`)*
