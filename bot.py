                                #!/usr/bin/env python
## MrBotto | Created by RubbixCube with help from lclc98. ##

# Import resources
from modules.IRCCommands import *
import importlib
import socket
import pickle
import time
import os
import re

# Define Variables
mods = {}
cmds = pickle.load(open('cmds.p', 'r+'))

# Get required information
HOST = 'irc.twitch.tv'                          # Twitch IRC Network
PORT = 6667                                     # Default IRC-Port
CHAN = ['#XXXXXX']                              # Channelname = #{Nickname}
NICK = 'XXXXXXX'                                # Twitch username
PASS = 'oauth:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'   # OAuth Key


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
# This allows the bot to 'see' an ID in the file
options = ['Join','Leave','Help','Commands','Who','Here',
           'MrBotto','Cylons','Age','DCounter',
           'ComAdd','ComDel','ComEdit','Com','TwitchSlot',
           'Roulette','PointsMOD','Check']

# Check whether a command exists
def parse_message(channel, user, msg):
    if (len(msg) >= 1):
        msg = msg.split(' ')
        global cmds
        for commandID in options:
            command = getattr(module_name, commandID)
            if (command.getCommand() == msg[0]):
                modStatus = False
                if (channel in mods):
                    modStatus = user in mods.get(channel)
                command.excuteCommand(con, channel, user, msg, modStatus, False)
                break
        if (msg[0] in cmds):
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

                # Add the mod to a dictionary
                message = ' '.join(line)
                x = re.findall('^:jtv MODE (.*?) \+o (.*)$', message) # Find the message
                if (len(x) > 0):
                    channel = x[0][0]
                    if (channel not in mods): # If the channel isn't already in the list
                        mods[channel] = []
                    modList = mods.get(channel)
                    # Experimental statement below...
                    if (type(modList) != str): # Check if the list is in str mode
                        modList.append(x[0][1])
                    
                # Remove the mod from the dictionary
                y = re.findall('^:jtv MODE (.*?) \-o (.*)$', message)
                if (len(y) > 0):
                    channel = y[0][0]
                    if (channel in mods):
                        if (type(mods.get(channel)) != str):
                            mods.get(channel).remove(y[0][1]) 

                if (line[1] == 'PRIVMSG'):
                    sender = get_sender(line[0])
                    message = get_message(line)
                    channel = line[2]
                    fileTime = time.strftime("%Y-%m-%d") + '.txt'
                    filename = os.getcwd() + '\Logs\\' + fileTime
                    dir_ = os.getcwd() + '\Logs\\'
                    print(time.strftime("%H:%M:%S") + ' | ' + sender + ' (' + channel + ')' + ': ' + message)
                    if not (os.path.exists(dir_)):
                        os.makedirs(dir_)
                    log = open(filename,'a')
                    log.write(time.strftime("%H:%M:%S") + ' | ' + sender + ' (' + channel + ')' + ': ' + message + '\n')
                    log.close()


                    ''' Thank new/recurring subs '''
                    if (sender == "twitchnotify"):
                        command = getattr(module_name, 'TwitchNotify')
                        command.excuteCommand(con, channel, sender, message, False, False)

                    ''' Load new commands whenever somebody adds a command '''
                    if (re.search('!com add \w*', message)):
                        cmds = pickle.load(open('cmds.p', 'r+'))

                    ''' Ban advertising bots '''
                    if (re.search("(.*)RAF2.*com (.*)Get.*Medieval.*Twitch(.*)5.000.*IP from Riots .*Refer.*A.*Friend on (.*)RAF2.*com", message)):
                        command = getattr(module_name, 'BanBot')
                        command.executeCommand(con, channel, sender, message, False, False)

                    ''' More advertising bots... (facepalm) '''
                    if (re.search("(.*)championship riven skin code (.*)http://bit.ly/riven-skins-giveaway", message)):
                        command = getattr(module_name, 'BanBot')
                        command.executeCommand(con, channel, sender, message, False, False)

                    ''' Find how long the channel has been live '''
                    msg = str.split(message)
                    if (msg[0] == '!live'):
                        url = 'http://nightdev.com/hosted/uptime.php?channel=' + channel[1:]
                        contents = urllib2.urlopen(url)
                        live = contents.read()
                        if (contents.read() == 'The channel is not live.'):
                            send_message(con, channel, live)
                        else:
                            send_message(con, channel, 'The channel has been live for ' + live)

                    ''' Last seen system '''
                    if (msg[0] == '!whereis'):
                        if (len(message) > 1):
                            if (msg[1] in last_seen):
                                s1 = last_seen[msg[1]]
                                s2 = datetime.datetime.now()
                                final = s2 - s1
                                final = divmod(final.days * 86400 + final.seconds, 60)
                                final_ = re.findall('(\d+)',str(final))
                                send_message(con, channel, msg[1] + ' was last seen ' + str(final_[0]) + ' minute(s) and ' + str(final_[1]) + ' second(s) ago.')
                            elif (msg[1] == 'mrbotto'):
                                send_message(con, channel, 'Error 404: I do not exist Kappa')
                            else:
                                send_message(con, channel, 'It seems ' + msg[1] + ' is MIA. We need to send a team after them! Who wants to volunteer?')

                    
                    parse_message(channel, sender, message)
                    
    except socket.error:
        print('Socket died')

    except socket.timeout:
        print('Socket timeout')
