"""
A dictionary for have all datas of heroes:
    -name
    -tier
    -img
    -archetype

This file also have all functions used for the hero power
"""
import time, copy
from random import choice, randint, choices, sample

from Components.Minion import Minion
from constants.minions import MINION_BY_ARCHETYPE, MINIONS_BY_TIER, ARCHETYPES, WITHOUT_MECA
from constants.position import LEN_SHOP

##############################
##### HERO POWER PASSIVE #####
##############################
# HERO PASSIVE 'TURN'
def hero_power_Afk(self):
    if self.turn < 3:
        self.gold = 0
        if not self.time_by_action == 0:
            [self.pool.add_to_pool(minion.name, minion.lvl) for minion in self.shop]
        else:
            [self.pool.add_to_pool(minion[0], minion[1]) for minion in self.shop]
        self.shop.clear()
    elif self.turn == 3:
        for _ in range(2):
            self.hand.append(self.get_discovery(tier=2, pool=self.pool.pool))

def hero_power_Ysera(self):
    names, copies, levels = [], [], []
    for minions in self.pool.pool[:self.lvl]:
        names += [name for name in minions if minions[name]['archetype'] == 'dragon']
        copies += [minions[name]['copy'] for name in minions if minions[name]['archetype'] == 'dragon']
        levels += [minions[name]['lvl'] for name in minions if minions[name]['archetype'] == 'dragon']
    buffs = [0]*len(levels)
    minion = choices(list(zip(names, levels, buffs)), weights=copies, k=1)[0]
    self.pool.remove_to_pool(minion[0], minion[1])
    if self.time_by_action == 0:
        self.shop.append(minion)
    else:
        minion = self.create_minion(False, minion[0])
        self.shop.append(minion)

def hero_power_Nozdormu(self):
    if self.first_refresh:
        self.refresh_cost = 0

def hero_power_Sindragosa(self):
    if self.is_freeze:
        if self.time_by_action == 0:
            for pos in range(len(self.shop)):
                self.shop[pos][2] += 1
        else:
            for minion in self.shop:
                minion.atk += 1
                minion.hp += 1

def hero_power_Ratking(self, minion=False):
    if not minion:
        if not self.hero.ratking:
            self.hero.ratking = choice(ARCHETYPES)
        else:
            choices = list({*ARCHETYPES} - set([self.hero.ratking, self.no_archetype]))
            self.hero.ratking = choice(choices)
    else:
        if minion.archetype == self.hero.ratking:
            minion.atk += 1
            minion.hp += 2


## CAN MERGE ALEX AND ELISE
# HERO PASSIVE 'UP'
def hero_power_Alexstrasza(self):
    if self.lvl == 5:
        for _ in range(2):
            discovery = self.get_discovery(hero='Alexstrasza', pool=self.pool.pool)
            if self.is_bot:
                time.sleep(2)
                dragons_discovery = self.see_discovery(nature='Alexstrasza')
                self.view_discover = discovery.display_discovery(buff_discovery)
            else:
                self.view_discover = discovery.display_discovery()
            self.timing_IA()
            target_discovery = self.get_answer_discovery() if self.is_human else choice([1,2,3])
            new_minion = discovery.cards_discover[target_discovery-1]
            new_minion = self.create_minion(False, new_minion)
            self.pool.remove_to_pool(new_minion.name, new_minion.lvl)
            self.hand.append(new_minion)

            self.update_doublon_minion(new_minion)
            self.view_discover = ''

def hero_power_Elise(self):
    self.hand.append(self.get_discovery(tier=self.lvl-1, pool=self.pool.pool, cost=3))

def hero_power_Vashj(self):
    new_minions = []
    for minion in self.shop:
        lvl = minion.lvl if self.time_by_action != 0 else minion[1]
        names, copies, levels, buffs = self.pool.select_in_pool(lvl)
        new_minion = choices(list(zip(names, levels, buffs)), weights=copies, k=1)[0]
        self.pool.remove_to_pool(new_minion[0], new_minion[1])
        if self.time_by_action == 0:
            self.pool.add_to_pool(minion[0], minion[1])
        else:
            self.pool.add_to_pool(minion.name, minion.lvl)
            new_minion = self.create_minion(False, new_minion[0])

        new_minions.append(new_minion)
        self.shop = new_minions

# HERO PASSIVE DIRECT IMPACT
def hero_power_Bartendotron(self):
    for i in range(len(self.up_cost[:-1])):
        self.up_cost[i] -= 1

