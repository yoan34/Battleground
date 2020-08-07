import copy
from random import choice, sample
import time, os
from operator import itemgetter

from Components.Minion import Minion
from Components.Simulation import Simulation

from constants.minions import MINIONS
from constants.heroes import DATA_HEROES

DATA_MINIONS = {key: {'points': 0, 'lvl': MINIONS[key]['lvl']} for key in MINIONS}
os.system("mode con cols=152 lines=50")
simulation = Simulation(DATA_MINIONS, time_action=0, is_human=True)
while len(simulation.players) > 1:
    simulation.play_all_actions_in_a_turn()
    simulation.matchmaking()
    simulation.run_all_fights()
    simulation.next_turn()
simulation.view_all_players()
print(simulation.players)[0]