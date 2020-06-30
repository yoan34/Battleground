import time
from random import randint, choice
from Components.Minion import Minion
from Components.Hero import Hero
from Components.Discovery import Discovery

from constants.minions import MINIONS
from constants.position import LEN_SHOP
from constants.heroes import TIER_LIST

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
        self.double = {}

        self.triple = 0
        self.m_gold = 0
        self.board_gold_minion = 0

        self.max_freeze = 2
        self.max_swap = 7
        self.in_shop = True
        self.is_win_fight = True
        self.is_start_turn = True
        self.is_end_turn = False
        self.is_freeze = False
        self.immunity = 0
        self.view_discover = ''
        self.debug = False
        self.isHuman = False

        # rely to minion
        self.n_pogo = 0
        self.n_pirate = 0
        self.oldmurloc = 0
        self.hoggarr = 0
        self.zerus = 0
        self.watcher = 0
        self.brann = 1
        self.n_brann = 0
        self.n_khadgar = 0
        self.n_g_khadgar = 0

        self.n_action = 0
        self.n_buy = 0
        self.n_sold = 0
        self.n_play = 0
        self.n_swap = 0
        self.n_refresh = 0
        self.n_up = 0
        self.n_freeze = 0

        self.best_team = ''

    def get_all_actions(self):
        actions = []
        if self.max_freeze != 0:
            actions.append('freeze')
        if len(self.up_cost) > 1 and self.gold >= self.up_cost[0]:
            actions.append('up')
        if self.gold >= 3 and len(self.shop):
            actions.append('buy')
        if self.gold > 0:
            actions.append('refresh')
        if self.isHuman and len(self.board) > 0:
            actions.append('sold')
        elif not self.isHuman and len(self.board) > 6:
            actions.append('sold')
        if len(self.board) > 1 and self.max_swap != 0:
            actions.append('swap')
        if len(self.hand) and len(self.board) < 7:
            actions.append('play')
        return actions

########### CREATE CUSTOM STUFF ###########
    def create_shop(self, lvl):
        minions, shop = list(filter(lambda x: MINIONS[x]['lvl'] <= lvl, MINIONS)), []
        for i in range(LEN_SHOP[lvl-1]):
            minion = choice(minions)
            shop.append(Minion(minion, *[value for value in MINIONS[minion].values()]))
        return shop

    def create_minions(self, length, gold=False, *names):
        minions, team = [minion for minion in MINIONS], []
        for i in range(length):
            minion = choice(minions)
            team.append(Minion(minion, gold, *[value for value in MINIONS[minion].values()][1:]))
        for minion in names:
            team.append(Minion(minion, gold, *[value for value in MINIONS[minion].values()][1:]))
        return team

    def create_minion(self, gold, name):
        return Minion(name,gold, *[value for value in MINIONS[name].values()][1:])
        
    def create_hero(self, name):
        return Hero(name, *[value for value in TIER_LIST[name].values()])
############################################


########### MANAGE HUMAN INPUT ###########
    def get_answer_action(self):
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
                if self.gold > 0:
                    good_choice = True
                else:
                    print('Not enough gold.')
                    time.sleep(0.7)
            elif len(action) == 1 and action[0] == 'freeze':
                if self.max_freeze > 0:
                    good_choice = True
                else:
                    print('Maximum freeze reach this turn...')
                    time.sleep(0.7)

            elif len(action) == 1 and action[0] == 'up':
                if self.up_cost[0] != 'M':
                    if self.gold >= self.up_cost[0]:
                        good_choice = True
                    else:
                        print('Not enough gold for upgrade.')

                        time.sleep(0.7)
                else:
                    print('Level tavern max.')
                    time.sleep(0.7)

            elif len(action) == 2 and action[0] == 'buy':
                try:
                    action[1] = int(action[1])
                except ValueError:
                    action[1] = -1
                if action[1] > 0 and action[1] <= len(self.shop):
                    if self.gold >= self.minion_cost:
                        action.append(len(self.shop))
                        good_choice = True
                    else:
                        print('Not enough gold.')
                        time.sleep(0.7)
                else:
                    print('Position minion out of range. (buy)')
                    time.sleep(0.7)

            elif len(action) == 2 and action[0] == 'sold':
                try:
                    action[1] = int(action[1])
                except ValueError:
                    action[1] = -1
                if action[1] > 0 and action[1] <= len(self.board):
                    action.append(len(self.board))
                    good_choice = True
                else:
                    print('position minion out of range. (sold)')
                    time.sleep(0.7)

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
                        print('Maximum swap reach this turn...')
                        time.sleep(0.7)
                else:
                    print('position minions out of range. (swap)')
                    time.sleep(0.7)
            
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
                    good_choice = True
                else:
                    print('position minions out of range. (play)')
                    time.sleep(0.7)
            elif action[0].upper() == 'Q':
                break
            elif len(action) == 1 and action[0] == 'next':
                return action
            else:
                print('Action doesn\'t exist.')
                time.sleep(0.7)
        return action

    def get_answer_discovery(self):
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

