# Making Commands

## Requirements

- **Python 3** Programming Language Knowledge
 - We suggest reading some books and lurking on StackOverflow.
- **discord.py** Library Knowledge
 - You can find the full documentation [here](https://discordpy.readthedocs.io/en/rewrite/index.html).
 - Yes, we use the Rewrite branch.
- An appropriate **IDE**
 - [PyCharm Community Edition](https://www.jetbrains.com/pycharm/) is strongly suggested.
- Familiarity with the **YAML** data syntax.
 - It's rather simple, like JSON, but much more Pythonic and not nearly as fragile.

## Creating a New Plugin

### Creating The `plugin.yml` File

Before you even get to the code you need to first make a `.yml` file that contains information necessary for Sigma to know what to load, and with which attributes.

- In `/sigma/plugins/` create a new folder, for this example let's call it `my_module`.
- Within that folder, in the location `/sigma/plugins/my_module` create a `plugin.yml` file.
 - The `plugin.yml` file contains information about the commands in your module, or rather, plugin.

The plugin file needs to contain data about your module and the commands within it.
Let's fill it up with some example data...

```yml
name: Simple Math

categories:
  - math

enabled: true

commands:
  - name:    echo # Marker A
    alts:
      - "repeat"
      - "say"
    global:  true
    enabled: true
    sfw:     false
    partner: false
    usage:   "{pfx:s}{cmd:s} Hello world!"
    description:
      Outputs what you tell it to say.
```

Let's explain what each variable does.

- **name** (outer): Specifies the name of the module group containing your commands.
 - Type: String
- **categories**: A list of categories your command belongs to.
 - Type: List of Strings
- **enabled** (outer): Specifies if the module group is enabled or not, if not, no commands will be loaded from it.
 - Type: Boolean
- **commands**: Contains a list of data that define your commands.
 - Type: List of Dictionaries
- **name** (inner): The name of the command, the string which the bot responds to primarily.
 - Type: String
- **alts**: A list of alternate names the command can be called with, it can be pretty much anything but make sure they don't repeat.
 - Type: List of Strings
- **global**: I have no clue actually, I should really talk to Valeth about this. Just leave it `true`.
 - Type: Boolean
- **enabled** (inner): Determines if the command should be loaded or not.
 - Type: Boolean
- **sfw**: Determines if a command is Safe For Work or Not Safe For Work. If it is `false` the channel the command is used in needs to be marked as a NSFW channel in order to execute.
 - Type: Boolean
- **partner**: If set to `true` the command will only be usable by servers who are marked as partners with the `togglepartner` command that is only available to the developers of the bot, or rather, the person who is hosting it on their machine.
 - Type: Boolean
- **usage**: Gives a usage example of how the command is used. The bot prefix will be placed where `{pfx:s}` is and the main command name will be placed where `{cmd:s}` is.
 - Type: String
- **description**: Pretty self explanatory. A description of the command.
 - Type: String

### Creating The Actual Functions

In the previously created `my_module` folder, location being `/sigma/plugins/my_module` make a file with the exact same name as the main `name` of your command. You'll notice that in the `plugin.yml` example above we've left a comment that says *"Marker A"*. The file needs to be the same name as this command name with the `.py` extension. So if our command is called `echo`, we need to create a new file called `spired.py`.

And now, the actual python programming begins! We need to make a new asyncronous function to be called.
Again, this function also needs to carry the same name as the name of the command, if the command is called `echo` the function too needs to be called `echo` as you'll see in the example below.

```py
async def echo(cmd, message, args):
    reply_message = ' '.join(args)
    await message.channel.send(reply_message)
```

We defined a new async function called `echo` that takes 3 arguments which are `cmd` (the command class proxying other classes and command information), `message` (which contains all data from the *discord.Message* class from the event) and `args` (which is a list of strings that were the arguments after the command).

The `cmd` class has subclasses that allow it to access Sigma's core classes.
- `cmd.bot` to access the bot `discord.Client` functions.
- `cmd.db` to access the functions that control the database connection of the bot.

We suggest inspecting the classes to see what else is contained and what functions it carries, but these two are the most important.
