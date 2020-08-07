import time, os
from random import choice

from Components.Battle import Battle
from Components.Player import Player
from Components.Minion import Minion
from Components.Pool import Pool

from constants.minions import dht_replicatingMenace, dht_spore


TIME = 0
GAMES = 1

TIME = 0 if GAMES > 1 else TIME
HISTORY = True if GAMES == 1 else False

result = {(1,0): 0, (0,1): 0, (0,0): 0}
a = time.time()
view_percent = 0
for i in range(GAMES):
    archetype = choice(('beast', 'demon', 'meca', 'dragon','murloc'))
    pool = Pool(archetype=archetype)
    friend, enemy = Player('I1', pool, archetype, is_human=False), Player('I2', pool, archetype, is_human=False)

    for pos, player in enumerate((friend, enemy)):
        player.debug = False
        player.time_by_action = 1
        player.hero = player.get_hero(archetype)
        if player.hero.name == 'Illidan':
            player.hero.illidan = True
        elif player.hero.name == 'Deathwing':
            player.hero.deathwing = True



# stock = (
#     'soulJunggler', 'impMama','impGangBoss', 'wrathWeaver','imprisoner','fiendishServant', #demon
#     'bronzeWarden','drakonidEnforcer','waxriderTogwaggle','heraldOfFlame', #dragon
#     'annoyOModule', 'securityRover','foeReaper4000', 'mecharoo','deflectOBot','mechanoEgg', #meca
#     'replicatingMenace','pilotedShredder',#meca
#     'selflessHero', 'scallyWag', 'bolvarFireblood', 'baronRivendare',#neutral
#     'spawnOfNzoth', #neutral
#     'caveHydra', 'packLeader', 'ironhideDirehorn', 'mamaBear','ratPack','theBeast',#beast
#     'goldrinnTheGreatWolf','infestedWolf','kindlyGrandmother', #beast
#     'dreadAdmiralEliza','ripsnarlCaptain', 'southseaCaptain','natPagleExtremeAngler',#pirate
#     'deckSwabbie',
#     'rockpoolHunter','murlocWarleader','oldMurkEye','coldlightSeer','toxfin','kingBagurgle') #pirate



# enemy.board = enemy.create_minions(3, False ,'seabreakerGoliath','zappSlywick', 'scallyWag')
# friend.board = friend.create_minions(0, False, 'malGanis', 'malGanis')


#---------------------------------------------------------------




    # EM1 = enemy.create_minion(False, 'selflessHero')
    # # EM1.atk, EM1.hp, EM1.shield, EM1.poisonous = 8,8, True, True
    # EM2 = enemy.create_minion(False, 'murlocTidehunter')
    # EM2.atk, EM2.hp = 1,1
    # EM3 = enemy.create_minion(False, 'oldMurkEye')
    # EM3.atk, EM3.hp, EM3.taunt, EM3.shield = 7,4, False,False
    # EM4 = enemy.create_minion(False, 'murlocTidehunter')
    # # EM4.atk, EM4.hp = 2,2
    # EM5 = enemy.create_minion(False, 'murlocTidehunter')
    # EM5.atk, EM5.hp = 1,1
    # EM6 = enemy.create_minion(False, 'murlocWarleader')
    # # EM6.atk, EM6.hp = 5,5
    # EM7 = enemy.create_minion(False, 'murlocWarleader')
    # # EM7.atk, EM7.hp, EM7.taunt = 3,3, True

    # enemy.board = [EM1,EM2,EM3,EM4,EM5,EM6,EM7]


    # FM1 = enemy.create_minion(False, 'monstrousMacaw')
    # # FM1.atk, FM1.hp = 13,13
    # FM2 = enemy.create_minion(False, 'spawnOfNzoth')
    # # FM2.atk, FM2.hp, FM2.taunt = 9,10,False
    # FM3 = enemy.create_minion(False, 'southseaCaptain')
    # # FM3.atk, FM3.hp = 24,24
    # FM4 = enemy.create_minion(False, 'alleycat')
    # # FM4.atk, FM4.hp = 32,32
    # FM5 = enemy.create_minion(False, 'righteousProtector')
    # # FM5.atk, FM5.hp = 17,17
    # FM6 = enemy.create_minion(False, 'monstrousMacaw')
    # # FM6.atk, FM6.hp = 7,9
    # FM7 = enemy.create_minion(False, 'pogoHopper')
    # FM7.atk, FM7.hp, FM7.taunt, FM7.shield = 22,24, True, True
    # friend.board = [FM1,FM2,FM3,FM4, FM5,FM6]


    enemy.board = enemy.create_minions(
        'natPagleExtremeAngler', 'natPagleExtremeAngler', 'natPagleExtremeAngler',
        length=0, gold=False, tier_min=1, tier_max=1)

    friend.board = friend.create_minions(
        'natPagleExtremeAngler','natPagleExtremeAngler','natPagleExtremeAngler',
        length=0, gold=False,tier_min=1, tier_max=1)
    
    battle = Battle(friend, enemy, t=TIME, h=HISTORY)
    res, damage, minion_rafaam, history = battle.fight()
    result[res] += 1
    if i % (GAMES/100) == 0:
        print(str(view_percent)+'%\r', end='')
        view_percent += 1
b = time.time()
print('time: {:.2f}'.format(b-a))
percent = lambda x: result[x]*100/GAMES
print("Win: {:.3f}%   | Tie: {:.3f}%   | Lose: {:.3f}%".format(percent((1,0)),
    percent((0,0)), percent((0,1)))) if GAMES > 1 else None
#-------------------------------------------------------

if HISTORY:
    answer, i = '', 0
    while answer != 'q':
        os.system('cls')
        print(history[i])
        answer = input('>>: ')
        if answer == 'm':
            i += 1 if i < len(history)-1 else 0
        elif answer == 'k':
            i -= 1 if i > 0 else 0


