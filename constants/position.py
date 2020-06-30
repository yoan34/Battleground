from random import randint
######################################################################
# Any duration less than this is rounded to 0.0 to instantly move the mouse.
# pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
# Minimal number of seconds to sleep between mouse moves.
# pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
# The number of seconds to pause after EVERY public function call.
# pyautogui.PAUSE = 0  # Default: 0.1
########################################################################

ZONE_HEROES = (360, 340, 1200, 330)
ZONE_HERO_OK = (900, 820, 130, 70) # not necessary just click in x,y
ZONE_HERO_POWER = (1050, 720, 170, 190) # not necessary, click right (x,y)

ZONE_UPGRADE = (760, 160, 70, 90) # not necessary, click right (x,y)
ZONE_FREEZE = (1210, 135, 60, 75) # not necessary, click right (x,y)
ZONE_REFRESH = (1100, 160, 70, 80) # not necessary, click right (x,y)
ZONE_SHOP = (420, 250, 1030, 300) 

ZONE_BOARD = (420, 490, 1030, 205)
ZONE_HAND = (550, 915, 700, 160)

ZONE_BUY_MINION = (650, 800, 600, 279)
ZONE_SOLD_MINION = (800, 70, 300, 230) # Should confirm the ZONE in game

# OTHER CONST
LEN_SHOP = [3, 4, 4, 5, 5, 6]

# About some random landing zone
ZONE_RANDOM_MINION = (randint(1, 60), randint(1, 90))
ZONE_RANDOM_BUY = (randint(1, 600), randint(1, 279))
ZONE_RANDOM_SOLD = (randint(1, 300), randint(1, 230))
ZONE_RANDOM_UPGRADE = (randint(1, 70), randint(1, 90))
ZONE_RANDOM_REFRESH = (randint(1, 70), randint(1, 80))
ZONE_RANDOM_FREEZE = (randint(1, 60), randint(1, 75))
ZONE_RANDOM_HERO_POWER = (randint(1, 80), randint(1, 90))
ZONE_RANDOM_HERO = (randint(1, 190), randint(1, 190))
ZONE_RANDOM_HERO_OK = (randint(1, 130), randint(1, 60))
ZONE_RANDOM_AFTER_ACTION = (randint(1, 450), randint(1,220))

# ALL CONSTANTE MOVEMENT
X_BUY_MINION = 650 + ZONE_RANDOM_BUY[0]
Y_BUY_MINION = 800 + ZONE_RANDOM_BUY[1]

X_SOLD_MINION = 800 + ZONE_RANDOM_SOLD[0]
Y_SOLD_MINION = 70 + ZONE_RANDOM_MINION[1]

X_UPGRADE = 760 + ZONE_RANDOM_UPGRADE[0]
Y_UPGRADE = 160 + ZONE_RANDOM_UPGRADE[1]

X_REFRESH = 1100 + ZONE_RANDOM_REFRESH[0]
Y_REFRESH = 160 + ZONE_RANDOM_REFRESH[1]

X_FREEZE = 1210 + ZONE_RANDOM_FREEZE[0]
Y_FREEZE = 135 + ZONE_RANDOM_FREEZE[1]

X_HERO_POWER = 1100 + ZONE_RANDOM_HERO_POWER[0]
Y_HERO_POWER = 780 + ZONE_RANDOM_HERO_POWER[1]

# ZONE MINION IN HAND WITH 5 CARDS MAX
ZONE_HAND_MINION = [
    {1:(860 + randint(1,120), 940 + randint(1,135))
	},
    {1: (800 + randint(1,110), 940 + randint(1,135)), 2: (930 + randint(1,110), 940 + randint(1,135))
	},
    {1: (730 + randint(1, 110), 940 + randint(1, 135)), 2: (865 + randint(1, 110), 940 + randint(1, 135)),
        3: (1000 + randint(1, 110), 940 + randint(1, 135))
	},
    {1: (666 + randint(1, 100), 970 + randint(1, 105)), 2: (800 + randint(1, 100), 950 + randint(1, 140)),
        3: (940 + randint(1, 100), 960 + randint(1, 115)), 4: (1080 + randint(1, 80), 990 + randint(1, 85))
	},
    {1: (670 + randint(1, 60), 980 + randint(1, 90)), 2: (770 + randint(1, 70), 960 + randint(1, 110)),
        3: (870 + randint(1, 80), 950 + randint(1, 120)), 4: (980 + randint(1, 70), 970 + randint(1, 100)),
        5: (1090 + randint(1, 80), 1000 + randint(1, 70))
	},
]
ZONE_PLAY_MINION = {
    'left': (400 + randint(1, 130), 520 + randint(1, 120)),
    'middle': (930 + randint(1, 60), 520 + randint(1, 120)),
    'right': (1370 + randint(1, 130), 520 + randint(1, 120)),
}

