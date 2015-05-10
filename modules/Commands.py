## Commands ##
# Import resources
from IRCCommands import *
import random
import pickle
import time  
import re

# Variables
cmds = {}
points = pickle.load(open('points.p', 'r+'))


# Basic Use of commands #
class ICommand(object):
    def getCommand():
        return 'UNKNOWN'
    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        print(message)
        
# Allow the bot to join other channels (DEPRECIATED)
class Join(ICommand):
    @staticmethod
    def getCommand():
        return '!join'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        #if (channel == ''): # Only works in my channel
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
            send_message(con, channel, 'Good bye')
            part_channel(con, channel)


## Global Commands ##
class Help(ICommand):
    @staticmethod
    def getCommand():
        return '!help'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'List of basic commands: !who, !here, !ver, !leave, !botto')

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

# Easter Egg
class MrBotto(ICommand):
    @staticmethod
    def getCommand():
        return '!botto'
    @staticmethod
    def excuteCommand(con, channel, user, message, isMod, isSub):
        send_message(con, channel, 'MrDestructoid Domo Arigato Mr Botto MrDestructoid')


## FEATURE: Sub welcome ##
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

## FEATURE: Add/Edit/Delete commands from chat ##
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

## FEATURE: TwitchEmote slot machine ## 
class TwitchSlot(ICommand):
    @staticmethod
    def getCommand():
        return '!slotpull'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        emote = ['4Head', 'ANELE', 'ArsonNoSexy', 'AsianGlow', 'AtGL', 'AthenaPMS', 'AtIvy', 'AtWW', 'BabyRage', 'BatChest', 'BCWarrior', 'BibleThump', 'BigBrother', 'BionicBunion', 'BlargNaut', 'BloodTrail', 'BORT', 'BrainSlug', 'BrokeBack', 'BuddhaBar', 'CorgiDerp', 'CougarHunt', 'DAESuppy', 'DansGame', 'DatHass', 'DatSheffy', 'DBstyle', 'DendiFace', 'DogFace', 'EagleEye', 'EleGiggle', 'EvilFetus', 'FailFish', 'FPSMarksman', 'FrankerZ', 'FreakinStinkin', 'FUNgineer', 'FunRun', 'FuzzyOtterOO', 'GasJoker', 'GingerPower', 'GrammarKing', 'HassanChop', 'HeyGuys', 'HotPokket', 'HumbleLife', 'ItsBoshyTime', 'Jebaited', 'JKanStyle', 'JonCarnage', 'KAPOW', 'Kappa', 'Keepo', 'KevinTurtle', 'Kippa', 'Kreygasm', 'KZskull', 'Mau5', 'mcaT', 'MechaSupes', 'MrDestructoid', 'MVGame', 'NightBat', 'NinjaTroll', 'NoNoSpot', 'noScope', 'NotAtk', 'OMGScoots', 'OneHand', 'OpieOP', 'OptimizePrime', 'panicBasket', 'PanicVis', 'PazPazowitz', 'PeoplesChamp', 'PermaSmug', 'PicoMause', 'PipeHype', 'PJHarley', 'PJSalt', 'PMSTwin', 'PogChamp', 'Poooound', 'PraiseIt', 'PRChase', 'PunchTrees', 'PuppeyFace', 'RaccAttack', 'RalpherZ', 'RedCoat', 'ResidentSleeper', 'RitzMitz', 'RuleFive', 'Shazam', 'shazamicon', 'ShazBotstix', 'ShibeZ', 'SMOrc', 'SMSkull', 'SoBayed', 'SoonerLater', 'SriHead', 'SSSsss', 'StoneLightning', 'StrawBeary', 'SuperVinlin', 'SwiftRage', 'tbBaconBiscuit', 'tbChickenBiscuit', 'tbQuesarito', 'tbSausageBiscuit', 'tbSpicy', 'tbSriracha', 'TF2John', 'TheRinger', 'TheTarFu', 'TheThing', 'ThunBeast', 'TinyFace', 'TooSpicy', 'TriHard', 'TTours', 'UleetBackup', 'UncleNox', 'UnSane', 'Volcania', 'WholeWheat', 'WinWaker', 'WTRuck', 'WutFace', 'YouWHY']
        slot1 = random.choice(emote) #Twitch Emote 1
        slot2 = random.choice(emote) #Twitch Emote 2
        slot3 = random.choice(emote) #Twitch Emote 3
        if (user not in points):
            points[user] = 0
        if (slot1 == 'Kappa'):
            if (slot2 == 'Kappa'):
                if (slot3 == 'Kappa'):
                    send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
                    send_message(con, channel, 'PogChamp We have a winner! Congratulations ' + user + '. You have won 100 000 points!')
                    points[user] = points[user] + 100000
                    pickle.dump(points, open('points.p','wb'))
        elif (slot1 == slot2 == slot3):
            send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
            send_message(con, channel, 'We have a winner! Congratulations ' + user + '. You have won 1000 points!')
            points[user] = points[user] + 1000
            pickle.dump(points, open('points.p','wb'))
        else:
            send_message(con, channel, slot1 + ' | ' + slot2 + ' | ' + slot3)
           
class TwitchSlotMod(ICommand):
    @staticmethod
    def getCommand():
        return '!slotmod'
    @staticmethod    
    def excuteCommand(con, channel, user, message, isMod, isSub):
        if (isMod):
            if (len(message) > 1):
                if (message[1] == 'remove'):
                    emote.remove(message[2])
                    send_message(con, channel, 'An emote has been removed')
                elif (message[1] == 'points'):
                    if (message[2] == 'add'):
                        if (message[3] in points):
                            points[message[3]] = points[message[3]] + int(message[4])
                            send_message(con, channel, message[4] + ' points have been added to ' + message[3] + '\'s balance.')
                            pickle.dump(points, open('points.p','wb'))
                        else:
                            #User not in the points dictionary
                            points[message[3]] = 0
                            points[message[3]] = points[message[3]] + int(message[4])
                            send_message(con, channel, message[4] + ' points have been added to ' + message[3] + '\'s balance.')
                            pickle.dump(points, open('points.p','wb'))
                    elif (message[2] == 'reset'):
                        if (message[3] in points):
                            points[message[3]] = 0
                            send_message(con, channel, message[3] + '\'s points have been reset.')
                            pickle.dump(points, open('points.p','wb'))
                    elif (message[2] == 'list'):
                        if (message[3] in points):
                            send_message(con, channel, message[3] + ': ' + str(points[message[3]]))

