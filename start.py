                                #!/usr/bin/env python
## MrBotto | Created by RubbixCube with help from lclc98. ##

# Import resources
import re
import socket
import pickle
from modules.IRCCommands import *
import importlib

# Define Variables
mods = {}
cmds = pickle.load(open('cmds.p', 'r+'))

# Get required information #
HOST = 'irc.twitch.tv'                          # Twitch IRC Network
PORT = 6667                                     # Default IRC-Port
CHAN = ['']                                     # Channelname = #{Nickname}
NICK = ''                                       # Twitch username
PASS = ''                                       # OAuth Key


# Show info in the shell/terminal
print('MrBotto ver. 3.0 | Created & Modified by RubbixCube & lclc98')
print('Important Information:')
print('HOST = ' + HOST)
print('PORT = ' + str(PORT))
for c in CHAN:
    print('CHAN = ' + c)
print('\n')
print('Chat Log:')

## Main Program ##
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
            
# List all commandID's in Commands.py
options = ['Join', 'Leave', 'Who', 'Here', 'Version', 'MrBotto', 'Hire','Peta',
           'Math','Mods']
# Check whether a command exists
def parse_message(channel, user, msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        for commandID in options:
            command = getattr(module_name, commandID)
            if(command.getCommand() == msg[0]):
                command.excuteCommand(con, channel, user, msg, user in mods.get(channel), False)
                break
        if (msg[0] in cmds):
            global cmds
            cmds = pickle.load(open('cmds.p', 'r+'))
            response = cmds[msg[0]]
            print response
            send_message(con, channel, response)

# Connect to the host and join the appropriate channel(s)            
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
            #line = str.rstrip(line)
            line = str.split(line)

	    # Stay connected to the server
            if len(line) >= 1:
                if line[0] == 'PING':
                    print(line[0] +":"+ line[1])
                    send_pong(con, line[1])

                # FEATURE: Adding mods (decided by JTV)
                message = ' '.join(line)
                x = re.findall('^:jtv MODE (.*?) \+o (.*)$', message)
                if (len(x) > 0):
                    channel = x[0][0] 
                    if (channel not in mods):
                        mods[channel] = []
                    list = mods.get(channel)
                    list.append(x[0][1])
                    print(mods)

                # Removing mods
                y = re.findall('^:jtv MODE (.*?) \-o (.*)$', message)
                if (len(y) > 0):
                    channel = y[0][0]
                    if (channel in mods):
                        mods.get(channel).remove(y[0][1])
                        print(mods)

                if (line[1] == 'PRIVMSG'):
                    sender = get_sender(line[0])
                    message = get_message(line)
                    channel = line[2]
                    if (sender == 'rubbixcube'):
                        print('*DEV* ' + sender + ': ' + message)
                    elif (sender == channel[1:]):
                        print('*STR* ' + sender + ': ' + message)
                    elif (channel in mods):
                        if (sender in mods.get(channel)):
                            print('*MOD* ' + sender + ': ' + message)
                    else:
                        print(sender + ': ' + message)

                    # FEATURE: Sub welcome
                    if (sender == "twitchnotify"):
                        command = getattr(module_name, 'TwitchNotify')
                        command.excuteCommand(con, channel, sender, message, False, False)

                    # Load new commands whenever somebody adds a command.
                    if (re.search('!com add \w*', message)):
                        cmds = pickle.load(open('cmds.p', 'r+'))
                        
                    parse_message(channel, sender, message)
                    
    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
