"""
Class player manage all the state and inherite most of the classes.
"""
import time, os
from random import randint, choice
from Components.Hero import Hero
from Components.Game import Game
from Components.Minion import Minion
from constants.position import LEN_SHOP

class Player(Game, Hero):

    def __init__(self, name, isHuman=False):
        Game.__init__(self)
        self.name = name
        self.isHuman = isHuman
        self.time_by_action = 0

########### MANAGE ACTIONS ###########

    def timing_IA_action(self, name, args):
        if not self.isHuman and self.time_by_action != 0:
            print(' - - IA: choose to {} {} - -'.format(name, '-'.join(map(str, args))))
            time.sleep(self.time_by_action)
    
    def timing_IA(self):
        if not self.isHuman and self.time_by_action != 0:
            print(self)
            time.sleep(self.time_by_action)

    def get_action(self):
        """
        Here we simulate the start of a random machin learning
        for learn the game play of battleground. So every possible actions
        are random with a limit for infinite action like freeze, swap.
        This is the enter of IA.
        """
        if self.isHuman:
            return self.get_answer_action()
        else:
            actions = self.get_all_actions()
            if not actions:
                return False
            action = choice(actions)
            if action == 'buy':
                return ('buy',randint(1, len(self.shop)), len(self.shop))
            elif action == 'sold':
                return ('sold', randint(1, len(self.board)), len(self.board))
            elif action == 'play':
                return ('play', randint(1, len(self.hand)), len(self.hand), randint(1, len(self.board)+1))
            elif action == 'swap':
                board = [i+1 for i in range(len(self.board))]
                first = choice(board)
                board.remove(first)
                second = choice(board)
                return ('swap', first, second, len(self.board))
            elif action == 'up':
                return ('up',)
            elif action == 'refresh':
                return ('refresh',)
            else:
                return ('freeze',)

    def make(self, action):
        if action:
            self.n_action += 1
            name, *args = action
            self.timing_IA_action(name, args)
            ACTIONS = {
                'buy': self.buy_minion,
                'sold': self.sold_minion,
                'play': self.play_minion,
                'swap': self.swap_minion,
                'up': self.up,
                'refresh': self.refresh,
                'freeze': self.freeze,
                'next': self.next_turn
            }
            ACTIONS[name](*args)
        else:
            if self.turn == 14:
                return True
            self.next_turn()
    
    def play_minion(self, *args):
        self.n_play += 1
        args = list(args)
        position, length, direction = args
        args.append(len(self.board))
        card = self.hand.pop(position-1)

        if isinstance(card, Minion):
            battlecry, target, buff = card.battlecry.values() if card.battlecry else (False, False, False)
            self.board.insert(direction-1, card)
            battlecry = battlecry(self, card, target, buff, direction, self.isHuman) if card.battlecry else ''
            self.execute_passive_play(card)
                
            if card.gold:
                card_discovery = self.get_discovery(self.lvl)
                self.hand.append(card_discovery)
        else:
            self.view_discover = card.display_discovery()
            self.timing_IA()
            target = self.get_answer_discovery() if self.isHuman else choice([1,2,3])
            new_minion = card.cards_discover[target-1]
            if new_minion not in self.double:
                self.double[new_minion] = 1
            else:
                self.double[new_minion] += 1
            self.hand.append(self.create_minion(False, new_minion))
            self.view_discover = ''

    def buy_minion(self, *args):
        self.n_buy += 1
        args = list(args)
        position, length = args
        minion = self.shop.pop(position-1)
        self.hand.append(minion)
        self.gold -= 3
        self.execute_passive_buy(minion)
        if minion.archetype == 'pirate':
            self.n_pirate += 1
        if minion.name in self.double:
            if self.double[minion.name] == 2:
                self.hand.pop(-1)
                self.triple_minion(minion, False)
                self.double.pop(minion.name)
            else:
                self.double[minion.name] += 1
        else:
            self.double[minion.name] = 1

    def sold_minion(self, *args):
        self.n_sold += 1
        args = list(args)
        position, length = args
        self.gold += 1
        self.gold = 10 if self.gold > 10 else self.gold
        minion = self.board.pop(position-1)
        self.execute_passive_sold(minion)
        if not minion.gold:
            self.double[minion.name] -= 1
            if self.double[minion.name] == 0:
                self.double.pop(minion.name)

    def swap_minion(self, *args):
        self.n_swap += 1
        args = list(args)
        first, second, length = args
        minion = self.board.pop(first-1)
        self.max_swap -= 1
        self.board.insert(second-1, minion)

    def up(self):
        self.n_up += 1
        self.gold -= self.up_cost[0]
        self.up_cost.pop(0)
        self.lvl += 1

    def refresh(self):
        self.n_refresh += 1
        self.gold -= 1
        self.shop = self.create_shop(self.lvl)

    def freeze(self):
        self.n_freeze += 1
        self.is_freeze = not self.is_freeze
        self.max_freeze -= 1
######################################


########### DISPLAY STATE ############
    def __str__(self):
        os.system('cls')
        dash, hero, display = '-'*28,'', ''
        title = "+{} Player: {} {}+".format(dash, self.name, dash)
        sep = "+{}+".format('-' * (len(title)-2))

        hero += title.center(152)+'\n'
        hero += (self.display_hero(len(title)) + sep.center(152)+'\n') if  self.hero else ''
        hero += (self.display_state()+ sep.center(152)+'\n')

        board = self.view_of(self.board, 'B O A R D')
        shop = self.view_of(self.shop, 'S H O P')
        hand_or_discovery = self.view_discover if self.view_discover else self.view_of(self.hand, 'H A N D')
        display += shop + board + '\n\n\n' + hero + '\n' + hand_or_discovery
        return display

    def display_hero(self, length):
        display = ''
        for key, state in (('-hero: ', self.hero.name), ('-tier: ', self.hero.tier)):
            s = (key + str(state)).ljust(length -9)
            display += "|       {}|".format(s).center(152)+'\n'
        return display

    def display_state(self):
        n_double, display = 0, ''
        STATE_VIEW = [
            (('-hp:', self.hp), ('-gold:', self.gold), ('-n_pogo:', self.n_pogo), ('-watcher:', self.watcher)),
            (('-lvl:', self.lvl), ('-double:', n_double), ('-n_pirate:', self.n_pirate), ('-brann:', self.brann)),
            (('-up_cost:', self.up_cost[0]), ('-m_gold:', self.m_gold), ('-oldmurloc:', self.oldmurloc), ('-n_brann:', self.n_brann)),
            (('-turn:', self.turn), ('-freeze:', int(self.is_freeze)), ('-hoggarr:', self.hoggarr), ('-n_khadgar:', self.n_khadgar)),
            (('-immune:', self.immunity), ('-triple:', self.triple), ('-zerus:', self.zerus), ('-n_g_khad:', self.n_g_khadgar)),
        ]
        for i in self.double.values():
            if i > 1: n_double += 1

        for state in STATE_VIEW:
            s1 = ''
            for key, props in state:
                props = str(props)
                if len(props) == 1:
                    props = ' '+props[0]
                s = (key.ljust(11) + " {}   ".format(props))
                s1 += s
            display += ('|'+s1+'|').center(152)+'\n'
        return display

    def view_of(self, contain, name):
        contain =  str(''.join([str(minion) for minion in contain])).split('\n')[:-1]
        border, border_top = "\n+{}+\n".format('-'*150), "\n+{}+\n".format(name.center(150, '-'))
        contain = '\n'.join(["|{}|".format((' '*5).join(contain[i::7]).center(150)) for i in range(7)])
        return border_top + contain + border
######################################