###########################################

  
########### MANAGE PASSIVE MINION ###########
    def execute_passive_play(self, minion_play):
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

        for minion in self.board:
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
        if self.zerus:
            for pos, minion in enumerate(self.board):
                if minion.name == 'shifterZerus':
                    self.zerus -= 1
                    if minion.qn[-1] == 'Z':
                        self.board[pos] = Minion(minion.true_name, minion.gold, *[value for value in MINIONS[minion.true_name].values()][1:])
                    else:
                        self.board[pos] = minion
                    
    def execute_passive_sold(self, minion):
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
            self.n_brann -= 1
            if self.n_brann == 0:
                self.brann = 1
        elif minion.name == 'khadgar':
            if minion.gold:
               self.n_g_khadgar -= 1
            else:
                self.n_khadgar -= 1
        
        if self.oldmurloc and minion.archetype == 'murloc':
            for minion in self.board:
                if minion.name == 'oldMurkEye':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    fc(self, minion, '', target, buff, 'play')
        
    def execute_passive_turn(self, timing):
        # timing should are: 'start_turn' or 'end_turn'
        for minion in self.board:
            if minion.passive and minion.passive['trigger'] == timing:
                fc, target, buff = list(minion.passive.values())[:-1]
                fc(self, minion, target, buff)
        if timing == 'start_turn' and self.zerus:
            for pos, minion in enumerate(self.hand):
                if minion.name  == 'shifterZerus':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    self.hand[pos] = fc(self, minion, target, buff)

    def execute_passive_buy(self, minion_buy):
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
        self.execute_passive_turn('end_turn')
        self.in_shop = True
        self.max_swap = 7
        self.max_freeze = 2
        self.is_freeze = False
        self.n_pirate = 0
        self.turn += 1
        if self.up_cost[0] != 'M':
            self.up_cost[0]-= 1
        self.gold = 2 + self.turn if self.turn < 9 else 10
        if not self.is_freeze:
            self.shop = self.create_shop(self.lvl)
        self.execute_passive_turn('start_turn')

    def board_position_of(self, target='all', minion=False):
        if target in ('murloc', 'dragon', 'pirate', 'demon', 'meca', 'beast'):
            all_target = [pos+1 for (pos, minion) in enumerate(self.board) if minion.archetype == target]
            
        elif target in ('taunt', 'shield', 'windufry', 'poisonous', 'reborn'):
            all_target = [pos+1 for (pos, minion) in enumerate(self.board) if minion.__dict__[target]]
        else:
            all_target = [pos+1 for pos in range(len(self.board))]
        if minion:
            minion_index = [pos+1 for pos, m in enumerate(self.board) if m == minion][0]
            if minion_index in all_target:
                all_target.remove(minion_index)
        return all_target
        
    def triple_minion(self, minion_to_triple, is_token):
        minions = []
        board_name = [minion.name if not minion.gold else '' for minion in self.board]
        hand_name = [minion.name if isinstance(minion, Minion) and not minion.gold else '' for minion in self.hand]
        if minion_to_triple.name == 'khadgar':
            self.n_khadgar = 0
        while minion_to_triple.name in board_name:
            minions.append(self.board.pop(board_name.index(minion_to_triple.name)))
            board_name.remove(minion_to_triple.name)
        while minion_to_triple.name in hand_name:
            minions.append(self.hand.pop(hand_name.index(minion_to_triple.name)))
            hand_name.remove(minion_to_triple.name)
        if not is_token:
            minion_gold = Minion(minions[0].name, True, *[value for value in MINIONS[minions[0].name].values()][1:])
            minion_gold.atk = minions[0].atk + minions[1].atk + minion_to_triple.atk - MINIONS[minions[0].name]['atk']
            minion_gold.hp = minions[0].hp + minions[1].hp + minion_to_triple.hp - MINIONS[minions[0].name]['hp']
        else:
            minion_gold = Minion(minions[0].qn[:-2], True, minions[0].qn[:-2], 1, 1, 1, minions[0].archetype)
            minion_gold.atk = minions[0].atk + minions[1].atk + minion_to_triple.atk - 1
            minion_gold.hp = minions[0].hp + minions[1].hp + minion_to_triple.hp - 1
        
        self.board_gold_minion += 1
        self.triple += 1
        self.hand.append(minion_gold)
    
    def get_discovery(self, tier=False, minion=False, isHuman=False):
        return Discovery(tier, minion, self.isHuman)
