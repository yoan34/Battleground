"""
The class Discovery manage all cases when a discover action occur and
the display card about minion & buff discover.
It manage:
    -Triple a cards and obtain a card discovery in our hand.
    -Play the discovery card and show the correct minions discover.
    -Play a minion 'primalfinLookout' and discover a specific 'murloc' minion.
    -Play a minion 'megasaur' and discover a specific buff on murloc.
"""
from random import choice, choices

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
        
        if self.minion and self.minion.name == 'primalfinLookout':
            names, copies, levels = self.select('murloc')
            if 'primalfinLookout' in names:
                ind = names.index('primalfinLookout')
                names.pop(ind)
                copies.pop(ind)
                levels.pop(ind)
            minions = choices(list(zip(names, levels)), weights=copies, k=3)
            while len(set(minions)) != 3:
                minions = choices(list(zip(names, levels)), weights=copies, k=3)
            return [name for name, pos in minions]

        elif self.minion and self.minion.name == 'gentleMegasaur':
            minions = list(BUFF_MEGASAUR.keys()).copy()
            self.megasaur, select = True, []
            for _ in range(3):
                minion = choice(minions)
                minions.remove(minion)
                select.append(minion)
            return select

        elif self.hero and self.hero == 'Alexstrasza':
            names, copies, levels = self.select('dragon')
            minions = choices(list(zip(names, levels)), weights=copies, k=3)
            while len(set(minions)) != 3:
                minions = choices(list(zip(names, levels)), weights=copies, k=3)
            return [name for name, pos in minions]
        
        elif self.hero and self.hero == 'Hooktusk':
            names, copies, levels = self.select(self.minion.lvl-1)
            if self.minion.name in names:
                ind = names.index(self.minion.name)
                names.pop(ind)
                copies.pop(ind)
                levels.pop(ind)
            minions = choices(list(zip(names, levels)), weights=copies, k=3)
            while len(set(minions)) != 3:
                minions = choices(list(zip(names, levels)), weights=copies, k=3)
            return [name for name, pos in minions]

        else:
            names, copies, levels = self.select(self.tier)
            minions = choices(list(zip(names, levels)), weights=copies, k=3)
            while len(set(minions)) != 3:
                minions = choices(list(zip(names, levels)), weights=copies, k=3)
            return [name for name, pos in minions]
        
    def select(self, target):
        if isinstance(target, int):
            names = [name for name in self.pool[target]]
            copies = [self.pool[target][name]['copy'] for name in self.pool[target]]
            levels = [self.pool[target][name]['lvl'] for name in self.pool[target]]
            return names, copies, levels

        elif isinstance(target, str):
            names, copies, levels = [], [], []
            for minions in self.pool:
                names += [name for name in minions if minions[name]['archetype'] == target]
                copies += [minions[name]['copy'] for name in minions if minions[name]['archetype'] == target]
                levels += [minions[name]['lvl'] for name in minions if minions[name]['archetype'] == target]
            return names, copies, levels

    def display_discovery(self, minions=False):
        """"
        Call the 'play_discovery' method and returns the view of the cards.
        """
        self.cards_discover = minions if minions else self.play_discovery()
        if self.megasaur:
            discover = str(''.join([self.card_megasaur(name) for name in self.cards_discover])).split('\n')[:-1]
        elif minions and isinstance(minions[0], Minion):
            discover =  str(''.join([str(minion) for minion in self.cards_discover])).split('\n')[:-1]
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