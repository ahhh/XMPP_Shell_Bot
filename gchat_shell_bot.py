#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ShellBot v0.1
# Code heavily borrowed from SleekXMPP's MUCBot 
# https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py

import sys, os, subprocess
import logging
import getpass
from optparse import OptionParser
import sleekxmpp
import random

USERNAME = ''
CMD_TOKEN = '$'
#SHELLCHAT = ''
#SHELLNIC = ''

if sys.version_info < (3, 0):
  reload(sys)
  sys.setdefaultencoding('utf8')
else:
  raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):

  def __init__(self, jid, password):  # , room, nick):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)
    #self.room = room
    #self.nick = nick

    # The session_start event will be triggered when the bot connects to the server
    self.add_event_handler("session_start", self.start)

    #The message event is triggered whenever you are sent a message
    self.add_event_handler("message", self.message)

    # The groupchat_message event
    #self.add_event_handler("groupchat_message", self.muc_message)

    # The groupchat_presence event is triggered whenever someone joins a room
    #self.add_event_handler("muc::%s::got_online" % self.room,
    #                       self.muc_online)

  # session_start event
  def start(self, event):
      self.get_roster()
      self.send_presence()
      #Don't join groupchat yet
      #self.plugin['xep_0045'].joinMUC(self.room,
      #                                self.nick,
      #                                # password=room_password,
      #                                wait=True)

  # reply to messages
  def message(self, msg):
      if msg['type'] in ('chat', 'normal'):
          body = msg['body']
          if body and body[0] == CMD_TOKEN:
            reply = self.run_command(body.lstrip(CMD_TOKEN))
            msg.reply(reply).send()
          else:
            reply = random.choice(['what?', 'huh..', 'mmmmm', 'I don\'t get it'])
            msg.reply(reply).send()

  # reply to nick_name mentions
  def muc_message(self, msg):
    if msg['mucnick'] != self.nick and self.nick in msg['body']:
      self.send_message(mto=msg['from'].bare,
                        mbody="I heard that, %s." % msg['mucnick'],
                        mtype='groupchat')

  #Announce when bot comes online
  def muc_online(self, presence):
    if presence['muc']['nick'] != self.nick:
      self.send_message(mto=presence['from'].bare,
                        mbody="Hello, %s %s" % (presence['muc']['role'],
                                                presence['muc']['nick']),
                        mtype='groupchat')

  def run_command(self, cmd):
      proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
      stdoutput = proc.stdout.read() + proc.stderr.read()
      return stdoutput


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
  #optp.add_option("-r", "--room", dest="room",
  #                help="MUC room to join")
  #optp.add_option("-n", "--nick", dest="nick",
  #                help="MUC nickname")

  opts, args = optp.parse_args()

  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')

  if opts.jid is None:
  #    opts.jid = raw_input("Username: ")
      opts.jid = USERNAME
  if opts.password is None:
      opts.password = getpass.getpass("Password: ")
  #if opts.room is None:
  #    opts.room = raw_input("MUC room: ")
  #    opts.room = SHELLCHAT
  #if opts.nick is None:
  #    opts.nick = raw_input("MUC nickname: ")
  #    opts.nick = SHELLNIC

  # Setup the MUCBot and register plugins.
  xmpp = MUCBot(opts.jid, opts.password) #, opts.room, opts.nick)
  xmpp.register_plugin('xep_0030') # Service Discovery
  xmpp.register_plugin('xep_0045') # Multi-User Chat
  xmpp.register_plugin('xep_0199') # XMPP Ping

  # Connect to the XMPP server and start processing XMPP stanzas.
  if xmpp.connect():
    #if xmpp.connect(('talk.google.com', 5222)):
    xmpp.process(block=True)
    print("Done")
  else:
    print("Unable to connect.")


if __name__ == '__main__':
  main()
