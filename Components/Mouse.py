"""
This class manage all mouse moves necessary for play.
-target minion     -Freeze
-Buy minion        -Refresh
-Sold minion       -Hero power
-Swap minion       -Start a game
-Play minion       -choose Hero
"""

import random
import pyautogui

from constants.position import *

class Mouse:
    
    def __init__(self):
        pass

    def bot_target_hero(self, pos):
        """ Compute, move and click on the specific hero's position. """
        x, y = 430 + ((pos-1)*295) + ZONE_RANDOM_HERO[0], 440 + ZONE_RANDOM_HERO[1]
        pyautogui.moveTo(x, y, random.randint(3,8)/10)
        pyautogui.click(interval=round(random.random(), 2))
        pyautogui.moveTo(900+ZONE_RANDOM_HERO_OK[0],
        820 + ZONE_RANDOM_HERO_OK[1], random.randint(3,8)/10)
        pyautogui.click()

    def bot_target_minion(self, pos, length, y, t):
        """ Compute and move on the specific minion's position. """
        x = 921 + (2 * pos - length - 1) * 69 + ZONE_RANDOM_MINION[0]
        y = y + ZONE_RANDOM_MINION[1]
        pyautogui.moveTo(x, y, random.randint(2, t)/10) # Change T and perform random 

    def bot_buff_minion(self, pos, length):
        """
        Calls the 'bot_target_minion' method and click on the specific minion.
        Usefull for a minion's battlecry.
        """
        self.bot_target_minion(pos, length,545, 5)
        pyautogui.click()

    def bot_buy_minion(self, pos, length):
        """
        Calls the 'bot_target_minion' method and click on the specific minion,
        and drags it to the hand.
        """
        self.bot_target_minion(pos, length, 360, 5)
        pyautogui.dragTo(X_BUY_MINION, Y_BUY_MINION, random.randint(2,5)/10)

    def bot_sold_minion(self, pos, length):
        """
        Calls the 'bot_target_minion' method and click on the specific minion,
        and drags it to the shop.
        """
        self.bot_target_minion(pos, length, 545, 5)
        pyautogui.dragTo(X_SOLD_MINION, Y_SOLD_MINION,random.randint(2,5)/10)
    
    def bot_play_minion(self, pos, length, direction, len_board):
        """
        Move to the specific minion's hand position and drags to the specific
        board's position.
        """
        x, y = ZONE_HAND_MINION[length-1][pos]
        pyautogui.moveTo(x, y, random.randint(2,5)/10, pyautogui.easeOutQuad)
        x, y = 850 + (2 * direction - len_board - 1) * 69 + ZONE_RANDOM_MINION[0], 545 + ZONE_RANDOM_MINION[1]
        pyautogui.dragTo(x, y, random.randint(2,5)/10, pyautogui.easeOutQuad)

    def bot_swap_minion(self, first, second, length):
        """Calls the 'bot_target_minion' and swap position with other target minion. """
        self.bot_target_minion(first, length, 545, 4)
        pyautogui.mouseDown(button='left')
        self.bot_target_minion(second, length, 545, 5)
        pyautogui.mouseUp(button='left')
        
    def bot_upgrade(self):
        """ Move and click on the specific upgrade's zone. """
        pyautogui.moveTo(X_UPGRADE, Y_UPGRADE, random.randint(2,5)/10)
        pyautogui.click(interval=round(random.random(), 2))

    def bot_refresh(self):
        """ Move and click on the specific refresh's zone. """
        pyautogui.moveTo(X_REFRESH, Y_REFRESH, random.randint(2,5)/10)
        pyautogui.click(interval=round(random.random(), 2))

    def bot_freeze(self):
        """ Move and click on the specific freeze's zone. """
        pyautogui.moveTo(X_FREEZE, Y_FREEZE, random.randint(2,5)/10)
        pyautogui.click(interval=round(random.random(), 2))

    def bot_target_hero_power(self):
        """ Move and click on the specific hero power's zone. """
        pyautogui.moveTo(X_HERO_POWER, Y_HERO_POWER, random.randint(2,5)/10)
    
    def bot_discovery(self, pos):
        """ Compute, move and click on the specific discover's card. """
        x, y = 450 + (390*(pos-1)) + randint(1, 240), 350 + randint(1, 340)
        pyautogui.moveTo(x, y, random.randint(2,5)/10, pyautogui.easeOutQuad) 
        pyautogui.click()

    def bot_target_btn_start(self):
        """ Move and click on the specific start button's zone. """
        pyautogui.moveTo(1390 + randint(1, 110), 815 +randint(1, 100), random.randint(2,5)/10, pyautogui.easeOutQuad)
        pyautogui.click()

    def bot_end(self):
        # When finish click click for go to page 'play'
        pass

    def bot_target_nothing(self):
        """ Move on the specific nothing's zone """
        pyautogui.moveTo(1450 + ZONE_RANDOM_AFTER_ACTION[0], 20 + ZONE_RANDOM_AFTER_ACTION[1], 0.3)

    

    
    

    
    