def hero_power_Deathwing(self, minion=False, add=False, action=False):
    self.hero.deathwing = True
    if self.time_by_action == 0 and action == 'play':
        minion.atk +=2

    elif self.time_by_action != 0:
        if minion:
            minion.atk +=2 if add else 0
        else:
            for minion in self.shop:
                minion.atk += 2

def hero_power_Millificent(self):
    self.hero.millificent = True
    if not self.time_by_action == 0:
        for minion in self.shop:
                if minion.archetype == 'meca':
                    minion.atk += 1
                    minion.hp += 1
    else:
        for pos in range(len(self.shop)):
            if self.shop[pos][0] in WITHOUT_MECA[:-1]:
                self.shop[pos][2] += 1

def hero_power_Millhouse(self):
    self.minion_cost = 2
    self.refresh_cost = 2
    self.refresh_max_cost = 2
    for i in range(len(self.up_cost[:-1])):
        self.up_cost[i] += 1

def hero_power_Patchwerk(self):
    self.max_hp = 50
    self.hp = 50

def hero_power_Curator(self):
    amalgame = Minion('amalgame', False, 'amalgame', 1, 1, 1, 'all',deathrattle=[], fight={'do': [], 'trigger': ''})
    self.board.append(amalgame)
    self.hero.amalgame = amalgame
    self.double[amalgame.name] = 1

# HERO PASSIVE 'SOLD'
def hero_power_Deryl(self, minion):
    if not self.shop: return
    for _ in range(2):
        minion = choice(self.shop)
        if self.time_by_action == 0:
            minion[2] += 1
        else:
            minion.atk += 1
            minion.hp += 1

def hero_power_Flurgl(self, minion):
    if len(self.shop) < 7 and minion.archetype == 'murloc':
        names, copies, levels, buffs = self.pool.select_in_pool('murloc', max=self.lvl)
        murloc = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
        self.pool.remove_to_pool(murloc[0], murloc[1])
        if self.time_by_action != 0:
            murloc = self.create_minion(False, murloc[0])
        self.shop.append(murloc)

# HERO PASSIVE 'BUY'
def hero_power_Kaelthas(self, minion):
    if self.n_buy % 3 == 0:
        minion.atk += 2
        minion.hp += 2

#HERO PASSIVE 'REFRESH'
def hero_power_Aranna(self):
    if self.n_refresh == 6:
        self.hero.aranna = True


############################
##### HERO POWER ACTIVE ####
############################
def hero_power_Eudora(self):
    self.hero.eudora += 1
    if self.hero.eudora == 4:
        self.n_eudora += 1
        self.hero.eudora, names = 0, []
        for lvl in range(self.lvl):
            names += self.pool.pool[lvl]
        name = choice(names)
        if name == 'shifterZerus':
            self.zerus += 1
        self.hand.append(self.create_minion(True, name))
    
def hero_power_Hooktusk(self, pos):
    lvl = self.board[pos-1].lvl
    if self.board[pos-1].name[-2:].upper() != '_T':
        self.pool.add_to_pool(self.board[pos-1].name, self.board[pos-1].lvl, self.board[pos-1].minions_magnetic)
    minion_remove = self.board.pop(pos-1)
    if not minion_remove.gold:
        self.double[minion_remove.name] -= 1
        if self.double[minion_remove.name] == 0:
            self.double.pop(minion_remove.name)
    lvl = 1 if lvl == 1 else lvl-1

    names, copies, levels, buffs = self.pool.select_in_pool(lvl-1)
    minion = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
    self.pool.remove_to_pool(minion[0], minion[1])
    minion = self.create_minion(False, minion[0])

    self.hand.append(minion)
    self.update_doublon_minion(minion)

def hero_power_Rafaam(self):
    # have to put rafaam to false after get minion
    self.hero.rafaam = True

def hero_power_Vancleef(self, pos):
    self.board[pos-1].atk += self.buy_in_turn
    self.board[pos-1].hp += self.buy_in_turn

def hero_power_Toki(self):
    if not self.is_bot:
        lvl = self.lvl if self.lvl < 6 else 5
        self.create_shop(self.lvl)
        names, copies, levels, buffs = self.pool.select_in_pool(lvl)
        minion = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
        self.pool.remove_to_pool(minion[0], minion[1])
        if self.time_by_action == 0:
            self.pool.add_to_pool(self.shop[-1][0], self.shop[-1][1])
        else:
            self.pool.add_to_pool(self.shop[-1].name, self.shop[-1].lvl)
            minion = self.create_minion(False, minion[0])

        self.shop = self.shop[:-1]
        self.shop.append(minion)

