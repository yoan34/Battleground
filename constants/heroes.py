"""
A dictionary for have all datas of heroes:
    -name
    -tier
    -img
    -archetype

This file also have all functions used for the hero power
"""
import time
from random import choice, randint

from Components.Minion import Minion
from constants.minions import MINION_BY_ARCHETYPE, MINIONS_BY_TIER, ARCHETYPES

##############################
##### HERO POWER PASSIVE #####
##############################
# HERO PASSIVE 'TURN'
def hero_power_Afk(self):
    if self.turn < 3:
        self.gold = 0
        self.shop.clear()
    elif self.turn == 3:
        for _ in range(2):
            self.hand.append(self.get_discovery(tier=2))

def hero_power_Ysera(self):
    if not self.time_by_action == 0:
        dragons, minions = set(MINION_BY_ARCHETYPE['dragon'].copy()), []
        for tier in range(self.lvl):
            minions.extend(MINIONS_BY_TIER[tier].copy())
        dragon = choice(list(dragons & set(minions)))
        self.shop.append(self.create_minion(False, dragon))

def hero_power_Nozdormu(self):
    if self.first_refresh:
        self.refresh_cost = 0

def hero_power_Sindragosa(self):
    if self.is_freeze:
        for minion in self.shop:
            minion.atk += 1
            minion.hp += 1

def hero_power_Ratking(self, minion=False):
    if not minion:
        if not self.hero.ratking:
            self.hero.ratking = choice(ARCHETYPES)
        else:
            choices = list({*ARCHETYPES} - set([self.hero.ratking]))
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
            discovery = self.get_discovery(hero='Alexstrasza', pool=self.pool)
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
            self.remove_to_pool(new_minion.name, new_minion.lvl)
            self.hand.append(new_minion)
            if new_minion.name in self.double and not new_minion.gold:
                if self.double[new_minion.name] == 2:
                    self.triple_minion(new_minion, is_token=False)
                    self.double.pop(new_minion.name)
                else:
                    self.double[new_minion.name] += 1
            else:
                self.double[new_minion.name] = 1
            self.view_discover = ''

def hero_power_Elise(self):
    self.hand.append(self.get_discovery(tier=self.lvl-1, cost=3))

def hero_power_Vashj(self):
    if not self.time_by_action == 0:
        new_minions = []
        for minion in self.shop:
            lvl = minion.lvl+1
            new_minions.append(self.create_minion(False, choice(MINIONS_BY_TIER[lvl-1])))
        self.shop.clear()
        self.shop = new_minions

# HERO PASSIVE DIRECT IMPACT
def hero_power_Bartendotron(self):
    for i in range(len(self.up_cost[:-1])):
        self.up_cost[i] -= 1

def hero_power_Deathwing(self, minion=False, add=False):
    if not self.time_by_action == 0:
        self.hero.deathwing = True
        if minion:
            minion.atk +=2 if add else -2
        else:
            for minion in self.shop:
                minion.atk += 2

def hero_power_Millificent(self):
    if not self.time_by_action == 0:
        self.hero.millificent = True
        for minion in self.shop:
                if minion.archetype == 'meca':
                    minion.atk += 1
                    minion.hp += 1

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
    amalgame = Minion('amalgame', False, 'amalgame', 1, 1, 1, 'all')
    self.board.append(amalgame)
    self.hero.amalgame = amalgame
    self.double[amalgame.name] = 1

# HERO PASSIVE 'SOLD'
def hero_power_Deryl(self, minion):
    if not self.time_by_action == 0:
        for _ in range(2):
            minion = choice(self.shop)
            minion.atk += 1
            minion.hp += 1

def hero_power_Flurgl(self, minion):
    if not self.time_by_action == 0:
        if len(self.shop) < 7 and minion.archetype == 'murloc':
            murlocs, minions = set(MINION_BY_ARCHETYPE['murloc'].copy()), []
            for tier in range(self.lvl):
                minions.extend(MINIONS_BY_TIER[tier].copy())
            murloc = choice(list(murlocs & set(minions)))
            self.shop.append(self.create_minion(False, murloc))

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
    # add feature for one time by turn
    self.gold -= self.hero.power['cost']
    self.hero.eudora += 1
    if self.hero.eudora == 4:
        self.hero.eudora, names = 0, []
        for lvl in range(self.lvl):
            names.extend(*[MINIONS_BY_TIER[lvl]])
        name = choice(names)
        self.hand.append(self.create_minion(True, name))
    
def hero_power_Hooktusk(self, pos):
    lvl = self.board[pos-1].lvl
    lvl = self.lvl-2 if self.lvl-2 > 0 else 0
    discovery = self.get_discovery(tier=lvl, pool=self.pool)
    if self.is_bot:
        time.sleep(2)
        buff_discovery = self.see_discovery(nature='triplet')
        self.view_discover = discovery.display_discovery(buff_discovery)
    else:
        self.view_discover = discovery.display_discovery()
    self.timing_IA()
    target_discovery = self.get_answer_discovery() if self.is_human else choice([1,2,3])
    new_minion = discovery.cards_discover[target_discovery-1]
    new_minion = self.create_minion(False, new_minion)
    minion = self.board.pop(pos-1)
    if not minion.gold:
        self.double[minion.name] -= 1
        if self.double[minion.name] == 0:
            self.double.pop(minion.name)
    self.hand.append(new_minion)
    if new_minion.name in self.double and not new_minion.gold:
        if self.double[new_minion.name] == 2:
            self.triple_minion(new_minion, is_token=False)
            self.double.pop(new_minion.name)
        else:
            self.double[new_minion.name] += 1
    else:
        self.double[new_minion.name] = 1
    self.view_discover = ''

