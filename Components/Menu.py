"""
This class display the menu of the program.
    -Simulation human
    -Simulation IA
    -Start Bot
"""

import os, time
from Components.Player import Player
from constants.position import LEN_SHOP
from constants.minions import MINIONS_POOL

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
        print("1. Simulation human\n".rjust(35))
        print("2. Simulation IA\n".rjust(32))
        print("-"*50)

    def simulation(self, is_human):
        """
        Method that simule the game in the shop, for a
        human and IA that perform action randomly.
        """
        timing = -1 if is_human else self.get_answer_timing_IA()
        if isinstance(timing, str) and timing.upper() == 'Q':
            return ''
        os.system("mode con cols=152 lines=46")
        pool = MINIONS_POOL.copy()
        player = Player('IA', pool, is_human=is_human)
        player.hero = player.get_hero()
        player.time_by_action = timing/1000
        player.create_shop(1)

        player.hero.power['do'](player) if player.hero.power['trigger'] in ('turn', 'now') else None

        while True:
            print(player) if player.time_by_action else None
            action = player.get_action()
            if action and action[0].upper() == 'Q':
                break
            end = player.make(action)
            if end:
                break
        if not is_human:        
            return input('Enter any touch to come back. [Q] --> quit: ')
        return ''

    def bot(self):
        """
        Method for runs the bot.
        """
        os.system("mode con cols=152 lines=46")
        pool = MINIONS_POOL.copy()
        bot = Player('IA', pool)
        bot.is_bot = True
        bot.start()
        bot.wait_game_start()
        bot.hero = bot.bot_chose_a_hero()
        bot.wait_the_shop()
        print('Enter in Bob\'s tavern.'.rjust(83), end='\r')
        time.sleep(4)
        bot.shop = bot.see_shop(1, 3)
        print(bot)

        while True:

            while bot.in_shop:
                print(bot)
                action = bot.get_action()
                if action:
                    bot.make(action)
                    bot.bot_target_nothing()
                else:
                    print('Waiting next turn...')
                if bot.is_ending_turn():
                    bot.in_shop = False
                    time.sleep(17)

            while not bot.in_shop:
                print('wait shop...'.center(152), end='\r')
                time.sleep(0.1)
                if bot.is_in_tavern():
                    bot.next_turn()
                    print('In the shop.'.center(152), end='\r')
                    time.sleep(4.5)
                    bot.shop = bot.see_shop(bot.lvl, LEN_SHOP[bot.lvl-1])
                    bot.hero.power['do'](self, add=True) if bot.deathwing else None

    def launch_feature(self, n):
        """ Method that runs the specific feature. """
        if n == 1:
            answer = self.read_me_human() if not self.n_simulation_human else None
            if isinstance(answer, str) and answer.upper() == 'Q':
                return ''
            self.n_simulation_human += 1
            return self.simulation(is_human=True)
        elif n == 2:
            answer = self.read_me_IA() if not self.n_simulation_IA else None
            if isinstance(answer, str) and answer.upper() == 'Q':
                return ''
            self.n_simulation_IA += 1
            return self.simulation(is_human=False)
        elif n == 3:
            answer = self.read_me_bot() if not self.n_bot else None
            if isinstance(answer, str) and answer.upper() == 'Q':
                return ''
            self.n_bot += 1
            self.bot()
            return ''

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
    
    def get_answer_timing_IA(self):
        """ Gets and manages the user's answer of the duration by action in IA mode. """
        choice = -1
        while choice < 10 or choice > 2000:
            os.system('cls')
            print('\n')
            choice = input("Enter a time between each action [10-2000]: ")
            if choice.upper() == 'Q':
                return choice
            try:
                choice = int(choice)
                if choice < 10 or choice > 2000:
                    print('Enter number between [10-2000].')
                    time.sleep(0.7)
            except ValueError:
                choice = -1
                print('Enter a number.')
                time.sleep(0.7)
        return choice
##########################

####### READ ME #######
    def read_me_human(self):
        """ Display this when simulation human mode is activate for the first time. """
        os.system('cls')
        os.system("mode con cols=135 lines=25")
        intro = 'You have to type an available action:'
        buy = 'buy: use for buy a minion with its position in number. (-3gold)'
        play = 'play: play a minion with two number, the position of the minion in your hand, and the landing position in the board.'
        swap = 'swap: Change position of minions with two number, the first target and the second one.'
        refresh = 'refresh: See other minions available. (-1 gold)'
        sold = 'sold: Sell a minion on the board using one number. (+1 gold)'
        up = 'up: Upgrade the level of your tavern.'
        freeze = 'freeze: You\'re next turn doesn\'t change your minions on the tavern.'
        answer = 'Enter any touch to start. [Q] --> menu: '
        example = "Example: buy 3  -  play 1 2  -  sold 1  -  swap 2 3  -  refresh  -  up"
        next = "*** Tape - next - when you finish you turn ***"
        note = "*** 7 swap max per turn and 2 freeze per turn ***"
        print("{}\n".format(intro.rjust(len(intro)+10)))
        for s in (buy, play, swap, refresh, sold, up, freeze):
            print("{}\n".format(s.rjust(len(s)+15)))
        print(example.rjust(len(example)+10)+'\n')
        print(next.rjust(len(next)+10)+'\n')
        print(note.rjust(len(note)+10)+'\n\n')
        return input("{}".format(answer.rjust(len(answer)+10)))

    def read_me_IA(self):
        """ Display this when simulation IA mode is activate for the first time. """
        os.system('cls')
        print('\n')
        intro1, intro2 = "This feature show the program running with one", "logic."
        intro3 = "He can sold minion only if its board is full."
        intro4 = "It choose an action randomly until it don't"
        intro5 = "have any action to do."
        answer = 'Enter any touch to start. [Q] --> menu: '
        for s in (intro1, intro2, intro3, intro4, intro5):
            print(s.rjust(len(s)+3))
        print('\n\n')
        return input("{}".format(answer.rjust(len(answer)+3)))

    def read_me_bot(self):
        """ Display this when Bot mode is activate for the first time. """
        os.system('cls')

        return input('Enter any touch to start. [Q] --> menu: ')
######################