
from random import choice
from Components.Minion import Minion
from constants.minions import MINIONS, MINIONS_BY_TIER, MINION_BY_ARCHETYPE, BUFF_MEGASAUR


class Discovery:
    def __init__(self, tier=False, minion=False, isHuman=False):
        if tier == 6:
            tier -= 1
        self.tier = tier
        self.minion = minion
        self.isHuman = isHuman
        self.cards_discover = []
        self.megasaur = False
    
    def play_discovery(self):
        select = []
        if self.minion and self.minion.name == 'primalfinLookout':
            minions =  MINION_BY_ARCHETYPE[self.minion.archetype].copy()
            minions.remove('primalfinLookout')

        elif self.minion and self.minion.name == 'gentleMegasaur':
            minions = list(BUFF_MEGASAUR.keys()).copy()
            self.megasaur = True
        else:
            minions = MINIONS_BY_TIER[self.tier].copy()
        for _ in range(3):
            minion = choice(minions)
            minions.remove(minion)
            select.append(minion)
        self.cards_discover = select

    def display_discovery(self):
        self.play_discovery()
        if self.megasaur:
            discover = str(''.join([self.card_megasaur(name) for name in self.cards_discover])).split('\n')[:-1]
        elif not self.isHuman:
            discover =  str(''.join([str(Minion(name ,False, *[value for value in MINIONS[name].values()][1:])) for name in self.cards_discover])).split('\n')[:-1]
        else:
            discover =  str(''.join([str(Minion(name ,False, *[value for value in MINIONS[name].values()][1:])) for name in self.cards_discover])).split('\n')[:-1]
        border = "\n+{}+\n".format('-'*150)
        border_top = "\n+{}+\n".format(" D I S C O V E R Y ".center(150, '-'))
        discover = '\n'.join(["|{}|".format((' '*5).join(discover[i::7]).center(150)) for i in range(7)])
        discover = border_top+discover+border
        return discover

    def card_megasaur(self, name):
        return '(0)-{}-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format(name.center(10, '-'), ' '*14, ' '*14, BUFF_MEGASAUR[name].center(14), ' '*14, ' '*14, '-'*14)

    def __str__(self):
        return '(0)--Discovery-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format(
            ' '*14, 'Discover'.center(14), 'a minion'.center(14), 'tier {}'.format(self.tier+1).center(14),
            ' '*14, '-'*14)