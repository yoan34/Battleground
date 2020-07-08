import time, os
from Components.Player import Player
from constants.minions import MINIONS_POOL



# player = Player('yoyo', pool, is_human=False)

# player.is_bot = False
# player.lvl = 6
# player.hero = player.get_hero()


# a = time.time()

# for _ in range(100000):
    
#     # if not player.is_bot:
#     #     timing = 0 if player.is_human else int(input('Enter a timing between each action [100-2000]: '))
#     # player.display_pool()
#     player.create_shop(player.lvl)
#     # print('\n\n')
#     # player.display_pool()
# b = time.time()
# print(player.shop)
# print(player.display_pool())

# print(b-a)



a = time.time()
for i in range(1):
    ###### SET UP TEST ######
    pool = MINIONS_POOL.copy()
    pool[2]['shifterZerus']['copy'] = 5000
    player = Player('IA', pool, is_human=True)
    player.debug = False
    player.time_by_action = 1 if player.is_human else 0
    player.hero = player.create_hero('George')
    player.lvl = 3
    player.gold = 10
    print(i, '' ,player.hero.name)
    player.create_shop(player.lvl)
    player.hero.power['do'](player) if player.hero.power['trigger'] in ('turn', 'now') else None

    
    ##### MODE HUMAN #####
    # player.shop = player.create_minions(0, False, 'alleycat', 'zoobot', 'zoobot', 'zoobot', 'zoobot', 'zoobot')
    # player.board.extend(player.create_minions(0,True, 'brannBronzebeard'))
    # player.brann = 1
    # player.n_brann = 1
    # player.n_khadgar = 2
    # player.n_g_khadgar = 1
    # player.gold = 99

    ###### MODE IA ######
    
    ########################
    while True:
        # player.history.append(str(player))
        print(player) if player.time_by_action else None
        
        action = player.get_action()
        end = player.make(action)

        if end:
            break
    

print('\n\n'+str(player)) if not player.is_human else None

b = time.time()
print(player.n_action)
print(b-a)



# 1-t-t-t-t-t