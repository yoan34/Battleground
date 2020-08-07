import time, os
from random import choice
from Components.Player import Player
from Components.Pool import Pool


a = time.time()
for i in range(1):
    archetype = choice(('beast', 'demon', 'meca', 'dragon','murloc'))
    pool = Pool(archetype=archetype)
    ###### SET UP TEST ######
    for _ in range(1):
        p1 = Player('IA1', pool, archetype, is_human=False)
        p2 = Player('IA2', pool, archetype, is_human=False)
        p3 = Player('IA3', pool, archetype, is_human=False)
        p4 = Player('IA4', pool, archetype, is_human=False)
        p5 = Player('IA5', pool, archetype, is_human=False)
        p6 = Player('IA6', pool, archetype, is_human=False)
        p7 = Player('IA7', pool, archetype, is_human=False)
        p8 = Player('IA8', pool, archetype, is_human=False)
        for player in (p1, p2, p3, p4, p5, p6, p7, p8):
            player.time_by_action = 1 if player.is_human else 0
            player.hero = player.get_hero(archetype)
            player.create_shop(player.lvl)
            player.hero.power['do'](player) if player.hero.power['trigger'] in ('turn', 'now') else None

        while (p1.turn != 14 or p2.turn != 14 or p3.turn != 14 or p4.turn != 14 or p5.turn != 14 or p6.turn != 14 or
            p7.turn != 14 or p8.turn != 14):
                for player in (p1, p2, p3, p4, p5, p6, p7, p8):
                    if player.turn != 14:
                        action = player.get_action()
                        end = player.make(action)
    
r = []
total_zerus = 0
for player in (p1, p2, p3,p4, p5, p6, p7, p8):
    for m in player.shop:
        player.pool.add_to_pool(m[0], m[1])
for player in (p1, p2, p3,p4, p5, p6, p7, p8):
    total_zerus += player.zerus_buy
    r.append(str(player))
for player in r:
    print(player)

b = time.time()
print(pool.get_difference_pool())
print(b-a)
