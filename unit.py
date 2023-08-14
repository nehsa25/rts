import time
import traceback
import pygame

# our stuff
from combattypes import CombatTypes
from pygameutility import PygameUtilities
from tile import Tile
from constants import Constants

# how much damage, how fast, ect
class Stats:
    combat_type = None
    combat_range = None
    combat_damage_low = None
    combat_damage_high = None
    attack_tiles = None
    move_tiles = None   

    def __init__(self):
        pass

    # def __init__(self, combat_type, combat_range, combat_damage_low, combat_damage_high, attack_tiles, move_tiles):
    #     self.combat_type = combat_type
    #     self.combat_range = combat_range
    #     self.combat_damage_low = combat_damage_low
    #     self.combat_damage_high = combat_damage_high
    #     self.attack_tiles = attack_tiles
    #     self.move_tiles = move_tiles

# probably will help with base skill sets
class UnitTypes:
    class Hero(Stats):
        combat_type = CombatTypes.melee
        attack_tiles = [Tile.Level.Ground, Tile.Level.Air]
        move_tiles = [Tile.Level.Ground]
        speed = 2
        def __init__(self):
            pass

    class MountedUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 4
        combat_damage_high = 7
        speed = 3
        attack_tiles = [Tile.Level.Ground]
        move_tiles = [Tile.Level.Ground]
        def __init__(self):
            pass

    class MeleeUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 2
        attack_tiles = [Tile.Level.Ground]
        move_tiles = [Tile.Level.Ground]
        def __init__(self):
            pass

    class RangedUnit(Stats):
        combat_type = CombatTypes.ranged
        combat_range = 2 # 2 tiles
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 1
        attack_tiles = [Tile.Level.Sea, Tile.Level.Ground, Tile.Level.Air]
        move_tiles = [Tile.Level.Ground]
        def __init__(self):
            pass

# the whole can of worms
class Unit:
    Name = None
    Type = None
    RectSettings = None
    Moving_Thread = None # so we can change direction

    def __init__(self):
        self.RectSettings = PygameUtilities.RectSettings()

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def MoveUnitOverTime(self, pgu, tiles, end_x, end_y):
        tiles.Grid.cleanup()
        default_speed = .35
        speed = default_speed - (self.Type.speed * .1)
        start_x_grid = int(self.RectSettings.Rect.x  / Constants.UNIT_SIZE)
        start_y_grid = int(self.RectSettings.Rect.y  / Constants.UNIT_SIZE)
        end_x_grid = int(end_x / Constants.UNIT_SIZE)
        end_y_grid = int(end_y / Constants.UNIT_SIZE)
        start = tiles.Grid.node(start_x_grid, start_y_grid)
        end = tiles.Grid.node(end_x_grid, end_y_grid)
        print(f"Checking path: {start_x_grid}x{start_y_grid} to {end_x_grid}x{end_y_grid}")
        try:
            paths, runs = tiles.Finder.find_path(start, end, tiles.Grid)
        except Exception as e:
            print("find_path exception:")
            # print(f"paths: {str(paths)}")
            # print(f"runs: {str(runs)}")
            print(f"start: {str(start)}")
            print(f"end: {str(end)}")
            print(f"Grid: {str(tiles.Grid)}")
            print(str(e))
            traceback.print_exc()

        return_msg = ""
        if len(paths) < 1:
            return_msg = f"{self.Name}: I can't get there"
        else:
            print(f"Moving {self.Name} at {round(speed, 2)} speed from ({start_x_grid}, {start_y_grid}) to ({end_x_grid}, {end_y_grid}), journey will take {runs} steps")
            print(f"paths: {paths}")
            x = self.RectSettings.Rect.x
            y = self.RectSettings.Rect.y
            oldrect = None

            start = time.perf_counter()
            for path in paths:
                newrect = pygame.Rect(x, y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                print(f"Sleeping: {round(speed, 2)} seconds before moving {self.Name} again ({self})")
                time.sleep(speed)
                newrect.x = int(path[0] * Constants.UNIT_SIZE)
                newrect.y = int(path[1] * Constants.UNIT_SIZE)
                if oldrect is None:
                    print(f"{self.Name} beginning travel to ({newrect.x}x{newrect.y})")
                else:
                    print(f"Moving {self.Name} from ({oldrect.x}x{oldrect.y}) to ({newrect.x}x{newrect.y})")
                newrect = self.move_unit(pgu, oldrect, newrect, self.RectSettings.BgColor)
                oldrect = newrect
            self.RectSettings.Rect = oldrect
            end = time.perf_counter()
            return_msg = f"{self.Name} arrived and their destination.  Commute took {round(end - start, 2)} second(s)"
        return return_msg

    # moves rect x,y cords
    def move_unit(self, pgu, prevrect, newrect, bg_color):
        # previous
        if prevrect is not None:
            rs = pgu.RectSettings()
            rs.BgColor = Constants.Colors.GAME_MAP_COLOR
            rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
            rs.Rect = prevrect
            pgu.create_rect(rs)
            #pygame.display.update(prevrect)

        # new
        rs = pgu.RectSettings()
        rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
        rs.Rect = newrect
        rs.BgColor = bg_color
        pgu.create_rect(rs)

        pygame.display.update(newrect)
        return newrect
