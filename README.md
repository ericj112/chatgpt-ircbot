# chatgpt-ircbot
ChatGPT3 irc bot

if response longer than 3 lines uploads to termbin.com and gives the link back

logs requests received and responses

Dependencies
------------
irc.bot

irc.strings

openai

subprocess

time

tested with python3.7

to log use "python3.7 -u /path/to/chatgpt-ircbot.py | tee -a /path/to/log"

Disclaimer: could give a longer than 3 line response since it parses the line for irc length later
