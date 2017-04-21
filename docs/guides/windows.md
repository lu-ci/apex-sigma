So you wanna set up Sigma eh?
Ill help you.

A text editor like Notepad++ or Atom is required
Git Bash is useful but eh you dont need it.

WINDOWS INSTALL
1. Downloading Python 3.6.1
	Download python 3.6 here: https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe
	b) Choose Install Now
	c) Close the installer

2. Downloading MongoDB
	a) Download MongoDB here: https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.4-signed.msi/download
	b) Run it.
	c) Choose complete install.
	d) Install.

3. Go to where you installed MongoDB
	a) Once you find the folder go to \server\3.X\bin
	b) Right Click mongod.exe and click create shortcut
	c) Click place on desktop

4. Downloading Sigma
	a) Go to: https://github.com/aurora-pro/apex-sigma and click clone or download and choose "Download ZIP"
	b) Extract the files to a folder on your desktop.
	c) Open the folder

5. Getting a token
	a) Go to Discord Developer Page here: https://discordapp.com/developers/applications/me
	b) Click "New App"
	c) In app name choose the name you want your copy of Sigma to be, and add a quick description
	d) Click "Create App"
	e) Once the page has reloaded choose "Create Bot User" then click "Yes, Do it!".
	f) Under the "App Bot User" category choose "Click to Reveal Token".
	g) Copy the token.

6. Configuring Sigma
	a) Go back to the Sigma folder on your desktop, and right click the "config_example.py" and click "Edit with Notepad++" if you installed Notepad++
	b) You should see a very large list of "API's".
	c) You should see "# Bot Token".
	d) Look under it and there is Token = getenv('DiscordBotToken') or ''
	e) Put your token in the empty quotes.
	f) Save all files
	g) Rename the "config_example.py" to "config"

7. Running Sigma
	a) Go back to the sigma folder, and double click run.py!
	b) A window should show up, and if it works after a few seconds you should see "Succesfully connected to Discord!"
	c) That means you have dont it right!

8. Inviting your bot to your server!
	a) Go back to the discord developer page.
	b) Copy the client id
	c) paste the client id in this link: https://discordapp.com/oauth2/authorize?client_id=&scope=bot&permissions=8
	d) Paste it after the "client_id="
	e) Select a server to add it to, and click Authorise!
	f) Your bot should connect to your server!

9. Installing pip modules
	a) Go to the apex-sigma-master folder and hold shift and right click.
	c) Click "Open Command Window here"
	c) Type this into the console. "pip install -U -r requirements.txt".


10. Defining yourself as owner
	a) Open the config.py file.
	b) Scroll down to the bottom of the file and you should see "permitted_id"
	c) For this step you need discord developer version on. If you need help message Lumenix#3495
	d) Right click your name in any server and click "Copy Id"
	e) Paste your ID inside the quotes within the brackets and save.
	f) Close the open Sigma window and relaunch it!

That's it you are done!
Make sure before you open run.py open "mongod.exe" as sigma doesn't work without it!