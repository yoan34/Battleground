"""
Class Scanner analyses the screen and return the boolean response or objects. It can analyse:
    -The shop and return the minions.
    -The discovery's cards and return the minions.
    -The Heroes on the start game and return the better one.
Manage some usefull case like:
    -wait the shop, wait the game start, wait the turn end...
"""
import pyautogui
import time

from Components.Mouse import Mouse
from Components.Hero import Hero
from Components.Minion import Minion

from constants.position import *
from constants.heroes import TIER_LIST
from constants.minions import MINIONS, MINIONS_BY_TIER, MINION_BY_ARCHETYPE, BUFF_MEGASAUR

# MAYBE HAND DIRECT ON PLAYER AND CHANGE 'bot_chose_a_hero'
class Scanner(Mouse):

    def __init__(self):
        pass

    def see_discovery(self, shop_lvl=1, nature='triplet'):
        """
        Scans the screen and display the correct cards by matching some
        images.
        Manage some specific case like:
            -discover by the minion 'primalfindLook'
            -discover by the minion 'Megasaur'
        """
        all_names, search_in = [], MINIONS.copy()
        if nature == 'primal':
            cards = MINION_BY_ARCHETYPE['murloc'].copy()
        elif nature == 'megasaur':
            cards = search_in = BUFF_MEGASAUR.copy()
        else:
            lvl = shop_lvl + 1 if shop_lvl < 6 else 6
            cards = MINIONS_BY_TIER[lvl-1].copy()
        for i in range(3):
            screen, found, confidence = pyautogui.screenshot(region=(444+389*i, 320, 256, 220)), False, 0.7
            while not found:
                for name in cards:
                    match_name = pyautogui.locate(search_in[name]['img_discovery'], screen, confidence=confidence)
                    if match_name:
                        all_names.append(name)
                        found = True
                        break
                confidence = round(confidence-0.1, 2)
                if not confidence:
                    print('Error: Not find matching with 0 confidence.')
                    break        
        return all_names

    def start(self, launch_game=False):
        """
        Scans the screen and wait until it match the start's image.
        """
        print("{}Start a Game{}\n".format('-'*20,'-'*20).center(152))
        if launch_game:
            # Have to search battlenet..-> hearsthone--> batlleground--> play
            pass
        else:
            screen, waiting = pyautogui.screenshot(region=(1240, 730, 400, 300)), 0
            while pyautogui.locate("./img/others/button_play.png", screen, confidence=0.8) is None:
                s = 'Waiting game {}s...'.format(waiting)
                print(s.rjust(100-len(s)), end='\r')
                screen = pyautogui.screenshot(region=(1240, 730, 400, 300))
                time.sleep(1)
                waiting += 1
                if waiting == 180:
                    print(" {}s no answer, stop the game.".format(waiting))
                    return
            self.bot_target_btn_start()

    def wait_game_start(self):
        """
        Scans the screen and wait until it match the heroes's image.
        """
        screen, waiting = pyautogui.screenshot(region=(800, 740, 300, 190)), 0
        while pyautogui.locate('./img/others/btn_hero_ok.png', screen, confidence=0.8) is None:
            screen = pyautogui.screenshot(region=(800, 740, 300, 190)) 
            s = "Waiting heroes: {}s...".format(waiting)
            print(s.rjust(100-len(s)), end='\r')
            time.sleep(1)
            waiting += 1
            if waiting == 300:
                print(" {}s no answer, stop the game.".format(waiting))
                return

    def wait_the_shop(self):
        """
        Scans the screen and wait until it match the shop's image.
        """
        screen, waiting = pyautogui.screenshot(region=(900,50,300,300)), 0
        while pyautogui.locate('./img/others/refresh.png', screen, confidence=0.7) is None:
            print('Waiting bob tavern: {}s...'.format(waiting).rjust(83), end='\r')
            screen = pyautogui.screenshot(region=(900,50,300,300))
            time.sleep(1)
            waiting += 1
            if waiting == 180:
                print(" {}s no answer, stop the game.".format(waiting))
                return

    def bot_chose_a_hero(self):
        """
        Scans the screen and pick the best hero.
        """
        print('Choose the best Hero...'.rjust(83), end='\r')
        screen, avatar, confidence = pyautogui.screenshot(region=ZONE_HEROES), False, 0.8
        while not avatar:
            for hero in TIER_LIST:
                position = pyautogui.locate(TIER_LIST[hero]['img'], screen, confidence=confidence)
                if position is not None:
                    avatar = Hero(hero, *[value for value in TIER_LIST[hero].values()])
                    break
            confidence = round(confidence-0.1, 2)
            if not confidence:
                print('Error: Not find matching with 0 confidence.')
                break
        x, pos = position[0], -1
        if x < 100: pos = 1
        elif x < 350: pos = 2
        elif x < 650: pos = 3
        else: pos = 4
        self.bot_target_hero(pos)
        return avatar
    
    def see_shop(self, shop_lvl, length):
        """
        Scans the shop and show all minions that match the corresponds images.
        """
        all_minions = []
        if shop_lvl < 6: shop_lvl += 1
        for pos in range(1, length+1):
            zone, confidence = (890 + (2*pos - length -1)*69, 290, 180, 210), 0.8
            screen = pyautogui.screenshot(region=(zone[0]+30, 290, 70, 60))
            for i in range(shop_lvl, 0, -1):
                lvl = pyautogui.locate('./img/others/lvl{}.png'.format(i), screen, confidence=0.75)
                if lvl is not None:
                    lvl = i
                    break
            minions = list(filter(lambda minion: MINIONS[minion]['lvl'] == lvl, MINIONS))
            screen, found, confidence = pyautogui.screenshot(region=zone), False, 0.8
            while not found:
                for minion in minions: # MAYBE CREATE FUNCTION MATCHING MINION
                    match_minion = pyautogui.locate(MINIONS[minion]['img'], screen, confidence=confidence)
                    if match_minion:
                        all_minions.append(Minion(minion,*[value for value in MINIONS[minion].values()]))
                        found = True
                        break
                confidence = round(confidence-0.1, 2)
                if not confidence:
                    print('Error: Not find matching with 0 confidence.')
                    break
        return all_minions

    def is_in_fight(self):
        """
        Scans the screen and wait until it match the fight's image.
        """
        screen = pyautogui.screenshot(region=(1400,420,250,140))
        if pyautogui.locate('./img/others/btn_fight.png', screen, confidence=0.7) is not None:
            return True
        return False
    
    def is_in_tavern(self):
        """
        Scans the screen and wait until it match the refresh's image.
        """
        screen = pyautogui.screenshot(region=(900,50,300,300))
        if pyautogui.locate('./img/others/refresh.png', screen, confidence=0.7) is not None:
            return True
        return False

    def is_ending_turn(self):
        """
        Scans the screen and wait until it match the last ten second's image before the turn ends.
        """
        screen = pyautogui.screenshot(region=(1550,480,40,40))
        if pyautogui.locate('./img/others/ending_turn.png', screen, confidence=0.8) is not None:
            return True
        return False











