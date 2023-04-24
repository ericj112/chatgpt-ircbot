#python3.7
#ChatGPT irc bot
#Eric J.
import irc.bot
import irc.strings
import openai
import subprocess
import time

#to log "python3.7 -u /path/to/chatgpt-ircbot.py | tee -a /path/to/log"

#chatgpt api key
openai.api_key = "paste-api-here"

#irc settings
nickname ="chatgpt"
channel = "#irchannel"
server = "irc.libera.chat"
port = 6667

#upload
line_limit = 3
nc_server = "termbin.com"
nc_port = 9999
tmpfile = "/tmp/chatgpt_upload"

class Chatbot(irc.bot.SingleServerIRCBot):
  def __init__(self, channel, nickname, server, port=6667):
    irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
    self.channel = channel

  def on_nicknameinuse(self, c, e):
    c.nick(c.get_nickname() + "_")

  def on_welcome(self, c, e):
    print(time.strftime("%b-%d-%Y %H:%M:%S", time.localtime()),"Connected to",server,"on port",port)
    print(time.strftime("%b-%d-%Y %H:%M:%S", time.localtime()),"Joining", self.channel,"as",c.get_nickname())
    c.join(self.channel)

  def on_pubmsg(self, c, e):
    message = e.arguments[0]
    if message.startswith(self._nickname):
      response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      ).choices[0].text
      print(time.strftime("%b-%d-%Y %H:%M:%S", time.localtime()),"Request received by", e.source.nick, ":",message)

#parsing to be irc friendly
      response1=response.lstrip('\n').lstrip('?')
      response2=response1.replace('\r', '').replace('\n\n', '\n')
      print("Response:",response1,"\n")

      response3=response2.split('\n')
      if len(response3) > line_limit:
        with open(tmpfile, "w") as f:
          f.write(response1)
        result = subprocess.run("cat {} | nc {} {}".format(tmpfile,nc_server,nc_port), stdout=subprocess.PIPE, shell=True)
        print(time.strftime("%b-%d-%Y %H:%M:%S", time.localtime()),"Output longer than",line_limit,"lines, uploaded to",result.stdout.decode('utf-8'))
        c.privmsg(self.channel, result.stdout.decode('utf-8').replace('\r','').replace('\n',''))
        return

#response below line limit, parse for max irc msg length
      for x in range(len(response3)):
        if len(response3[x]) < 440:
          c.privmsg(self.channel, response3[x])
        else:
          n = 440
          responsestring=response3[x]
          chunks = [responsestring[i:i+n] for i in range(0, len(responsestring), n)]
          for x in range(len(chunks)):
            c.privmsg(self.channel, chunks[x])

def main():
  chatbot = Chatbot(channel, nickname, server, port)
  chatbot.start()

if __name__ == "__main__":
  main()