def hero_power_Yogg(self):
    if len(self.shop):
        position = randint(1, len(self.shop))
        minion = self.shop.pop(position-1)
        if self.time_by_action == 0:
            minion = self.create_minion(False, minion[0])
        
        minion.atk += 1
        minion.hp += 1
        self.hand.append(minion)
        self.update_doublon_minion(minion)

def hero_power_Pyramad(self):
    if self.board:
        position = randint(0, len(self.board)-1)
        self.board[position].hp += 4

def hero_power_Kragg(self):
    if self.hero.n_power == 1:
        total_gold = self.gold + self.turn
        self.gold = 10 if total_gold > 10 else total_gold

def hero_power_Lich(self):
    if not self.immunity:
        self.hp -= 2
    card = '(0)-{}-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format('Gold Coin'.center(10, '-'), ' '*14,
            ' '*14, 'Gain 1 gold.'.center(14), ' '*14, ' '*14, '-'*14)
    self.hand.append(card)    

def hero_power_Malygos(self, place, pos):
    # FACTORISE CODE
    if self.time_by_action != 0:
        lvl = self.board[pos-1].lvl if place == 'board' else self.shop[pos-1].lvl
    else:
        lvl = self.board[pos-1].lvl if place == 'board' else self.shop[pos-1][1]
    lvl = lvl if lvl < 6 else 5
    names, copies, levels, buffs = self.pool.select_in_pool(lvl)
    minion = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
    self.pool.remove_to_pool(minion[0], minion[1])
        
    if place == 'board':
        self.pool.add_to_pool(self.board[pos-1].name, self.board[pos-1].lvl, self.board[pos-1].minions_magnetic)
        minion = self.create_minion(False, minion[0])
        self.board[pos-1] = minion
    else:
        if self.time_by_action != 0:
            self.pool.add_to_pool(self.shop[pos-1].name, self.shop[pos-1].lvl)
            minion = self.create_minion(False, minion[0])
        else:
            self.pool.add_to_pool(self.shop[pos-1][0], self.shop[pos-1][1])
        self.shop[pos-1] = minion

