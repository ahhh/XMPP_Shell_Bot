# XMPP_Shell_Bot
A python shell / chat bot for XMPP and cloud services, designed for penetration testers to bypass network filters.
To better understand the inspiration behind this project, please see: http://lockboxx.blogspot.com/2015/02/python-xmpp-command-and-control.html

The gchat_shell_bot.py requires a Google account user name and password to login and be the bot to chat with. 
Further you have to navigate to https://www.google.com/settings/security/lesssecureapps and turn on access for less secure apps.

### Requires:
  - sleekxmpp
  - dnspython
  - Pillow
  - pyscreenshot

### Commands:
- [**Any**] : Replies with standard bot response.
- [**$** *Prepended*] : Replies with the shell output.
- [**!** *Prepended*] : Downloads file from the following URL.
- [**^** *Prepended*] : Upload following file to public pastebin.
- [**%** *Prepended*] : XORs following file with a hardcoded byte array.
- [**&** *Prepended*] : Takes a screenshot and names it the following string.

### Available Startup Options:
- **-q** :: Start in quiet mode
- **-d** :: Start in debug mode
- **-v** :: Activate more verbosity
- **-j** :: User ID (email)
- **-p** :: Password



