

import copy, time, os
from random import choice, randint

from Components.Game import Game
from Components.Minion import Minion

class Battle(Game):
    def __init__(self, p1, p2, t=0, h=False, simulation=False):
        self.t = t
        self.simulation = simulation
        self.no_archetype = p1.no_archetype
        self.winner = False
        self.p1_name = p1.name
        self.p2_name = p2.name
        self.p1_lvl = p1.lvl
        self.p2_lvl = p2.lvl
        self.p1_hero = p1.hero.name
        self.p2_hero = p2.hero.name
        self.p1_hero_true_name = p1.hero.true_name
        self.p2_hero_true_name = p2.hero.true_name
        self.p1 = [copy.copy(minion) for minion in p1.board]
        
        self.p2 = [copy.copy(minion) for minion in p2.board]
        self.deathwing = True if (p1.hero.name == 'Deathwing') or (p2.hero.name == 'Deathwing') else False
        self.rafaam_add = False
        if p1.hero.rafaam:
            self.rafaam = 'p1'
        elif p2.hero.rafaam:
            self.rafaam = 'p2'
        else:
            self.rafaam = False
        if p1.hero.nefarian:
            self.nefarian = ('nefarian','p1')
        elif p2.hero.nefarian:
            self.nefarian = ('nefarian','p2')
        else:
            self.nefarian = False
        if p1.hero.illidan:
            self.illidan = 'p1'
        elif p2.hero.illidan:
            self.illidan = 'p2'
        else:
            self.illidan = False
        self.attackers = False
        self.minion_atk = False
        self.pos_def = 0
        self.pos_atk = 0
        self.next_friend = 0
        self.next_enemy = 0
        self.deathrattles = []
        self.add_dead = 1
        self.add_enemy_dead = 0
        self.add_friend_dead = 0
        self.aoe_ghoul = False
        self.scally_dead = 0
        self.minion_deal_dmg = False
        
        self.next1 = 0
        self.p1_deathrattle = []
        self.p1_pos_deathrattle = 0
        self.count_dead_p1 = 0
        self.stuff1 = {
            'khadgar': 0, 'khadgar_golden': 0, 'baronRivendare': 1, 'dreadAdmiralEliza': 0, 'ripsnarlCaptain': 0, 'waxriderTogwaggle': 0,
            'scavengingHyena': 0, 'soulJunggler': 0, 'junkbot': 0, 'drakonidEnforcer': 0, 'bolvarFireblood': 0,
            'impMama': 0, 'securityRover': 0, 'impGangBoss': 0, 'mamaBear': 0, 'packLeader': 0, 'deflectOBot': 0,
            'ghastcoiler': 0,'kangorsApprentice': 0, 'arcaneCannon': 0 }
        self.first1_meca_die = []

        self.next2 = 0
        self.p2_deathrattle = []
        self.p2_pos_deathrattle = 0
        self.count_dead_p2 = 0
        self.stuff2 = {
            'khadgar': 0, 'khadgar_golden': 0, 'baronRivendare': 1, 'dreadAdmiralEliza': 0, 'ripsnarlCaptain': 0, 'waxriderTogwaggle': 0,
            'scavengingHyena': 0, 'soulJunggler': 0, 'junkbot': 0, 'drakonidEnforcer': 0, 'bolvarFireblood': 0,
            'impMama': 0, 'securityRover': 0, 'impGangBoss': 0, 'mamaBear': 0, 'packLeader': 0, 'deflectOBot': 0,
            'ghastcoiler': 0, 'kangorsApprentice': 0, 'arcaneCannon': 0}
        self.first2_meca_die = []
        

        self.view_targets = False
        self.h = h
        self.history = []
        self.game_block = False


        self.update_state()

    def fight(self):
        if not self.illidan:
            if len(self.p1) > len(self.p2):
                team, self.attackers = self.p1, 'p1'
            elif len(self.p1) < len(self.p2):
                team, self.attackers = self.p2, 'p2'
            else:
                team = choice((self.p1, self.p2))
                self.attackers = 'p1' if team == self.p1 else 'p2'
        else:
            (team, self.attackers, self.illidan) = (self.p1, 'p1', 2) if self.illidan == 'p1' else (self.p2, 'p2', 2)

        self.manage_view()
        self.start_of_fight()

        while len(self.p1) and len(self.p2):
            if self.is_game_block():break
            if team == self.p1:
                team = self.minion_attacks(self.p1, self.next1, self.stuff1, self.p1_deathrattle, self.p2, self.next2, self.stuff2, self.p2_deathrattle)
                self.attackers = 'p2' if self.illidan == 0 else 'p1'
            else:
                team = self.minion_attacks(self.p2, self.next2, self.stuff2, self.p2_deathrattle, self.p1, self.next1, self.stuff1, self.p1_deathrattle)
                self.attackers = 'p1' if self.illidan == 0 else 'p2'

        if not self.game_block:
            if len(self.p1) > len(self.p2):
                damage = sum([minion.lvl for minion in self.p1]) + self.p1_lvl
                self.winner, res = '{} win !'.format(self.p1_hero_true_name), (1,0)
            elif len(self.p1) < len(self.p2):
                damage = sum([minion.lvl for minion in self.p2]) + self.p2_lvl
                self.winner, res = '{} win !'.format(self.p2_hero_true_name), (0,1)
            else:
                damage = 0
                self.winner, res = 'tie ...', (0,0)
        else:
            damage = 0
            self.winner, res = 'minions are present but Tie...', (0,0)
        

        self.manage_view()
        if self.h:
            return res, damage, self.rafaam_add, self.history
        else:
            return res, damage, self.rafaam_add, False

    ## PASSIVE FIGHT ##
    def passive_attack(self, friend, friends, enemies):
        values = self.stuff1 if self.attackers == 'p1' else self.stuff2
        if (values['dreadAdmiralEliza'] or values['ripsnarlCaptain']) and friend.archetype == 'pirate':
            [minion.fight['do'](friend, friends) for minion in friends if minion.fight['trigger'] == 'friendly_pirate_atk']

    def passive_macaw(self, friend, friends, friends_values, enemies):
        if friend.fight['trigger'] == 'after_attacks':
            friend.fight['do'](self, friend, friends, enemies)

    def start_of_fight(self):
        all_sof = []
        n_sof_p1 = [(minion, 'p1') for minion in self.p1 if minion.fight['trigger'] == 'start_of_fight']
        n_sof_p2 = [(minion, 'p2') for minion in self.p2 if minion.fight['trigger'] == 'start_of_fight']
        if len(n_sof_p1) > len(n_sof_p2):
            for i in range(len(n_sof_p1)):
                all_sof.append(n_sof_p1[0])
                if n_sof_p2:
                    all_sof.append(n_sof_p2[0])
                    n_sof_p2 = n_sof_p2[1:]
                n_sof_p1 = n_sof_p1[1:]
        elif len(n_sof_p1) < len(n_sof_p2):
            for i in range(len(n_sof_p2)):
                all_sof.append(n_sof_p2[0])
                if n_sof_p1:
                    all_sof.append(n_sof_p1[0])
                    n_sof_p1 = n_sof_p1[1:]
                n_sof_p2 = n_sof_p2[1:]
        else:
            c = choice(('p1','p2'))
            if c == 'p1':
                for i in range(len(n_sof_p1)):
                    all_sof.append(n_sof_p1[0])
                    all_sof.append(n_sof_p2[0])
                    n_sof_p2 = n_sof_p2[1:]
                    n_sof_p1 = n_sof_p1[1:]
            else:
                for i in range(len(n_sof_p2)):
                    all_sof.append(n_sof_p2[0])
                    all_sof.append(n_sof_p1[0])
                    n_sof_p1 = n_sof_p1[1:]
                    n_sof_p2 = n_sof_p2[1:]
        
        all_sof.append(self.nefarian) if self.nefarian else None
        for minion, team in all_sof:
            if minion == 'nefarian' or minion.hp > 0:
                if team == 'p1':
                    friends, enemies, values_friends, values_enemies = self.p1, self.p2, self.stuff1, self.stuff2
                    friends_deathrattle, enemies_deathrattle = self.p1_deathrattle, self.p2_deathrattle
                else:
                    friends, enemies, values_friends, values_enemies = self.p2, self.p1, self.stuff2, self.stuff1
                    friends_deathrattle, enemies_deathrattle = self.p2_deathrattle, self.p1_deathrattle
                
                if minion == 'nefarian':
                    self.play_nefarian(enemies, values_enemies)
                else:
                    minion.fight['do'](self, minion, friends, values_friends, enemies, values_enemies)

                friends_dead, enemies_dead = self.manage_cycle_fight(friends, values_friends, friends_deathrattle, enemies, values_enemies, enemies_deathrattle)

                self.manage_enemies_reborn(friends, friends_dead) 
                self.manage_enemies_reborn(enemies, enemies_dead)
                self.add_dead = 1
                self.p1_deathrattle, self.p2_deathrattle, self.p1_pos_deathrattle, self.p2_pos_deathrattle = [], [], 0, 0           

    def manage_kangor(self, minion, friends):
        values = self.stuff1 if friends == self.p1 else self.stuff2
        add_list_kangor = self.first1_meca_die if friends == self.p1 else self.first2_meca_die
        if len(add_list_kangor) < 4:
            if minion.archetype == 'meca' and (values['kangorsApprentice'] or values['ghastcoiler']):
                if minion.name[-2:].upper() == '_T':
                    minion.name == minion.name[:-2]
                    add_list_kangor.append((minion, minion.gold, True, minion.atk, minion.max_hp))
                else:
                    add_list_kangor.append((minion.name, minion.gold, False, minion.atk, minion.max_hp))

    def play_nefarian(self, enemies, values_enemies):
        for pos, enemy in enumerate(enemies):
            self.deal_damage(1, enemy, pos, enemies, values_enemies)
            if enemy.hp <= 0:
                self.add_enemy_dead += 1
                self.add_dead += 1
        self.manage_view(show_targets=False)

    def passive_dragon_kill(self, enemy, friends, values_friends):
        if enemy.hp <= 0 and values_friends['waxriderTogwaggle']:
            [f.fight['do'](f) for f in friends if f.name == 'waxriderTogwaggle']

    def passive_dead(self, minion, minions, values):
        # we call this function after remove the minion
        if minion.fight['trigger'] == 'present':
            minion.fight['do'](minion, minions)
        if minion.archetype == 'meca' and values['junkbot']:
            for m in minions:
                if m.name == 'junkbot':
                    m.fight['do'](m)
        elif minion.archetype == 'beast' and values['scavengingHyena']:
            for m in minions:
                if m.name == 'scavengingHyena':
                    m.fight['do'](m)

    def passive_summon(self, token, friends, values):
        if (values['mamaBear'] or values['packLeader']) and token.archetype == 'beast':
            for minion in friends:
                if minion.id != token.id and (minion.name == 'mamaBear' or minion.name == 'packLeader'):
                    minion.fight['do'](minion, token)
        if values['deflectOBot'] and token.archetype == 'meca':
            for minion in friends:
                if minion.id != token.id and minion.name == 'deflectOBot':
                    minion.fight['do'](minion)

    def passive_cannon(self, friends, pos, enemy, enemies, values_enemies):
        if pos > 0 and friends[pos-1].name == 'arcaneCannon':
            cannon = friends[pos-1]
            cannon.fight['do'](self, cannon, enemy, enemies, values_enemies)
        if pos < len(friends)-1 and friends[pos+1].name == 'arcaneCannon':
            cannon = friends[pos+1]
            cannon.fight['do'](self, cannon, enemy, enemies, values_enemies)

    def update_state(self):
        # set up warlerder and check baron et other
        # maybe have to put some state for minions that trigger when other minions
        # do something, so we don't have to search every time, just check if we have to searh.
        # this technique work for:
        # - friendly_die (hyena, jungler, junkbot)
        # - dragon_kill_enemy (warider)
        # - friendly_pirate_atk (ripsnarl, eliza)
        # - friendly_lose_shield (not necessary)
        for minions, hero in ((self.p1, self.p1_hero), (self.p2,self.p2_hero)):
            values = self.stuff1 if minions == self.p1 else self.stuff2
            for minion in minions:
                minion.atk += 2 if (hero != 'Deathwing' and self.deathwing) else 0
                if minion.name == 'khadgar':
                    values['khadgar'] += 1 if not minion.gold else 0
                    values['khadgar_golden'] += 1 if minion.gold else 0
                if minion.name == 'baronRivendare': values['baronRivendare'] = 2 if not minion.gold else 3
                if minion.name == 'dreadAdmiralEliza': values['dreadAdmiralEliza'] += 1
                if minion.name == 'ripsnarlCaptain': values['ripsnarlCaptain'] += 1
                if minion.name == 'waxriderTogwaggle': values['waxriderTogwaggle'] += 1
                if minion.name == 'junkbot': values['junkbot'] += 1
                if minion.name == 'drakonidEnforcer': values['drakonidEnforcer'] += 1
                if minion.name == 'bolvarFireblood': values['bolvarFireblood'] += 1
                if minion.name == 'impMama': values['impMama'] += 1
                if minion.name == 'securityRover': values['securityRover'] += 1
                if minion.name == 'impGangBoss': values['impGangBoss'] += 1
                if minion.name == 'scavengingHyena': values['scavengingHyena'] += 1
                if minion.name == 'soulJunggler': values['soulJunggler'] += 1
                if minion.name == 'deflectOBot': values['deflectOBot'] += 1
                if minion.name == 'packLeader': values['packLeader'] += 1
                if minion.name == 'mamaBear': values['mamaBear'] += 1
                if minion.name == 'kangorsApprentice': values['kangorsApprentice'] += 1
                if minion.name == 'ghastcoiler': values['ghastcoiler'] += 1
                if minion.name == 'arcaneCannon': values['arcaneCannon'] += 1

                # just for test
                # if minion.name == 'murlocWarleader':
                #     minion.fight['do'](minion, minions, repop=True)
                # if minion.name == 'southseaCaptain':
                #     minion.fight['do'](minion, minions, repop=True)
                # if minion.name == 'siegeBreaker':
                #     minion.fight['do'](minion, minions, repop=True)
                # if minion.name == 'malGanis':
                #     minion.fight['do'](minion, minions, repop=True)

    def update_state_dead(self, friends, friend, values):
        name = friend.name
        if name == 'khadgar' and friend.gold:
            name += '_golden'
        if name == 'baronRivendare':
            values[name] = 1
            for minion in friends:
                if minion.name == 'baronRivendare':
                    if minion.gold:
                        values[name] = 3
                        break
                    else:
                        values[name] = 2
        elif name in values:
            if not values[name] == 0:
                values[name] -= 1

    def minion_attacks(self, friends, next_friend, values_friends, friends_deathrattle, enemies, next_enemy, values_enemies, enemies_deathrattle):
        self.next_friend, self.next_enemy = next_friend, next_enemy
        self.pos_atk = self.next_friend
        friend = friends[self.pos_atk]
        if self.illidan == 1:
            self.pos_atk = len(friends)-1
            friend = friends[self.pos_atk]
        while (friend.atk == 0 or friend.name == 'arcaneCannon') and not self.illidan:
            any_atk = [True for friend in friends if (friend.atk > 0 and friend.name != 'arcaneCannon')]
            if not any_atk:
                return enemies
            self.pos_atk += 1
            if self.pos_atk == len(friends):
                self.pos_atk = 0
            friend = friends[self.pos_atk]
        self.next_friend = self.pos_atk
        self.minion_deal_dmg = friend

        n = 2 if friend.windfury else 1

        for i in range(n):
            enemy = self.target_enemy(enemies)
            target = self.passive_attack(friend, friends, enemies)
            if target is not None: enemy = target

            self.manage_view()
            
            # red whelp

            #put manage shield and wound enemy directly in 'attacks' feature
            self.attacks(friend, self.pos_atk, friends, values_friends, enemy, self.pos_def, enemies, values_enemies, friend.cleave)
            self.passive_macaw(friend, friends, values_friends, enemies)
            self.passive_dragon_kill(enemy, friends, values_friends) if friend.archetype == 'dragon' else None
            self.passive_dragon_kill(friend, enemies, values_enemies) if enemy.archetype == 'dragon' else None
            # yo ogre is wound and survive, so trigger his passive attacks

            if self.minion_deal_dmg.overkill:
                if enemies[self.pos_def].hp < 0:
                    if self.minion_deal_dmg.name == 'heraldOfFlame':
                        self.minion_deal_dmg.overkill(self, self.minion_deal_dmg, friends, enemy, enemies, values_enemies, values_friends)
                    else:
                        self.minion_deal_dmg.overkill(self, self.minion_deal_dmg, enemy, friends, enemies, values_friends)

            if values_friends['arcaneCannon']:
                self.passive_cannon(friends, self.pos_atk, enemy, enemies, values_enemies)

            self.manage_view()
        
            if not friend.is_dead():
                self.next_friend += 1 if i == 0 else 0
                self.next_friend = 0 if self.next_friend == len(friends) else self.next_friend

            friends_dead, enemies_dead = self.manage_cycle_fight(friends, values_friends, friends_deathrattle, enemies, values_enemies, enemies_deathrattle)

            self.manage_enemies_reborn(friends, friends_dead) 
            self.manage_enemies_reborn(enemies, enemies_dead)

            if friend.is_dead() and i == 0: break
            if not enemies: break

        # self.manage_view()
        self.add_dead = 1
        self.p1_deathrattle, self.p2_deathrattle, self.p1_pos_deathrattle, self.p2_pos_deathrattle = [], [], 0, 0
        if friends == self.p1:
            self.next1, self.next2 = self.next_friend, self.next_enemy
        else:
            self.next1, self.next2 = self.next_enemy, self.next_friend
        if self.illidan:
            self.illidan -= 1
            if self.illidan:
                return friends
        return enemies

    def manage_cycle_fight(self, friends, values_friends, friends_deathrattle, enemies, values_enemies, enemies_deathrattle):
        trigger, pos_trigger = False, -1
        friends_dead, enemies_dead = [], []
        while self.add_dead:
            while self.add_dead:
                #manage ghoul, if AOE ghoul and jungler dead, no trigger
                self.add_dead = 0
                self.manage_soul_junggler(friends, enemies, values_friends, values_enemies)
                self.manage_soul_junggler(enemies, friends, values_enemies, values_friends)

                    
            friends_dead, self.next_friend = self.get_minions_dead(friends, enemies, values_friends, self.next_friend, friends_deathrattle)
            enemies_dead, self.next_enemy = self.get_minions_dead(enemies, friends, values_enemies, self.next_enemy, enemies_deathrattle)
                    
            self.aoe_ghoul = False
            if not trigger:
                if friends_deathrattle or enemies_deathrattle:
                    if friends_deathrattle and enemies_deathrattle:
                        trigger = choice((['friends', 'enemies'],['enemies', 'friends']))
                    elif friends_deathrattle or enemies_deathrattle:
                        trigger = ['friends'] if friends_deathrattle else ['enemies']
                else:
                    trigger = []
            else:
                        
                        
                if len(trigger) == 2:
                    if pos_trigger == 0:
                        if self.add_enemy_dead:
                            if self.add_friend_dead:
                                trigger = ['friends', 'enemies'] if trigger == ['enemies', 'friends'] else ['enemies', 'friends']
                                self.add_enemy_dead = self.add_friend_dead = 0
                            else:
                                trigger = ['friends'] if trigger == ['enemies', 'friends'] else ['enemies']
                                self.add_enemy_dead = 0
                        else:
                            trigger = ['enemies', 'friends'] if trigger == ['friends', 'enemies'] else ['friends', 'enemies']
                            self.add_friend_dead = 0

                    else:
                        if self.add_enemy_dead:
                            if self.add_friend_dead:
                                trigger = ['friends', 'enemies'] if trigger == ['friends', 'enemies'] else ['enemies', 'friends']
                                self.add_enemy_dead = self.add_friend_dead = 0
                            else:
                                trigger = ['friends'] if trigger == ['friends', 'enemies'] else ['enemies']
                                self.add_enemy_dead = 0
                        else:
                            trigger = ['enemies'] if trigger == ['friends', 'enemies'] else ['friends']
                            self.add_enemy_dead = 0
                else:
                            
                    if self.add_enemy_dead:
                        if self.add_friend_dead:
                            trigger = ['friends', 'enemies'] if trigger == ['enemies'] else ['enemies', 'friends']
                            self.add_friend_dead = self.add_enemy_dead = 0
                        else:
                            trigger = ['friends'] if trigger == ['enemies'] else ['enemies']
                            self.add_enemy_dead = 0
                    else:
                        self.add_friend_dead = 0

            dd = {
                'friends': self.manage_deathrattle(friends, values_friends, enemies, values_enemies, friends_deathrattle, self.next_friend),
                'enemies': self.manage_deathrattle(enemies, values_enemies, friends, values_friends, enemies_deathrattle, self.next_enemy)
                }

            for pos, team in enumerate(trigger):
                if team == 'friends':
                    self.next_friend = dd[team]
                else:
                    self.next_enemy = dd[team]  
                pos_trigger = pos
                if self.add_dead: break
                    

        return friends_dead, enemies_dead

    def attacks(self, friend, pos_friend, friends, v_friends, enemy, pos_enemy, enemies, v_enemies, cleave=False, deathrattle=False):
        if not cleave:
            self.manage_minions(friend, pos_friend, friends, v_friends, enemy, pos_enemy, enemies, v_enemies)
        else:
            minions = []
            if pos_enemy != 0:
                minions.append((enemies[pos_enemy-1], pos_enemy-1, False))
                minions.append((enemies[pos_enemy], pos_enemy, True))
                if pos_enemy+1 < len(enemies):
                    minions.append((enemies[pos_enemy+1], pos_enemy+1, False))
            else:
                minions.append((enemies[pos_enemy], pos_enemy, True))
                if pos_enemy+1 < len(enemies):
                    minions.append((enemies[pos_enemy+1], pos_enemy+1, False))
            
            for enemy, pos_enemy, front in minions:
                if front:
                    self.manage_minions(friend, pos_friend, friends, v_friends, enemy, pos_enemy, enemies, v_enemies)
                else:
                    if enemy.shield:
                        enemy.shield = False
                        self.manage_shield(enemies, v_enemies)
                    else:
                        enemy.hp = (enemy.hp-friend.atk) if not friend.poisonous else 0
                        self.manage_wound(enemy, pos_enemy, enemies, v_enemies)
        
    def deal_damage(self, damage, enemy, pos_enemy, enemies, v_enemies):
        if enemy.shield:
            enemy.shield = False
            self.manage_shield(enemies, v_enemies)
        else:
            enemy.hp -= damage
            self.manage_wound(enemy, pos_enemy, enemies, v_enemies)
        
    def manage_shield(self, team, values_team):
        if values_team['drakonidEnforcer'] or values_team['bolvarFireblood']:
            for minion in team:
                if minion.fight['trigger'] == 'friendly_lose_shield':
                    minion.fight['do'](minion)

    def manage_wound(self, minion, pos, team, values_team):
        if minion.fight['trigger'] == 'wound':
            minion.fight['do'](self, minion, pos, team, values_team)

    def manage_minions(self, friend, pos_friend, friends, v_friends, enemy, pos_enemy, enemies, v_enemies):
        manage_enemy_shield = manage_enemy_wound = False
        if enemy.shield:
            enemy.shield = False
            manage_enemy_shield = True
        else:
            enemy.hp = (enemy.hp-friend.atk) if not friend.poisonous else 0
            manage_enemy_wound = True
            
        if friend.shield:
            friend.shield = False
            self.manage_shield(friends, v_friends)
        else:
            friend.hp = (friend.hp-enemy.atk) if not enemy.poisonous else 0
            self.manage_wound(friend, pos_friend, friends, v_friends)
        self.manage_shield(enemies, v_enemies) if manage_enemy_shield else None
        self.manage_wound(enemy, pos_enemy, enemies, v_enemies) if manage_enemy_wound else None

    def manage_deathrattle(self, friends, values_friends, enemies, values_enemies, team_deathrattle, next_pos):
        team_deathrattle.sort(key=lambda x: x[1])
        pos_death = self.p1_pos_deathrattle if friends == self.p1 else self.p2_pos_deathrattle
        while team_deathrattle:
            minion, pos_minion = team_deathrattle[0][0], team_deathrattle[0][1]
            res = minion.play_deathrattle(self, pos_minion + pos_death,
                friends, enemies, values_friends, values_enemies)
            pos_death += res
            if team_deathrattle:
                if next_pos > pos_minion:
                    next_pos += res
                    next_pos = 0 if next_pos >= len(friends)-1 else next_pos
                team_deathrattle.pop(0)
        return next_pos

    def manage_soul_junggler(self, friends, enemies, values_friends, values_enemies):
        if values_friends['soulJunggler']:
            for minion in friends:
                if not minion.dead and minion.is_dead() and minion.archetype == 'demon':
                    minion.dead = True
                    for friend in friends:
                        if friend.name == 'soulJunggler':
                            if self.aoe_ghoul:
                                if not friend.is_dead():
                                    friend.fight['do'](self, friend, enemies, values_enemies)
                            else:
                                friend.fight['do'](self, friend, enemies, values_enemies)

    def manage_rafaam(self, enemy, team):
        self.count_dead_p1 += 1 if team == self.p1 else 0
        self.count_dead_p2 += 1 if team == self.p2 else 0
        if self.rafaam == 'p1' and self.count_dead_p2 == 1:
            self.rafaam_add = copy.copy(enemy)
            self.rafaam = False
        elif self.rafaam == 'p2' and self.count_dead_p1 == 1:
            self.rafaam_add = copy.copy(enemy)
            self.rafaam = False

    def get_minions_dead(self, team, opponents, values, next_pos, team_deathrattle):
        minions_dead = []
        for pos, minion in enumerate(team[:]):
            if minion.is_dead():
                next_pos -= 1 if pos < next_pos else 0
                next_pos = 0 if next_pos == len(team)-1 else next_pos
                position = team.index(minion) + len(minions_dead)
                team.remove(minion)
                
                self.manage_rafaam(minion, team) if self.rafaam else None
                self.manage_kangor(minion, team)
                self.update_state_dead(team, minion, values)
                self.passive_dead(minion, team, values)
                if minion.play_deathrattle:
                    team_deathrattle.append((minion, position-len(minions_dead)))
                minions_dead.append((minion, position))
        return minions_dead, next_pos

    def manage_enemies_reborn(self, team, minions_dead):
        n_no_reborn = 0
        for minion_dead, pos in minions_dead:
            if minion_dead.reborn:
                self.minion_reborn(team, minion_dead, pos - n_no_reborn)
            else:
                n_no_reborn += 1        

    def minion_reborn(self, team, minion, pos):
        minion = self.create_minion(minion.gold, minion.name)
        minion.hp, minion.reborn = 1, False
        team.insert(pos, minion)

    def target_enemy(self, enemies):
        targets = self.board_position_of(enemies, 'taunt')
        self.pos_def = (choice(targets) if targets else randint(1, len(enemies))) -1
        return enemies[self.pos_def]

    def view_fight(self):
        os.system('cls')
        print(self.simulation) if self.simulation else None
        print('\n')
        print("FIGHT !".center(152))
        print(self)
        time.sleep(self.t)

    def manage_view(self, show_targets=True):
        self.view_targets = False if not show_targets else True
        self.history.append(str(self)) if self.h else None
        self.view_fight() if self.t else None
        self.view_targets = True

    def is_game_block(self):
        for minion in (self.p1 + self.p2):
            if minion.atk and minion.name != 'arcaneCannon':
                break
        else:
            self.game_block = True
            return True
        return False

    def __str__(self):
        # os.system('cls')
        display = ''
        for pos, team in enumerate(((self.p2, self.p2_name, self.p2_hero_true_name), (self.p1, self.p1_name, self.p1_hero_true_name))):
            team, name, hero_name = team
            name = "{}---{}".format(name, hero_name)
            contain =  str(''.join([str(minion) for minion in team])).split('\n')[:-1]
            border, border_top = "\n+{}+\n".format('-'*150), "\n+{}+\n".format(name.center(150, '-'))
            contain = '\n'.join(["|{}|".format((' '*5).join(contain[i::7]).center(150)) for i in range(7)])
            if self.winner:
                show = self.winner.center(152) if pos == 0 else ' '
            else:
                pos_target = lambda x, y: ' '*int(75+((2*(x+1)-len(team)-1)*10.5)) + y
                if not self.view_targets:
                    show_attacker, show_deffender = ' ', ' '
                else:
                    show_attacker = pos_target(self.pos_atk, 'A')
                    show_deffender = pos_target(self.pos_def, 'D')
                show = (show_attacker if pos == 0 else show_deffender) if self.attackers == 'p2' else (show_deffender if pos == 0 else show_attacker)
            display += (border_top + contain + border + show+ '\n') if pos == 0 else (show + border_top + contain + border)
        if self.view_targets:
            next_attacker = self.next_friend if self.attackers == 'p1' else self.next_enemy 
        return display

