"""
Class Player manage states about the name and if is a human or IA mode.
It inherites Scanner, Hero and Game class and can perform three disctinct mode:
    -Human mode: allows to simulate the game by tape some actions.
    -IA mode: Simulate 14 turns of the game in randomly strategy.
    -Bot mode: Play to the real game standalone in randomly strategy.

All methods perform actions and manages states about these actions:
    -play   -refresh    
    -buy    -up
    -sold   -freeze
    -swap

Some methods just displays all the player's states:
    -display_hero()
    -display_state()
    -view_of()
"""
import time, os
from random import randint, choice

from Components.Scanner import Scanner
from Components.Hero import Hero
from Components.Game import Game
from Components.Discovery import Discovery
from Components.Minion import Minion

from constants.position import LEN_SHOP
from constants.heroes import HERO_POWER_ACTIVE_SHOP, HERO_POWER_ACTIVE_BOARD, HERO_POWER_ACTIVE_ONLY, LIST_HEROES

class Player(Game, Hero, Scanner):

    def __init__(self, name, pool, archetype, is_human=False):
        Game.__init__(self)
        self.name = name
        self.pool = pool
        self.no_archetype = archetype
        self.is_human = is_human
        self.time_by_action = 0

########### MANAGE ACTIONS ###########

    def timing_IA_action(self, name, args):
        """ Display a sentence if mode Bot or IA with a duration between actions. """
        if not self.is_human and self.time_by_action != 0:
            print(' - - IA: choose to {} {} - -'.format(name, '-'.join(map(str, args))))
            time.sleep(self.time_by_action)
        elif self.is_bot:
            print(' - - IA: choose to {} {} - -'.format(name, '-'.join(map(str, args))))
    
    def timing_IA(self, fight=False, team1=[], team2=[]):
        """ Display player's states if mode IA with a duration between actions. """
        if not self.is_human and self.time_by_action != 0:
            pass
            # print(self)
            # time.sleep(self.time_by_action)

    def get_action(self):
        """
        Gets and manages an action of the actions available.
        Writes action in human mode and choice randomly if IA mode.
        """
        if self.is_human:
            return self.get_answer_action()
        else:
            actions = self.get_all_actions()
            if not actions:
                self.do_action = ''
                return False
            action = choice(actions)
            if action == 'buy':
                return ('buy', randint(len(self.hero.maiev)+1, len(self.shop)), len(self.shop))
            elif action == 'sold':
                return ('sold', randint(1, len(self.board)), len(self.board))
            elif action == 'play':
                #here to resolve
                if not self.board:
                    targets = [pos+1 for pos, card in enumerate(self.hand) if (isinstance(card, Minion) or isinstance(card, Discovery))]
                    return ('play', choice(targets), len(self.hand), randint(1, len(self.board)+1), len(self.board))
                return ('play', randint(1, len(self.hand)), len(self.hand), randint(1, len(self.board)+1), len(self.board))
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
            elif action == 'power':
                if self.hero.name in HERO_POWER_ACTIVE_SHOP and self.gold >= self.hero.power['cost']:
                    if len(self.shop) > len(self.hero.maiev):
                        return ('power', randint(1+len(self.hero.maiev), len(self.shop)))
                elif self.hero.name in HERO_POWER_ACTIVE_BOARD and self.gold >= self.hero.power['cost']:
                    try:
                        return ('power', randint(1, len(self.board)))
                    except Exception:
                        print(self)
                        x=input('bug HERO POWER ACTIVE SHOP')
                elif (self.hero.name in HERO_POWER_ACTIVE_ONLY and self.gold >= self.hero.power['cost']):
                    return ('power',)
                elif self.hero.name == 'Malygos' and self.gold >= self.hero.power['cost']:
                    if self.board and self.shop:
                        place = choice('shop', 'board')
                    else:
                        place = 'shop' if self.shop else 'board'
                    if place == 'shop':
                        return ('power', 'shop', randint(1, len(self.shop)))
                    else:
                        return ('power', 'board', randint(1, len(self.board)))
            else:
                return ('freeze',)

    def make(self, action):
        """
        Execute the specific action and stop the simulation if
        mode IA and it reachs turn 14.
         """
        if action:
            self.do_action = action
            self.n_action += 1
            name, *args = action
            # self.timing_IA_action(name, args)
            ACTIONS = {
                'buy': self.buy_minion,
                'sold': self.sold_minion,
                'play': self.play_minion,
                'swap': self.swap_minion,
                'up': self.up,
                'refresh': self.refresh,
                'freeze': self.freeze,
                'next': self.next_turn,
                'finish': self.finish_action,
                'power': self.hero.play_power,
            }
            ACTIONS[name](*args) if name != 'power' else ACTIONS[name](self, *args)
        else:
            self.do_action = ''
            if self.solo:
                self.next_turn()
        if self.solo and self.turn == 14:
            return True
    
    def play_minion(self, *args):
        """
        Manages the 'play' action. If a minion is play or discover's card.
        Trigger battlecry, trigger Bot move if it activate, execute passives minions,
        in human/IA/Bot mode.
        """
        self.n_play += 1
        args = list(args)
        position, length_hand, direction, length_board = args
        self.bot_play_minion(*args) if self.is_bot else False
        card = self.hand[position-1]

        if isinstance(card, Minion):
            self.hand.pop(position-1)
            battlecry, target, buff = card.battlecry.values() if card.battlecry else (False, False, False)
            self.board.insert(direction-1, card)
            if card.name != 'shifterZerus' and card.magnetic and direction != len(self.board) and self.board[direction].archetype == 'meca':
                card.add_magnetic(self.board[direction])
                if not card.gold:
                    self.double[card.name] -= 1
                self.board.pop(direction-1)
                
            self.hero.power['do'](self, minion=card, add=True, action='play') if self.hero.deathwing else None
            battlecry(self, card, target, buff, direction, self.is_human) if card.battlecry else False
            if self.hero.shudderwock and battlecry:
                self.brann = 1
                self.hero.shudderwock = False
            self.execute_passive_play(card, self.board)
            if card.gold:
                card_discovery = self.get_discovery(tier=self.lvl, pool=self.pool.pool)
                self.hand.append(card_discovery)
            time.sleep(1.2) if self.is_bot else None

        elif isinstance(card, Discovery):
            if (card.cost == 3 and self.gold > 2) or (not card.cost):
                self.hand.pop(position-1)
                self.gold -= 3 if card.cost else 0
                self.view_discover = card.display_discovery()
                self.timing_IA()
                target = self.get_answer_discovery() if self.is_human else choice([1,2,3])
                new_minion = card.cards_discover[target-1]
                self.zerus += 1 if new_minion == 'shifterZerus' else 0
                new_minion = self.create_minion(False, new_minion)
                self.hand.append(new_minion)
                self.update_doublon_minion(new_minion)
                self.pool.remove_to_pool(new_minion.name, new_minion.lvl)
                self.view_discover = ''
        
        else:
            if self.hero.name == 'Lich':
                self.hand.pop(position-1)
                self.gold += 1 if self.gold < 10 else 0
            else:
                if not self.board:
                    print('Can\'t buff, no minion in the board.')
                    time.sleep(0.7)
                    return
                answer = self.get_answer_mukla() if self.is_human else choice([i for i in range(len(self.board))])
                self.board[answer].atk += 1
                self.board[answer].hp += 1
                self.hand.pop(position-1)
        self.get_type_of_board()
            
    def buy_minion(self, *args):
        """
        Manages 'buy' action when we buys a minion to the shop.
        See if we are triple cards, execute passives minions,
        in human/IA/Bot mode.
        """
        self.n_buy += 1
        self.buy_in_turn += 1
        args = list(args)
        position, length_shop = args
        self.bot_buy_minion(*args) if self.is_bot else False
        minion_buy = self.shop.pop(position-1)
        
        if self.time_by_action == 0:
            self.zerus_buy += 1 if minion_buy[0] == 'shifterZerus' else 0
            minion = self.create_minion(False, minion_buy[0])
            if minion_buy[2] != 0:
                minion.atk += minion_buy[2]
                minion.hp += minion_buy[2]
        else:
            self.zerus_buy += 1 if minion_buy.name == 'shifterZerus' else 0
            minion = self.create_minion(False, minion_buy.name)
            
        self.hero.power['do'](self, minion=minion) if self.hero.ratking else None
        self.hero.power['do'](self, minion=minion, add=False) if self.hero.deathwing else None
        self.hero.power['do'](self, minion) if self.hero.power['trigger'] == 'buy' else None
        self.hand.append(minion)
        self.gold -= self.minion_cost
        self.execute_passive_buy(minion)
        if minion.archetype == 'pirate':
            self.pirate_buy_in_turn += 1
            self.n_pirate += 1
            if self.hero.name == 'Patches':
                self.hero.power['cost'] -= 1 if self.hero.power['cost'] > 0 else 0
        self.update_doublon_minion(minion)
        
    def sold_minion(self, *args):
        """
        Manages 'sold' action, execute passives minions,
        in human/IA/Bot mode.
        """
        self.n_sold += 1
        args = list(args)
        position, length_board = args
        self.bot_sold_minion(*args) if self.is_bot else False
        self.gold += 1
        self.gold = 10 if self.gold > 10 else self.gold
        minion = self.board.pop(position-1)
        if minion.name[-2:].upper() != '_T' and minion.name != 'amalgame' and minion.name != 'treasure':
            self.pool.add_to_pool(minion.name, minion.lvl, minion.gold, minion.minions_magnetic)
        self.execute_passive_sold(minion)
        self.zerus -= 1 if minion.name == 'shifterZerus' else 0
        if self.hero.amalgame and minion.name == 'amalgame':
            self.hero.amalgame = False
        if not minion.gold:
            self.double[minion.name] -= 1
            if self.double[minion.name] == 0:
                self.double.pop(minion.name)
        self.hero.power['do'](self, minion) if self.hero.power['trigger'] == 'sold' else None
        
    def swap_minion(self, *args):
        """ Manages 'swap' action in human/IA/Bot mode. """
        self.n_swap += 1
        args = list(args)
        first, second, length = args
        self.bot_swap_minion(*args) if self.is_bot else False
        minion = self.board.pop(first-1)
        self.max_swap -= 1
        self.board.insert(second-1, minion)

    def up(self):
        """ manage 'up' action in human/IA/Bot mode. """
        self.bot_upgrade() if self.is_bot else False
        self.n_up += 1
        self.gold -= self.up_cost[0]
        self.up_cost.pop(0)
        self.lvl += 1
        self.hero.power['do'](self) if self.hero.power['trigger'] == 'up' else None

    def refresh(self):
        """ manage 'refresh' action in human/IA/Bot mode. """
        self.first_refresh = False
        self.bot_refresh() if self.is_bot else False
        self.n_refresh += 1
        self.gold -= self.refresh_cost
        if not self.is_bot:
            self.create_shop(self.lvl)
        else:
            time.sleep(1.7)
            self.shop = self.see_shop(self.lvl, LEN_SHOP[self.lvl-1])
        self.hero.power['do'](self, add=True) if self.hero.deathwing else None
        self.hero.power['do'](self) if self.hero.millificent else None
        self.refresh_cost = self.refresh_max_cost
        self.hero.power['do'](self) if self.hero.power['trigger'] == 'refresh' else None

    def freeze(self):
        """ manage 'freeze' action in human/IA/Bot mode. """
        self.bot_freeze() if self.is_bot else False
        self.n_freeze += 1
        self.is_freeze = not self.is_freeze
        self.max_freeze -= 1
        time.sleep(0.3) if self.is_bot else None
    
    def finish_action(self):
        self.can_play_action = False

