class Unit:
    combat_type = None
    combat_range = None
    combat_damage_low = None
    combat_damage_high = None
    attack_tiles = None
    move_tiles = None
    
    def __init__(self, combat_type, combat_range, combat_damage_low, combat_damage_high, attack_tiles, move_tiles):
        self.combat_type = combat_type
        self.combat_range = combat_range
        self.combat_damage_low = combat_damage_low
        self.combat_damage_high = combat_damage_high
        self.attack_tiles = attack_tiles
        self.move_tiles = move_tiles