def hero_power_Reno(self, pos):
    if self.hero.n_power == 1:
        self.n_reno += 1
        name = self.board[pos-1].name
        if not self.board[pos-1].gold:
            self.double[name]-= 1
        minion = self.create_minion(True, name)
        minion.atk += self.board[pos-1].atk - (minion.atk//2)
        minion.hp += self.board[pos-1].hp - (minion.hp//2)
        self.board[pos-1] = minion

def hero_power_Shudderwock(self):
    if self.brann == 1:
        self.hero.shudderwock = True
        self.brann = 2

def hero_power_George(self, pos):
    self.board[pos-1].shield = True

def hero_power_Patches(self):
    names, copies, levels, buffs = self.pool.select_in_pool('pirate', max=self.lvl)
    minion = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
    self.n_patches += 1
    pirate = self.create_minion(False, minion[0])
    self.hand.append(pirate)
    self.update_doublon_minion(pirate)
    self.hero.power['cost'] = 4
    
def hero_power_Lichking(self, pos):
    self.hero.lichking = self.board[pos-1]
    self.board[pos-1].reborn = True

def hero_power_Wagtoggle(self):
    if self.board:
        for archetype in ARCHETYPES:
            targets = self.board_position_of(self.board, archetype)
            if targets:
                target = choice(targets)
                self.board[target-1].atk += 2
            
def hero_power_Nefarian(self):
    self.hero.nefarian = True

def hero_power_Maiev(self, pos=False):
    if pos:
        minion = self.shop.pop(pos-1)
        if self.time_by_action == 0:
            minion[2] = 2
        else:
            minion.maiev = 2 
        self.hero.maiev.append(minion)
        self.shop = self.hero.maiev + self.shop[len(self.hero.maiev)-1:]
    else:
        if self.time_by_action == 0:
            for minion in self.hero.maiev:
                minion[2] -= 1
            position = [pos for pos, m in enumerate(self.hero.maiev) if m[2] == 0]
        else:
            for minion in self.hero.maiev:
                minion.maiev -= 1
            position = [pos for pos, m in enumerate(self.hero.maiev) if m.maiev == 0]
        if position:
            minion = self.hero.maiev.pop(position[0])
            self.shop = self.hero.maiev + self.shop[len(self.hero.maiev)+1:]
            if self.time_by_action == 0:
                minion = self.create_minion(False, minion[0])
            minion.atk += 1
            minion.hp += 1
            if minion.name == 'shifterZerus':
                self.zerus += 1
            self.hand.append(minion)
            self.update_doublon_minion(minion)
        
def hero_power_Galakrond(self, pos):
    if self.time_by_action == 0:
        lvl = self.shop[pos-1][1]
        self.pool.add_to_pool(self.shop[pos-1][0], self.shop[pos-1][1])
    else:
        lvl = self.shop[pos-1].lvl
        self.pool.add_to_pool(self.shop[pos-1].name, self.shop[pos-1].lvl)
    lvl = lvl if lvl < 6 else 5
    names, copies, levels, buffs = self.pool.select_in_pool(lvl)
    minion = choices(list(map(list, zip(names, levels, buffs))), weights=copies, k=1)[0]
    self.pool.remove_to_pool(minion[0], minion[1])
    if self.time_by_action != 0:
        minion = self.create_minion(False, minion[0])
    self.shop[pos-1] = minion

def hero_power_Jaraxxus(self):
    targets = self.board_position_of(self.board, 'demon')
    for pos in targets:
        self.board[pos-1].atk += 1
        self.board[pos-1].hp += 1

def hero_power_Akazamzarak(self):
    pass

def hero_power_Greymane(self):
    if not self.is_bot:
        player_lvl = self.lvl if self.lvl < 6 else 5
        if self.time_by_action == 0:
            [self.pool.add_to_pool(name, lvl) for name, lvl, buff in self.shop]
            self.shop.clear()
            for minion in self.last_enemies:
                if (minion.name[-2:].upper() != '_T' and minion.name != 'amalgame' and
                    minion.name.lower() != 'treasure' and self.pool.pool[minion.lvl-1][minion.name]['copy'] > 0):
                    self.pool.remove_to_pool(minion.name, minion.lvl)
                    self.shop.append([minion.name, minion.lvl, 0])
        else:
            [self.pool.add_to_pool(minion.name, minion.lvl) for minion in self.shop]
            self.shop.clear()
            for minion in self.last_enemies:
                if (minion.name[-2:].upper() != '_T' and minion.name != 'amalgame' and
                    minion.name.lower() != 'treasure' and self.pool.pool[minion.lvl-1][minion.name]['copy'] > 0):
                    self.pool.remove_to_pool(minion.name, minion.lvl)
                    self.shop.append(self.create_minion(False, minion.name))
        if LEN_SHOP[player_lvl-1] - len(self.shop) > 0:
            self.fulfill_shop(player_lvl)

def hero_power_Brann(self):
    names, copies, levels, buffs = self.pool.select_in_pool('battlecry', max=self.lvl)
    minions = choices(list(zip(names, levels, buffs)), weights=copies, k=LEN_SHOP[self.lvl-1])
    while len(set(minions)) != LEN_SHOP[self.lvl-1]:
        minions = choices(list(zip(names, levels, buffs)), weights=copies, k=LEN_SHOP[self.lvl-1])
    if self.time_by_action == 0:
        [self.pool.add_to_pool(name, lvl) for name, lvl, buff in self.shop]
        self.shop.clear()
        [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
        self.shop.extend([list(arr[:]) for arr in minions])
    else:
        [self.pool.add_to_pool(minion.name, minion.lvl) for minion in self.shop]
        self.shop.clear()
        [self.pool.remove_to_pool(name, lvl) for name, lvl, buff in minions]
        for name, pos, buff in minions:
            self.shop.append(self.create_minion(False, name))

def hero_power_Mukla(self):
    self.hero.mukla = True
    for _ in range(2):
        card = '(0)-{}-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format('Banana'.center(10, '-'), ' '*14,
            ' '*14, 'Give +1/+1'.center(14), ' '*14, ' '*14, '-'*14)
        self.hand.append(card) 

def hero_power_Illidan(self):
    self.hero.illidan = True

def hero_power_Finley(self, rest_heroes):
    heroes = sample(rest_heroes, 3)
    self.display_heroes(heroes) if self.is_human else None
    answer = self.get_answer_hero(heroes, 3) if self.is_human else choice([1,2,3])
    hero = heroes[answer-1]
    self.hero.name = hero
    self.hero.power = LIST_HEROES[hero]['power']
    self.hero.play_power = self.hero._play_power if self.hero.power['active'] else None

def hero_power_Bigglesworth(self, player_dead):
    # board = copy.copy(player_dead.board) #normally
    board = copy.copy(player_dead)
    minions = []
    for _ in range(3):
        minion = choice(board)
        board.remove(minion)
        minions.append(minion)
    discovery = self.get_discovery()
    self.view_discover = discovery.display_discovery(minions=minions)
    self.timing_IA()
    target_discovery = self.get_answer_discovery() if self.is_human else choice([1,2,3])
    new_minion = discovery.cards_discover[target_discovery-1]
    self.hand.append(new_minion)
    self.update_doublon_minion(new_minion) if not new_minion.gold else None
    self.view_discover = ''




HERO_POWER_ACTIVE_SHOP = ['Galakrond', 'Maiev']
HERO_POWER_ACTIVE_BOARD = ['Hooktusk', 'Vancleef', 'George', 'Reno', 'Lichking']
HERO_POWER_ACTIVE_ONLY = ['Rafaam', 'Eudora', 'Toki', 'Lich', 'Jaraxxus', 'Nefarian', 'Patches',
    'Pyramad', 'Wagtoggle', 'Shudderwock', 'Kragg', 'Yogg', 'Greymane', 'Brann','Mukla']

LIST_HEROES = {
    'Hooktusk': {
		'tier': 1,
		'img': './img/hero/hooktusk.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 0,
            'do': hero_power_Hooktusk,
            'trigger': None,
            'view': [' del a minion.', ' get a random', ' minion lower'],
        },
		},
    'Rafaam' : {
		'tier': 2,
		'img': './img/hero/rafaam.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Rafaam,
            'trigger': None,
            'view': [' add copy of', ' first minion', ' kill.']
        },
		},
    'Deryl' : {
		'tier': 2,
		'img': './img/hero/deryl.png',
		'archetype': None,
        'power': {
            'active': False,
            'cost': 0,
            'do': hero_power_Deryl,
            'trigger': 'sold',
            'view': [' after sell a', ' minion. Give a', ' +1/+1 twice'],
        },
		},
    'Kaelthas' : {
		'tier': 2,
		'img': './img/hero/kaelthas.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Kaelthas,
            'cost': 0,
            'trigger': 'buy',
            'view': [' Every thrid', ' minion you buy', ' gain +2/+2'],
        },
		},
    'Nozdormu' : {
		'tier': 2,
		'img': './img/hero/nozdormu.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Nozdormu,
            'cost': 0,
            'trigger': 'turn',
            'view': [' Your first', ' refresh each', ' turn cost 0G'],
        },
		},
    'Pyramad' : {
		'tier': 2,
		'img': './img/hero/pyramad.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Pyramad,
            'trigger': None,
            'view': [' Give a random', ' friendly minion', ' +4 health'],
        },
		},
    'Yogg' : {
		'tier': 2,
		'img': './img/hero/yogg.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 2,
            'do': hero_power_Yogg,
            'trigger': None,
            'view': [' Get random', ' minion from', ' shop, +1/+1'],
        },
		},
    'Vancleef' : {
		'tier': 3,
		'img': './img/hero/vancleef.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Vancleef,
            'trigger': None,
            'view': [' Give +1/+1 for', ' each minion', ' buy this turn'],
        },
		},
    'Deathwing' : {
		'tier': 3,
		'img': './img/hero/deathwing.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Deathwing,
            'cost': 0,
            'trigger': 'now',
            'view': [' All minion', ' have +2 attack', ' '],
        },
		},
    'Finley' : {
		'tier': 3,
		'img': './img/hero/finley.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Finley,
            'cost': 0,
            'trigger': 'start_game',
            'view': [' Choice', ' another', ' hero power.'],
        },
		},
    'Eudora' : {
		'tier': 3,
		'img': './img/hero/eudora.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Eudora,
            'trigger': None,
            'view': [' Dig for a', ' golden minion!', ' '],
        },
		},
    'Millhouse' : {
		'tier': 3,
		'img': './img/hero/millhouse.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Millhouse,
            'cost': 0,
            'trigger': 'now',
            'view': [' Minion cost 2G', ' refresh cost 2G', ' up cost 1G more'],
        },
		},
    'Toki' : {
		'tier': 3,
		'img': './img/hero/toki.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Toki,
            'trigger': None,
            'view': [' Refresh and', ' include higher', ' tavern tier'],
        },
		},
    'Kragg' : {
		'tier': 4,
		'img': './img/hero/kragg.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 0,
            'do': hero_power_Kragg,
            'trigger': None,
            'view': [' Gain 1G by', ' turn passed', ' '],
        },
		},
    'Elise' : {
		'tier': 4,
		'img': './img/hero/elise.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Elise,
            'cost': 0,
            'trigger': 'up',
            'view': [' when update', ' get a', ' recruitment map'],
        },
		},
    'Lich' : {
		'tier': 4,
		'img': './img/hero/lich.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 0,
            'do': hero_power_Lich,
            'trigger': None,
            'view': [' Take two dmg', ' and add a Gold', ' Coin in hand'],
        },
		},
    'Alexstrasza' : {
		'tier': 4,
		'img': './img/hero/alexstrasza.png',
		'archetype': 'dragon',
        'power': {
            'active': False,
            'do': hero_power_Alexstrasza,
            'cost': 0,
            'trigger': 'up',
            'view': [' When tavern', ' lvl 5 discover', ' two dragons'],
        },
		},
    'Sindragosa' : {
		'tier': 4,
		'img': './img/hero/sindragosa.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Sindragosa,
            'cost': 0,
            'trigger': 'turn',
            'view': [' At end of turn', ' frozen minions', ' get +1/+1'],
        },
		},
    'Afk' : {
		'tier': 4,
		'img': './img/hero/afk.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Afk,
            'cost': 0,
            'trigger': 'turn',
            'view': [' Wait two turn', ' discover two', ' minions tier 3'],
        },
		},
    'Millificent' : {
		'tier': 5,
		'img': './img/hero/millificent.png',
		'archetype': 'meca',
        'power': {
            'active': False,
            'do': hero_power_Millificent,
            'cost': 0,
            'trigger': 'now',
            'view': [' Mech in bob\'s', ' Tavern have', ' +1/+1'],
        },
		},
    'Ratking' : {
		'tier': 5,
		'img': './img/hero/ratking.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Ratking,
            'cost': 0,
            'trigger': 'turn',
            'view': [' When buy', ' minion correct', ' type, +1/+2'],
        },
		},
    'Curator' : {
		'tier': 5,
		'img': './img/hero/curator.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Curator,
            'cost': 0,
            'trigger': 'now',
            'view': [' Start the game', ' with one', ' amalgame'],
        },
		},
    'Patchwerk' : {
		'tier': 5,
		'img': './img/hero/patchwerk.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Patchwerk,
            'cost': 0,
            'trigger': 'now',
            'view': [' Start with 50', ' health instead', ' of 40'],
        },
		},
    'Malygos' : {
		'tier': 5,
		'img': './img/hero/malygos.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 0,
            'do': hero_power_Malygos,
            'trigger': None,
            'view': [' Replace minion', ' with a random', ' one. Same tier'],
        },
		},
    'Illidan' : {
		'tier': 6,
		'img': './img/hero/illidan.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Illidan,
            'cost': 0,
            'trigger': None,
            'view': [' Your left and', ' right minions', ' atk immediately'],
        },
		},
    'Reno' : {
		'tier': 6,
		'img': './img/hero/reno.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 2,
            'do': hero_power_Reno,
            'trigger': None,
            'view': [' Make a friendly', ' minion golden', ' '],
        },
		},
    'Bartendotron' : {
		'tier': 6,
		'img': './img/hero/bartendotron.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Bartendotron,
            'cost': 0,
            'trigger': 'now',
            'view': [' Reduce the', ' cost of tavern', ' tier by (1)'],
        },
		},
    'Shudderwock' : {
		'tier': 6,
		'img': './img/hero/shudderwock.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Shudderwock,
            'trigger': None,
            'view': [' You next btc', ' this turn', ' trigger twice'],
        },
		},
    'George' : {
		'tier': 6,
		'img': './img/hero/george.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 3,
            'do': hero_power_George,
            'trigger': None,
            'view': [' Give a friendly', ' minion divine', ' shield'],
        },
		},
    'Flurgl' : {
		'tier': 7,
		'img': './img/hero/flurgl.png',
		'archetype': 'murloc',
        'power': {
            'active': False,
            'do': hero_power_Flurgl,
            'cost': 0,
            'trigger': 'sold',
            'view': [' after sell', ' minion, add', ' murloc in shop'],
        },
		},
    'Ysera' : {
		'tier': 7,
		'img': './img/hero/ysera.png',
		'archetype': 'dragon',
        'power': {
            'active': False,
            'do': hero_power_Ysera,
            'cost': 0,
            'trigger': 'turn',
            'view': [' At start of', ' turn, add', ' dragon in shop'],
        },
		},
    'Patches' : {
		'tier': 7,
		'img': './img/hero/patches.png',
		'archetype': 'pirate',
        'power': {
            'active': True,
            'cost': 4,
            'do': hero_power_Patches,
            'trigger': None,
            'view': [' Get a pirate.', ' buy pirate', ' reduce cost 1G'],
        },
		},
    'Vashj' : {
		'tier': 7,
		'img': './img/hero/vashj.png',
		'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Vashj,
            'cost': 0,
            'trigger': 'up',
            'view': [' after you up', ' replace minions', ' by higher tier'],
        },
		},
    'Lichking' : {
		'tier': 7,
		'img': './img/hero/lichking.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Lichking,
            'trigger': None,
            'view': [' Give a minion', ' reborn for', ' next fight'],
        },
		},
    'Wagtoggle' : {
		'tier': 8,
		'img': './img/hero/wagtoggle.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Wagtoggle,
            'trigger': None,
            'view': [' Give for all', ' types minions', ' +2 attack'],
        },
		},
    'Nefarian' : {
		'tier': 8,
		'img': './img/hero/nefarian.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Nefarian,
            'trigger': None,
            'view': [' Deal 1 dmg', ' to all enemy', ' minions.'],
        },
		},
    'Maiev' : {
		'tier': 8,
		'img': './img/hero/maiev.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Maiev,
            'trigger': None,
            'view': [' Make a minion', ' dormant in shop', ' 2 turns, +1/+1'],
        },
		},
    'Galakrond' : {
		'tier': 8,
		'img': './img/hero/galakrond.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Galakrond,
            'trigger': None,
            'view': [' replace minion', ' in shop with', ' a higher minion'],
        },
		},
    'Jaraxxus' : {
		'tier': 8,
		'img': './img/hero/jaraxxus.png',
		'archetype': 'demon',
        'power': {
            'active': True,
            'cost': 1,
            'do': hero_power_Jaraxxus,
            'trigger': None,
            'view': [' Give your', ' demons +1/+1', ' '],
        },
		},
    'Aranna': {
        'tier': 8,
        'img': './img/hero/aranna.png',
        'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Aranna,
            'cost': 0,
            'trigger': 'refresh',
            'view': [' After refresh', ' 7 times, bob', ' has 7 minions'],
        },
        },
    'Greymane':{
        'tier': 8,
        'img': '',
        'archetype': None,
        'power': {
            'active': True,
            'do': hero_power_Greymane,
            'cost': 1,
            'trigger': None,
            'view': [' refresh tavern', ' with last', ' enemy warband']
        },
        },
    'Brann': {
        'tier': 8,
        'img': '',
        'archetype': None,
        'power': {
            'active': True,
            'do': hero_power_Brann,
            'cost': 1,
            'trigger': None,
            'view': [' refresh tavern', ' with battlecry', 'minions.']
        }
        },
    'Mukla': {
        'tier': 8,
        'img': '',
        'archetype': None,
        'power': {
            'active': True,
            'do': hero_power_Mukla,
            'cost': 1,
            'trigger': None,
            'view': [' get 2 bananas.', ' At end turn,', ' all get one.']
        }
        },
    'Bigglesworth': {
        'tier': 8,
        'img': '',
        'archetype': None,
        'power': {
            'active': False,
            'do': hero_power_Bigglesworth,
            'cost': 0,
            'trigger': 'player_dead',
            'view': [' When player', ' die discover a', ' minion of him']
        }
        },
}



