# Setting Up Sigma For Windows

## Requirements
* A text editor like Notepad++ or Atom is required
* Git Bash is useful but you dont need it and is not reccomended unless you will be updating a _lot_
* **_Basic_** Computer Skills


## WINDOWS INSTALL
### Downloading Python 3.6.1
	Download python 3.6 here: https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe
	b) Choose Install Now
	c) Close the installer

### Downloading MongoDB
	a) Download MongoDB here: https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.4-signed.msi/download
	b) Run it.
	c) Choose complete install.
	d) Install.

### Go to where you installed MongoDB
	a) Once you find the folder go to \server\3.X\bin
	b) Right Click mongod.exe and click create shortcut
	c) Click place on desktop

### Downloading Sigma
	a) Go to: https://github.com/aurora-pro/apex-sigma and click clone _or_ download and choose **_Download ZIP_**
	b) Extract the files to a folder on your desktop.
	c) Open the folder

### Getting a token!
	a) Go to Discord Developer Page here: _https://discordapp.com/developers/applications/me_
	b) Click **_New App_**
	c) In app name choose the name you want your copy of Sigma to be, and add a _quick_ description.
	d) Click **_Create App_**
	e) Once the page has reloaded choose **_Create Bot User_** then click **_Yes, Do it!_**.
	f) Under the _App Bot User_ category choose **_Click to Reveal Token_**.
	g) Copy the token.

### Configuring Sigma
	a) Go back to the Sigma folder on your desktop, and right click the _config_example.py_ and click _Edit with Notepad++_ if you installed Notepad++
	b) You should see a very large list of _API's_.
	c) You should see _# Bot Token_.
	d) Look under it and there is _Token = getenv('DiscordBotToken') or ''_
	e) Put your token in the empty quotes.
	f) Save all files
	g) Rename the _config_example.py_ to _config_

### Running Sigma
	a) Go back to the sigma folder, and double click run.py!
	b) A window should show up, and if it works after a few seconds you should see **_Succesfully connected to Discord!_**
	c) That means you have dont it right!

### Inviting your bot to your server!
	a) Go back to the discord developer page.
	b) Copy the client id
	c) paste the client id in this link: https://discordapp.com/oauth2/authorize?client_id=&scope=bot&permissions=8
	d) Paste it after the _client_id=_
	e) Select a server to add it to, and click Authorise!
	f) Your bot should connect to your server!

### Installing pip modules
	a) Go to the apex-sigma-master folder and hold shift and right click.
	c) Click _Open Command Window here_
	c) Type this into the console. _pip install -U -r requirements.txt_.


### Defining yourself as owner
	a) Open the _config.py_ file.
	b) Scroll down to the bottom of the file and you should see _permitted_id_
	c) For this step you need discord developer version on. If you need help message **_Lumenix#3495_**
	d) Right click your name in any server and click _Copy Id_
	e) Paste your ID inside the quotes within the brackets and save.
	f) Close the open Sigma window and relaunch it!

That's it you are done!
Make sure before you open run.py open _mongod.exe_ as sigma doesn't work without it!
