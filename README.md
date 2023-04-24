# chatgpt-ircbot
ChatGPT3 irc bot, if response longer than 3 lines uploads to termbin.com and gives the link back

Dependencies
import irc.bot
import irc.strings
import openai
import subprocess
import time

tested with python3.7

Disclaimer: could give a longer than 3 line response since it parses the line for irc length later
