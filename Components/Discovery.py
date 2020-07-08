"""
The class Discovery manage all cases when a discover action occur and
the display card about minion & buff discover.
It manage:
    -Triple a cards and obtain a card discovery in our hand.
    -Play the discovery card and show the correct minions discover.
    -Play a minion 'primalfinLookout' and discover a specific 'murloc' minion.
    -Play a minion 'megasaur' and discover a specific buff on murloc.
"""
from random import choice

from Components.Minion import Minion
from constants.minions import MINIONS, MINIONS_BY_TIER, MINION_BY_ARCHETYPE, BUFF_MEGASAUR


class Discovery:
    def __init__(self, tier=False, minion=False, hero=False, pool=False, cost=0):
        if tier == 6:
            tier -= 1
        self.tier = tier
        self.minion = minion
        self.hero = hero
        self.pool = pool
        self.cost = cost
        self.cards_discover = []
        self.megasaur = False
    
    def play_discovery(self):
        """
        Gets the correct names of minions or buffs (depends on the specific nature of the discover)
        and choice three randomly name and returns them.
        """
        select = []
        if self.minion and self.minion.name == 'primalfinLookout':
            minions =  MINION_BY_ARCHETYPE[self.minion.archetype].copy()
            
            minions.remove('primalfinLookout')

        elif self.minion and self.minion.name == 'gentleMegasaur':
            minions = list(BUFF_MEGASAUR.keys()).copy()
            self.megasaur = True
        elif self.hero and self.hero == 'Alexstrasza':
            minions = MINION_BY_ARCHETYPE['dragon'].copy()
        else:
            minions = MINIONS_BY_TIER[self.tier].copy()
        for _ in range(3):
            minion = choice(minions)
            minions.remove(minion)
            select.append(minion)
        return select

    def select(self, target):
        if isinstance(target, int):
            minions = self.pool[target-1]
            minions_names = minions.keys()
            minions_values = minions.values()

        elif isinstance(target, str):
            pass

    def display_discovery(self, minions=False):
        """"
        Call the 'play_discovery' method and returns the view of the cards.
        """
        self.cards_discover = minions if minions else self.play_discovery()
        if self.megasaur:
            discover = str(''.join([self.card_megasaur(name) for name in self.cards_discover])).split('\n')[:-1]
        else:
            discover =  str(''.join([str(Minion(name ,False, *[value for value in MINIONS[name].values()][1:])) for name in self.cards_discover])).split('\n')[:-1]
        border = "\n+{}+\n".format('-'*150)
        border_top = "\n+{}+\n".format(" D I S C O V E R Y ".center(150, '-'))
        discover = '\n'.join(["|{}|".format((' '*5).join(discover[i::7]).center(150)) for i in range(7)])
        discover = border_top+discover+border
        return discover

    def card_megasaur(self, name):
        """
        Specific view of megasaur's cards.
        """
        return '(0)-{}-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format(name.center(10, '-'), ' '*14,
            ' '*14, BUFF_MEGASAUR[name]['text'].center(14), ' '*14, ' '*14, '-'*14)

    def __str__(self):
        """
        View of discover card.
        """
        return '({})--Discovery-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format(
            self.cost,' '*14, 'Discover'.center(14), 'a minion'.center(14), 'tier {}'.format(self.tier+1).center(14),
            ' '*14, '-'*14)