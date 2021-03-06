#
# hitzSaveRead.py
#
# extract data from a PS2 NHL Hitz 20-02 save file (unknown if it works for xbox or GC saves)
#

import binascii
import pprint
import os
import csv
import datetime

FILENAME = 'BASLUS-20140NHLHitz'
PATH = '/media/pool/games/PlayStation 2/saves/NHL Hitz 20-02/'

#if you have a save file directly, the offset is 8. if you have a OPL memory card image, the offset is 46080 + the 8 of the file
OFFSET = 8
#OFFSET = 46088

# Converts the hex string to an integer value

def convert(hexString):  
    return int(binascii.hexlify(hexString),16)

def hitzSaveRead(filename, offset = OFFSET): 
    with open(filename,'rb') as fp:
        contents=fp.read()
        fp.close()

    #strip header
    contents=contents[offset:]

    players={}


    namelength=5
    gamesplayedPosition=10 
    shotsPosition=12
    goalsPosition=14
    assistsPosition=16
    consecutivewinsPosition=18
    consecutivelossesPosition=20
    onetimergoalsPosition=22
    onetimershotsPosition=24
    unknown01Position=26
    passesPosition=28
    unknown02Position=30
    hitsPosition=32
    winsPosition=34
    unknown03Position=36
    fightswonPosition=38
    p = lambda x,y: contents[x+y+1:x+y-1:-1] # get 2 bytes of data in reverse endianness
    for i in range(20): # there's a max of 20 users stored in a save

        startpos = i * 304
        name=contents[startpos:startpos+5].rstrip('\x00')
        gamesplayedhex=p(startpos,gamesplayedPosition)
        shotshex=p(startpos,shotsPosition) 
        goalshex = p(startpos,goalsPosition)
        assistshex = p(startpos,assistsPosition)
        consecutivewinshex = p(startpos,consecutivewinsPosition)
        consecutivelosseshex = p(startpos,consecutivelossesPosition)
        onetimergoalshex = p(startpos,onetimergoalsPosition)
        onetimershotshex = p(startpos,onetimershotsPosition)
        unknown01hex = p(startpos,unknown01Position)
        passeshex = p(startpos,passesPosition)
        unknown02hex = p(startpos,unknown02Position)
        hitshex = p(startpos,hitsPosition)
        winshex = p(startpos,winsPosition)
        unknown03hex = p(startpos,unknown03Position)
        fightswonhex = p(startpos,fightswonPosition)

        gamesplayed = convert(gamesplayedhex)
        shots = convert(shotshex)
        goals = convert(goalshex)
        assists = convert(assistshex)
        consecutivewins = convert(consecutivewinshex)
        consecutivelosses = convert(consecutivelosseshex)
        onetimergoals = convert(onetimergoalshex)
        onetimershots = convert(onetimershotshex)
        unknown01 = convert(unknown01hex)
        passes = convert(passeshex)
        unknown02 = convert(unknown02hex)
        hits = convert(hitshex)
        wins = convert(winshex)
        unknown03 = convert(unknown03hex)
        fightswon = convert(fightswonhex)
        player={'name':name,
                'games_played':gamesplayed,
                'shots':shots,
                'goals':goals,
                'assists':assists,
                'consecutive_wins':consecutivewins,
                'consecutive_losses':consecutivelosses,
                'one-timer_goals':onetimergoals,
                'one-timer_shots':onetimershots,
                'unknown01':unknown01,
                'passes':passes,
                'unknown02':unknown02,
                'hits':hits,
                'wins':wins,
                'unknown03':unknown03,
                'fights_won':fightswon
                }
        players[name]=player
    return players

if __name__ == '__main__':
    players = hitzSaveRead(os.path.join(PATH,FILENAME)) 
    pprint.pprint(players)
    # CSV output
    # list of keys for first row of CSV
    headings = ['name','games_played','shots','goals','assists','consecutive_wins','consecutive_losses','one-timer_goals','one-timer_shots','unknown01','passes','unknown02','hits','wins','unknown03','fights_won']
    # use list of keys to make sure CSV is in the same order
    with open('output.csv','wb+') as fp:
        csvwriter=csv.writer(fp)
        csvwriter.writerow(headings)
        for player in players:
            csvwriter.writerow([player[heading] for heading in headings].append(datetime.datetime.today()))