def hero_power_Rafaam(self):
    pass

def hero_power_Vancleef(self, pos):
    self.board[pos-1].atk += self.buy_in_turn
    self.board[pos-1].hp += self.buy_in_turn

def hero_power_Toki(self):
    if not self.is_bot and not self.time_by_action == 0:
        lvl = self.lvl+1 if self.lvl < 6 else 6
        self.create_shop(self.lvl)
        self.shop = self.shop[:-1]
        minions = MINIONS_BY_TIER[lvl-1]
        self.shop.append(self.create_minion(False, choice(minions)))

def hero_power_Yogg(self):
    if not self.time_by_action == 0:
        if len(self.shop):
            position = randint(1, len(self.shop))
            minion = self.shop.pop(position-1)
            minion.atk += 1
            minion.hp += 1
            self.hand.append(minion)
            if minion.name in self.double:
                if self.double[minion.name] == 2:
                    self.hand.pop(-1)
                    self.triple_minion(minion, False)
                    self.double.pop(minion.name)
                else:
                    self.double[minion.name] += 1
            else:
                self.double[minion.name] = 1

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
    if place == 'board':
        lvl = self.board[pos-1].lvl
        minions = MINIONS_BY_TIER[lvl]
        minion = self.create_minion(False, choice(minions))
        self.board[pos-1] = minion

    elif place == 'shop':
        lvl = self.shop[pos-1].lvl
        minions = MINIONS_BY_TIER[lvl]
        minion = self.create_minion(False, choice(minions))
        self.shop[pos-1] = minion

def hero_power_Reno(self, pos):
    # Dont know if minions keep all buff
    if self.hero.n_power == 1:
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
    pirates, minions = set(MINION_BY_ARCHETYPE['pirate'].copy()), []
    for tier in range(self.lvl):
        minions.extend(MINIONS_BY_TIER[tier].copy())
    name = choice(list(pirates & set(minions)))
    pirate = self.create_minion(False, name)
    self.hand.append(pirate)
    if pirate.name in self.double:
        if self.double[pirate.name] == 2:
            self.triple_minion(pirate, False)
            self.double.pop(pirate.name)
        else:
            self.double[pirate.name] += 1
    else:
        self.double[pirate.name] = 1
    self.hero.power['cost'] = 4
    

def hero_power_Lichking(self, pos):
    self.hero.lichking = self.board[pos-1]
    self.board[pos-1].reborn = True

def hero_power_Wagtoggle(self):
    if self.board:
        for archetype in ARCHETYPES:
            targets = self.board_position_of(archetype)
            if targets:
                target = choice(targets)
                self.board[target-1].atk += 2
            
def hero_power_Nefarian(self):
    pass

def hero_power_Maiev(self, pos=False):
    if not self.time_by_action == 0:
        if pos:
            minion = self.shop.pop(pos-1)
            minion.maiev = 2
            self.hero.maiev.append(minion)
            self.shop = self.hero.maiev + self.shop[len(self.hero.maiev)-1:]
        else:
            for minion in self.hero.maiev:
                minion.maiev -= 1
            position = [pos for pos, m in enumerate(self.hero.maiev) if m.maiev == 0]
            if position:


                minion = self.hero.maiev.pop(position[0])
                self.shop = self.hero.maiev + self.shop[len(self.hero.maiev)+1:]
                minion.atk += 1
                minion.hp += 1
                self.hand.append(minion)

                if minion.name in self.double:
                    if self.double[minion.name] == 2:
                        self.hand.pop(-1)
                        self.triple_minion(minion, False)
                        self.double.pop(minion.name)
                    else:
                        self.double[minion.name] += 1
                else:
                    self.double[minion.name] = 1
        
def hero_power_Galakrond(self, pos):
    if not self.time_by_action == 0:
        lvl = self.shop[pos-1].lvl
        minions = MINIONS_BY_TIER[lvl]
        minion = self.create_minion(False, choice(minions))
        self.shop[pos-1] = minion

def hero_power_Jaraxxus(self):
    targets = self.board_position_of('demon')
    for pos in targets:
        self.board[pos-1].atk += 1
        self.board[pos-1].hp += 1

def hero_power_Akazamzarak(self):
    pass



# TODO Illidian; Finley; Rafaam; Nefarian

HERO_POWER_ACTIVE_SHOP = ('Galakrond', 'Maiev')
HERO_POWER_ACTIVE_BOARD = ('Hooktusk', 'Vancleef', 'George', 'Reno', 'Lichking')
HERO_POWER_ACTIVE_ONLY = ('Rafaam', 'Eudora', 'Toki', 'Lich', 'Jaraxxus', 'Nefarian', 'Patches',
    'Pyramad', 'Wagtoggle', 'Shudderwock', 'Kragg', 'Yogg')

TIER_LIST = {
    'Hooktusk': {
		'tier': 1,
		'img': './img/hero/hooktusk.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 0,
            'do': hero_power_Hooktusk,
            'trigger': None,
            'view': [' del a minion.', ' Discover one', ' of lvl lower'],
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
    'Akazamzarak' : {
		'tier': 5,
		'img': './img/hero/akazamzarak.png',
		'archetype': None,
        'power': {
            'active': True,
            'cost': 2,
            'do': hero_power_Akazamzarak,
            'trigger': None,
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
}