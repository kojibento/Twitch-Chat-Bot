# Import resources
from IRCCommands import *
import random
import pickle
import time  
import re
import os

# Variables
dcounter = 0
cmds = {}
banned = []
points = pickle.load(open('points.p', 'r+'))
#points = {}
fileN = 'banned.txt'
filename = os.getcwd() + '\\Banned Users\\' + fileN
dir_ = os.getcwd() + '\\Banned Users\\'

# Command template #
class ICommand(object):
    def getCommand():
        return 'UNKNOWN'

    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'MESSAGE')
        
# Allow the bot to join other channels
class Join(ICommand):
    @staticmethod
    def getCommand():
        return '!join'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            if (channel == '#mrbotto'): # Only works in bot's channel
                if (('#' + user) == message[1]) or (user == 'rubbixcube'):
                    if (len(message) > 1):
                        if (message[1][0] == '#'): 
                            send_message(con, channel, 'Now joining ' + message[1])
                            join_channel(con, message[1])
                            send_message(con, message[1], 'Hey there! I\'m MrBotto, my owner is RubbixCube who takes good care of me! I can do a lot of things and work best with Nightbot & Moobot.')
                        elif (message[1] == 'silent'): # No welcome message on join
                            if (message[2][0] == '#'):
                                send_message(con, channel, 'Now joining ' + message[2])
                                join_channel(con, message[2])
                        else:
                            # Assume invalid syntax
                            send_message(con, channel, 'Error: Invalid syntax. Please add a # before the channel name')

# Allow the bot to leave other channels
class Leave(ICommand):
    @staticmethod
    def getCommand():
        return '!leave'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            send_message(con, channel, 'Forced disconnect.')
            part_channel(con, channel)

#------------------------------------------------------------------------------#

## Global Commands ##
class Help(ICommand):
    @staticmethod
    def getCommand():
        return '!help'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'Need help? You can find a Wiki all about me here: http://github.com/RubbixCube/Twitch-Chat-Bot/wiki')

# List Commands
class Commands(ICommand):
    @staticmethod
    def getCommand():
        return '!cmdlist'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'All the commands can be found here: http://github.com/RubbixCube/Twitch-Chat-Bot/wiki/commands')

# Who made the bot
class Who(ICommand):
    @staticmethod
    def getCommand():
        return '!who'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, '/me is a bot created by RubbixCube and co developed with lclc98.')

# Check whether the bot is in the channel
class Here(ICommand):
    @staticmethod
    def getCommand():
        return '!here'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'I\'m here ' + user + '-senpai!')

# ??
class MrBotto(ICommand):
    @staticmethod
    def getCommand():
        return '!botto'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'MrDestructoid Domo Arigato Mr Botto MrDestructoid')

# Sass
class Daddy(ICommand):
    @staticmethod
    def getCommand():
        return '!daddy'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'My father is RubbixCube and my "other" father would be lclc98... Sadly, he is never around FeelsBadMan')

class Rivalry(ICommand):
    @staticmethod
    def getCommand():
        return '!rivalry'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'If you want a bot that does what it needs to, Nightbot and Moobot are your answers. But if you require advanced scripts/commands, I\'m your bot :D')

class Age(ICommand):
    @staticmethod
    def getCommand():
        return '!age'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'In Human years, I/m considered an Infant. In Computer years, maybe a few thousand OpieOP')

#------------------------------------------------------------------------------#

## Channel specific commands ##
# Deathcounter for Chris
class DCounter(ICommand):
    @staticmethod
    def getCommand():
        return '!deaths'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        global dcounter
        if (channel == '#teiresias911'):
            if (len(message) > 2):
                if (message[1] == 'add'):
                    if (isMod):
                        dcounter = int(dcounter) + 1
                        send_message(con, channel, 'Deathcounter now at ' + str(dcounter))
                if (message[1] == 'set'):
                    if (isMod):
                        dcounter = int(message[2])
                        send_message(con, channel, 'Deathcounter now set to ' + str(dcounter))
                if (message[1] == 'reset'):
                    if (isMod):
                        dcounter = 0
                        send_message(con, channel, 'The Deathcounter has been reset')
        else:
            send_message(con, channel, 'Deathcounter: ' + str(dcounter))


# Sub Notify
class TwitchNotify(ICommand):
    @staticmethod
    def getCommand():
        return 'twitchnotify'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        msg = str.split(message)
        if (re.match('\w* subscribed for \w* months in a row!', message)):
            send_message(con, channel, 'Thanks for your continued contribution %s!' % msg[0])
        elif (re.match('\w* just subscribed!', message)):
            send_message(con, channel, str.format('Welcome to the channel %s. Enjoy your stay!' % msg[0]))
        elif (re.match('\w* viewers resubscribed while you were away!', message)):
            send_message(con, channel, 'Thanks for subscribing!')