######################################


########### DISPLAY STATE ############
    def __str__(self):
        """ Display the view of all player's states. """
        # os.system('cls')
        
        dash, hero, display = '-'*28,'', ''
        display = self.in_simulation if self.in_simulation else ''
        title = "+{} Player: {} {}+".format(dash, self.name, dash)
        sep = "+{}+".format('-' * (len(title)-2))

        hero += title+'\n'
        hero += (self.display_hero(len(title)) + sep+'\n') if  self.hero else ''
        hero += (self.display_state()+ sep+'\n')
        hero =self.add_view_hero_power(hero)

        board = self.view_of(self.board, 'B O A R D') 
        shop =  self.view_of(self.shop, 'S H O P') if self.time_by_action != 0 else str(self.shop)
        hand_or_discovery = self.view_discover if self.view_discover else self.view_of(self.hand, 'H A N D')
        view_action = "turn: {} -- name: {} -- action: {}".format(self.turn, self.name, self.do_action if self.do_action else ' ')
        display += shop + board + '\n\n\n' + hero + '\n' + hand_or_discovery

        return display

    def display_hero(self, length):
        """ Gets and returns the view of the hero. """
        display = ''
        for key, state in (('-hero: ', self.hero.name), ('-tier: ', self.hero.tier)):
            state = str(state).center(len(str(self.hero.name)))
            s = (key + str(state)).center(length-2)
            display += "|{}|".format(s)+'\n'
        return display

    def display_state(self):
        """ Gets and returns the view of the player's states. """
        n_double, display = 0, ''
        if self.debug:
            STATE_VIEW = [
                (('-hp:', self.hp), ('-gold:', self.gold), ('-n_pogo:', self.n_pogo), ('-watcher:', self.watcher)),
                (('-lvl:', self.lvl), ('-double:', n_double), ('-pirate_t:', self.pirate_buy_in_turn), ('-brann:', self.brann)),
                (('-up_cost:', self.up_cost[0]), ('-m_gold:', self.m_gold), ('-oldmurloc:', self.oldmurloc), ('-n_brann:', self.n_brann)),
                (('-turn:', self.turn), ('-freeze:', int(self.is_freeze)), ('-hoggarr:', self.hoggarr), ('-n_khadgar:', self.n_khadgar)),
                (('-immune:', self.immunity), ('-triple:', self.triple), ('-zerus:', self.zerus), ('-n_g_khad:', self.n_g_khadgar)),
            ]
        else:
            STATE_VIEW = [(('-hp:', self.hp), ('-gold:', self.gold)), (('-lvl:', self.lvl), ('-up_cost:', self.up_cost[0])),
                (('-turn:', self.turn), ('-freeze:', int(self.is_freeze)))]
        for i in self.double.values():
            if i > 1: n_double += 1

        for state in STATE_VIEW:
            s1 = '' if self.debug else ' '*13
            for key, props in state:
                props = str(props)
                if len(props) == 1:
                    props = ' '+props[0]
                s = (key.ljust(12 if self.debug else 9) + " {}  ".format(props))
                s1 += (s + '') if self.debug else (s+' '*14)
            display += ('|'+s1+'|')+'\n'
        return display

    def view_of(self, contain, name):
        """ Gets and returns the view of the board/shop/hand. """
        contain =  str(''.join([str(minion) for minion in contain])).split('\n')[:-1]
        border, border_top = "\n+{}+\n".format('-'*150), "\n+{}+\n".format(name.center(150, '-'))
        contain = '\n'.join(["|{}|".format((' '*5).join(contain[i::7]).center(150)) for i in range(7)])
        return border_top + contain + border

    def display_heroes(self, heroes):
        display = l1 = l2 = l3 = l4 = l5 = l6 = l7 = l8 = ''
        top = "+{}+".format(" CHOOSES AN HERO ".center(98,'-'))
        # print(top.center(152))
        for pos, hero in enumerate(heroes):
            l1 += "+{}+".format(hero.center(17,'-')) +' '*5
            l2 += "|{}|".format(' '*17) + ' '*5
            l3 += "| {}|".format(LIST_HEROES[hero]['power']['view'][0].ljust(16)) + ' '*5
            l4 += "| {}|".format(LIST_HEROES[hero]['power']['view'][1].ljust(16)) + ' '*5
            l5 += "| {}|".format(LIST_HEROES[hero]['power']['view'][2].ljust(16)) + ' '*5
            l6 += "|{}|".format(' '*17) + ' '*5
            l7 += "+{}+".format('-'*17) + ' '*5
            l8 += "{}".format(str(pos+1).center(19)) + ' '*5
        
        display += ("|{}|".format(l1[:-5].center(98)).center(152) + '\n' + "|{}|".format(l2[:-5].center(98)).center(152) + '\n' +
            "|{}|".format(l3[:-5].center(98)).center(152) + '\n' + "|{}|".format(l4[:-5].center(98)).center(152) +
            '\n' + "|{}|".format(l5[:-5].center(98)).center(152) + '\n' + "|{}|".format(l6[:-5].center(98)).center(152) +
            '\n' + "|{}|".format(l7[:-5].center(98)).center(152) + '\n' + "+{}+".format(''.center(98,'-')).center(152) +
            '\n' + l8[:-5].center(152) + '\n' +
            'Minion types this game: {}'.format(', '.join(list({'meca', 'dragon','murloc','beast','pirate','demon'} - {self.no_archetype}))).center(152)+'\n')
        print(display) if self.is_human else None

    def add_view_hero_power(self, hero):
        list_hero = hero.split('\n')[:-1]
        list_hp = self.hero.display_hero_power(self).split('\n')[:-1]
        for i in range(len(list_hero)):
            list_hero[i] = (list_hero[i] + (' '*7) + list_hp[i]).center(152)
        display = '\n'.join(list_hero)
        return display+'\n'

    def test_minions_pool(self):
        cards = 0
        for name, lvl, buff in self.shop:
            self.pool.add_to_pool(name, lvl)
        for minion in self.board + self.hand:
            if isinstance(minion, Minion) and minion.name[-2:] != '_t':
                cards += 3 if minion.gold else 1
        cards -= 2*self.n_reno
        cards -= 3*self.n_eudora
        cards -= 1*self.n_patches
        return cards





######################################





