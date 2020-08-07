
import os
import copy
from random import choice, sample

players = []
players_dead = []
fights = []
class Player:
    def __init__(self, name):
        self.name = name
        self.last_enemies = []
        self.last_enemies_test = []
        self.alive = True

for pos in range(8):
    name = 'IA' + str(pos+1)
    players.append(Player(name))


def matchmaking():
    players_no_matchs = copy.copy(players)
    if len(players) % 2 == 0:
        while players_no_matchs:
            player = choice(players_no_matchs)
            players_no_matchs.remove(player)
            enemy = choice(list(set(players_no_matchs)))
            players_no_matchs.remove(enemy)
            fights.append((player, enemy))

            



    else:
        kt = players_dead[-1]
        player_can_target_kt = []
        for player in players:
            if kt.name not in [p.name for p in player.last_enemies]:
                player_can_target_kt.append(player)
        fights.append((choice(player_can_target_kt), kt))
        players_no_matchs.remove(player)
        while players_no_matchs:
            player = choice(players_no_matchs)
            players_no_matchs.remove(player)
            choice_enemy = choice(list(set(players_no_matchs) - set(player.last_enemies)))
            player.last_enemies.append(choice_enemy)
            if len(player.last_enemies) > 2:
                    player.last_enemies.pop(0)
            fights.append((player.name, choice_enemy.name))
            players_no_matchs.remove(choice_enemy)
    
    
    

# choisi un adversaire
# regarde si en prennant cette adversaire, tous le monde a un adversaire
# sinon je choisi un autre adversaire



if __name__ == '__main__':
    while len(players) > 1:
        matchmaking()
        for player in players:
            print("{} - last enemies: ({}).".format(player.name, ", ".join([p.name for p in player.last_enemies])))
        print('fights: ',fights)
        fights = []
        x=input('x')

    os.system('pause')

