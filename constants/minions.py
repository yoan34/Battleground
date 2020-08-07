"""
This file contain all functions about the feature of some minions.
these functions are attached to the specific minion's object at its creation.
The functions manages:
	-all battlecry
	-all passives
	-all deathrattle (not finish)

It contain a dictionary with all dates about the minions:
	-name         -img
	-atk          -poisonous
	-hp           -taunt
	-lvl          -deathrattle
	-img          -shield
	-archetype    -reborn
	-battlecry    -magnetic
	-passive      -overkill
	and so on....

It has two objects about the minions group by tier or archetype and one other
for the specific minion 'Megasaur' who have a specific battlecry and require
some extra data.
"""

from random import choice
import time
from Components.Minion import Minion

def btc_token(self, minion, target, buff,  direction, is_human):
    token_place = 0
    for _ in range(self.brann):
        if len(self.board) < 7:
            is_gold = True if minion.gold else False
            for token in range(int((2**self.n_khadgar)*(3**self.n_g_khadgar))):
                if len(self.board) < 7:
                    self.timing_IA()
                    token_place += 1
                    minion_token = Minion(minion.qn+'_t', is_gold, minion.qn+'_t', 1, 1, 1, minion.archetype, deathrattle=[], fight={'do': [], 'trigger': ''})
                    self.hero.power['do'](self, minion=minion_token, add=False) if self.hero.deathwing else None
                    if token > 0:
                        self.execute_passive_play(minion_token, self.board)
                        self.execute_passive_play(minion_token, self.board)
                    else:
                        self.execute_passive_play(minion_token, self.board)
                    self.board.insert(direction+token_place-1, minion_token)
                    if token_place % 3 == 0:
                        token_place = 0
                    if not minion_token.gold:
                        if minion_token.name in self.double:
                            if self.double[minion_token.name] == 2:
                                self.timing_IA()
                                self.triple_minion(minion_token, is_token=True)
                                self.double.pop(minion_token.name)
                            else:
                                self.double[minion_token.name] += 1
                        else:
                            self.double[minion_token.name] = 1

