"""
The class allows to create and manage minions.
Minions has a lot of properties like:
    -name         -img
    -gold         -taunt
    -atk          -passive
    -hp           -battlecry
    -lvl          -shield
    -archetype    -taunt
    and so on...

For now methods are only usefull for display the minion.
"""
import os, copy
from random import randint, choice
import time

class Minion:

    def __init__(self, name, gold, quick_name, atk, hp, lvl, archetype, legendary=False, img=False, img_d=False, battlecry=False,
        poisonous=False, taunt=False, passive=False,n_passive=0, deathrattle=[], fight={'do': [], 'trigger': ''}, shield=False,
        reborn=False, magnetic=False, overkill=False, cleave=False, windfury=False, morph=0, max_hp=0, max_atk=0):
        self.name = name
        self.gold = gold
        self.qn = quick_name
        self.atk = atk *2 if self.gold else atk
        self.max_atk = atk*2 if self.gold else atk
        self.hp = hp*2 if self.gold else hp
        self.max_hp = hp*2 if self.gold else hp
        self.lvl = lvl
        self.archetype = archetype
        self.legendary = legendary
        self.img = img
        self.img_d = img_d
        self.battlecry = battlecry
        self.poisonous = poisonous
        self.taunt = taunt
        self.passive = passive
        self.n_passive = n_passive
        self.deathrattle = deathrattle[:]
        self.play_deathrattle = self._play_deathrattle if self.deathrattle else None
        self.fight = fight
        self.shield = shield
        self.reborn = reborn
        self.magnetic = magnetic
        self.minions_magnetic = []
        self.overkill = overkill
        self.cleave = cleave
        self.windfury = windfury
        self.maiev = 0
        self.morph = morph
        self.dead = False
        self.attackers = False
        self.id = id(self)
    
    def _play_deathrattle(self, battlefield, pos, friends, enemies, f_values, e_values):
        pos_token, n = 0, 0
        for position, deathrattle in enumerate(self.deathrattle):
            if position > 0 and self.minions_magnetic:
                n = deathrattle(battlefield, self.minions_magnetic[position-1], pos+1+pos_token, friends, enemies, f_values, e_values)
                pos_token += 3
            else:
                n = deathrattle(battlefield, self, pos, friends, enemies, f_values, e_values)
        return n

    def is_dead(self):
        return True if self.hp < 1 else False

    def has_deathrattle(self):
        return True if self.play_deathrattle else False

    def board_position_of(self, team=[], target='all', minion=False):
        """
        Return all positions of a minions that match a specific value.
        Example: we want to know the positions of all murloc in the board.
        we tape target='murloc' and minion parameter allow us to delete the position of the
        current minion we plays.
        """
        if target in ('dragon', 'beast', 'murloc', 'demon', 'pirate', 'meca'):
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

    def add_magnetic(self, minion):
        minion.atk += self.atk
        minion.hp += self.hp
        minion.shield = True if self.shield else False
        minion.taunt = True if self.taunt else False
        minion.minions_magnetic.append(self)
        if self.deathrattle:
            minion.deathrattle.append(self.deathrattle[0]) if self.deathrattle else None
        

    def __str__(self):
        """ Calls and displays the minion's view. """
        dash = '-'*3
        sep_down = 12 - (len(str(self.atk))+len(str(self.hp)))
        name = self.qn[:12].center(12,'-')
        name  = name.upper() if self.gold else name
        return "({}){}+\n{}\n({}){}({})\n".format(self.lvl, name,
        self.display_effect(), self.atk, self.archetype.center(sep_down, '-'), self.hp)
    
    def display_effect(self):
        """
        Translates the minion's properties into a view.
        """
        display = ''
        taunt = '-' if self.taunt else ' '
        shield_l = '(' if self.shield else '|'
        shield_r = ')' if self.shield else '|' 
        a = "{}{}{}\n".format(shield_l, 'battlecry'.center(14,taunt), shield_r) if self.battlecry else "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        b = "{}{}{}\n".format(shield_l, 'passive'.center(14,taunt), shield_r) if self.passive else "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        if self.windfury:
            c = "{}{}{}\n".format(shield_l, 'windfury'.center(14,taunt), shield_r)
        elif self.reborn:
            c = "{}{}{}\n".format(shield_l, 'reborn'.center(14,taunt), shield_r)
        else:
            c = "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        d = "{}{}{}\n".format(shield_l, 'deathrattle'.center(14,taunt), shield_r) if self.deathrattle else "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        if self.poisonous:
            e = "{}{}{}".format(shield_l, "poisonous".center(14,taunt), shield_r) 
        elif self.overkill:
            e = "{}{}{}".format(shield_l, "overkill".center(14,taunt), shield_r)
        else:
            e = "{}{}{}".format(shield_l, ''.center(14,taunt), shield_r)
        display = a + b + c + d + e
        return display








