"""
Create all hero in a structure way.
"""

class Hero:

    def __init__(self, name, tier, img, archetype):
        self.name = name
        self.archetype = archetype
        self.tier = tier
        self.img = img
    
    def hero_power(self):
        # HERE MANAGE ALL HERO POWER POSSIBLE
        # DONT KNOW HOW TO DO THAT
        target_hero_power[self.name]
    
    def __str__(self):
        dash = '- '*5
        return "{}Avatar: {}{}\n   -name: {}\n   -tier: {}\n   -archetype: {}".format(
            dash, self.name, dash, self.name, self.tier, self.archetype
        )
    

