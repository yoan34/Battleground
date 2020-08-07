import copy
from random import choice, sample
import time, os

from Components.Minion import Minion
from Components.Discovery import Discovery
from Components.Player import Player
from Components.Battle import Battle
from Components.Pool import Pool

from constants.heroes import HEROES
from constants.minions import ALL_POOLS, ARCHETYPES

class Simulation:

    def __init__(self, data_minions, time_action=0, is_human=False):
        self.data_minions = data_minions
        self.human_player = False
        self.is_human = choice([1,2,3,4,5,6,7,8]) if is_human else False
        self.players = []
        self.players_deads = []
        self.fights = []
        self.turn = 0
        self.mukla = False
        self.time_action = time_action
        self.view_small_players = ''
        self.without_archetype = choice(ARCHETYPES)
        self.pool = Pool(archetype=self.without_archetype)
        self.initialize_players()
        self.initialize_heroes()
    
    def initialize_heroes(self):
        list_heroes = list(copy.copy(HEROES[self.without_archetype]))
        for pos, player in enumerate(self.players):
            sample_heroes = sample(list_heroes, 4)
            if self.is_human and pos+1 == self.is_human:
                name = player.get_answer_hero(sample_heroes, 4)
                hero = sample_heroes[name-1]
            else:
                hero = choice(sample_heroes)
            player.hero = player.create_hero(hero)
            player.create_shop(player.lvl)
            [list_heroes.remove(h) for h in sample_heroes]
        for player in self.players:
            if player.hero.name == 'Illidan':
                player.hero.illidan = True
            player.hero.power['do'](player) if player.hero.power['trigger'] in ('turn', 'now') else None
            player.hero.power['do'](player, list_heroes) if player.hero.power['trigger'] == 'start_game' else None
    
    def initialize_players(self):
        for i in range(8):
            if self.is_human and i+1 == self.is_human:
                name = 'ME!'
                p = Player(name, self.pool, self.without_archetype, is_human=True)
                p.in_simulation = self.view_small_players
                self.human_player = p
                p.time_by_action = 1
            else:
                name = 'IA' + str(i+1)
                p = Player(name, self.pool, self.without_archetype)
                p.time_by_action = self.time_action
            self.players.append(p)

    def play_all_actions_in_a_turn(self):
        self.turn += 1
        is_action_to_do = True
        all_players = [p for p in self.players if p.can_play_action]
        
        self.view_all_players() if self.is_human else None
        print(self.human_player) if self.human_player else None
        while is_action_to_do:
            player = choice(all_players)
            action = player.get_action()
            if action:
                player.make(action)
            if not self.mukla and player.hero.mukla:
                self.mukla, player.hero.mukla = True, False
            all_players = [p for p in self.players if p.can_play_action]
            is_action_to_do = any([p.can_play_action for p in self.players])
            if self.is_human:
                self.human_player.in_simulation = self.view_small_players
            
            if self.time_action:
                self.view_all_players()
                print(player)
                time.sleep(self.time_action)
            # self.review() if self.view else None

        for player in self.players:
            if self.mukla:
                card = '(0)-{}-+\n|{}|\n|{}|\n|{}|\n|{}|\n|{}|\n+{}+\n'.format('Banana'.center(10, '-'), ' '*14,
                ' '*14, 'Give +1/+1'.center(14), ' '*14, ' '*14, '-'*14)
                if len(player.hand) < 10:
                    player.hand.append(card)  
            player.execute_passive_turn('end_turn')
            player.can_play_action = True
        self.mukla = False
        
    def matchmaking(self):
        players_no_match = copy.copy(self.players)
        if len(self.players) % 2 == 0:
            while players_no_match:
                player = choice(players_no_match)
                players_no_match.remove(player)
                enemy = choice(players_no_match)
                players_no_match.remove(enemy)
                player.last_enemies = [copy.copy(m) for m in enemy.board]
                enemy.last_enemies = [copy.copy(m) for m in player.board]
                self.fights.append((player, enemy))
        else:
            kelthuzad = self.players_deads[-1]
            kelthuzad.hp = 0
            kelthuzad.kt = True
            player = choice(players_no_match)
            players_no_match.remove(player)
            player.last_enemies = [copy.copy(m) for m in kelthuzad.board]
            self.fights.append((player, kelthuzad))
            while players_no_match:
                player = choice(players_no_match)
                players_no_match.remove(player)
                enemy = choice(players_no_match)
                players_no_match.remove(enemy)
                player.last_enemies = [copy.copy(m) for m in enemy.board]
                enemy.last_enemies = [copy.copy(m) for m in player.board]
                self.fights.append((player, enemy))

    def run_all_fights(self):
        time = self.time_action
        for p1, p2 in self.fights:
            time = 0.7 if (p1.is_human or p2.is_human) else self.time_action
            if p1.is_human or p2.is_human:
                battle = Battle(p1, p2, t=time, simulation=self.view_small_players) if p1.is_human else Battle(p2, p1, t=time, simulation=self.view_small_players)
            else:
                battle = Battle(p1, p2, t=time, simulation=self.view_small_players)
            res, damage, minion_rafaam, history = battle.fight()
            minion_rafaam = p1.get_minion_enemies(False, minion_rafaam) if minion_rafaam else False
            if minion_rafaam:
                if p1.hero.name == 'Rafaam':
                    p1.hand.append(minion_rafaam)
                    is_token = True if minion_rafaam.name[-2:].upper() == '_T' else False
                    p1.update_doublon_minion(minion_rafaam, token=is_token)
                    p1.hero.rafaam = False
                else:
                    p2.hand.append(minion_rafaam)
                    is_token = True if minion_rafaam.name[-2:].upper() == '_T' else False
                    p2.update_doublon_minion(minion_rafaam, token=is_token)
                    p2.hero.rafaam = False

            if p2.is_human:
                if res == (1,0):
                    p1.hp -= damage
                    if p1.hp <= 0 and not p1.kt:
                        self.players_deads.append(p1)
                        p1.finish = len(self.players)
                else:
                    p2.hp -= damage
                    if p2.hp <= 0 and not p2.kt:
                        self.players_deads.append(p2)
                        p2.finish = len(self.players)
                
            else:
                if res == (1,0):
                    p2.hp -= damage
                    if p2.hp <= 0 and not p2.kt:
                        self.players_deads.append(p2)
                        p2.finish = len(self.players)
                elif res == (0,1):
                    p1.hp -= damage
                    if p1.hp <= 0 and not p1.kt:
                        self.players_deads.append(p1)
                        p1.finish = len(self.players)


        for player in self.players_deads:
            player.hp = 0
            if player in self.players:
                for minion in player.board:
                    if minion.name[-2:].upper() != '_T' and minion.name.lower() != 'amalgame' and minion.name.lower() != 'treasure':
                        player.pool.add_to_pool(minion.name, minion.lvl, minion.gold, minion.minions_magnetic)
                if player.time_by_action == 0:
                    [player.pool.add_to_pool(name, lvl) for name, lvl, buff in player.shop]
                else:
                    [player.pool.add_to_pool(minion.name, minion.lvl) for minion in player.shop]
                for card in player.hand:
                    if (isinstance(card, Minion) and card.name[-2:].upper() != '_T' and card.name.lower() != 'amalgame' and 
                        card.name.lower() != 'treasure'):
                        player.pool.add_to_pool(card.name, card.lvl)
                self.players.remove(player)
        self.fights = []
            
    def next_turn(self):
        for player in self.players:
            player.next_turn()

    def review(self):
        print(self)
        time.sleep(0.1)

    def __str__(self): 
        display = 'No {} this game.\n'.format(self.without_archetype)
        for player in self.players:
            r = ''
            hero_power = 'passive' if not player.hero.power['active'] else 'active'
            can_power = 'Off' if hero_power == 'passive' else 'On' if player.hero.can_power else 'Off'
            r += "{:5} ==> {:13} --- [{}: {}]     gold: {} | lvl: {} | hp: {}\n".format(player.name,player.hero.name, hero_power, can_power,
            player.gold, player.lvl, player.hp)
            r += "shop: {}\n".format(', '.join([m for m,lvl, buff in player.shop]))
            r += "board: {}\n".format(' | '.join(map(str, [(minion.name, minion.atk, minion.hp) for minion in player.board])))
            card_hand = []
            for card in player.hand:
                if isinstance(card, Minion):
                    card_hand.append(card.name)
                elif isinstance(card, Discovery):
                    card_hand.append("discovery {}".format(card.tier+1))
                elif isinstance(card, str):
                    if player.hero.name == 'Mukla':
                        card_hand.append('banana')
                    elif player.hero.name == 'Lich':
                        card_hand.append('Gold lich')
            
            r += "hand: {}\n".format(', '.join([name for name in card_hand]))
            r += '-'*60+'\n'
            display += r
        os.system('cls')
        return display

    def view_all_players(self):
        all_display_alive, all_display_dead, all_display = [], [], []
        for player in self.players:
            l1 = "+{}+".format(player.name.center(12, '-'))
            l2 = "|{}|".format(player.hero.true_name[:10].center(12))
            l3 = "|hp:{:2}  lvl:{}|".format(player.hp, player.lvl)
            l4 = "|type:{:>7}|".format(player.type_board)
            l5 = "+{}+".format('-'*12)
            r = [l1,l2,l3,l4,l5]
            all_display_alive.append(r)
        if self.players_deads:
            for player in self.players_deads:
                l1 = "+{}-{}-+".format(player.name.center(9, '-'), player.finish)
                l2 = "|{}|".format(player.hero.true_name[:10].center(12))
                l3 = "|hp:{:2}  lvl:{}|".format(player.hp, player.lvl)

                l4 = "|type:{:>7}|".format(player.type_board)
                l5 = "+{}+".format('-'*12)
                r = [l1,l2,l3,l4,l5]
                all_display_dead.append(r)
        s_alive = [' '*7, ' '*7, 'ALIVE: ', ' '*7, ' '*7]
        s_dead = [' '*7, ' '*7, ' DEAD: ', ' '*7, ' '*7]
        all_display.append(s_alive)
        all_display += all_display_alive
        all_display.append(s_dead)
        if all_display_dead:
            all_display += all_display_dead[::-1]
        display = ''
        for i in range(5):
            for j in range(len(all_display)):
                display += str(all_display[j][i]) + '  '
            display += '\n'
        os.system('cls')
        self.view_small_players = display
        print(self.view_small_players)


            


