import time
from Components.Player import Player

player = Player('yoyo', isHuman=True)
timing = 0 if player.isHuman else int(input('Enter a timing between each action [100-2000]: '))
player.time_by_action = timing/1000
player.shop = player.create_shop(1)

total, force, team = 0, 0, ''
for i in range(1):
    a = time.time()
    player = Player('yoyo', isHuman=False)
    # player.shop = player.create_minions(0, False, 'alleycat', 'alleycat', 'alleycat', 'alleycat')
    player.shop = player.create_shop(1)
    while True:
        print(player) if player.time_by_action else None
        action = player.get_action()
        end = player.make(action)
        if end:
            break
    b = time.time()
    total += b-a
    board_force = player.board_force()
    if board_force > force:
        force = board_force
        team = player.__str__()

print(player)
print(team)
print(force)
# print("average time by run: {}".format(total/1000))
# print(' - - turn {} - -'.format(player.turn))
# print('Total action: {} in {}'.format(player.n_action, round(b-a, 5)))
# print('total buy: {}'.format(player.n_buy))
# print('total play: {}'.format(player.n_play))
# print('total sold: {} '.format(player.n_sold))
# print('total swap: {}'.format(player.n_swap))
# print('total up: {} '.format(player.n_up))
# print('total refresh: {}'.format(player.n_refresh))
# print('total freeze: {}'.format(player.n_freeze))