HEROES_WITHOUT_BEAST = [name for name in LIST_HEROES]
HEROES_WITHOUT_MECA = list({name for name in LIST_HEROES} - {'Millificent'})
HEROES_WITHOUT_DEMON = list({name for name in LIST_HEROES} - {'Jaraxxus'})
HEROES_WITHOUT_MURLOC = list({name for name in LIST_HEROES} - {'Flurgl'})
HEROES_WITHOUT_DRAGON = list({name for name in LIST_HEROES} - {'Ysera', 'Alexstrasza'})
HEROES_WITHOUT_PIRATE = list({name for name in LIST_HEROES} - {'Patches'})

HEROES = {
    'beast': HEROES_WITHOUT_BEAST,
    'murloc': HEROES_WITHOUT_MURLOC,
    'meca': HEROES_WITHOUT_MECA,
    'demon': HEROES_WITHOUT_DEMON,
    'dragon': HEROES_WITHOUT_DRAGON,
    'pirate': HEROES_WITHOUT_PIRATE,
}


DATA_HEROES = {
    'Hooktusk': {
		'points': 0 ,
		'count': 0,
		},
    'Rafaam' : {
		'points': 0 ,
		'count': 0,
		},
    'Deryl' : {
		'points': 0 ,
		'count': 0,
		},
    'Kaelthas' : {
		'points': 0 ,
		'count': 0,
		},
    'Nozdormu' : {
		'points': 0 ,
		'count': 0,
		},
    'Pyramad' : {
		'points': 0 ,
		'count': 0,
		},
    'Yogg' : {
		'points': 0 ,
		'count': 0,
		},
    'Vancleef' : {
		'points': 0 ,
		'count': 0,
		},
    'Deathwing' : {
		'points': 0 ,
		'count': 0,
		},
    'Finley' : {
		'points': 0 ,
		'count': 0,
		},
    'Eudora' : {
		'points': 0 ,
		'count': 0,
		},
    'Millhouse' : {
		'points': 0 ,
		'count': 0,
		},
    'Toki' : {
		'points': 0 ,
		'count': 0,
		},
    'Kragg' : {
		'points': 0 ,
		'count': 0,
		},
    'Elise' : {
		'points': 0 ,
		'count': 0,
		},
    'Lich' : {
		'points': 0 ,
		'count': 0,
		},
    'Alexstrasza' : {
		'points': 0 ,
		'count': 0,
		},
    'Sindragosa' : {
		'points': 0 ,
		'count': 0,
		},
    'Afk' : {
		'points': 0 ,
		'count': 0,
		},
    'Millificent' : {
		'points': 0 ,
		'count': 0,
		},
    'Ratking' : {
		'points': 0 ,
		'count': 0,
		},
    'Curator' : {
		'points': 0 ,
		'count': 0,
		},
    'Patchwerk' : {
		'points': 0 ,
		'count': 0,
		},
    'Malygos' : {
		'points': 0 ,
		'count': 0,
		},
    'Illidan' : {
		'points': 0 ,
		'count': 0,
		},
    'Reno' : {
		'points': 0 ,
		'count': 0,
		},
    'Bartendotron' : {
		'points': 0 ,
		'count': 0,
		},
    'Shudderwock' : {
		'points': 0 ,
		'count': 0,
		},
    'George' : {
		'points': 0 ,
		'count': 0,
		},
    'Flurgl' : {
		'points': 0 ,
		'count': 0,
		},
    'Ysera' : {
		'points': 0 ,
		'count': 0,
		},
    'Patches' : {
		'points': 0 ,
		'count': 0,
		},
    'Vashj' : {
		'points': 0 ,
		'count': 0,
		},
    'Lichking' : {
		'points': 0 ,
		'count': 0,
		},
    'Wagtoggle' : {
		'points': 0 ,
		'count': 0,
		},
    'Nefarian' : {
		'points': 0 ,
		'count': 0,
		},
    'Maiev' : {
		'points': 0 ,
		'count': 0,
		},
    'Galakrond' : {
		'points': 0 ,
		'count': 0,
		},
    'Jaraxxus' : {
		'points': 0 ,
		'count': 0,
		},
    'Aranna': {
        'points': 0 ,
		'count': 0,
        },
    'Greymane':{
        'points': 0 ,
		'count': 0,
        },
    'Brann': {
        'points': 0 ,
		'count': 0,
        },
    'Mukla': {
        'points': 0 ,
		'count': 0,
        },
    'Bigglesworth': {
        'points': 0 ,
		'count': 0,
        },
}

    # 'Akazamzarak' : {
	# 	'tier': 5,
	# 	'img': './img/hero/akazamzarak.png',
	# 	'archetype': None,
    #     'power': {
    #         'active': True,
    #         'cost': 2,
    #         'do': hero_power_Akazamzarak,
    #         'trigger': None,
    #     },
    #     },
