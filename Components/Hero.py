"""
The class allows to create and manage heroes.

"""

class Hero:

    def __init__(self, name, tier, img, archetype, power):
        self.name = name
        self.true_name = name
        self.archetype = archetype
        self.tier = tier
        self.img = img
        self.power = power
        self.can_power = True
        self.n_power = 0
        
        self.deathwing = False
        self.amalgame = False
        self.millificent = False
        self.ratking = ''
        self.aranna = False
        self.mukla = False
        self.eudora = 0
        self.rafaam = False
        self.illidan = False
        self.nefarian = False
        self.lichking = -1
        self.shudderwock = False
        self.maiev = []


        self.play_power = self._play_power if self.power['active'] else None
    
    def _play_power(self, player, *args):
        self.can_power = False
        self.n_power += 1
        player.gold -= self.power['cost']
        self.power['do'](player, *args)
    
    def __str__(self):
        """ Calls and displays the minion's view. """
        dash = '- '*5
        return "{}Avatar: {}{}\n   -name: {}\n   -tier: {}\n   -archetype: {}".format(
            dash, self.name, dash, self.name, self.tier, self.archetype
        )
    
    def display_hero_power(self, player):
        """ Show view hero power """
        display, disable = '', '|'*18
        s_title = 'active' if self.power['active'] else 'passive'
        if self.power['active']:
            title = "+{}({})---+".format(s_title.center(10, '-'), self.power['cost'])
        else:
            title = "+{}+".format(s_title.center(16, '-'))
        body1 = "|{}|".format(' '*16) if self.can_power else disable
        body2 = "|{}|".format(self.power['view'][0].ljust(16)) if self.can_power else disable
        body3 = "|{}|".format(self.power['view'][1].ljust(16)) if self.can_power else disable
        body4 = "|{}|".format(self.power['view'][2].ljust(16)) if self.can_power else disable

            # View of state
        body5 = "|{}|".format(' '*16) if self.can_power else disable
        dict_hero = {
            'Kaelthas': (str(player.n_buy % 3) + ' buys').ljust(14),
            'Vancleef': ('+' + str(player.buy_in_turn)+'/+'+str(player.buy_in_turn)).ljust(14),
            'Eudora': ('dig ' + str(4-self.eudora) + ' again').ljust(14),
            'Kragg': ('gain ' + str(player.turn) + ' golds').ljust(14),
            'Ratking': ('type ' + self.ratking).ljust(14),
            'Aranna': (str(7-player.n_refresh if 7-player.n_refresh >= 0 else 0) + ' again').ljust(14),
        }
        if self.name in dict_hero:
            body6 = "|  {}|".format(dict_hero[self.name]) if self.can_power else disable
        else:
            body6 = "|{}|".format(' '*16) if self.can_power else disable

        foot = "+{}+".format('-'*16)
        display += (title + '\n' + body1 + '\n' + body2 + '\n' + body3 + '\n' + 
            body4 + '\n' + body5 + '\n' + body6 + '\n' + foot + '\n')
        return display

