"""
The Game class manage all states about the player.
Some of the most important are:
    -hero     -turn
    -hp       -shop
    -gold     -board
    -lvl      -hand

Two types of methods in this class:
    -passives methods that just serve to simulate the game.
        -execute_passive_...()
        -get_answer_...()
        -get_all_actions()
        -next_turn()
        -triple_minion()
        -get_discovery()

    -actives methods that allow to test some case and
    simulate the game.
        -create_...()
        -fulfill_shop()
        -board_position_of()
"""

import time, os
from random import randint, choice, sample, choices
from collections import Counter
from operator import itemgetter

from Components.Minion import Minion
from Components.Hero import Hero
from Components.Discovery import Discovery

from constants.minions import MINIONS, ARCHETYPES
from constants.position import LEN_SHOP
from constants.heroes import (LIST_HEROES, HERO_POWER_ACTIVE_SHOP,
    HERO_POWER_ACTIVE_BOARD, HERO_POWER_ACTIVE_ONLY, HEROES)

## TRY FACTORISE CODE WHEN SEE IF WE HAVE 3 SAME CARDS AND EDIT STATE DOUBLE

class Game:

    def __init__(self):

        self.hero = None
        self.hp = 40 # 40
        self.max_hp = 40
        self.gold = 3 # 3
        self.lvl = 1 # 1
        self.minion_cost = 3
        self.turn = 1
        self.up_cost = [5, 7, 8, 9, 10, 'M']

        self.shop = []
        self.hand = []
        self.board = []
        self.last_players = []
        self.last_enemies = []
        self.first_enemy_kill = ''
        self.double = {}

        self.triple = 0
        self.m_gold = 0
        self.board_gold_minion = 0
        self.finish = 0
        self.type_board = ''

        self.max_freeze = 2
        self.max_swap = 3
        self.in_shop = True
        self.is_win_fight = True
        self.is_start_turn = True
        self.is_end_turn = False
        self.is_freeze = False
        self.immunity = 0
        self.view_discover = ''
        self.debug = False
        self.is_human = False
        self.is_bot = False

        #specific hero


        # rely to minion
        self.n_murozon = 0
        self.n_pogo = 0
        self.pirate_buy_in_turn = 0
        self.n_pirate = 0
        self.oldmurloc = 0
        self.hoggarr = 0
        self.zerus = 0
        self.zerus_buy = 0
        self.watcher = 0
        self.brann = 1
        self.n_brann = 0

        self.n_khadgar = 0
        self.n_khadgar_fight = 0
        self.n_g_khadgar = 0
        self.n_g_khadgar_fight = 0
        self.baron = 1
        self.baron_fight = 1
        
        # about actions
        self.kt = False
        self.can_play_action = True
        self.n_action = 0
        self.n_buy = 0
        self.buy_in_turn = 0
        self.n_sold = 0
        self.n_play = 0
        self.n_swap = 0
        self.n_refresh = 0
        self.refresh_cost = 1
        self.refresh_max_cost = 1
        self.n_up = 0
        self.n_freeze = 0
        self.first_refresh = True
        self.in_simulation = False
        self.do_action = 0

        #JUST DEBUG
        self.n_eudora = 0
        self.n_patches = 0
        self.n_reno = 0
        self.solo = False
        self.history = []


    def get_all_actions(self):
        actions = []
        if self.max_freeze != 0:
            actions.append('freeze')
        if len(self.up_cost) > 1 and self.gold >= self.up_cost[0]:
            actions.append('up')
        if self.gold >= self.minion_cost and (len(self.shop) > len(self.hero.maiev)):
            actions.append('buy')
        if self.gold >= self.refresh_max_cost and self.gold % 3 != 0:
            actions.append('refresh')
        if self.is_human and len(self.board) > 0:
            actions.append('sold')
        elif not self.is_human and len(self.board) > 6:
            actions.append('sold')
        if len(self.board) > 1 and self.max_swap != 0:
            actions.append('swap')
        if len(self.hand):
            if self.hero.name == 'Elise':
                for card in self.hand:
                    if isinstance(card, Minion) and len(self.board) < 7:
                        actions.append('play')
                        break
                    elif not isinstance(card, Minion) and not isinstance(card, str) and self.gold >= card.cost:
                        actions.append('play')
                        break
            elif len(self.board) < 7:
                if len(self.board) == 0:
                    for minion in self.hand:
                        if (isinstance(minion, Minion) or isinstance(minion, Discovery)):
                            actions.append('play')
                            break
                else:
                    actions.append('play')
        if self.hero.power['active'] and self.hero.can_power and self.gold >= self.hero.power['cost']:
            if self.hero.name in HERO_POWER_ACTIVE_SHOP and self.shop:
                actions.append('power')
            elif self.hero.name in HERO_POWER_ACTIVE_BOARD and self.board:
                actions.append('power')
            elif self.hero.name in HERO_POWER_ACTIVE_ONLY:
                actions.append('power')
        self.can_play_action = True if actions else False
        return actions

    def get_hero(self, archetype):
        """ Get an hero in Human mode, IA and bot """
        all_heroes = HEROES[archetype]
        if self.is_bot:
            return self.bot_chose_a_hero(archetype)
        heroes = sample(all_heroes, 4)
        
        if self.is_human:
            answer = self.get_answer_hero(heroes, 4)
            
            hero = heroes[answer-1]
        else:
            self.display_heroes(heroes) if self.time_by_action != 0 else None
            hero = choice(heroes)
        return self.create_hero(hero)

    ########### CREATE CUSTOM STUFF ###########
    def create_shop(self, lvl):
        """
        Create minions in the shop.Depend on the player's level.
        """
        if self.time_by_action == 0:
            # here
            [self.pool.add_to_pool(name, lvl) for name, lvl, buff in self.shop[len(self.hero.maiev):]]
            self.shop.clear()
        
            minions = self.pool.get_minions_pool(lvl, self.hero.aranna, self.shop, len(self.hero.maiev))
            [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
            self.shop.extend(minions)
        else:
            
            [self.pool.add_to_pool(minion.name, minion.lvl) for minion in self.shop[len(self.hero.maiev):]]
            self.shop.clear()
            minions = self.pool.get_minions_pool(lvl, self.hero.aranna, self.shop,  len(self.hero.maiev))
            [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
            for name, pos, buff in minions:
                self.shop.append(self.create_minion(False, name))


        if self.hero.maiev:
            self.shop = self.hero.maiev + self.shop

    def fulfill_shop(self, lvl):
        """
        When the shop is freeze. The next turn keep the already minions
        and add minions if the shop is not fulfill.
        """
        if self.time_by_action == 0:
            minions = self.pool.get_minions_pool(lvl, self.hero.aranna, self.shop, len(self.hero.maiev))
            [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
            self.shop.extend(minions)

        else:
            minions = self.pool.get_minions_pool(lvl, self.hero.aranna, self.shop,  len(self.hero.maiev))
            [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
            for name, pos, buff in minions:
                minion = self.create_minion(False, name)
                self.hero.power['do'](self, minion=minion, add=True) if self.hero.deathwing else None
                self.hero.power['do'](self) if self.hero.millificent else None
                self.shop.append(minion)

    def create_minions(self, *names, length=0, gold=False, tier_min=1, tier_max=6):
        """
        Return a couple of minions. Can be Gold (simulate a triple minion),
        can enter a length and create  minions randomly, or write some
        names and create these minions.
        """
        
        minions, team = [minion for minion in MINIONS if (MINIONS[minion]['lvl'] >= tier_min and MINIONS[minion]['lvl'] <= tier_max)], []
        for i in range(length):
            minion = choice(minions)
            team.append(Minion(minion, gold, *[value for value in MINIONS[minion].values()][1:]))
        for minion in names:
            team.append(Minion(minion, gold, *[value for value in MINIONS[minion].values()][1:]))
        return team

    def create_minion(self, gold, name):
        """
        Return a specific minion. Enter if it's a golden minion and its name.
        """
        if name[-2:].upper() == '_T':
            archetype = 'beast' if name[:-2] == 'alleycat' else 'murloc'
            return Minion(name, gold, name, 1, 1, 1, archetype, deathrattle=[], fight={'do': [], 'trigger': ''})
        return Minion(name,gold, *[value for value in MINIONS[name].values()][1:])
        
    def create_hero(self, name):
        """ Create a specific hero by its name. """
        return Hero(name, *[value for value in LIST_HEROES[name].values()])
############################################


########### MANAGE HUMAN INPUT ###########
    def get_answer_action(self):
        """
        Gets and manages the current answer for a specific action when a
        human plays. Ask the user as long as the answer is not allowed.
        actions available:
            -play       -up
            -buy        -refresh
            -swap       -freeze
            -sold       -next
            -power
            -q (for quit)
        """
        #HAVE TO MANAGE POWER
        good_choice = False
        all_actions = self.get_all_actions()
        while not good_choice:
            print(self)
            if all_actions:
                print("- - - Action availabe: {} - - -".format(', '.join(all_actions)))
            else:
                print("- - - Action to do: next - - -")
            action = input('- - - choice: ')
            action = action.split(' ')
            if len(action) == 1 and action[0] == 'refresh':
                if self.gold >= self.refresh_cost:
                    good_choice = True
                else:
                    print('Not enough gold.') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None

            elif len(action) == 1 and action[0] == 'freeze':
                if self.max_freeze > 0:
                    good_choice = True
                else:
                    print('Maximum freeze reach this turn...') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None

            elif len(action) == 1 and action[0] == 'up':
                if self.up_cost[0] != 'M':
                    if self.gold >= self.up_cost[0]:
                        good_choice = True
                    else:
                        print('Not enough gold for upgrade.') if not self.in_simulation else None

                        time.sleep(0.7) if not self.in_simulation else None
                else:
                    print('Level tavern max.') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None

            elif len(action) == 2 and action[0] == 'buy':
                try:
                    action[1] = int(action[1])
                except ValueError:
                    action[1] = -1
                if action[1] > 0 and action[1] <= len(self.shop):
                    if self.gold >= self.minion_cost:
                        if self.time_by_action != 0 and (action[1] in [i+1 for i in range(len(self.hero.maiev))]):
                            print('Cant buy minion prisoned.') if not self.in_simulation else None
                            time.sleep(0.7) if not self.in_simulation else None
                        else:
                            action.append(len(self.shop))
                            good_choice = True
                    else:
                        print('Not enough gold.') if not self.in_simulation else None
                        time.sleep(0.7) if not self.in_simulation else None
                else:
                    print('Position minion out of range. (buy)') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None

            elif len(action) == 2 and action[0] == 'sold':
                try:
                    action[1] = int(action[1])
                except ValueError:
                    action[1] = -1
                if action[1] > 0 and action[1] <= len(self.board):
                    action.append(len(self.board))
                    good_choice = True
                else:
                    print('position minion out of range. (sold)') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None

            elif len(action) == 3 and action[0] == 'swap':
                try:
                    action[1] = int(action[1])
                    action[2] = int(action[2])
                except ValueError:
                    action[1] = -1
                    action[2] = -1
                if (action[1] > 0 and action[1] <= len(self.board) and action[2] > 0 and
                    action[2] <= len(self.board) and action[1] != action[2]):
                    if self.max_swap > 0:
                        action.append(len(self.board))
                        good_choice = True
                    else:
                        print('Maximum swap reach this turn...') if not self.in_simulation else None
                        time.sleep(0.7) if not self.in_simulation else None
                else:
                    print('position minions out of range. (swap)') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None
            
            elif len(action) == 3 and action[0] == 'play':
                try:
                    action[1] = int(action[1])
                    action[2] = int(action[2])
                except ValueError:
                    action[1] = -1
                    action[2] = -1
                if (action[1] > 0 and action[1] <= len(self.hand) and action[2] > 0 and
                    action[2] <= len(self.board) + 1):
                    action.insert(2, len(self.hand))
                    action.append(len(self.board))
                    good_choice = True
                else:
                    print('position minions out of range. (play)') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None
            elif action[0].upper() == 'Q':
                break
            elif len(action) == 1 and action[0] == 'next':
                return action
            
            elif len(action) == 1 and action[0] == 'finish':
                return action
            
            elif action[0] == 'power' and self.hero.can_power:
                if not self.hero.power['active']:
                    print('Hero power passive.') if not self.in_simulation else None
                    time.sleep(0.7) if not self.in_simulation else None
                else:
                    if self.gold >= self.hero.power['cost']:
                        if len(action) == 1:
                            if self.hero.name in HERO_POWER_ACTIVE_ONLY:
                                return action
                            else:
                                print('Hero power take arguments.') if not self.in_simulation else None
                                time.sleep(0.7) if not self.in_simulation else None

                        elif len(action) == 2:
                            try:
                                action[1] = int(action[1])
                            except ValueError:
                                action[1] = -1
                            if self.hero.name in HERO_POWER_ACTIVE_BOARD:
                                if action[1] > 0 and action[1] <= len(self.board):
                                    return action
                                else:
                                    print('Wrong position target.') if not self.in_simulation else None
                                    time.sleep(0.7) if not self.in_simulation else None
                            elif self.hero.name in HERO_POWER_ACTIVE_SHOP:
                                if self.hero.name == 'Maiev':
                                    no_power = len(self.hero.maiev)
                                    if action[1] in [i+1 for i in range(no_power)]:
                                        print('Can\'t hero power minion already prisoned.') if not self.in_simulation else None
                                        time.sleep(0.7) if not self.in_simulation else None
                                    else:
                                        return action
                                elif action[1] > 0 and action[1] <= len(self.shop):
                                    return action
                                else:
                                    print('Wrong position target.') if not self.in_simulation else None
                                    time.sleep(0.7) if not self.in_simulation else None

                        elif len(action) == 3 and self.hero.name == 'Malygos':
                            if action[1] in ('shop', 'board'):
                                try:
                                    action[2] = int(action[2])
                                except ValueError:
                                    action[2] = -1
                                if action[1] == 'shop':
                                    if action[2] > 0 and action[2] <= len(self.shop):
                                        return action
                                    else:
                                        print('Wrong position.') if not self.in_simulation else None
                                        time.sleep(0.7) if not self.in_simulation else None
                                elif action[1] == 'board':
                                    if action[2] > 0 and action[2] <= len(self.board):
                                        return action
                                    else:
                                        print('Wrong position') if not self.in_simulation else None
                                        time.sleep(0.7) if not self.in_simulation else None
                            else:
                                print('Hero don\'t take arguments.') if not self.in_simulation else None
                                time.sleep(0.7) if not self.in_simulation else None
                        else:
                            print('Wrong arguments.') if not self.in_simulation else None
                            time.sleep(0.7) if not self.in_simulation else None
                    else:
                        print('Not enough gold for hero power.') if not self.in_simulation else None
                        time.sleep(0.7) if not self.in_simulation else None
            elif action[0] == 'power' and not self.hero.can_power:
                print('Hero power already used.') if not self.in_simulation else None
                time.sleep(0.7) if not self.in_simulation else None

            elif action[0] == 'pool':
                print(self.pool.pool[int(action[1])-1][self.hand[int(action[2])-1].name])
                time.sleep(1.5)    
            else:
                print('Action doesn\'t exist.') if not self.in_simulation else None
                time.sleep(0.7) if not self.in_simulation else None
        return action

    def get_answer_discovery(self):
        """
        Gets and manages the answer if discovery occur when a
        human plays. Ask the user as long as the answer is not allowed.
        actions available:
            -1     -2      -3
        """
        answer = -1
        while answer < 1 or answer > 3:
            print(self)
            answer = input('choose the card 1, 2 or 3: ')
            try:
                answer = int(answer)
            except ValueError:
                print('Incorrect answer.')
                answer = -1
                time.sleep(0.7) 
            else:
                if answer < 1 or answer > 3:
                    print('Have to be between [1, 3].')
                    time.sleep(0.7)
        return answer

    def get_answer_battlecry(self, targets):
        """
        Gets and manages the answer if battlcry of minion occur when a
        human plays. Ask the user as long as the answer is not allowed.
        actions available:
            Depend on the current minions in the board.
        """
        answer = -1
        while answer not in targets:
            print(self)
            answer = input("choice minion buff ({}): ".format(', '.join(map(str, targets))))
            try:
                answer = int(answer)
            except ValueError:
                print('Incorrect answer.')
                answer = -1
                time.sleep(0.7) 
            else:
                if answer not in targets:
                    print('Have to be in ({}).'.format(', '.join(map(str, targets))))
                    time.sleep(0.7)
        return answer - 1

    def get_answer_hero(self, heroes, n):
        """ Gets and manages the answer when heroes are present """
        answer = -1
        while answer < 1 or answer > n:
            os.system('cls')
            self.display_heroes(heroes)
            answer = input('choice hero: '.rjust(82))
            try:
                answer = int(answer)
            except ValueError:
                print('Incorrect answer')
                answer = -1
                time.sleep(0.7)
        return answer

    def get_answer_mukla(self):
        answer = -1
        targets = [i+1 for i in range(len(self.board))]
        while answer < 1 or answer > len(self.board):
            print(self)
            answer = input('choice minion buff with banana ({}): '.format(', '.join(map(str, targets))))
            try:
                answer = int(answer)
            except ValueError:
                print('Incorrect answer.')
                answer = -1
                time.sleep(0.7) 
            else:
                if answer not in targets:
                    print('Have to be in ({}).'.format(', '.join(map(str, targets))))
                    time.sleep(0.7)
        return answer - 1
###########################################

  
########### MANAGE PASSIVE MINION ###########
    def execute_passive_play(self, minion_play, team, fight=False):
        """
        Triggers all minions passives when a minion is play on the board.
        Manage some specific case like:
            -minion: floatingWatcher
            -minion: capnHoggarr
            -minion: brannBronzebeard
            -minion: khadgar
            -minion: shifterZerus
        """
        if not fight:
            if minion_play.name == 'floatingWatcher':
                self.watcher += 1
            elif minion_play.name == 'capnHoggarr':
                self.hoggarr += 1
            elif minion_play.name == 'brannBronzebeard':
                self.n_brann += 1
                self.brann = 3 if minion_play.gold else 2
            elif minion_play.name == 'khadgar':
                if minion_play.gold:
                    self.n_g_khadgar += 1
                else:
                    self.n_khadgar += 1
            if self.zerus:
                for pos, minion in enumerate(team):
                    if minion.qn[-1] == 'Z':
                        self.zerus -= 1
                        minion.name = minion.true_name
                        new_minion = Minion(minion.name, minion.gold, *[value for value in MINIONS[minion.true_name].values()][1:])
                        minion_play = new_minion
                        team[pos] = new_minion
                        if not minion.gold:
                            self.update_doublon_minion(minion)

        for minion in team:
            if minion.passive:
                if minion.passive['trigger'] == 'play':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    if (minion.passive['target'] == minion_play.archetype or
                        minion.passive['target'] == 'battlecry' and minion_play.battlecry or
                        minion.passive['target'] == 'deathrattle' and minion_play.deathrattle) :
                        fc(self, minion, minion_play, target, buff)
                elif minion.passive['trigger'] == 'present':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    fc(self, minion, minion_play, target, buff, 'play')
                    
    def execute_passive_sold(self, minion):
        """
        Triggers all minions passives when a minion is sold to the shop.
        Manage some specific case like:
            -minion: floatingWatcher
            -minion: oldMurkScanner
            -minion: brannBronzebeard
            -minion: khadgar
        """
        if minion.passive:
            if minion.passive['trigger'] == 'sold':
                fc, target, buff = list(minion.passive.values())[:-1]
                fc(self, minion, target, buff)
            elif minion.passive['trigger'] == 'present':
                fc, target, buff = list(minion.passive.values())[:-1]
                fc(self, minion, '', target, buff, 'sold')
            elif minion.passive['trigger'] == 'buy':
                fc, target, buff = list(minion.passive.values())[:-1]
                fc(self, minion, '', target, buff, 'sold')
        elif minion.name == 'floatingWatcher':
            self.watcher -= 1
        elif minion.name == 'brannBronzebeard':
            self.n_brann -= 1 if not minion.gold else 3
            if self.n_brann == 0:
                self.brann = 1
        elif minion.name == 'khadgar':
            if minion.gold:
               self.n_g_khadgar -= 1
            else:
                self.n_khadgar -= 1
        
        if self.oldmurloc and minion.archetype == 'murloc':
            for minion in self.board:
                if minion.name == 'oldMurkScanner':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    fc(self, minion, '', target, buff, 'play')
        
    def execute_passive_turn(self, timing):
        """
        Triggers all minions passives when a turn is end or start.
        Manage some specific case like:
            -minion: shifterZerus
        """
        for minion in self.board:
            if minion.passive and minion.passive['trigger'] == timing:
                fc, target, buff = list(minion.passive.values())[:-1]
                fc(self, minion, target, buff)
        if timing == 'start_turn' and self.zerus:
            for pos, minion in enumerate(self.hand):
                if isinstance(minion, Minion) and minion.name  == 'shifterZerus':
                    minion.morph += 1
                    if minion.morph == 1 and not minion.gold:
                        self.double[minion.name] -= 1
                    fc, target, buff = list(minion.passive.values())[:-1]
                    self.hand[pos] = fc(self, minion, target, buff)

    def execute_passive_buy(self, minion_buy):
        """
        Triggers all minions passives when a minion is buy in the shop.
        Manage some specific case like:
            -minion: capnHoggarr
            -minion: shifterZerus
        """
        if self.hoggarr and minion_buy.archetype == 'pirate':
            for minion in self.board:
                if minion.name == 'capnHoggarr':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    fc(self, minion, minion_buy, target, buff, 'play')

        elif minion_buy.name == 'shifterZerus':
            self.zerus += 1

    

#############################################


########## OTHER ############
    def next_turn(self):
        """
        Manages states that should reload every turn.
        Particular case if human plays, the shop is update 
        and not scans by the bot.
        """
        # We have to decompose this feature into two feature when we implemente fight
        self.execute_passive_turn('end_turn') if self.solo else None
        self.in_shop = True
        if not self.hero.can_power:
            if self.hero.lichking in self.board:
                self.hero.lichking.reborn = False
            if self.hero.shudderwock:
                self.brann = 1
                self.hero.shudderwock = False
            self.hero.can_power = True if not self.hero.name in ('Reno', 'Kragg') else False
        self.buy_in_turn = 0
        self.max_swap = 3
        self.max_freeze = 2
        self.pirate_buy_in_turn = 0
        self.turn += 1
        self.first_refresh = True
        if self.up_cost[0] != 'M':
            self.up_cost[0]-= 1 if self.up_cost[0] > 0 else 0
        self.gold = 2 + self.turn if self.turn < 9 else 10

        self.hero.power['do'](self) if self.hero.name == 'Maiev' else None
        #MAYBE ADD FUNCTION FOR CALL FC DEATHWING AND MILLIFICIENT
        if self.is_freeze:
            if not self.is_bot:
                if self.hero.power['trigger'] == 'turn' and self.hero.name == 'Sindragosa':
                    self.hero.power['do'](self)
                self.fulfill_shop(self.lvl)
            else:
                #sindragosa with compute after scan which minion have to take buff
                self.hero.power['do'](self, add=True) if self.hero.deathwing else None
                self.hero.power['do'](self) if self.hero.millificent else None
        else:
            self.create_shop(self.lvl) if not self.is_bot else None
            self.hero.power['do'](self, add=True) if self.hero.deathwing else None
            self.hero.power['do'](self) if self.hero.millificent else None

        self.execute_passive_turn('start_turn')
        self.hero.power['do'](self) if self.hero.power['trigger'] == 'turn' and self.hero.name != 'Sindragosa' else None
        self.is_freeze = False

    def get_board_archetype(self):
        """ Returns all differents archetypes in the board. """
        archetypes = []
        for minion in self.board:
            if minion.archetype in ARCHETYPES and minion.archetype not in archetypes:
                archetypes.append(minion.archetype)
        return archetypes

    def get_type_of_board(self):
        archetypes = [m.archetype for m in self.board]
        archetypes = Counter(archetypes)
        if archetypes:
            archetype, value = max(archetypes.items(), key=itemgetter(1))
            self.type_board = 'mixed' if list(archetypes.values()).count(value) > 1 else archetype
            self.type_board = 'mixed' if self.type_board == 'neutral' else self.type_board
        
    def define_type_for_all(self, minions, all_types, base_types=ARCHETYPES):
        if len(base_types) < 3:
            type_res = list(set(ARCHETYPES) - set(base_types))
        else:
            type_res = list(set(base_types) - set(all_types))
        for minion in minions:
            if type_res:
                minion.archetype = choice(type_res)
                type_res = list(set(type_res)-set(minion.archetype))
            else:
                minion.archetype = choice(base_types)

    def board_position_of(self, team=[], target='all', minion=False):
        """
        Return all positions of a minions that match a specific value.
        Example: we want to know the positions of all murloc in the board.
        we tape target='murloc' and minion parameter allow us to delete the position of the
        current minion we plays.
        """
        if target in ARCHETYPES:
            all_target = []
            for pos, m in enumerate(team):
                if m.archetype == target or m.archetype == 'all':
                    all_target.append(pos+1)
            
        elif target in ('taunt', 'shield', 'windufry', 'poisonous', 'reborn'):
            all_target = [pos+1 for (pos, m) in enumerate(team) if m.__dict__[target]]
        else:
            all_target = [pos+1 for pos in range(len(team))]
        if minion:
            minion_index = [pos+1 for pos, m in enumerate(team) if m.id == minion.id][0]
            if minion_index in all_target:
                all_target.remove(minion_index)
        return all_target
        
    def update_doublon_minion(self, minion, token=False):
        if minion.name in self.double:
            if self.double[minion.name] == 2:
                self.triple_minion(minion, is_token=token)
                self.double.pop(minion.name)
            else:
                self.double[minion.name] += 1
        else:
            self.double[minion.name] = 1

    def triple_minion(self, minion_to_triple, is_token=False):
        """
        Manages a merges of three minions and add the new golden minion in
        the hand.
        """
        minions = []
        board_name = [minion.name if not minion.gold else '' for minion in self.board]
        hand_name = [minion.name if (isinstance(minion, Minion) and not minion.gold and 'true_name' not in minion.__dict__) else '' for minion in self.hand]
        if minion_to_triple.name == 'khadgar':
            self.n_khadgar = 0
        if minion_to_triple.name == 'shifterZerus':
            self.zerus -= 2

        while minion_to_triple.name in board_name:
            minion = self.board.pop(board_name.index(minion_to_triple.name))
            minion.atk -= 2 if self.hero.deathwing else 0
            minions.append(minion)
            board_name.remove(minion_to_triple.name)
        while minion_to_triple.name in hand_name:
            minions.append(self.hand.pop(hand_name.index(minion_to_triple.name)))
            hand_name.remove(minion_to_triple.name)
        if not is_token:
            if minions[0].name == 'amalgame':
                minion_gold = Minion('amalgame', True, 'amalgame', 1, 1, 1, 'all',deathrattle=[], fight={'do': [], 'trigger': ''})
            else:
                minion_gold = Minion(minions[0].name, True, *[value for value in MINIONS[minions[0].name].values()][1:])
                minion_gold.atk = minions[0].atk + minions[1].atk + minion_to_triple.atk - MINIONS[minions[0].name]['atk']
                minion_gold.hp = minions[0].hp + minions[1].hp + minion_to_triple.hp - MINIONS[minions[0].name]['hp']
                minion_gold.taunt = True if (minions[0].taunt or minions[1].taunt) else False
                minion_gold.poisonous = True if (minions[0].poisonous or minions[1].poisonous) else False
                minion_gold.shield = True if (minions[0].shield or minions[1].shield) else False
                minion_gold.windfury = True if (minions[0].windfury or minions[1].windfury) else False
                minion_gold.minions_magnetic = minions[0].minions_magnetic + minions[1].minions_magnetic
                minion_gold.deathrattle = minions[0].deathrattle if (len(minions[0].deathrattle) >  len(minions[1].deathrattle)) else minions[1].deathrattle
                minion_gold.play_deathrattle = minion_gold._play_deathrattle if minion_gold.deathrattle else None
        else:
            minion_gold = Minion(minions[0].qn, True, minions[0].qn, 1, 1, 1, minions[0].archetype)
            minion_gold.atk = minions[0].atk + minions[1].atk + minion_to_triple.atk - 1
            minion_gold.hp = minions[0].hp + minions[1].hp + minion_to_triple.hp - 1
            minion_gold.taunt = True if (minions[0].taunt or minions[1].taunt) else False
            minion_gold.poisonous = True if (minions[0].poisonous or minions[1].poisonous) else False
            minion_gold.shield = True if (minions[0].shield or minions[1].shield) else False
            
            minion_gold.deathrattle = minions[0].deathrattle if (len(minions[0].deathrattle) >  len(minions[1].deathrattle)) else minions[1].deathrattle
            minion_gold.play_deathrattle = minion_gold._play_deathrattle if minion_gold.deathrattle else None
        
        self.board_gold_minion += 1
        self.triple += 1

        self.hand.append(minion_gold)
    
    def get_discovery(self, tier=False, minion=False, hero=False, pool=False, cost=0):
        """ Create a discover's card and return it. """
        return Discovery(tier, minion, hero, pool, cost)

    def get_minion_enemies(self, gold, minion):
        if minion.name[-2:].upper() == '_T':
            atk, hp = minion.max_atk, minion.max_hp
            return Minion(minion.name, gold, minion.name, atk, hp, 1,
                minion.archetype, taunt=minion.taunt, deathrattle=minion.deathrattle, fight=minion.fight,
                max_hp=minion.max_hp, max_atk=minion.max_atk)
        elif minion.name.lower() == 'amalgame':
            return Minion('amalgame', gold, 'amalgame', 1, 1, 1, 'all',deathrattle=[], fight={'do': [], 'trigger': ''})
        elif minion.name.lower() == 'treasure':
            treasure = Minion('treasure', gold, 'treasure', 0, 2, 1, 'neutral', deathrattle=minion.deathrattle, fight={'do': [], 'trigger': ''})
            treasure.hp = 2
            return treasure
        else:
            return self.create_minion(gold, minion.name)


