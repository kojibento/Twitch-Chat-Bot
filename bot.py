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


# Show info in the shell/terminal
print('Connection Information:')
print('HOST = ' + HOST)
print('PORT = ' + str(PORT))
for c in CHAN:
    print('CHAN = ' + c)
print('\n')
print('Chat Log:')

## Main Program ##
def get_sender(msg):
    result = ''
    for char in msg:
        if char == '!':
            break
        if char != ':':
            result += char
    return result

def get_message(msg):
    result = ''
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + ' '
        i += 1
    result = result.lstrip(':')
    return result

module_name = importlib.import_module('modules.Commands')
            
# List all commandID's in Commands.py
options = ['Join', 'Leave','Help' ,'Who', 'Here', 'MrBotto',
            'DCounter', 'ComAdd', 'ComDel', 'ComEdit', 'Com',
           'TwitchSlot', 'TwitchSlotMod', 'PointsMOD']
# Check whether a command exists
def parse_message(channel, user, msg):
    if (len(msg) >= 1):
        msg = msg.split(' ')
        for commandID in options:
            command = getattr(module_name, commandID)
            if (command.getCommand() == msg[0]):
                modStatus = False
                if (channel in mods):
                    modStatus = user in mods.get(channel)
                command.excuteCommand(con, channel, user, msg, modStatus, False)
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
        data_split = re.split(r'[\r\n]+', data)
        data = data_split.pop()

        for line in data_split:
            #print(line)
            #line = str.rstrip(line)
            line = str.split(line)

	    # Stay connected to the server
            if len(line) >= 1:
                if line[0] == 'PING':
                    print(line[0] +':'+ line[1])
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
                        print('*DEV* ' + sender + ' (' + channel + ')' + ': ' + message)
                    elif (sender == 'lclc98'):
                        print('*DEV* ' + sender + ' (' + channel + ')' + ': ' + message)
                    elif (sender == channel[1:]):
                        print('*STR* ' + sender + ' (' + channel + ')' + ': ' + message)
                    elif (channel in mods):
                        if (sender in mods.get(channel)):
                            print('*MOD* ' + sender + ' (' + channel + ')' + ': ' + message)
                    else:
                        print(sender + ' (' + channel + ')' + ': ' + message)

                    # FEATURE: Sub welcome
                    if (sender == "twitchnotify"):
                        command = getattr(module_name, 'TwitchNotify')
                        command.excuteCommand(con, channel, sender, message, False, False)

                    # Load new commands whenever somebody adds a command.
                    if (re.search('!com add \w*', message)):
                        cmds = pickle.load(open('cmds.p', 'r+'))

                    if (re.search("(.*)RAF2.*com (.*)Get.*Medieval.*Twitch(.*)5.000.*IP from Riots .*Refer.*A.*Friend on (.*)RAF2.*com", message)):
                        command = getattr(module_name, 'BanBot')
                        command.executeCommand(con, channel, sender, message, False, False)
                    
                    parse_message(channel, sender, message)
                    
    except socket.error:
        print('Socket died')

    except socket.timeout:
        print('Socket timeout')
