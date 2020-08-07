"""
This class display the menu of the program.
    -Simulation human
    -Simulation IA
    -Start Bot
"""

import os, time, copy
from random import choice, sample
from operator import itemgetter

from Components.Player import Player
from Components.Pool import Pool
from Components.Minion import Minion
from Components.Simulation import Simulation

from constants.position import LEN_SHOP
from constants.minions import MINIONS_POOL, MINIONS
from constants.heroes import DATA_HEROES

class Menu:
    def __init__(self):
        """ states for show the 'read_me' """
        self.n_simulation_human = 0
        self.n_simulation_IA = 0
        self.n_bot = 0

    def start(self):
        """" Display the menu """
        os.system('cls')
        os.system("mode con cols=50 lines=12")
        print(" M E N U ".center(50, '-'))
        print('\n')
        print("1. Simulate and see one game.\n".rjust(40))
        print("2. Simulate many games.\n".rjust(34))
        print("-"*50)

    def simulation(self, t):
        """
        Method that simule the game in the shop, for a
        human and IA that perform action randomly.
        """
        os.system("mode con cols=152 lines=51")
        DATA_MINIONS = {key: {'points': 0, 'lvl': MINIONS[key]['lvl']} for key in MINIONS}
        simulation = Simulation(DATA_MINIONS, time_action=t)
        while len(simulation.players) > 1:
            simulation.play_all_actions_in_a_turn()
            simulation.matchmaking()
            simulation.run_all_fights()
            simulation.next_turn()
        simulation.view_all_players()
        print(simulation.players[0])
        return input('tape to back to the menu.')
    
    def many_simulation(self, n):
        DATA_MINIONS = {key: {'points': 0, 'lvl': MINIONS[key]['lvl']} for key in MINIONS}
        GAMES = n
        average_turn = view_percent = 0
        view = True if GAMES == 1 else False
        view_shop = True if GAMES == 1 else False
        a = time.time()
        for hero in DATA_HEROES:
            for i in range(8):
                DATA_HEROES[hero][i+1] = 0
        
        errors = 0
        for i in range(GAMES):
            simulation = Simulation(DATA_MINIONS)
            try:
                while len(simulation.players) > 1:
                    simulation.play_all_actions_in_a_turn()
                    simulation.matchmaking()
                    simulation.run_all_fights()
                    simulation.next_turn()
            except Exception:
                errors += 1
                continue
            else:
                simulation.players_deads.append(simulation.players[0])
                
                for pos, player in enumerate(simulation.players_deads):
                    DATA_HEROES[player.hero.true_name]['count'] += 1
                    DATA_HEROES[player.hero.true_name]['points'] += pos+1
                    DATA_HEROES[player.hero.true_name][8-pos] += 1

            average_turn += simulation.turn
            print('{}'.format(' '*23) + str(round(i/GAMES*100, 2))+'%\r', end='')
        b = time.time()
        os.system("mode con cols=85 lines=56")
        
        secondes = int(b-a+1)
        minutes = secondes //60
        secondes = secondes - (minutes*60)
        if minutes:
            t_game = "time: {}min {}s".format(minutes, secondes)
        else:
            t_game = "time: {}s".format(secondes)
        print('\n')
        # print('errors:', errors)
        print('average turn: {:.2f}  ||  {}'.format(average_turn/GAMES, t_game).center(75))
        print("games by sec: {:.2f}  || games: {}".format(GAMES/(b-a), GAMES).center(75))
        print('\n')
        for hero in DATA_HEROES:
            DATA_HEROES[hero]['average'] = (DATA_HEROES[hero]['points'] / DATA_HEROES[hero]['count']) if DATA_HEROES[hero]['count'] != 0 else 0

        print(' +--------------+-------+-----+-----+-----+-----+-----+-----+-----+-----+---------+')
        print(' |{}| games | 1st | 2sd | 3th | 4th | 5th | 6th | 7th | 8th | average |'.format('hero'.center(14)))
        print(' +--------------+-------+-----+-----+-----+-----+-----+-----+-----+-----+---------+')

        for hero in sorted(DATA_HEROES, key=lambda x: DATA_HEROES[x]['average'], reverse=True):
            c_hero = hero.ljust(13)
            c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8 = (DATA_HEROES[hero][1],
                DATA_HEROES[hero][2], DATA_HEROES[hero][3], DATA_HEROES[hero][4], DATA_HEROES[hero][5], DATA_HEROES[hero][6],
                DATA_HEROES[hero][7], DATA_HEROES[hero][8])
            if len(str(c_1)) < 3: c_1 = ' '*(3 - len(str(c_1))) + str(c_1)
            if len(str(c_2)) < 3: c_2 = ' '*(3 - len(str(c_2))) + str(c_2)
            if len(str(c_3)) < 3: c_3 = ' '*(3 - len(str(c_3))) + str(c_3)
            if len(str(c_4)) < 3: c_4 = ' '*(3 - len(str(c_4))) + str(c_4)
            if len(str(c_5)) < 3: c_5 = ' '*(3 - len(str(c_5))) + str(c_5)
            if len(str(c_6)) < 3: c_6 = ' '*(3 - len(str(c_6))) + str(c_6)
            if len(str(c_7)) < 3: c_7 = ' '*(3 - len(str(c_7))) + str(c_7)
            if len(str(c_8)) < 3: c_8 = ' '*(3 - len(str(c_8))) + str(c_8)
            print(" | {}| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(c_hero, str(DATA_HEROES[hero]['count']).rjust(5), c_1, c_2, c_3, c_4, c_5, c_6,
            c_7, c_8, str("{:.2f}".format(DATA_HEROES[hero]['average'])).rjust(7)))
        
        print(' +--------------+-------+-----+-----+-----+-----+-----+-----+-----+-----+---------+')
        print('\n')
        return input('tape to back to the menu.')

    def launch_feature(self, n):
        """ Method that runs the specific feature. """
        if n == 1:
            answer = self.get_answer_timing_IA(n)
            return self.simulation(answer/1000)
        elif n == 2:
            answer = self.get_answer_games_IA(n)
            return self.many_simulation(answer)
        
