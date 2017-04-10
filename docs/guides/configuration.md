# Configuration File Documentation
This page explains what each configuration variable is for and where you can obtain it.
For each variable in the configuration file you'll notice it has something like:
```python
VARIABLE = getenv('VARIABLE') or ''
```
Each and every configuration variable can also be set as an environment variable.
In case you don't want to store your keys and information in the file itself.
As to how to set things as an environment variable, you'll have to look it up based on your OS.
# Main Variables
Variables required for proper Bot functionality.
## Variable Types
### String
Anything that is surrounded by quotation marks or apostrophes.
```python
Variable = 'my_pretty_little_variable'
```
### Integer
A pure number with a decimal base that is **not** within any quotation marks or apostrophes.
```python
Variable = 84615942354
```
### List Of Strings
A list is something between square parentheses separated by comas.
When the items within the list are a form of string, it is a list of strings.
```python
Variable = ['something_1', 'something_2', 'something_3']
```
### List Of Integers
A list is something between square parentheses separated by comas.
When the items within the list are a form of integer, it is a list of integers.
```python
Variable = [9415, 841320, 42, 69]
```
## Token
Discord Application token obtainable from their [Developer](https://discordapp.com/developers/applications/me) page.
Note that this is the **Token** variable and **not** the **Secret**.
* Type: `String`
