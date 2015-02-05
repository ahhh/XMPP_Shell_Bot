# XMPP_Shell_Bot
A python shell / chat bot for XMPP and cloud services, designed for penetration testers to bypass network filters.
To better understand the inspiration behind this project, please see: http://lockboxx.blogspot.com/2015/02/python-xmpp-command-and-control.html

gchat_shell_bot.py requires a Google account user name and password to login and be the bot to chat with. 
Further you have to navigate to https://www.google.com/settings/security/lesssecureapps and turn on access for less secure apps.

### Commands:
- [**Any**] : Replies with Standard Bot Response.
- [**$** *Prepended*] : Replies with the Shell Output.

### Options:
- [*-q*] - Start in Quiet Mode
- [*-d*] - Start in Debug Mode
- [*-v*] - Activate more Verbosity
- [*-j*] - User ID (Email)
- [*-p*] - Password

### Requires:
  - sleekxmpp
  - dnspython
