from IRCCommands import *
import time  
import re

# Variables #
now = time.strftime("%c")

# Basic Use of commands #
class ICommand(object):
    def getCommand():
        return 'UNKNOWN'
    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        print(message)
        
# Allow the bot to join other channels #
class Join(ICommand):
    @staticmethod
    def getCommand():
        return '!join'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        print(message)
        if len(message) > 1:
            if message[1][0] == '#':
                send_message(con, channel, 'Now joining ' + message[1])
                join_channel(con, message[1])
                #send_message(con, message[1], 'Hello ' + message[1])
# Allow the bot to leave other channels #
class Leave(ICommand):
    @staticmethod
    def getCommand():
        return '!leave'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'Good bye')
        part_channel(con, channel)


# Basic commands in ALL channels #
class Who(ICommand):
    @staticmethod
    def getCommand():
        return '!who'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (len(message) == 2):
            send_message(con, channel, '/me is a bot created by RubbixCube and co developed with lclc98.')

class Here(ICommand):
    @staticmethod
    def getCommand():
        return '!here'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'I\'m here ' + user + '-senpai!')

class Version(ICommand):
    @staticmethod
    def getCommand():
        return '!ver'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'MrBotto ver. 2.1.7')

class MrBotto(ICommand):
    @staticmethod
    def getCommand():
        return '!botto'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'Domo Arigato Mr Botto')
        
# Start channel specific commands #
class Peta(ICommand):
    @staticmethod
    def getCommand():
        return '!here'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if channel == '#takarita324':
            send_message(con, channel, '/me is now dialing PETA to report Taka')

class Math(ICommand):
    @staticmethod
    def getCommand():
        return '!math'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if channel == '#takarita324':
            send_message(con, channel, '3 * 10 = 13')
# End channel specific commands #