# Chat Commands
class ComAdd(ICommand):
    @staticmethod
    def getCommand():
        return '!comadd'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            global cmds
            space = ' '
            cmdmsg = space.join(message)
            if (len(message) > 1):
                if (message[1] not in cmds):
                    maxword = 8 + len(message[1])
                    cmds[message[1]] = cmdmsg[maxword:-1]
                    pickle.dump(cmds, open('cmds.p','wb'))
                    send_message(con, channel, 'A new command has been added.')
                else:
                    send_message(con, channel, 'Error: This command already exists.')
            else:
                 send_message(con, channel, 'Invalid Syntax. Please try again or ask for help.')
                
class ComDel(ICommand):
    @staticmethod
    def getCommand():
        return '!comdel'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            global cmds
            space = ' '
            cmdmsg = space.join(message)
            if (len(message) > 1):
                if (message[1] in cmds):
                    cmds.pop(message[1])
                    pickle.dump(cmds, open('cmds.p','wb'))
                    send_message(con, channel, 'An existing command has been deleted.')
                else:
                    send_message(con, channel, 'Error: This command doesn\'t exist.')

class ComEdit(ICommand):
    @staticmethod
    def getCommand():
        return '!comedit'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            global cmds
            space = ' '
            cmdmsg = space.join(message)
            if (len(message) > 1):
                if (message[1] in cmds):
                    maxword = 9 + len(message[1])
                    cmds[message[1]] = cmdmsg[maxword:-1]
                    pickle.dump(cmds, open('cmds.p','wb'))
                    send_message(con, channel, 'An existing command has been changed.')
                else:
                    send_message(con, channel, 'Error: This command doesn\'t exist.')

class Com(ICommand):
    @staticmethod
    def getCommand():
        return '!com'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            global cmds
            space = ' '
            cmdmsg = space.join(message)
            if (len(message) > 1):
                if (message[1] == 'list'):
                    send_message(con, channel, str(cmds))
                elif (message[1] == 'save'):
                    pickle.dump(cmds, open('cmds.p','wb'))
                    print('The commands dictionary has been saved.')
                elif (message[1] == 'load'):
                    cmds = pickle.load(open('cmds.p', 'r+'))
                    print('The commands dictionary has been loaded.')
                else:
                    send_message(con, channel, 'Invalid Syntax. Please try again or ask for help.')

# MiniGame: TwitchSlots 
class TwitchSlot(ICommand):
    @staticmethod
    def getCommand():
        return '!slotpull'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (user not in points):
            send_message(con, channel, 'You have been given 100 points as you just joined the system.')
            points[user] = 100
        if (points[user] > 20):
            points[user] = points[user] - 20
            emote = ['4Head', 'ANELE', 'ArsonNoSexy', 'AsianGlow', 'AtGL', 'AthenaPMS', 'AtIvy', 'AtWW', 'BabyRage', 'BatChest', 'BCWarrior', 'BibleThump', 'BigBrother', 'BionicBunion', 'BlargNaut', 'BloodTrail', 'BORT', 'BrainSlug', 'BrokeBack', 'BuddhaBar', 'CorgiDerp', 'CougarHunt', 'DAESuppy', 'DansGame', 'DatHass', 'DatSheffy', 'DBstyle', 'DendiFace', 'DogFace', 'EagleEye', 'EleGiggle', 'EvilFetus', 'FailFish', 'FPSMarksman', 'FrankerZ', 'FreakinStinkin', 'FUNgineer', 'FunRun', 'FuzzyOtterOO', 'GasJoker', 'GingerPower', 'GrammarKing', 'HassanChop', 'HeyGuys', 'HotPokket', 'HumbleLife', 'ItsBoshyTime', 'Jebaited', 'JKanStyle', 'JonCarnage', 'KAPOW', 'Kappa', 'Keepo', 'KevinTurtle', 'Kippa', 'Kreygasm', 'KZskull', 'Mau5', 'mcaT', 'MechaSupes', 'MrDestructoid', 'MVGame', 'NightBat', 'NinjaTroll', 'NoNoSpot', 'noScope420', 'NotAtk', 'OMGScoots', 'OneHand', 'OpieOP', 'OptimizePrime', 'panicBasket', 'PanicVis', 'PazPazowitz', 'PeoplesChamp', 'PermaSmug', 'PicoMause', 'PipeHype', 'PJHarley', 'PJSalt', 'PMSTwin', 'PogChamp', 'Poooound', 'PraiseIt', 'PRChase', 'PunchTrees', 'PuppeyFace', 'RaccAttack', 'RalpherZ', 'RedCoat', 'ResidentSleeper', 'RitzMitz', 'RuleFive', 'Shazam', 'shazamicon', 'ShazBotstix', 'ShibeZ', 'SMOrc', 'SMSkull', 'SoBayed', 'SoonerLater', 'SriHead', 'SSSsss', 'StoneLightning', 'StrawBeary', 'SuperVinlin', 'SwiftRage', 'tbBaconBiscuit', 'tbChickenBiscuit', 'tbQuesarito', 'tbSausageBiscuit', 'tbSpicy', 'tbSriracha', 'TF2John', 'TheRinger', 'TheTarFu', 'TheThing', 'ThunBeast', 'TinyFace', 'TooSpicy', 'TriHard', 'TTours', 'UleetBackup', 'UncleNox', 'UnSane', 'Volcania', 'WholeWheat', 'WinWaker', 'WTRuck', 'WutFace', 'YouWHY']
            slot1 = random.choice(emote) #Twitch Emote 1
            slot2 = random.choice(emote) #Twitch Emote 2
            slot3 = random.choice(emote) #Twitch Emote 3
            if (slot1 == 'Kappa'):
                if (slot2 == 'Kappa'):
                    if (slot3 == 'Kappa'):
                        send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
                        send_message(con, channel, 'PogChamp We have a winner! Congratulations ' + user + '. You have won 1 000 000 points!')
                        points[user] = points[user] + 1000000 # 1Mil
                        pickle.dump(points, open('points.p','wb'))
            elif (slot1 == slot2 == slot3):
                send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
                send_message(con, channel, 'We have a winner! Congratulations ' + user + '. You have won 1000 points!')
                points[user] = points[user] + 50000 # 50K
                pickle.dump(points, open('points.p','wb'))
            else:
                send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
        else:
            send_message(con, channel, 'Sorry. You do not have enough points')

