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

class Minion:

    def __init__(self, name, gold, quick_name, atk, hp, lvl, archetype, legendary=False, img=False, img_d=False, battlecry=False,
        poisonous=False, taunt=False, passive=False,n_passive=0, deathrattle=False, shield=False, reborn=False, magnetic=False,
        overkill=False, cleave=False, windfury=False, morph=0):
        self.name = name
        self.gold = gold
        self.qn = quick_name
        self.atk = atk *2 if self.gold else atk
        self.hp = hp*2 if self.gold else hp
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
        self.deathrattle = deathrattle
        self.shield = shield
        self.reborn = reborn
        self.magnetic = magnetic
        self.overkill = overkill
        self.cleave = cleave
        self.windfury = windfury
        self.maiev = 0
        self.morph = morph
        self.id = id(self)
    
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
        c = "{}{}{}\n".format(shield_l, 'reborn'.center(14,taunt), shield_r) if self.reborn else "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        d = "{}{}{}\n".format(shield_l, 'deathrattle'.center(14,taunt), shield_r) if self.deathrattle else "{}{}{}\n".format(shield_l, ''.center(14,taunt), shield_r)
        if self.poisonous:
            e = "{}{}{}".format(shield_l, "poisonous".center(14,taunt), shield_r) 
        elif self.overkill:
            e = "{}{}{}".format(shield_l, "overkill".center(14,taunt), shield_r)
        else:
            e = "{}{}{}".format(shield_l, ''.center(14,taunt), shield_r)
        display = a + b + c + d + e
        return display

