## BOT ##

# TODO:
# 1. Call the API to store the Mods & Subs of the connected channel appropriately


# Import resources #
import re
import socket
from modules.IRCCommands import *

import importlib

## Start Settings ##
HOST = 'irc.twitch.tv'                          # Twitch IRC Network
PORT = 6667                                     # Default IRC-Port
CHAN = ['#']                                    # Channelname = #{Nickname}
NICK = 'MrBotto'                                # Twitch username
PASS = ''                                       # OAuth Key
## End Settings ##

# List info in the shell #
print('MrBotto ver. 3.1.7 | Created & Modified by RubbixCube & lclc98 | Original code: Liquid')
print('Important Information:')
print('HOST = ' + HOST)
print('PORT = ' + str(PORT))
for c in CHAN:
    print('CHAN = ' + c)
print('\n')
print('Chat Log:')

## Start Helper Functions ##
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result

def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

module_name = importlib.import_module('modules.Commands')
            
## End Helper Functions ##

options = ['Join', 'Leave', 'Who', 'Here', 'Version', 'MrBotto', 'Peta', 'Math','Mods']
def parse_message(channel, user, msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        for commandID in options:
            command = getattr(module_name, commandID)
            if(command.getCommand() == msg[0]):
                command.excuteCommand(con, channel, user, msg, False, False)
                break
            
con = socket.socket()
con.connect((HOST, PORT))

send_pass(con, PASS)
send_nick(con, NICK)
for c in CHAN:
    join_channel(con, c)

data = ""

while True:
    try:
        data = data+con.recv(1024)
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            print(line)
            line = str.rstrip(line)
            line = str.split(line)

			
            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(con, line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    channel = line[2]
                    print(sender + ": " + message)
                    
                    if (sender == "twitchnotify"):
                        msg = message.split(' ')
                        send_message(con, channel, 'Welome to the channel, ' + msg[0] + '!')
                    else:
                        parse_message(channel, sender, message)
                    
    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