# MiniGame: Roulette
class Roulette(ICommand):
    @staticmethod
    def getCommand():
        return '!bet'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (len(message) > 1):
            if (points[user] >= message[1]):
                points[user] = points[user] - message[1]
                chance = [1,2] #RNG System
                result = random.choice(chance)
                if (result == 1):
                    send_message(con, channel, 'Lady luck did not consent to smile, ' + user + ' have been killed...')
                else:
                    send_message(con, channel, 'You beat the system ' + user +'. We have depostited ' + str(2*num) + ' into your account.')
            else:
                send_message(con, channel, 'Sorry ' + user + '. You do not have enough points for that bet.')

# Points Moderation
class PointsMOD(ICommand):
    @staticmethod
    def getCommand():
        return '!mpoints'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            if (message[1] == 'add'):
                if (message[2] in points):
                    points[message[2]] = points[message[2]] + int(message[3])
                    send_message(con, channel, message[3] + ' points have been added to ' + message[2] + '\'s balance.')
                    pickle.dump(points, open('points.p','wb'))
                else: #User not in the points dictionary
                    points[message[2]] = 100
                    points[message[2]] = points[message[2]] + int(message[3])
                    send_message(con, channel, message[3] + ' points have been added to ' + message[2] + '\'s balance.')
                    pickle.dump(points, open('points.p','wb'))
            elif (message[1] == 'reset'):
                if (message[2] in points):
                    points[message[2]] = 0
                    send_message(con, channel, message[2] + '\'s points have been reset.')
                    pickle.dump(points, open('points.p','wb'))
                else: #User not in points dictionary
                    send_message(con, channel, 'Error: The username was not found in the dictionary')
            elif (message[1] == 'list'):
                if (message[2] in points):
                    send_message(con, channel, message[2] + ': ' + str(points[message[2]]))
                else: #User not in points dictionary
                    send_message(con, channel, 'Error: The username was not found in the dictionary')

# Auto Ban
class BanBot(ICommand):
    @staticmethod
    def getCommand():
        return 'banbot'
    @staticmethod
    def executeCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, '.ban ' + user) # Bans the user
        send_message(con, channel, 'Punishment has been served.')
        if not (os.path.exists(dir_)):
            os.makedirs(dir_)
        banned = open(filename,'a')
        banned.write(time.strftime("%Y-%m-%d %H:%M") + ' | ' + user + '\n')
        banned.close()

# Check how many users are banned
class Check(ICommand):
    @staticmethod
    def getCommand():
        return '!check'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        lines = 0
        with open(filename,'r') as li:
            for line in li:
                if line.strip():
                    lines += 1
        send_message(con, channel, str(lines) + ' bots have been banned from this channel.')