def btc_buff_one_minion(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    self.timing_IA()
    if targets:
        pos = self.get_answer_battlecry(targets) if is_human else choice(targets)-1
        n = 2 if minion.gold else 1
        for _ in range(self.brann):
            self.board[pos].atk += buff*n
            self.board[pos].hp += buff*n
        if direction < len(self.board)//2:
            pos -= 1
        self.bot_buff_minion(pos+2, len(self.board)) if self.is_bot else None

def btc_houndMaster(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    self.timing_IA()
    if targets:
        pos = self.get_answer_battlecry(targets) if is_human else choice(targets)-1
        n = 2 if minion.gold else 1
        for _ in range(self.brann):
            self.board[pos].taunt = True
            self.board[pos].atk += buff*n
            self.board[pos].hp += buff*n
        if direction < len(self.board)//2:
                pos -= 1
        self.bot_buff_minion(pos+2, len(self.board)) if self.is_bot else None

def btc_deckSwabbie(self, minion, target, buff, direction, is_human):
    n = 2 if minion.gold else 1
    for _ in range(self.brann):
        if self.up_cost[0] != 'M':
            self.up_cost[0] -= 1*n if self.up_cost[0] > 0 else 0

def btc_pogoHopper(self, minion, target, buff, direction, is_human):
    n = 2 if minion.gold else 1
    for _ in range(self.brann):
        minion.atk += buff*n * self.n_pogo
        minion.hp += buff*n * self.n_pogo
    self.n_pogo += 1

def btc_buff_random_minion(self, minion, target, buff, direction, is_human):
    archetypes, target = self.get_board_archetype(), []
    if len(archetypes) < 4:
        target = archetypes
    else:
        for _ in range(3):
            c = choice(archetypes)
            archetypes.remove(c)
            target.append(c)

    minions_type_all = [minion for minion in self.board if minion.archetype == 'all']
    self.define_type_for_all(minions_type_all, archetypes, base_types=target)
    for _ in range(self.brann):
        for archetype in target:
            targets = self.board_position_of(self.board, archetype, minion)
            if targets:
                n = 2 if minion.gold else 1
                pos = choice(targets)-1
                self.board[pos].atk += buff*n
                self.board[pos].hp += buff*n
    for minion in minions_type_all:
        minion.archetype = 'all'
              
def btc_buff_atk_all_minion(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    if targets:
        n = 2 if minion.gold else 1
        for _ in range(self.brann):
            for pos in targets:
                self.board[pos-1].atk += buff*n

def btc_buff_hp_all_minion(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    if targets:
        for _ in range(self.brann):
            n = 2 if minion.gold else 1
            for pos in targets:
                self.board[pos-1].hp += buff*n

def btc_buff_all_minion(self, minion, target, buff, direction, is_human):
    btc_buff_hp_all_minion(self, minion, target, buff, direction, is_human)
    btc_buff_atk_all_minion(self, minion, target, buff, direction, is_human)

def btc_defenderOfArgus(self, minion, target, buff, direction, is_human):
    n = 2 if minion.gold else 1
    if len(self.board) > 1:
        for _ in range(self.brann):
            if direction == 1:
                self.board[direction].taunt = True
                self.board[direction].atk += 1*n
                self.board[direction].hp += 1*n
            elif direction == len(self.board):
                self.board[direction-2].taunt = True
                self.board[direction-2].atk += 1*n
                self.board[direction-2].hp += 1*n
            else:
                for i in range(0,3,2):
                    self.board[direction-i].taunt = True
                    self.board[direction-i].atk += 1*n
                    self.board[direction-i].hp += 1*n

def btc_southseaStrongarm(self, minion, target, buff, direction, is_human):
    btc_buff_one_minion(self, minion, target, buff*self.pirate_buy_in_turn, direction, is_human)

def btc_toxfin(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    if targets:
        pos = self.get_answer_battlecry(targets) if is_human else choice(targets)-1
        self.board[pos].poisonous = True
        if direction < len(self.board)//2:
            pos -= 1
        self.bot_buff_minion(pos+2, len(self.board)) if self.is_bot else None

def btc_annihilanBattlemaster(self, minion, target, buff, direction, is_human):
    n = 2 if minion.gold else 1
    for _ in range(self.brann):
        minion.hp += (self.max_hp - self.hp) * (buff*n)

def btc_vulgarHomunculus(self, minion, target, buff, direction, is_human):
    for _ in range(self.brann):
        self.hp -= 2

def btc_murozond(self, minion, target, buff, direction, is_human):
	if self.last_enemies:
		for _ in range(self.brann):
			self.n_murozon += 1
			minion_enemy = choice(self.last_enemies)
			minion_enemy = self.get_minion_enemies(minion.gold, minion_enemy)
			self.hand.append(minion_enemy)
			is_token = True if minion_enemy.name[-2:].upper() == '_T' else False
			self.update_doublon_minion(minion_enemy, token=is_token)
		
def btc_amalgadon(self, minion, target, buff, direction, is_human):
	n = 2 if minion.gold else 1
	n_type = [minion.archetype for minion in self.board if minion.archetype != 'neutral']
	if 'all' in n_type:
		n_all = n_type.count('all')
		n_type = len(set([archetype for archetype in n_type if archetype != 'all']))
		n_type = n_type + n_all
	for _ in range(n_type):
		for _ in range(n):
			buff = choice(('crackling', 'flaming','spores','poison','massive','volcanic',
				'lightning','carapace'))
			if buff == 'crackling':
				minion.shield = True
			elif buff == 'flaming':
				minion.atk += 3
			elif buff == 'spores':
				minion.deathrattle.append(dht_spore)
			elif buff == 'poison':
				minion.poisonous = True
			elif buff == 'massive':
				minion.taunt = True
			elif buff == 'volcanic':
				minion.atk += 1
				minion.hp += 1
			elif buff == 'lightning':
				minion.windfury = True
			elif buff == 'carapace':
				minion.hp += 3

def btc_gentleMegasaur(self, minion, target, buff, direction, is_human):
    targets = self.board_position_of(self.board, target, minion)
    if len(targets) > 0:
        discovery = self.get_discovery(minion=minion, pool=self.pool.pool)
        n = 2 if minion.gold else 1
        for _ in range(self.brann):
            for i in range(n):
                if self.is_bot:
                    discovery.megasaur = True
                    time.sleep(2)
                    buff_discovery = self.see_discovery(nature='megasaur')
                    self.view_discover = discovery.display_discovery(buff_discovery)
                else:
                    self.view_discover = discovery.display_discovery()
                self.timing_IA()
                target_discovery = self.get_answer_discovery() if is_human else choice([1,2,3])
                name_buff = discovery.cards_discover[target_discovery-1]
                if name_buff == 'crackling':
                    for pos in targets:
                        self.board[pos-1].shield = True
                elif name_buff == 'flaming':
                    for pos in targets:
                        self.board[pos-1].atk += 3
                elif name_buff == 'spores':
                    for pos in targets:
                        self.board[pos-1].deathrattle.append(dht_spore)
                elif name_buff == 'poison':
                    for pos in targets:
                        self.board[pos-1].poisonous = True
                elif name_buff == 'massive':
                    for pos in targets:
                        self.board[pos-1].taunt = True
                elif name_buff == 'volcanic':
                    for pos in targets:
                        self.board[pos-1].atk += 1
                        self.board[pos-1].hp += 1
                elif name_buff == 'lightning':
                    for pos in targets:
                        self.board[pos-1].windfury = True
                else:
                    for pos in targets:
                        self.board[pos-1].hp += 3
        self.view_discover = ''

def btc_primalfinLookout(self, minion, target, buff, direction, is_human):
    if len(self.board_position_of(self.board, 'murloc')) > 1:
        discovery = self.get_discovery(minion=minion, pool=self.pool.pool)
        n = 2 if minion.gold else 1
        for _ in range(self.brann):
            for i in range(n):
                if self.is_bot:
                    discovery.megasaur = True
                    time.sleep(2)
                    buff_discovery = self.see_discovery(nature='primal')
                    self.view_discover = discovery.display_discovery(buff_discovery)
                else:
                    self.view_discover = discovery.display_discovery()
                self.timing_IA()
                target_discovery = self.get_answer_discovery() if is_human else choice([1,2,3])
                new_minion = discovery.cards_discover[target_discovery-1]
                new_minion = self.create_minion(False, new_minion)
                self.pool.remove_to_pool(new_minion.name, new_minion.lvl)
                self.hand.append(new_minion)
                self.update_doublon_minion(new_minion)
        self.view_discover = ''

def pas_microMachine(self, minion, target, buff):
	n = 2 if minion.gold else 1
	minion.atk += 1*n

def pas_hangryDragon(self, minion, target, buff):
	if self.is_win_fight:
		n = 2 if minion.gold else 1
		minion.atk += 2*n
		minion.hp += 2*n

def pas_shifterZerus(self, minion, target, buff):
    random_minion = choice([name for minions in self.pool.pool for name in minions])
    gold = True if minion.gold else False
    morph = minion.morph
    minion = Minion(random_minion, gold, *[value for value in MINIONS[random_minion].values()][1:])
    minion.name  = 'shifterZerus'
    minion.morph = morph
    minion.qn = "Z{}Z".format(minion.qn[:10])
    minion.passive = MINIONS['shifterZerus']['passive']
    minion.true_name = random_minion
    return minion
   

# at 'end_turn'
def pas_razorgoreTheUntamed(self, minion, target, buff):
	n_dragon = self.board_position_of(self.board, target)
	if n_dragon:
		n = 2 if minion.gold else 1
		minion.atk += len(n_dragon)*n
		minion.hp += len(n_dragon)*n

def pas_cobaltScalebane(self, minion, target, buff):
    targets = self.board_position_of(self.board)
    if len(targets) > 1:
        n = 2 if minion.gold else 1
        targets.remove(int([pos+1 for (pos, m) in enumerate(self.board) if m.id == minion.id][0]))
        pos = choice(targets)
        self.board[pos-1].atk += buff*n

def pas_ironSensei(self, minion, target, buff):
    targets = self.board_position_of(self.board, 'meca')
    if len(targets) > 1:
        n = 2 if minion.gold else 1
        targets.remove(int([pos+1 for (pos, m) in enumerate(self.board) if m.id == minion.id][0]))
        pos = choice(targets)
        self.board[pos-1].atk += buff*n
        self.board[pos-1].hp += buff*n

def pas_lightfangEnforcer(self, minion, target, buff):
    archetypes = self.get_board_archetype()
    minions_type_all = [minion for minion in self.board if minion.archetype == 'all']
    self.define_type_for_all(minions_type_all, archetypes)
    for archetype in ARCHETYPES:
        targets = self.board_position_of(self.board, archetype)
        if targets:
            n = 2 if minion.gold else 1
            pos = choice(targets)
            self.board[pos-1].atk += buff*n
            self.board[pos-1].hp += buff//2*n
    for minion in minions_type_all:
        minion.archetype = 'all'

def pas_goldgrubber(self, minion, target, buff):
    if self.board_gold_minion:
        n = 2 if minion.gold else 1
        self.board_gold_minion += 1 if minion.gold else 0
        minion.atk += buff*n*self.board_gold_minion
        minion.hp += buff*n*self.board_gold_minion

# when 'play' minion
def pas_wrathWeaver_saltyLooter_crowdFavorite_rabidSaurolisk(self, minion, minion_play, target, buff):
    n = 2 if minion.gold else 1
    minion.atk += buff*n
    minion.hp += buff*n
    if not self.immunity and minion.name == 'wrathWeaver':
        self.hp -= 1
        if self.watcher:
            for minion in self.board:
                if minion.name == 'floatingWatcher':
                    fc, target, buff = list(minion.passive.values())[:-1]
                    fc(self, minion, target, buff)

def pas_kalecgosArcaneAspect(self, minion, minion_play, target, buff):
    n_dragon = self.board_position_of(self.board, 'dragon')
    n = 2 if minion.gold else 1
    for pos in n_dragon:
        self.board[pos-1].atk += buff*n
        self.board[pos-1].hp += buff*n
    if minion_play.archetype == 'dragon':
        minion_play.atk += buff*n
        minion_play.hp += buff*n

def pas_murlocTidecaller(self, minion, minion_play, target, buff):
    n = 2 if minion.gold else 1
    minion.atk += buff*n

def pas_packLeader(self, minion, minion_play, target, buff):
    n = 2 if minion.gold else 1
    minion_play.atk += buff*n

def pas_mamaBear(self, minion, minion_play, target, buff):
	if minion_play.id != minion.id:
		n = 2 if minion.gold else 1
		minion_play.atk += buff*n
		minion_play.hp += buff*n

def pas_floatingWatcher(self, minion, target, buff):
    n = 2 if minion.gold else 1
    minion.atk += buff*n
    minion.hp += buff*n



# when 'sold' minion
def pas_stewardOfTime(self, minion, target, buff):
	if not self.time_by_action == 0:
		n = 2 if minion.gold else 1
		for minion in self.shop:
			minion.atk += buff*n
			minion.hp += buff*n

def pas_freedealingGambler(self, minion, target, buff):
    n = 2 if minion.gold else 1
    self.gold += (buff*n-1)
    self.gold = 10 if self.gold > 10 else self.gold

# when 'present' minion
def pas_murlocWarleader_southseaCaptain_malGanis_siegeBreaker(self, minion, minion_play, target, buff, action):
    targets = self.board_position_of(self.board, target)
    n = 2 if minion.gold else 1
    if action == 'play':
        targets.remove(int([pos+1 for (pos, m) in enumerate(self.board) if m.id == minion.id][0]))
        if minion.n_passive == 0:
            minion.n_passive += 1
            if minion.name == 'malGanis':
                self.immunity += 1
            for pos in targets:
                self.board[pos-1].atk += buff*n
                if minion.name == 'southseaCaptain' or minion.name == 'malGanis':
                    self.board[pos-1].hp += buff*n
        elif minion.n_passive >= 1:
            if minion_play.archetype == target:
                minion_play.atk += buff*n 
                if minion.name == 'southseaCaptain' or minion.name == 'malGanis':
                    minion_play.hp += buff*n
    else:
        if minion.name == 'malGanis':
            self.immunity -= 1
        if len(targets) > 1:
            for pos in targets:
                self.board[pos-1].atk -= buff*n
                if minion.name == 'southseaCaptain' or minion.name == 'malGanis':
                    self.board[pos-1].hp -= buff*n

def pas_oldMurkEye(self, minion, minion_play, target, buff, action=False):
    n = 2 if minion.gold else 1
    targets = self.board_position_of(self.board, target)
    if action == 'play':
        if minion.n_passive == 0:
            self.oldmurloc += 1
        minion.n_passive += 1
        minion.atk = (len(targets)-1)*n + (2*n)
    elif action == 'sold':
        self.oldmurloc -= 1

# when buy
def pas_capnHoggarr(self, minion, minion_play, target, buff, action):
    n = 2 if minion.gold else 1
    if action == 'play':
        self.gold += buff*n
    elif action == 'sold':
        self.hoggarr -= 1

#########################################################################
############################### FIGHT ###################################
#########################################################################
def summon_token(btf, minion, friends, values, atk=1, hp=1, taunt=False, position=None):
	tokens = 0
	for i in range((2**values['khadgar'])*(3**values['khadgar_golden'])):
		if len(friends) >= 7: break
		tokens += 1
		is_gold = minion.gold
		if minion.name == 'theBeast': is_gold = False
		token = Minion(minion.name+'_t', is_gold, minion.name[:8]+'_t', atk, hp, 1,
		minion.archetype, taunt=taunt, deathrattle=[], fight={'do': [], 'trigger': ''},
		max_hp=hp)
		token.atk += 2 if btf.deathwing else 0
		if minion.name == 'theBeast':
			values = btf.stuff1 if values == btf.stuff2 else btf.stuff2
		if i > 0:
			[btf.passive_summon(token, friends, values) for _ in range(2)]
		else:
			btf.passive_summon(token, friends, values)
		if token.archetype == 'demon':
			for m in friends:
				if (m.fight['trigger'] == 'present') and (m.archetype == 'demon'):
					m.fight['do'](m, friends, minion=token)
		if token.archetype == 'pirate':
			for m in friends:
				if (m.fight['trigger'] == 'present') and (m.archetype == 'pirate'):
					m.fight['do'](m, friends, minion=token)
		if position is None:
			position = friends.index(minion)+1
		if not minion.name == 'theBeast':
			friends.insert(position+i, token)
		else:
			friends.append(token)
		btf.manage_view(show_targets=False)

	return i, tokens

#############################
########## ATTACKS ##########
#############################
def fgt_zappSlywick(btf, friend, friends, enemies):
		low_targets = []
		minimum = min([enemy.atk for enemy in enemies])
		for pos, enemy in enumerate(enemies):
			if enemy.atk == minimum:
				low_targets.append(pos)
		btf.pos_def = choice(low_targets)
		return enemies[btf.pos_def]

def fgt_glyphGuardian(btf, friend, friends, enemies):
	n = 3 if friend.gold else 2
	friend.atk *= n

def fgt_monstrousMacaw(btf, friend, friends, enemies):
	targets = [minion for minion in friends if minion.deathrattle]
	if btf.attackers == 'p1':
		values = btf.stuff1
		e_values = btf.stuff2
	else:
		values = btf.stuff2
		e_values = btf.stuff1
	n = 2 if friend.gold else 1
	for _ in range(n):
		targets = [(pos, m) for pos, m in enumerate(friends) if m.play_deathrattle is not None]
		if targets:
			pos, minion = choice(targets)
			minion.play_deathrattle(btf, pos+1, friends, enemies, values, e_values)

def fgt_arcaneCannon(btf, friend, enemy, enemies, values_enemies):
	n = 2 if friend.gold else 1
	for _ in range(n):
		targets = [(enemy, pos) for pos, enemy in enumerate(enemies) if enemy.hp > 0]
		if not targets:return 
		enemy, pos_enemy = choice(targets)
		btf.deal_damage(2, enemy, pos_enemy, enemies, values_enemies)
		btf.manage_view(show_targets=False)

#############################
###### PIRATE ATTACKS #######
#############################
def fgt_dreadAdmiralEliza(friend, friends):
	n = 2 if friend.gold else 1
	for minion in friends:
		minion.atk += n
		minion.hp += n

def fgt_ripsnarlCaptain(friend, friends):
	if friend.name != 'ripsnarlCaptain':
		n = 4 if friend.gold else 2
		friend.atk += n
		friend.hp += n

#############################
####### LOSE SHIELD #########
#############################
def fgt_bolvarFireblood(minion):
	n = 4 if minion.gold else 2
	minion.atk += n

def fgt_drakonidEnforcer(minion):
	n = 4 if minion.gold else 2
	minion.atk += n
	minion.hp += n

#############################
####### MINION WOUND ########
#############################
def fgt_imppGang(btf, minion, pos, team, values, atk=1, hp=1, taunt=False):
    token_place = 0
    is_gold = True if minion.gold else False
    if len(team) >= 7: return
    for token in range((2**values['khadgar'])*(3**values['khadgar_golden'])):
        if len(team) >= 7: break
        token_place += 1
        minion_token = Minion(minion.qn+'_t', is_gold, minion.qn+'_t', atk, hp, 1, minion.archetype,
            taunt=taunt,deathrattle=[], fight={'do': [], 'trigger': ''})
        minion_token.atk += 2 if btf.deathwing else 0
        if minion_token.archetype == 'demon':
            for m in team:
                if (m.fight['trigger'] == 'present') and (m.archetype == 'demon'):
                    m.fight['do'](m, team, minion=minion_token)
        position = team.index(minion)
        team.insert(position+token_place, minion_token)
        btf.manage_view(show_targets=False)

def fgt_rover(btf, minion, pos, team, values):
	fgt_imppGang(btf, minion, pos, team, values, atk=2, hp=3, taunt=True)

def fgt_impMama(btf, minion, pos, team, values):
	khadgar_token = tokens = 0
	n = 2 if minion.gold else 1
	for i in range(n):
		name = choice(list(set(MINION_BY_ARCHETYPE['demon'])-{'impMama'}))
		res = summon_minion(btf, name, team, values,
			pos+i+khadgar_token+1, impMama=True)
		khadgar_token += res[0]
		

#############################
###### MINION PRESENT #######
#############################
def fgt_murlocWarleader(friend, friends, repop=False, minion=False):
	n = 4 if friend.gold else 2
	for minion in friends:
		if minion.archetype == 'murloc' or minion.archetype == 'all':
			if minion.id != friend.id:
				minion.atk += n if repop else -n

def fgt_southseaCaptain(friend, friends, repop=False, minion=False):
	n = 2 if friend.gold else 1
	if minion:
		minion.atk += n
		minion.hp += n
	else:
		for minion in friends:
			if minion.archetype == 'pirate' or minion.archetype == 'all':
				if minion.id != friend.id:
					minion.atk += n if repop else -n
					minion.hp += n if repop else -n if minion.hp > minion.max_hp else 0

def fgt_siegeBreaker(friend, friends, repop=False, minion=False):
	n = 2 if friend.gold else 1
	if minion:
		minion.atk += n
	else:
		for minion in friends:
			if minion.archetype == 'demon' or minion.archetype == 'all':
				if minion.id != friend.id:
					minion.atk += n if repop else -n

def fgt_malGanis(friend, friends, repop=False, minion=False):
	n = 4 if friend.gold else 2
	if minion:
		minion.atk += n
		minion.hp += n
	else:
		for minion in friends:
			if minion.archetype == 'demon' or minion.archetype == 'all':
				if minion.id != friend.id:
					minion.atk += n if repop else -n
					minion.hp += n if repop else -n if minion.hp > minion.max_hp else 0


#############################
###### FRIENDLY DEAD ########
#############################
def fgt_junkbot(minion):
	n = 4 if minion.gold else 2
	minion.atk += n
	minion.hp += n

def fgt_scavengingHyena(minion):
	n = 4 if minion.gold else 2
	minion.atk += n
	minion.hp += n//2

def fgt_soulJunggler(btf, minion, enemies, values_enemies):
	n = 2 if minion.gold else 1
	btf.minion_deal_dmg = minion
	for _ in range(n):
		targets = [(enemy, pos) for pos, enemy in enumerate(enemies) if enemy.hp > 0]
		if not targets:return 
		enemy, pos_enemy = choice(targets)
		btf.deal_damage(3, enemy, pos_enemy, enemies, values_enemies)
		if enemy.hp <= 0:
			btf.add_enemy_dead += 1
			btf.add_dead += 1
		btf.manage_view(show_targets=False)

#############################
### FRIENDLY DRAGON KILL ####
#############################
def fgt_waxriderTogwaggle(minion):
	n = 4 if minion.gold else 2
	minion.atk += n
	minion.hp += n


#############################
######### OVERKILL ##########
#############################
def ovk_seabreakerGoliath(btf, minion, enemy, friends, enemies, values):
	n = 4 if minion.gold else 2
	for friend in friends:
		if friend.id != minion.id and friend.archetype == 'pirate':
			friend.atk += n
			friend.hp += n 
		
def ovk_natPagleExtremeAngler(btf, minion, enemy, friends, enemies, values):
	for i in range((2**values['khadgar'])*(3**values['khadgar_golden'])):
		if len(friends) < 7:
			treasure = Minion('treasure', minion.gold, 'treasure', 0, 2, 1, 'neutral',
			deathrattle=[dht_treasure], fight={'do': [], 'trigger': ''})
			treasure.hp = 2
			treasure.atk += 2 if btf.deathwing else 0
			position = friends.index(minion)
			friends.insert(position+1+i, treasure)

def dht_treasure(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	n = 2 if minion.gold else 1
	for i in range(n):
		for j in range(values['baronRivendare']):
			names = list(set([name for minions in MINIONS_BY_TIER for name in minions]) - set(WITHOUT_MINIONS[btf.no_archetype]))
			name = choice(names)
			res = summon_minion(btf, name, friends, values,
				values['baronRivendare']*i+pos+j+khadgar_token, natpagle=True)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens
			
def ovk_ironhideDirehorn(btf, minion, enemy, friends, enemies, values):
	summon_token(btf, minion, friends, values, atk=5, hp=5)

def ovk_heraldOfFlame(btf, minion, friends, current_enemy, enemies, v_enemies, v_friends):
	damage = 6 if minion.gold else 3
	enemies_wound, enemies_shields = [], 0
	for pos, enemy in enumerate(enemies):
		if enemy.id != current_enemy.id:
			btf.deal_damage(damage, enemy, pos, enemies, v_enemies)
			btf.passive_dragon_kill(enemy, friends, v_friends)
			btf.history.append(str(btf)) if btf.h else None
			btf.view_fight() if btf.t else None
			if enemy.hp >= 0:
				break


#############################
##### FRIENDLY SUMMON #######
#############################
def fgt_packLeader(minion, token):
	n = 6 if minion.gold else 3
	token.atk += n

def fgt_mamaBear(minion, token):
	n = 10 if minion.gold else 5
	token.atk += n
	token.hp += n

def fgt_deflectOBot(minion):
	n = 2 if minion.gold else 1
	minion.shield = True
	minion.atk += n


#############################
##### START OF FIGHT ########
#############################
def fgt_redWhelp(btf, minion, friends, values_friends, enemies, values_enemies):
	n = 2 if minion.gold else 1
	damage = len(btf.board_position_of(team=friends, target='dragon'))
	btf.minion_deal_dmg = minion
	for _ in range(n):
		targets = [(enemy, pos) for pos, enemy in enumerate(enemies) if enemy.hp > 0]
		if not targets:return 
		enemy, pos_enemy = choice(targets)
		btf.deal_damage(damage, enemy, pos_enemy, enemies, values_enemies)
		btf.passive_dragon_kill(enemy, friends, values_friends)
		if enemy.hp <= 0:
			btf.add_enemy_dead += 1
			btf.add_dead += 1
		btf.manage_view(show_targets=False)

#############################
#### DEATHRATTLE SUMMON #####
#############################
def dht_mecharoo(btf, minion, pos, friends, enemies, values, e_values, atk=1, hp=1):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]
	return tokens

def dht_harvestGolem(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values, atk=2,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]
	return tokens

def dht_imprisoner(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]
	return tokens

def dht_kindlyGrandmother(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values, atk=3, hp=2,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]	
	return tokens

def dht_ratPack(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for j in range(values['baronRivendare']):
		for i in range(minion.atk):
			res = summon_token(btf, minion, friends, values,
				position=minion.atk*j+i+pos+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens
			
def dht_infestedWolf(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for j in range(values['baronRivendare']):
		for i in range(2):
			res = summon_token(btf, minion, friends, values,
			position=2*j+pos+i+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_replicatingMenace(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for j in range(values['baronRivendare']):
		for i in range(3):
			res = summon_token(btf, minion, friends, values,
			position=3*j+pos+i+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens
	
def dht_theBeast(btf, minion, pos, friends, enemies, values, e_values):
	for _ in range(values['baronRivendare']):
		summon_token(btf, minion, enemies, values, atk=3, hp=3, position=pos)
	return 0

def dht_pilotedShredder(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	n = 2 if minion.gold else 1
	for i in range(n):
		for j in range(values['baronRivendare']):
			names = list(set(MINIONS_BY_TIER[1]) - set(WITHOUT_MINIONS[btf.no_archetype]))
			name = choice(names)
			res = summon_minion(btf, name, friends, values,
				values['baronRivendare']*i+pos+j+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_mechanoEgg(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values, atk=8, hp=8,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]
	return tokens

def dht_savannahHighmane(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for j in range(values['baronRivendare']):
		for i in range(2):
			res = summon_token(btf, minion, friends, values, atk=2, hp=2,
			position=2*j+pos+i+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_voidlord(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for j in range(values['baronRivendare']):
		for i in range(3):
			res = summon_token(btf, minion, friends, values, atk=1, hp=3,
			taunt=True, position=2*j+pos+i+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_sneedsOldShredder(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	n = 2 if minion.gold else 1
	for i in range(n):
		for j in range(values['baronRivendare']):
			names = list(set(MINIONS_LEGENDARY) - 
			set(WITHOUT_MINIONS[btf.no_archetype])-{'sneedsOldShredder'})
			name = choice(names)
			res = summon_minion(btf, name, friends, values,
				values['baronRivendare']*i+pos+j+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_ghastcoiler(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	n = 4 if minion.gold else 2
	for i in range(n):
		for j in range(values['baronRivendare']):
			names = list(set(MINIONS_DEATHRATTLE) - 
			set(WITHOUT_MINIONS[btf.no_archetype])-{'ghastcoiler'})
			name = choice(names)
			res = summon_minion(btf, name, friends, values,
				values['baronRivendare']*i+pos+j+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_theTideRazor(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	n = 6 if minion.gold else 3
	for i in range(n):
		for j in range(values['baronRivendare']):
			names = list(set(MINION_BY_ARCHETYPE['pirate']) - 
			set(WITHOUT_MINIONS[btf.no_archetype]))
			name = choice(names)
			res = summon_minion(btf, name, friends, values,
				values['baronRivendare']*i+pos+j+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_kangorsApprentice(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	arr_kangor = btf.first1_meca_die if friends == btf.p1 else btf.first2_meca_die
	n = 4 if minion.gold else 2
	for i in range(values['baronRivendare']):
		for j, properties in enumerate(arr_kangor[:n]):
			name, is_gold, is_token, m_atk, m_hp = properties
			if is_token:
				res = summon_token(btf, name, friends, values, atk=m_atk, hp=m_hp,
					position=n*i+pos+j+khadgar_token)
			else:
				res = summon_minion(btf, name, friends, values,
					n*i+pos+j+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_spore(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	spore = Minion('spore_t', False, 'spore_t', 1, 1, 1, 'neutral',
	deathrattle=[], fight={'do': [], 'trigger': ''})
	for j in range(values['baronRivendare']):
		for i in range(2):
			res = summon_token(btf, spore, friends, values,
			position=2*j+pos+i+khadgar_token)
			khadgar_token += res[0]
			tokens += res[1]
	return tokens

def dht_scallyWag(btf, minion, pos, friends, enemies, values, e_values):
	khadgar_token = tokens = 0
	for i in range(values['baronRivendare']):
		res = summon_token(btf, minion, friends, values,
			position=pos+i+khadgar_token)
		khadgar_token += res[0]
		tokens += res[1]
	return tokens

def summon_minion(btf, name, friends, values, position, impMama=False, natpagle=False):
	try:
		tokens = 0
		for i in range((2**values['khadgar'])*(3**values['khadgar_golden'])):
			if len(friends) >= 7: break
			tokens += 1
			is_gold = False if not natpagle else True
			minion = btf.create_minion(is_gold, name)
			minion.atk += 2 if btf.deathwing else 0
			if impMama: minion.taunt = True
			if minion.name in values:
				values[minion.name] += 1
			if (minion.name == 'murlocWarleader' or minion.name == 'southseaCaptain' or
				minion.name == 'siegeBreaker' or minion.name == 'malGanis'):
				minion.fight['do'](minion, friends, repop=True)
			if i > 0:
				if minion.archetype == 'beast':
					[btf.passive_summon(minion, friends, values) for _ in range(2)]
				else:
					btf.passive_summon(minion, friends, values)
			else:
				btf.passive_summon(minion, friends, values)
			if minion.archetype == 'demon':
				for m in friends:
					if (m.fight['trigger'] == 'present') and (m.archetype == 'demon'):
						m.fight['do'](m, friends, minion=minion)
			elif minion.archetype == 'pirate':
				for m in friends:
					if (m.fight['trigger'] == 'present') and (m.archetype == 'pirate'):
						m.fight['do'](m, friends, minion=minion)
			friends.insert(position+i, minion)
			btf.manage_view(show_targets=False)
		return i, tokens
	except Exception as e:
		print(e)
		print(values)
		btf.view_fight()
		a=input()


#############################
### DEATHRATTLE NO SUMMON ###
#############################

def dht_fiendishServant(btf, minion, pos, friends, enemies, values, e_values):
	targets = btf.board_position_of(friends)
	if targets:
		n = 2 if minion.gold else 1
		for _ in range(values['baronRivendare']):
			for _ in range(n):
				pos = choice(targets)
				friends[pos-1].atk += minion.atk
				if not targets:
					break
			if not targets:
				break
	return 0
	
def dht_selflessHero(btf, minion, pos, friends, enemies, values, e_values):
	targets = btf.board_position_of(friends, 'shield')
	targets = [t+1 for t in range(len(friends)) if t+1 not in targets]
	if targets:
		n = 2 if minion.gold else 1
		for _ in range(values['baronRivendare']):
			for _ in range(n):
				pos = choice(targets)
				targets.remove(pos)
				friends[pos-1].shield = True
				if not targets:
					break
			if not targets:
				break
	btf.manage_view(show_targets=False)
	return 0

def dht_spawnOfNzoth(btf, minion, pos, friends, enemies, values, e_values):
	if friends:
		n = 2 if minion.gold else 1
		for _ in range(values['baronRivendare']):
			for friend in friends:
				friend.atk += n
				friend.hp += n
	return 0

def dht_kingBagurgle(btf, minion, pos, friends, enemies, values, e_values):
	n = 4 if minion.gold else 2
	for _ in range(values['baronRivendare']):
		for friend in friends:
			if friend.archetype == 'murloc':
				friend.atk += n
				friend.hp += n
	return 0

def dht_goldrinnTheGreatWolf(btf, minion, pos, friends, enemies, values, e_values):
	if friends:
		n = 8 if minion.gold else 4
		for _ in range(values['baronRivendare']):
			for friend in friends:
				if friend.archetype == 'beast':
					friend.atk += n
					friend.hp += n
	return 0

def dht_nadinaTheRed(btf, minion, pos, friends, enemies, values, e_values):
	if friends:
		for friend in friends:
			if friend.archetype == 'dragon':
				friend.shield = True
	return 0

def dht_kaboomBot(btf, minion, pos, friends, enemies, values_friends, values_enemies):
	n = 2 if minion.gold else 1
	btf.minion_deal_dmg = minion
	for _ in range(values_friends['baronRivendare']):
		for _ in range(n):
			targets = [(enemy, pos) for pos, enemy in enumerate(enemies) if enemy.hp > 0]
			if not targets:break
			enemy, pos_enemy = choice(targets)
			btf.deal_damage(4, enemy, pos_enemy, enemies, values_enemies)
			if enemy.hp <= 0:
				btf.add_enemy_dead += 1
				btf.add_dead += 1
			btf.manage_view(show_targets=False)
	return 0

def dht_unstableGhoul(btf, minion, pos, friends, enemies, values_friends, values_enemies):
	n = 2 if minion.gold else 1
	for _ in range(values_friends['baronRivendare']):
		for pos, enemy in enumerate(enemies):
			btf.deal_damage(n, enemy, pos, enemies, values_enemies)
			if enemy.hp <= 0:
				btf.add_enemy_dead += 1
				btf.add_dead += 1
				btf.aoe_ghoul = True
		for pos, friend in enumerate(friends):
			btf.deal_damage(n, friend, pos, friends, values_friends)
			if friend.hp <= 0:
				btf.add_dead += 1
				btf.add_friend_dead += 1
				btf.aoe_ghoul = True
		btf.manage_view(show_targets=False)
	return 0




def fgt():
	pass

MINIONS = {
    'dreadAdmiralEliza': {
		'gold': False,
		'qn': 'Eliza',
		'atk': 6,
		'hp': 7,
		'lvl': 6, 
        'archetype':'pirate',
		'legendary': True,
		'img': './img/minion6/dreadAdmiralEliza.png',
		'img_discovery': './img/discovery_minion6/dreadAdmiralEliza.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_dreadAdmiralEliza,
			'trigger': 'friendly_pirate_atk',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'gentleMegasaur': {
		'gold': False,
		'qn': 'Megasaur',
		'atk': 5,
		'hp': 4,
		'lvl': 6,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion6/gentleMegasaur.png',
		'img_discovery': './img/discovery_minion6/gentleMegasaur.png',
		'battlecry': {
            'fc': btc_gentleMegasaur,
            'target': 'murloc',
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'ghastcoiler': {
		'gold': False,
		'qn': 'Coiler',
		'atk': 7,
		'hp': 7,
		'lvl': 6,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion6/ghastcoiler.png',
		'img_discovery': './img/discovery_minion6/ghastcoiler.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_ghastcoiler],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'theTideRazor': {
		'gold': False,
		'qn': 'Razor',
		'atk': 6,
		'hp': 4,
		'lvl': 6,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion6/theTideRazor.png',
		'img_discovery': './img/discovery_minion6/theTideRazor.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_theTideRazor],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'zappSlywick': {
		'gold': False,
		'qn': 'Zapp',
		'atk': 7,
		'hp': 10,
		'lvl': 6,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion6/zappSlywick.png',
		'img_discovery': './img/discovery_minion6/zappSlywick.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_zappSlywick,
			'trigger': 'attacks',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': True,
		},
    'foeReaper4000': {
		'gold': False,
		'qn': 'Reaper',
		'atk': 6,
		'hp': 9,
		'lvl': 6,
		'archetype': 'meca',
		'legendary': True,
		'img': './img/minion6/foeReaper4000.png',
		'img_discovery': './img/discovery_minion6/foeReaper4000.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': True,
		'windfury': False,
		},
    'kalecgosArcaneAspect': {
		'gold': False,
		'qn': 'Kalecgos',
		'atk': 4,
		'hp': 12,
		'lvl': 6,
		'archetype': 'dragon',
		'legendary': True,
		'img': './img/minion6/kalecgosArcaneAspect.png',
		'img_discovery': './img/discovery_minion6/kalecgosArcaneAspect.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_kalecgosArcaneAspect,
			'target': 'battlecry',
			'buff': 1,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'mamaBear': {
		'gold': False,
		'qn': 'Mamabear',
		'atk': 5,
		'hp': 5,
		'lvl': 6,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion6/mamaBear.png',
		'img_discovery': './img/discovery_minion6/mamaBear.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_mamaBear,
			'target': 'beast',
			'buff': 5,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_mamaBear,
			'trigger': 'friendly_summon',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'maexxna': {
		'gold': False,
		'qn': 'Maexxna',
		'atk': 2,
		'hp': 8,
		'lvl': 6,
		'archetype': 'beast',
		'legendary': True,
		'img': './img/minion6/maexxna.png',
		'img_discovery': './img/discovery_minion6/maexxna.png',
		'battlecry': False,
		'poisonous': True,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'kangorsApprentice': {
		'gold': False,
		'qn': 'Kangor',
		'atk': 3,
		'hp': 6,
		'lvl': 6,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion6/kangorsApprentice.png',
		'img_discovery': './img/discovery_minion6/kangorsApprentice.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_kangorsApprentice],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'nadinaTheRed': {
		'gold': False,
		'qn': 'Nadina',
		'atk': 7,
		'hp': 4,
		'lvl': 6,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion6/nadinaTheRed.png',
		'img_discovery': './img/discovery_minion6/nadinaTheRed.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_nadinaTheRed],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'impMama': {
		'gold': False,
		'qn': 'ImpMama',
		'atk': 6,
		'hp': 10,
		'lvl': 6,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion6/impMama.png',
		'img_discovery': './img/discovery_minion6/impMama.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_impMama,
			'trigger': 'wound',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
	'goldrinnTheGreatWolf': {
		'gold': False,
		'qn': 'Goldrinn',
		'atk': 4,
		'hp': 4,
		'lvl': 6,
		'archetype': 'beast',
		'legendary': True,
		'img': './img/minion5/goldrinnTheGreatWolf.png',
		'img_discovery': './img/discovery_minion5/goldrinnTheGreatWolf.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_goldrinnTheGreatWolf],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
	'amalgadon': {
		'gold': False,
		'qn': 'Amalgadon',
		'atk': 6,
		'hp': 6,
		'lvl': 6,
		'archetype': 'all',
		'legendary': False,
		'img': './img/minion5/amalgadon.png',
		'img_discovery': './img/discovery_minion5/amalgadon.png',
		'battlecry': {
            'fc': btc_amalgadon,
            'target': None,
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
	},
    #TIER 5
    'annihilanBattlemaster': {
		'gold': False,
		'qn': 'BattleMaster',
		'atk': 3,
		'hp': 1,
		'lvl': 5,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion5/AnnihilanBattlemaster.png',
		'img_discovery': './img/discovery_minion5/AnnihilanBattlemaster.png',
		'battlecry': {
            'fc': btc_annihilanBattlemaster,
            'target': None,
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'baronRivendare': {
		'gold': False,
		'qn': 'Baron',
		'atk': 1,
		'hp': 7,
		'lvl': 5,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion5/baronRivendare.png',
		'img_discovery': './img/discovery_minion5/baronRivendare.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'brannBronzebeard': {
		'gold': False,
		'qn': 'Brann',
		'atk': 2,
		'hp': 4,
		'lvl': 5,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion5/brannBronzebeard.png',
		'img_discovery': './img/discovery_minion5/brannBronzebeard.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'capnHoggarr': {
		'gold': False,
		'qn': 'Hoggarr',
		'atk': 6,
		'hp': 6,
		'lvl': 5,
		'archetype': 'pirate',
		'legendary': True,
		'img': './img/minion5/capnHoggarr.png',
		'img_discovery': './img/discovery_minion5/capnHoggarr.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_capnHoggarr,
			'target': 'pirate',
			'buff': 1,
			'trigger': 'buy',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'ironhideDirehorn': {
		'gold': False,
		'qn': 'Ironhide',
		'atk': 7,
		'hp': 7,
		'lvl': 5,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion5/ironhideDirehorn.png',
		'img_discovery': './img/discovery_minion5/ironhideDirehorn.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': ovk_ironhideDirehorn,
		'cleave': False,
		'windfury': False,
		},
    'junkbot': {
		'gold': False,
		'qn': 'Junkbot',
		'atk': 1,
		'hp': 5,
		'lvl': 5,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion5/junkbot.png',
		'img_discovery': './img/discovery_minion5/junkbot.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_junkbot,
			'trigger': 'friendly_dead',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'kingBagurgle': {
		'gold': False,
		'qn': 'Bagurgle',
		'atk': 6,
		'hp': 3,
		'lvl': 5,
		'archetype': 'murloc',
		'legendary': True,
		'img': './img/minion5/kingBagurgle.png',
		'img_discovery': './img/discovery_minion5/kingBagurgle.png',
		'battlecry': {
            'fc': btc_buff_all_minion,
            'target': 'murloc',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_kingBagurgle],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'lightfangEnforcer': {
		'gold': False,
		'qn': 'Lightfang',
		'atk': 2,
		'hp': 2,
		'lvl': 5,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion5/lightfangEnforcer.png',
		'img_discovery': './img/discovery_minion5/lightfangEnforcer.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_lightfangEnforcer,
			'target': 'all',
			'buff': 2,
			'trigger': 'end_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'malGanis': {
		'gold': False,
		'qn': 'Mal\'Ganis',
		'atk': 9,
		'hp': 7,
		'lvl': 5,
		'archetype': 'demon',
		'legendary': True,
		'img': './img/minion5/malGanis.png',
		'img_discovery': './img/discovery_minion5/malGanis.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_murlocWarleader_southseaCaptain_malGanis_siegeBreaker,
			'target': 'demon',
			'buff': 2,
			'trigger': 'present',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_malGanis,
			'trigger': 'present',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'murozond': {
		'gold': False,
		'qn': 'Murozond',
		'atk': 5,
		'hp': 5,
		'lvl': 5,
		'archetype': 'dragon',
		'legendary': True,
		'img': './img/minion5/murozond.png',
		'img_discovery': './img/discovery_minion5/murozond.png',
		'battlecry': {
            'fc': btc_murozond,
            'target': None,
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'natPagleExtremeAngler': {
		'gold': False,
		'qn': 'Nat Pagle',
		'atk': 8,
		'hp': 5,
		'lvl': 5,
		'archetype': 'pirate',
		'legendary': True,
		'img': './img/minion5/natPagleExtremeAngler.png',
		'img_discovery': './img/discovery_minion5/natPagleExtremeAngler.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': ovk_natPagleExtremeAngler,
		'cleave': False,
		'windfury': False,
		},
    'primalfinLookout': {
		'gold': False,
		'qn': 'Primalfin',
		'atk': 3,
		'hp': 2,
		'lvl': 5,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion5/primalfinLookout.png',
		'img_discovery': './img/discovery_minion5/primalfinLookout.png',
		'battlecry': {
            'fc': btc_primalfinLookout,
            'target': 'murloc',
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'razorgoreTheUntamed': {
		'gold': False,
		'qn': 'Razorgore',
		'atk': 2,
		'hp': 4,
		'lvl': 5,
		'archetype': 'dragon',
		'legendary': True,
		'img': './img/minion5/razorgoreTheUntamed.png',
		'img_discovery': './img/discovery_minion5/razorgoreTheUntamed.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_razorgoreTheUntamed,
			'target': 'dragon',
			'buff': 1,
			'trigger': 'end_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'seabreakerGoliath': {
		'gold': False,
		'qn': 'Goliath',
		'atk': 6,
		'hp': 7,
		'lvl': 5,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion5/seabreakerGoliath.png',
		'img_discovery': './img/discovery_minion5/seabreakerGoliath.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': ovk_seabreakerGoliath,
		'cleave': False,
		'windfury': True,
		},
    'sneedsOldShredder': {
		'gold': False,
		'qn': 'Sneed',
		'atk': 5,
		'hp': 7,
		'lvl': 5,
		'archetype': 'meca',
		'legendary': True,
		'img': './img/minion5/sneedsOldShredder.png',
		'img_discovery': './img/discovery_minion5/sneedsOldShredder.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_sneedsOldShredder],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'strongshellScavenger': {
		'gold': False,
		'qn': 'Strongshell',
		'atk': 2,
		'hp': 3,
		'lvl': 5,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion5/strongshellScavenger.png',
		'img_discovery': './img/discovery_minion5/strongshellScavenger.png',
		'battlecry': {
            'fc': btc_buff_all_minion,
            'target': 'taunt',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'voidlord': {
		'gold': False,
		'qn': 'Voidlord',
		'atk': 3,
		'hp': 9,
		'lvl': 5,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion5/voidlord.png',
		'img_discovery': './img/discovery_minion5/voidlord.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_voidlord],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    # TIER 4
    'annoyOModule': {
		'gold': False,
		'qn': 'Annoy-Module',
		'atk': 2,
		'hp': 4,
		'lvl': 4,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion4/annoyOModule.png',
		'img_discovery': './img/discovery_minion4/annoyOModule.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':True,
		'reborn': False,
		'magnetic': True,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'bolvarFireblood': {
		'gold': False,
		'qn': 'Bolvar',
		'atk': 1,
		'hp': 7,
		'lvl': 4,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion4/bolvarFireblood.png',
		'img_discovery': './img/discovery_minion4/bolvarFireblood.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_bolvarFireblood,
			'trigger': 'friendly_lose_shield',
			},
		'shield':True,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'caveHydra': {
		'gold': False,
		'qn': 'Hydra',
		'atk': 2,
		'hp': 4,
		'lvl': 4,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion4/caveHydra.png',
		'img_discovery': './img/discovery_minion4/caveHydra.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': True,
		'windfury': False,
		},
    'cobaltScalebane': {
		'gold': False,
		'qn': 'Cobalt',
		'atk': 5,
		'hp': 5,
		'lvl': 4,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion4/cobaltScalebane.png',
		'img_discovery': './img/discovery_minion4/cobaltScalebane.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_cobaltScalebane,
			'target': None,
			'buff': 3,
			'trigger': 'end_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'defenderOfArgus': {
		'gold': False,
		'qn': 'Argus',
		'atk': 2,
		'hp': 3,
		'lvl': 4,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion4/defenderOfArgus.png',
		'img_discovery': './img/discovery_minion4/defenderOfArgus.png',
		'battlecry': {
            'fc': btc_defenderOfArgus,
            'target': None,
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'drakonidEnforcer': {
		'gold': False,
		'qn': 'Drakonid',
		'atk': 3,
		'hp': 6,
		'lvl': 4,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion4/drakonidEnforcer.png',
		'img_discovery': './img/discovery_minion4/drakonidEnforcer.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_drakonidEnforcer,
			'trigger': 'friendly_lose_shield',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'floatingWatcher': {
		'gold': False,
		'qn': 'Watcher',
		'atk': 4,
		'hp': 4,
		'lvl': 4,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion4/floatingWatcher.png',
		'img_discovery': './img/discovery_minion4/floatingWatcher.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_floatingWatcher,
			'target': None,
			'buff': 2,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'goldgrubber': {
		'gold': False,
		'qn': 'Goldgrubber',
		'atk': 2,
		'hp': 2,
		'lvl': 4,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion4/goldgrubber.png',
		'img_discovery': './img/discovery_minion4/goldgrubber.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_goldgrubber,
			'target': None,
			'buff': 2,
			'trigger': 'end_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'heraldOfFlame': {
		'gold': False,
		'qn': 'Herald',
		'atk': 5,
		'hp': 6,
		'lvl': 4,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion4/heraldOfFlame.png',
		'img_discovery': './img/discovery_minion4/heraldOfFlame.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': ovk_heraldOfFlame,
		'cleave': False,
		'windfury': False,
		},
    'ironSensei': {
		'gold': False,
		'qn': 'Sensei',
		'atk': 2,
		'hp': 2,
		'lvl': 4,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion4/ironSensei.png',
		'img_discovery': './img/discovery_minion4/ironSensei.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_ironSensei,
			'target': 'meca',
			'buff': 2,
			'trigger': 'end_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'mechanoEgg': {
		'gold': False,
		'qn': 'Mechano-Egg',
		'atk': 0,
		'hp': 5,
		'lvl': 4,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion4/mechanoEgg.png',
		'img_discovery': './img/discovery_minion4/mechanoEgg.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_mechanoEgg],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'menagerieJug': {
		'gold': False,
		'qn': 'Menagerie',
		'atk': 3,
		'hp': 3,
		'lvl': 4,
		'archetype': 'neutral',
		'legendary': False,
		'img': '',
		'img_discovery': '',
		'battlecry': {
            'fc': btc_buff_random_minion,
            'target': None,
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'ripsnarlCaptain': {
		'gold': False,
		'qn': 'Ripsnarl',
		'atk': 3,
		'hp': 4,
		'lvl': 4,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion4/ripsnarlCaptain.png',
		'img_discovery': './img/discovery_minion4/ripsnarlCaptain.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_ripsnarlCaptain,
			'trigger': 'friendly_pirate_atk',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'savannahHighmane': {
		'gold': False,
		'qn': 'Savannah',
		'atk': 6,
		'hp': 5,
		'lvl': 4,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion4/savannahHighmane.png',
		'img_discovery': './img/discovery_minion4/savannahHighmane.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_savannahHighmane],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'securityRover': {
		'gold': False,
		'qn': 'Rover',
		'atk': 2,
		'hp': 6,
		'lvl': 4,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion4/securityRover.png',
		'img_discovery': './img/discovery_minion4/securityRover.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_rover,
			'trigger': 'wound',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'siegeBreaker': {
		'gold': False,
		'qn': 'Siegebreaker',
		'atk': 5,
		'hp': 8,
		'lvl': 4,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion4/siegeBreaker.png',
		'img_discovery': './img/discovery_minion4/siegeBreaker.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': {
			'fc': pas_murlocWarleader_southseaCaptain_malGanis_siegeBreaker,
			'target': 'demon',
			'buff': 1,
			'trigger': 'present',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_siegeBreaker,
			'trigger': 'present',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'southseaStrongarm': {
		'gold': False,
		'qn': 'Strongarm',
		'atk': 5,
		'hp': 4,
		'lvl': 4,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion4/southseaStrongarm.png',
		'img_discovery': './img/discovery_minion4/southseaStrongarm.png',
		'battlecry': {
            'fc': btc_southseaStrongarm,
            'target': 'pirate',
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'toxfin': {
		'gold': False,
		'qn': 'Toxfin',
		'atk': 1,
		'hp': 2,
		'lvl': 4,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion4/toxfin.png',
		'img_discovery': './img/discovery_minion4/toxfin.png',
		'battlecry': {
            'fc': btc_toxfin,
            'target': 'murloc',
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'virmenSensei': {
		'gold': False,
		'qn': 'Virmen',
		'atk': 4,
		'hp': 5,
		'lvl': 4,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion4/virmenSensei.png',
		'img_discovery': './img/discovery_minion4/virmenSensei.png',
		'battlecry': {
            'fc': btc_buff_one_minion,
            'target': 'beast',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    # TIER 3
    'bloodsailCannoneer': {
		'gold': False,
		'qn': 'Cannoneer',
		'atk': 4,
		'hp': 2,
		'lvl': 3,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion3/bloodsailCannoneer.png',
		'img_discovery': './img/discovery_minion3/bloodsailCannoneer.png',
		'battlecry': {
            'fc': btc_buff_atk_all_minion,
            'target': 'pirate',
            'buff': 3,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'bronzeWarden': {
		'gold': False,
		'qn': 'Bronze',
		'atk': 2,
		'hp': 1,
		'lvl': 3,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion3/bronzeWarden.png',
		'img_discovery': './img/discovery_minion3/bronzeWarden.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':True,
		'reborn': True,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'coldlightSeer': {
		'gold': False,
		'qn': 'Coldlight',
		'atk': 2,
		'hp': 3,
		'lvl': 3,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion3/coldlightSeer.png',
		'img_discovery': './img/discovery_minion3/coldlightSeer.png',
		'battlecry': {
            'fc': btc_buff_hp_all_minion,
            'target': 'murloc',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'crowdFavorite': {
		'gold': False,
		'qn': 'Favorite',
		'atk': 4,
		'hp': 4,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion3/crowdFavorite.png',
		'img_discovery': './img/discovery_minion3/crowdFavorite.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_wrathWeaver_saltyLooter_crowdFavorite_rabidSaurolisk,
			'target': 'battlecry',
			'buff': 1,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'crystalweaver': {
		'gold': False,
		'qn': 'Crystal',
		'atk': 5,
		'hp': 4,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion3/crystalweaver.png',
		'img_discovery': './img/discovery_minion3/crystalweaver.png',
		'battlecry': {
            'fc': btc_buff_all_minion,
            'target': 'demon',
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'deflectOBot': {
		'gold': False,
		'qn': 'Deflect-o-Bot',
		'atk': 3,
		'hp': 2,
		'lvl': 3,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion3/deflectOBot.png',
		'img_discovery': './img/discovery_minion3/deflectOBot.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_deflectOBot,
			'trigger': 'friendly_summon',
			},
		'shield':True,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'felfinNavigator': {
		'gold': False,
		'qn': 'Navigator',
		'atk': 4,
		'hp': 4,
		'lvl': 3,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion3/felfinNavigator.png',
		'img_discovery': './img/discovery_minion3/felfinNavigator.png',
		'battlecry': {
            'fc': btc_buff_all_minion,
            'target': 'murloc',
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'hangryDragon': {
		'gold': False,
		'qn': 'Hangry',
		'atk': 4,
		'hp': 4,
		'lvl': 3,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion3/hangryDragon.png',
		'img_discovery': './img/discovery_minion3/hangryDragon.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_hangryDragon,
			'target': None,
			'buff': 2,
			'trigger': 'start_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'houndMaster': {
		'gold': False,
		'qn': 'Houndmaster',
		'atk': 4,
		'hp': 3,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion3/houndMaster.png',
		'img_discovery': './img/discovery_minion3/houndMaster.png',
		'battlecry': {
            'fc': btc_houndMaster,
            'target': 'beast',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'impGangBoss': {
		'gold': False,
		'qn': 'Gang Boss',
		'atk': 2,
		'hp': 4,
		'lvl': 3,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion3/impGangBoss.png',
		'img_discovery': './img/discovery_minion3/impGangBoss.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_imppGang,
			'trigger': 'wound',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'infestedWolf': {
		'gold': False,
		'qn': 'Wolf',
		'atk': 3,
		'hp': 3,
		'lvl': 3,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion3/infestedWolf.png',
		'img_discovery': './img/discovery_minion3/infestedWolf.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_infestedWolf],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'khadgar': {
		'gold': False,
		'qn': 'Khadgar',
		'atk': 2,
		'hp': 2,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion3/khadgar.png',
		'img_discovery': './img/discovery_minion3/khadgar.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'monstrousMacaw': {
		'gold': False,
		'qn': 'Macaw',
		'atk': 3,
		'hp':2,
		'lvl': 3,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion2/monstrousMacaw.png',
		'img_discovery': './img/discovery_minion2/monstrousMacaw.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_monstrousMacaw,
			'trigger': 'after_attacks',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'packLeader': {
		'gold': False,
		'qn': 'Leader',
		'atk': 3,
		'hp': 3,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion3/packLeader.png',
		'img_discovery': './img/discovery_minion3/packLeader.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_packLeader,
			'target': 'beast',
			'buff': 3,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_packLeader,
			'trigger': 'friendly_summon',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'pilotedShredder': {
		'gold': False,
		'qn': 'Shredder',
		'atk': 4,
		'hp': 3,
		'lvl': 3,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion3/pilotedShredder.png',
		'img_discovery': './img/discovery_minion3/pilotedShredder.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_pilotedShredder],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'replicatingMenace': {
		'gold': False,
		'qn': 'Menace',
		'atk': 3,
		'hp': 1,
		'lvl': 3,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion3/replicatingMenace.png',
		'img_discovery': './img/discovery_minion3/replicatingMenace.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_replicatingMenace],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': True,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'saltyLooter': {
		'gold': False,
		'qn': 'Looter',
		'atk': 3,
		'hp': 3,
		'lvl': 3,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion3/saltyLooter.png',
		'img_discovery': './img/discovery_minion3/saltyLooter.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_wrathWeaver_saltyLooter_crowdFavorite_rabidSaurolisk,
			'target': 'pirate',
			'buff': 1,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'screwjankClunker': {
		'gold': False,
		'qn': 'Clunker',
		'atk': 2,
		'hp': 5,
		'lvl': 3,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion3/screwjankClunker.png',
		'img_discovery': './img/discovery_minion3/screwjankClunker.png',
		'battlecry': {
            'fc': btc_buff_one_minion,
            'target': 'meca',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'shifterZerus': {
		'gold': False,
		'qn': 'Zerus',
		'atk': 1,
		'hp': 1,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion3/shifterZerus.png',
		'img_discovery': './img/discovery_minion3/shifterZerus.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_shifterZerus,
			'target': None,
			'buff': None,
			'trigger': 'start_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'soulJunggler': {
		'gold': False,
		'qn': 'Juggler',
		'atk': 3,
		'hp': 3,
		'lvl': 3,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion3/soulJunggler.png',
		'img_discovery': './img/discovery_minion3/soulJunggler.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_soulJunggler,
			'trigger': 'friendly_dead',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'theBeast': {
		'gold': False,
		'qn': 'theBeast',
		'atk': 9,
		'hp': 7,
		'lvl': 3,
		'archetype': 'beast',
		'legendary': True,
		'img': './img/minion3/theBeast.png',
		'img_discovery': './img/discovery_minion3/theBeast.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_theBeast],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'twilightEmissary': {
		'gold': False,
		'qn': 'Twilight',
		'atk': 4,
		'hp': 4,
		'lvl': 3,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion3/twilightEmissary.png',
		'img_discovery': './img/discovery_minion3/twilightEmissary.png',
		'battlecry': {
            'fc': btc_buff_one_minion,
            'target': 'dragon',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'yoHoOgre': {
		'gold': False,
		'qn': 'Yo-Ho-Ogre',
		'atk': 2,
		'hp': 8,
		'lvl': 3,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion3/yoHoOgre.png',
		'img_discovery': './img/discovery_minion3/yoHoOgre.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},

    # TIER 2
    'arcaneCannon': {
		'gold': False,
		'qn': 'Cannon',
		'atk': 2,
		'hp': 2,
		'lvl': 2,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion2/arcaneCannon.png',
		'img_discovery': './img/discovery_minion2/arcaneCannon.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_arcaneCannon,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'freedealingGambler': {
		'gold': False,
		'qn': 'Gambler',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion2/freedealingGambler.png',
		'img_discovery': './img/discovery_minion2/freedealingGambler.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_freedealingGambler,
			'target': None,
			'buff': 3,
			'trigger': 'sold',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'glyphGuardian': {
		'gold': False,
		'qn': 'Guardian',
		'atk': 2,
		'hp': 4,
		'lvl': 2,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion2/glyphGuardian.png',
		'img_discovery': './img/discovery_minion2/glyphGuardian.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_glyphGuardian,
			'trigger': 'attacks',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'harvestGolem': {
		'gold': False,
		'qn': 'Golem',
		'atk': 2,
		'hp': 3,
		'lvl': 2,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion2/harvestGolem.png',
		'img_discovery': './img/discovery_minion2/harvestGolem.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_harvestGolem],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'imprisoner': {
		'gold': False,
		'qn': 'Imprisoner',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion2/imprisoner.png',
		'img_discovery': './img/discovery_minion2/imprisoner.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_imprisoner],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'kaboomBot': {
		'gold': False,
		'qn': 'Kaboom',
		'atk': 2,
		'hp': 2,
		'lvl': 2,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion2/kaboomBot.png',
		'img_discovery': './img/discovery_minion2/kaboomBot.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_kaboomBot],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'kindlyGrandmother': {
		'gold': False,
		'qn': 'Grandmother',
		'atk': 1,
		'hp': 1,
		'lvl': 2,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion2/kindlyGrandmother.png',
		'img_discovery': './img/discovery_minion2/kindlyGrandmother.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_kindlyGrandmother],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'metaltoothLeaper': {
		'gold': False,
		'qn': 'Leaper',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion2/metaltoothLeaper.png',
		'img_discovery': './img/discovery_minion2/metaltoothLeaper.png',
		'battlecry': {
            'fc': btc_buff_atk_all_minion,
            'target': 'meca',
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'murlocWarleader': {
		'gold': False,
		'qn': 'Warleader',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion2/murlocWarleader.png',
		'img_discovery': './img/discovery_minion2/murlocWarleader.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_murlocWarleader_southseaCaptain_malGanis_siegeBreaker,
			'target': 'murloc',
			'buff': 2,
			'trigger': 'present',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_murlocWarleader,
			'trigger': 'present',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'nathrezimOverseer': {
		'gold': False,
		'qn': 'Overseer',
		'atk': 2,
		'hp': 3,
		'lvl': 2,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion2/nathrezimOverseer.png',
		'img_discovery': './img/discovery_minion2/nathrezimOverseer.png',
		'battlecry': {
            'fc': btc_buff_one_minion,
            'target': 'demon',
            'buff': 2,
			},
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'oldMurkEye': {
		'gold': False,
		'qn': 'Murk-Eye',
		'atk': 2,
		'hp': 4,
		'lvl': 2,
		'archetype': 'murloc',
		'legendary': True,
		'img': './img/minion2/oldMurkEye.png',
		'img_discovery': './img/discovery_minion2/oldMurkEye.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_oldMurkEye,
			'target': 'murloc',
			'buff': 1,
			'trigger': 'present',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'pogoHopper': {
		'gold': False,
		'qn': 'Pogo',
		'atk': 1,
		'hp': 1,
		'lvl': 2,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion2/pogoHopper.png',
		'img_discovery': './img/discovery_minion2/pogoHopper.png',
		'battlecry': {
            'fc': btc_pogoHopper,
            'target': None,
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'rabidSaurolisk': {
		'gold': False,
		'qn': 'Saurolisk',
		'atk': 3,
		'hp': 2,
		'lvl': 2,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion2/rabidSaurolisk.png',
		'img_discovery': './img/discovery_minion2/rabidSaurolisk.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_wrathWeaver_saltyLooter_crowdFavorite_rabidSaurolisk,
			'target': 'deathrattle',
			'buff': 1,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'ratPack': {
		'gold': False,
		'qn': 'Rat Pack',
		'atk': 2,
		'hp': 2,
		'lvl': 2,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion2/ratPack.png',
		'img_discovery': './img/discovery_minion2/ratPack.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_ratPack],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'southseaCaptain': {
		'gold': False,
		'qn': 'Captain',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion2/southseaCaptain.png',
		'img_discovery': './img/discovery_minion2/southseaCaptain.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_murlocWarleader_southseaCaptain_malGanis_siegeBreaker,
			'target': 'pirate',
			'buff': 1,
			'trigger': 'present',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_southseaCaptain,
			'trigger': 'present',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'spawnOfNzoth': {
		'gold': False,
		'qn': 'Spawn',
		'atk': 2,
		'hp': 2,
		'lvl': 2,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion2/spawnOfNzoth.png',
		'img_discovery': './img/discovery_minion2/spawnOfNzoth.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_spawnOfNzoth],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'stewardOfTime': {
		'gold': False,
		'qn': 'Steward',
		'atk': 3,
		'hp': 4,
		'lvl': 2,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion2/stewardOfTime.png',
		'img_discovery': './img/discovery_minion2/stewardOfTime.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_stewardOfTime,
			'target': None,
			'buff': 1,
			'trigger': 'sold',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'unstableGhoul': {
		'gold': False,
		'qn': 'Ghoul',
		'atk': 1,
		'hp': 3,
		'lvl': 2,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion2/unstableGhoul.png',
		'img_discovery': './img/discovery_minion2/unstableGhoul.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_unstableGhoul],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'waxriderTogwaggle': {
		'gold': False,
		'qn': 'Towaggle',
		'atk': 1,
		'hp': 2,
		'lvl': 2,
		'archetype': 'neutral',
		'legendary': True,
		'img': './img/minion2/waxriderTogwaggle.png',
		'img_discovery': './img/discovery_minion2/waxriderTogwaggle.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_waxriderTogwaggle,
			'trigger': 'friendly_dragon_kill',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'menagerieMug': {
		'gold': False,
		'qn': 'Menagerie',
		'atk': 2,
		'hp': 2,
		'lvl': 2,
		'archetype': 'neutral',
		'legendary': False,
		'img': '',
		'img_discovery': '',
		'battlecry': {
            'fc': btc_buff_random_minion,
            'target': None,
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
	
	# TIER 1
    'alleycat': {
		'gold': False,
		'qn': 'Alleycat',
		'atk': 1,
		'hp': 1,
		'lvl': 1,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion1/alleycat.png',
		'img_discovery': './img/discovery_minion1/alleycat.png',
		'battlecry': {
            'fc': btc_token,
            'target': None,
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'deckSwabbie': {
		'gold': False,
		'qn': 'Swabbie',
		'atk': 2,
		'hp': 2,
		'lvl': 1,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion1/deckSwabbie.png',
		'img_discovery': './img/discovery_minion1/deckSwabbie.png',
		'battlecry': {
            'fc': btc_deckSwabbie,
            'target': None,
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'dragonspawnLieutenant': {
		'gold': False,
		'qn': 'Lieutenant',
		'atk': 2,
		'hp': 3,
		'lvl': 1,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion1/dragonspawnLieutenant.png',
		'img_discovery': './img/discovery_minion1/dragonspawnLieutenant.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'fiendishServant': {
		'gold': False,
		'qn': 'Servant',
		'atk': 2,
		'hp': 1,
		'lvl': 1,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion1/fiendishServant.png',
		'img_discovery': './img/discovery_minion1/fiendishServant.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_fiendishServant],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'mecharoo': {
		'gold': False,
		'qn': 'Mecharoo',
		'atk': 1,
		'hp': 1,
		'lvl': 1,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion1/mecharoo.png',
		'img_discovery': './img/discovery_minion1/mecharoo.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_mecharoo],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'microMachine': {
		'gold': False,
		'qn': 'Machine',
		'atk': 1,
		'hp': 2,
		'lvl': 1,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion1/microMachine.png',
		'img_discovery': './img/discovery_minion1/microMachine.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_microMachine,
			'target': None,
			'buff': 1,
			'trigger': 'start_turn',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'murlocTidecaller': {
		'gold': False,
		'qn': 'Tidecaller',
		'atk': 1,
		'hp': 2,
		'lvl': 1,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion1/murlocTidecaller.png',
		'img_discovery': './img/discovery_minion1/murlocTidecaller.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_murlocTidecaller,
			'target': 'murloc',
			'buff': 1,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'murlocTidehunter': {
		'gold': False,
		'qn': 'Tidehunter',
		'atk': 2,
		'hp': 1,
		'lvl': 1,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion1/murlocTidehunter.png',
		'img_discovery': './img/discovery_minion1/murlocTidehunter.png',
		'battlecry': {
            'fc': btc_token,
            'target': None,
            'buff': None,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'redWhelp': {
		'gold': False,
		'qn': 'Red Whelp',
		'atk': 1,
		'hp': 2,
		'lvl': 1,
		'archetype': 'dragon',
		'legendary': False,
		'img': './img/minion1/redWhelp.png',
		'img_discovery': './img/discovery_minion1/redWhelp.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_redWhelp,
			'trigger': 'start_of_fight',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'righteousProtector': {
		'gold': False,
		'qn': 'Protector',
		'atk': 1,
		'hp': 1,
		'lvl': 1,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion1/righteousProtector.png',
		'img_discovery': './img/discovery_minion1/righteousProtector.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':True,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'rockpoolHunter': {
		'gold': False,
		'qn': 'Hunter',
		'atk': 2,
		'hp': 3,
		'lvl': 1,
		'archetype': 'murloc',
		'legendary': False,
		'img': './img/minion1/rockpoolHunter.png',
		'img_discovery': './img/discovery_minion1/rockpoolHunter.png',
		'battlecry': {
            'fc': btc_buff_one_minion,
            'target': 'murloc',
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'scallyWag': {
		'gold': False,
		'qn': 'Scallywag',
		'atk': 2,
		'hp': 1,
		'lvl': 1,
		'archetype': 'pirate',
		'legendary': False,
		'img': './img/minion1/scallyWag.png',
		'img_discovery': './img/discovery_minion1/scallyWag.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_scallyWag],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'scavengingHyena': {
		'gold': False,
		'qn': 'Hyena',
		'atk': 2,
		'hp': 2,
		'lvl': 1,
		'archetype': 'beast',
		'legendary': False,
		'img': './img/minion1/scavengingHyena.png',
		'img_discovery': './img/discovery_minion1/scavengingHyena.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt_scavengingHyena,
			'trigger': 'friendly_dead',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'selflessHero': {
		'gold': False,
		'qn': 'Selfless',
		'atk': 2,
		'hp': 1,
		'lvl': 1,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion1/selflessHero.png',
		'img_discovery': './img/discovery_minion1/selflessHero.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [dht_selflessHero],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'vulgarHomunculus': {
		'gold': False,
		'qn': 'Homunculus',
		'atk': 2,
		'hp': 4,
		'lvl': 1,
		'archetype': 'demon',
		'legendary': False,
		'img': './img/minion1/vulgarHomunculus.png',
		'img_discovery': './img/discovery_minion1/vulgarHomunculus.png',
		'battlecry': {
            'fc': btc_vulgarHomunculus,
            'target': None,
            'buff': 2,
        },
		'poisonous': False,
		'taunt': True,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'wrathWeaver': {
		'gold': False,
		'qn': 'Wrath',
		'atk': 1,
		'hp': 1,
		'lvl': 1,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion1/wrathWeaver.png',
		'img_discovery': './img/discovery_minion1/wrathWeaver.png',
		'battlecry': False,
		'poisonous': False,
		'taunt': False,
		'passive': {
			'fc': pas_wrathWeaver_saltyLooter_crowdFavorite_rabidSaurolisk,
			'target': 'demon',
			'buff': 2,
			'trigger': 'play',
			},
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
}

ARCHETYPES = ('dragon', 'beast', 'murloc', 'demon', 'pirate', 'meca')
	
MINIONS_LEGENDARY = [name for name in MINIONS if MINIONS[name]['legendary']]
MINIONS_DEATHRATTLE = [name for name in MINIONS if MINIONS[name]['deathrattle']]
MINION_BY_ARCHETYPE = {
    'dragon': [name for name in MINIONS if MINIONS[name]['archetype'] == 'dragon'],
    'beast': [name for name in MINIONS if MINIONS[name]['archetype'] == 'beast'],
    'murloc': [name for name in MINIONS if MINIONS[name]['archetype'] == 'murloc'],
    'demon': [name for name in MINIONS if MINIONS[name]['archetype'] == 'demon'],
    'pirate': [name for name in MINIONS if MINIONS[name]['archetype'] == 'pirate'],
    'meca': [name for name in MINIONS if MINIONS[name]['archetype'] == 'meca'],
}

MINIONS_BY_TIER = [
    [name for name in MINIONS if MINIONS[name]['lvl'] == 1],
    [name for name in MINIONS if MINIONS[name]['lvl'] == 2],
    [name for name in MINIONS if MINIONS[name]['lvl'] == 3],
    [name for name in MINIONS if MINIONS[name]['lvl'] == 4],
    [name for name in MINIONS if MINIONS[name]['lvl'] == 5],
    [name for name in MINIONS if MINIONS[name]['lvl'] == 6],
]

# MAYBE ADD FUNCTION TO THIS DICT AND USE ON BTC_MEGASAUR
BUFF_MEGASAUR = {
    'crackling': {
        'text': 'Shield',
        'img_discovery': './img/discovery_megasaur/crackling.png',
        },
    'flaming': {
        'text': '+3attacks',
        'img_discovery': './img/discovery_megasaur/flaming.png',
        },
    'spores': {
        'text': 'drt: 2*(1/1)',
        'img_discovery': './img/discovery_megasaur/spores.png',
        },
    'poison': {
        'text': 'Poisonous',
        'img_discovery': './img/discovery_megasaur/poison.png',
        },
    'massive': {
        'text': 'Taunt',
        'img_discovery': './img/discovery_megasaur/massive.png',
        },
    'volcanic': {
        'text': '+1/+1',
        'img_discovery': './img/discovery_megasaur/volcanic.png',
        },
    'lightning': {
        'text': 'Windfury',
        'img_discovery': './img/discovery_megasaur/lightning.png',
        },
    'carapace': {
        'text': '+3health',
        'img_discovery': './img/discovery_megasaur/carapace.png',
    },
}

WITHOUT_BEAST = ('alleycat', 'scavengingHyena', 'kindlyGrandmother', 'rabidSaurolisk', 'ratPack', 'infestedWolf', 'monstrousMacaw', 
            'theBeast', 'caveHydra', 'savannahHighmane', 'goldrinnTheGreatWolf', 'ironhideDirehorn', 'ghastcoiler', 'mamaBear', 'maexxna', 
            'packLeader', 'houndMaster', 'virmenSensei')
WITHOUT_DEMON = ('fiendishServant','vulgarHomunculus','imprisoner','nathrezimOverseer','impGangBoss','floatingWatcher',
            'siegeBreaker','annihilanBattlemaster','malGanis','voidlord','impMama','wrathWeaver','crystalweaver','soulJunggler')
WITHOUT_MECA = ('mecharoo','microMachine','harvestGolem','kaboomBot','metaltoothLeaper','pogoHopper','deflectOBot','pilotedShredder',
            'replicatingMenace','screwjankClunker','annoyOModule','ironSensei','mechanoEgg','securityRover','junkbot','sneedsOldShredder',
            'foeReaper4000','kangorsApprentice')
WITHOUT_MURLOC = ('murlocTidecaller','murlocTidehunter','rockpoolHunter','murlocWarleader','oldMurkEye','coldlightSeer',
            'felfinNavigator','toxfin','kingBagurgle','primalfinLookout','gentleMegasaur')
WITHOUT_DRAGON = ('dragonspawnLieutenant','redWhelp','glyphGuardian','stewardOfTime','bronzeWarden','hangryDragon','twilightEmissary',
            'cobaltScalebane','drakonidEnforcer','heraldOfFlame','murozond','razorgoreTheUntamed','kalecgosArcaneAspect','nadinaTheRed',
            'waxriderTogwaggle')
WITHOUT_PIRATE = ('deckSwabbie','scallyWag','freedealingGambler','southseaCaptain','yoHoOgre','saltyLooter','bloodsailCannoneer','southseaStrongarm',
	'ripsnarlCaptain','goldgrubber','capnHoggarr','natPagleExtremeAngler','seabreakerGoliath','dreadAdmiralEliza', 'theTideRazor')

WITHOUT_MINIONS = {
	'beast': WITHOUT_BEAST,
	'demon': WITHOUT_DEMON,
	'meca': WITHOUT_MECA,
	'murloc': WITHOUT_MURLOC,
	'dragon': WITHOUT_DRAGON,
	'pirate': WITHOUT_PIRATE,
}

MINIONS_POOL = [
    {name: {'copy': 16, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 1},
    {name: {'copy': 15, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 2},
    {name:{'copy': 13, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 3},
    {name:{'copy': 11, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 4},
    {name:{'copy': 9, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 5},
    {name:{'copy': 7, 'lvl': MINIONS[name]['lvl'], 'archetype': MINIONS[name]['archetype']} for name in MINIONS if MINIONS[name]['lvl'] == 6},
]

# MINIONS_POOL[5]['amalgadon']['copy'] = 400
# MINIONS_POOL[1]['menagerieMug']['copy'] = 300
# MINIONS_POOL[3]['menagerieJug']['copy'] = 300
# MINIONS_POOL[0]['deckSwabbie']['copy'] = 13
# MINIONS_POOL[0]['alleycat']['copy'] = 400
# MINIONS_POOL[2]['replicatingMenace']['copy'] = 250
#yoanbousquet45

ALL_POOLS = {'beast': [], 'murloc': [],'demon': [],'meca': [],'dragon': [], 'pirate': []}

for minions in MINIONS_POOL:
    ADD_GOOD_MINIONS = {'beast': {}, 'murloc': {},'demon': {}, 'meca': {},'dragon': {}, 'pirate': {}}
    for minion in minions:
        for archetype in ARCHETYPES:
            if minion not in WITHOUT_MINIONS[archetype]:
                ADD_GOOD_MINIONS[archetype][minion] = {'copy': minions[minion]['copy'], 'lvl': minions[minion]['lvl'], 'archetype': minions[minion]['archetype']}

    for archetype in ARCHETYPES:
        ALL_POOLS[archetype].append(ADD_GOOD_MINIONS[archetype])




# https://www.youtube.com/watch?v=Z19vrGTBrMc&t=246s at 20min30



graveyard = {
	'zoobot': {
		'gold': False,
		'qn': 'Zoobot',
		'atk': 3,
		'hp': 3,
		'lvl': 2,
		'archetype': 'meca',
		'legendary': False,
		'img': './img/minion2/zoobot.png',
		'img_discovery': './img/discovery_minion2/zoobot.png',
		'battlecry': {
            'fc': btc_buff_random_minion,
            'target': {'dragon', 'beast', 'murloc'},
            'buff': 1,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		},
    'menagerieMagician': {
		'gold': False,
		'qn': 'Menagerie',
		'atk': 4,
		'hp': 4,
		'lvl': 4,
		'archetype': 'neutral',
		'legendary': False,
		'img': './img/minion4/menagerieMagician.png',
		'img_discovery': './img/discovery_minion4/menagerieMagician.png',
		'battlecry': {
            'fc': btc_buff_random_minion,
            'target': {'dragon', 'beast', 'murloc'},
            'buff': 2,
        },
		'poisonous': False,
		'taunt': False,
		'passive': False,
		'n_passive': 0,
		'deathrattle': [],
		'fight': {
			'do': fgt,
			'trigger': '',
			},
		'shield':False,
		'reborn': False,
		'magnetic': False,
		'overkill': False,
		'cleave': False,
		'windfury': False,
		}
}
    

