import time, copy
from random import choices
from constants.minions import ALL_POOLS, MINIONS
from constants.position import LEN_SHOP


class Pool:
    def __init__(self, archetype):
        self.archetype = archetype
        self.pool = copy.deepcopy(ALL_POOLS[self.archetype])

    def add_to_pool(self, name, tier, gold=False, magnetic=[]):
        if magnetic:
            for minion in magnetic:
                m = 3 if minion.gold else 1
                for _ in range(m):
                    self.pool[minion.lvl-1][minion.name]['copy'] += 1
        if name != 'amalgame':
            n = 3 if gold else 1
            for _ in range(n):
                self.pool[tier-1][name]['copy'] += 1

    def remove_to_pool(self, name, tier):
        # print('remove {}'.format(name))
        # time.sleep(0.5)
        self.pool[tier-1][name]['copy'] -= 1

    def get_minions_pool(self, lvl, aranna, shop, maiev=0):
        minions_names, minions_values = [], []
        length_shop = 7 if aranna else LEN_SHOP[lvl-1]
        if maiev == 2 and length_shop == 6:
            length_shop -= 1
        for minions_pool in self.pool[:lvl]:
            minions_names.extend(minions_pool)
            minions_values.extend(minions_pool.values())

        levels = [d['lvl'] for d in minions_values]
        weights = [d['copy'] for d in minions_values]
        buffs = [0]*len(minions_values)
        return [arr[:] for arr in choices(list(map(list, zip(minions_names, levels, buffs))), weights=weights ,k=length_shop-len(shop))]

    def view_pool_by_tier(self):
        for tier, minions in enumerate(self.pool):
            print('\n')
            print(('tier: ' + str(tier+1)).center(70, '-'))
            for minion in minions:
                print("{} | copy: {} | lvl: {} | archetype: {}".format(minion.rjust(22), minions[minion]['copy'],
                    minions[minion]['lvl'], minions[minion]['archetype']))
            print('-'*70)

    def view_pool_by_archetype(self):
        for archetype in ('murloc', 'pirate', 'beast', 'dragon', 'demon', 'meca','neutral'):
            print('\n')
            print(('archetype: ' + archetype).center(70, '-'))
            for minions in self.pool:
                for minion in minions:
                    if minions[minion]['archetype'] == archetype:
                        print("{} | copy: {:02} | lvl: {} | archetype: {}".format(minion.rjust(22), minions[minion]['copy'],
                        minions[minion]['lvl'], minions[minion]['archetype']))
            print('-'*70)

    def get_difference_pool(self):
        COPIES = [16,15,13,11,9,7]
        res,r = {}, 0
        for pos, minions in enumerate(self.pool):
            for minion in minions:
                diff = minions[minion]['copy'] - COPIES[pos]
                if diff != 0:
                    res[minion] = diff
        return res

    def select_in_pool(self, target, max=1):
        if isinstance(target, int):
            names = [name for name in self.pool[target]]
            copies = [self.pool[target][name]['copy'] for name in self.pool[target]]
            levels = [self.pool[target][name]['lvl'] for name in self.pool[target]]
            buffs = [0] * len(levels)
            return names, copies, levels, buffs

        elif isinstance(target, str):
            names, copies, levels = [], [], []
            if target in ('demon', 'murloc', 'beast', 'meca', 'dragon','pirate'):
                for minions in self.pool[:max]:
                    names += [name for name in minions if minions[name]['archetype'] == target]
                    copies += [minions[name]['copy'] for name in minions if minions[name]['archetype'] == target]
                    levels += [minions[name]['lvl'] for name in minions if minions[name]['archetype'] == target]
                    buffs = [0] * len(levels)
                return names, copies, levels, buffs
            elif target == 'battlecry':
                buffs = []
                for minions in self.pool[:max]:
                    for name in minions:
                        if MINIONS[name]['battlecry']:
                            names.append(name)
                            copies.append(minions[name]['copy'])
                            levels.append(minions[name]['lvl'])
                            buffs.append(0)
                return names, copies, levels, buffs

