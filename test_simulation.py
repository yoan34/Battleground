import copy
from random import choice, sample
import time, os
from operator import itemgetter

from Components.Minion import Minion
from Components.Simulation import Simulation

from constants.minions import MINIONS
from constants.heroes import DATA_HEROES

DATA_MINIONS = {key: {'points': 0, 'lvl': MINIONS[key]['lvl']} for key in MINIONS}

GAMES = 1
average_turn = 0
view_percent = 0
view = True if GAMES == 1 else False
view_shop = True if GAMES == 1 else False



a = time.time()
for i in range(GAMES):
    simulation = Simulation(DATA_MINIONS, view_shop=view_shop, view=view)
    while len(simulation.players) > 1:
        simulation.play_all_actions_in_a_turn()
        simulation.matchmaking()
        simulation.run_all_fights()
        simulation.next_turn()
    
    simulation.players_deads.append(simulation.players[0])
    for pos, player in enumerate(simulation.players_deads):
        DATA_HEROES[player.hero.true_name]['count'] += 1
        DATA_HEROES[player.hero.true_name]['points'] += pos+1
    
    average_turn += simulation.turn
    if i % (GAMES/100) == 0:
        print(str(view_percent)+'%\r', end='')
        view_percent += 1
b = time.time()



for hero in DATA_HEROES:
    DATA_HEROES[hero]['average'] = (DATA_HEROES[hero]['points'] / DATA_HEROES[hero]['count']) if DATA_HEROES[hero]['count'] != 0 else 0
for hero in sorted(DATA_HEROES, key=lambda x: DATA_HEROES[x]['average'], reverse=True):
    print("{:12}: pts: {:4} counts: {:3}  average: {:.2f}".format(hero, DATA_HEROES[hero]['points'],
        DATA_HEROES[hero]['count'], DATA_HEROES[hero]['average'] ))

list_data_minions = [(name, simulation.data_minions[name]['points'], simulation.data_minions[name]['lvl']) for name in simulation.data_minions]
list_data_minions =  sorted(list_data_minions, key=lambda x: x[2])
list_data_minions =  sorted(list_data_minions, key=itemgetter(1))

for name, points, lvl in list_data_minions:
    print("{:22} --> points: {}   lvl: {:2}".format(name, points, lvl))


print('average turn: ', average_turn/GAMES)
print("time: {:.2f}".format(b-a))