####### INPUT USER #######
    def get_answer(self):
        """ Gets and manages the user's answer of the menu. """
        choice = -1
        while choice < 0 or choice > 2:
            self.start()
            choice = input('Choose an option: '.rjust(30))
            if choice.upper() == 'Q':
                return choice
            try:
                choice = int(choice)
                if isinstance(choice, int) and choice < 0 or choice > 2:
                    print('Enter a number between 1 and 2.')
                    time.sleep(0.7)
            except ValueError:
                print('Enter a number between 1 and 2.')
                time.sleep(0.7)
                choice = -1
        return choice
    
    def get_answer_timing_IA(self, n):
        """ Gets and manages the user's answer of the duration by action in IA mode. """
        choice = -1
        while choice < 1 or choice > 1000:
            self.before_start(n)
            choice = input('Enter number between [1-1000]: '.rjust(39))
            if choice.upper() == 'Q':
                return choice
            try:
                choice = int(choice)
            except ValueError:
                choice = -1
        return choice

    def get_answer_games_IA(self, n):
        """ Gets and manages the user's answer of the number of games simulates. """
        choice = -1
        while choice < 10 or choice > 10000:
            self.before_start(n)
            choice = input('Enter number between [100-10000]: '.rjust(39))
            if choice.upper() == 'Q':
                return choice
            try:
                choice = int(choice)
            except ValueError:
                choice = -1
        return choice

    def before_start(self, n):
        """" Display the menu """
        os.system('cls')
        os.system("mode con cols=50 lines=12")
        print(" M E N U ".center(50, '-'))
        print('\n')
        print("Simulate and see one game.\n".rjust(39)) if n == 1 else print("Simulate many games.\n".rjust(36))
        print("Choice time by action [1-1000] ms.\n".rjust(43)) if n == 1 else print("Choice the number of games [10-10000].\n".rjust(45))
        print("-"*50)
##########################
