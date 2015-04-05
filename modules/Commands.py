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
                send_message(con, message[1], 'Hello ' + chan + '. A probably don\'t have any commands for this channel, if that is true please contact RubbixCube. If false, disregard this message!')
                
# Allow the bot to leave other channels #
class Leave(ICommand):
    @staticmethod
    def getCommand():
        return '!leave'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
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
        send_message(con, channel, 'MrBotto ver. 2.5.0')

class MrBotto(ICommand):
    @staticmethod
    def getCommand():
        return '!botto'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'Domo Arigato Mr Botto')

class Hire(ICommand):
    @staticmethod
    def getCommand():
        return '!hire'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            send_message(con, channel, 'Hello ' + user + '. If you wish to hire me, just type !join #<channel> and I\'ll be there to help you out. Just a heads up though, I won\'t be all that functional unless you talk to RubbixCube who will add commands for you.')

class Mods(ICommand):
    @staticmethod
    def getCommand():
        return '!mods'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, '/mods')

            
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

# Welcome new subs to the channel!
class TwitchNotify(ICommand):
    @staticmethod
    def getCommand():
        return 'twitchnotify'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        msg = str.split(message)
        if re.match('\w* subscribed for \w* months in a row!', message):
            send_message(con, channel, 'Thanks for your continued contribution %s!' % msg[0])
        elif re.match('\w* just subscribed!', message):
            send_message(con, channel, str.format('Welcome to the channel %s. Enjoy your stay!' % msg[0]))
