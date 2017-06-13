# Configuration File Documentation

This page explains what each configuration variable is for and where you can obtain it. For each variable in the configuration file you'll notice it has something like:

```python
VARIABLE = getenv('VARIABLE') or ''
```

Each and every configuration variable can also be set as an environment variable. In case you don't want to store your keys and information in the file itself. As to how to set things as an environment variable, you'll have to look it up based on your OS.

# Variable Types

## String

Anything that is surrounded by quotation marks or apostrophes.

```python
MyString = 'my_pretty_little_variable'
```

## Integer

A pure number with a decimal base that is **not** within any quotation marks or apostrophes.

```python
MyInteger = 84615942354
```

## Boolean

A simple Yes or No, in Python a `True` or `False`.

```python
On = True
Off = False
```

## List Of Strings

A list is something between square parentheses separated by comas. When the items within the list are a form of string, it is a list of strings.

```python
MyListOfStrings = ['something_1', 'something_2', 'something_3']
```

## List Of Integers

A list is something between square parentheses separated by comas. When the items within the list are a form of integer, it is a list of integers.

```python
MyListOfIntegers = [9415, 841320, 42, 69]
```

# Main Variables

Variables required for proper Bot functionality.

## Token

**Type**: `String`

Discord Application token obtainable from their [Developer](https://discordapp.com/developers/applications/me) page. Note that this is the **Token** variable and **not** the **Secret**.

## MongoAddress

**Type**: `String`

The IP address of your MongoDB instance. By default this is `127.0.0.1` or `localhost` and it will be that if you are running MongoDB on the same machine as Sigma.

## MongoPort

**Type**: `Integer`

The port your MongoDB instance is running on. Default being `27017`. It will be this port if you haven't made changes to your MongoDB installation.

## MongoAuth

**Type**: `Boolean`

This tells the bot if your MongoDB requires authorization to be accessed. By default Mongo has no authorization settings enabled and this should be `False`.

## MongoUser

**Type**: `String`

If your MongoDB instance requires authorization, place the username here.

## MongoPass

**Type**: `String`

If your MongoDB instance requires authorization, place the password here.

## DevMode

**Type**: `Boolean`

Tells the bot if it is or is not running in a development environment. This toggles numerous features bound to error reporting, and other stuff required for developing plugins for Sigma. By default this is set to `True` but if you plan to simply run the bot change it to `False`.

## PlayingStatusRotation

**Type**: `Boolean`

Tells the bot if it should start the automatic status message rotation on boot. This controls the `Now Playing GAME_NAME` status in Discord. If this is active the `>>setgame` command will be automatically overwritten every 60 seconds. Which is the rotation time of the status clockwork.

## Prefix

**Type**: `String`

Sets the prefix of the bot's commands. By default it's `>>`, making commands be `>>help` and `>>stats`. If you set it to `69`, the commands will be `69help` and `69stats`.

## Currency

**Type**: `String`

Here you can set what you want the currency of the bot to be. By default it's `Kud ⚜` but you can change it to whatever you want. If you do replace the icon on the right side, replace it with a UTF-8 character.

## SlotWinChannelID

**Type**: `Integer`

The ID of the channel you want to bot to report to when somebody wins in a slot machine minigame. A channel's ID can be obtained with the `>>cid` command. If you want to disable this, set it to `None`, like this:

```python
SlotWinChannelID = None
```

## DefaultVolume

**Type**: `Integer`

Sets the default volume of the music player. If it's the first time a server plays music or have never used the `>>volume` command the bot will use this value instead. This can be from `0` to `200`. You can set it to something else. But that's still the maximum regardless.

## permitted_id

**Type**: `List Of Integers`

A list of User IDs that can access Bot Owner commands. You can have as many as you like, just be sure to follow proper list formatting. And make sure they're all integers.
