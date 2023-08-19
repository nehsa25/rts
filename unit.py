import inspect
import random
import time
import traceback
import pygame
from enum import Enum
from names import Names

# our stuff
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
    logutils = None  

    def __init__(self, logutils):
        self.logutils = logutils

    # def __init__(self, combat_type, combat_range, combat_damage_low, combat_damage_high, attack_tiles, move_tiles):
    #     self.combat_type = combat_type
    #     self.combat_range = combat_range
    #     self.combat_damage_low = combat_damage_low
    #     self.combat_damage_high = combat_damage_high
    #     self.attack_tiles = attack_tiles
    #     self.move_tiles = move_tiles

class CombatTypes(Enum):
    melee = 0
    ranged = 1

class UnitTypes:
    class Hero(Stats):
        combat_type = CombatTypes.melee
        attack_tiles = [Tile.level.ground, Tile.level.air]
        move_tiles = [Tile.level.ground]
        speed = 2
        def __init__(self):
            pass

    class MountedUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 4
        combat_damage_high = 7
        speed = 3
        attack_tiles = [Tile.level.ground]
        move_tiles = [Tile.level.ground]
        def __init__(self):
            pass

    class MeleeUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 2
        attack_tiles = [Tile.level.ground]
        move_tiles = [Tile.level.ground]
        def __init__(self):
            pass

    class RangedUnit(Stats):
        combat_type = CombatTypes.ranged
        combat_range = 2 # 2 tiles
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 1
        attack_tiles = [Tile.level.sea, Tile.level.ground, Tile.level.air]
        move_tiles = [Tile.level.ground]
        def __init__(self):
            pass

# the whole can of worms
class Unit:
    name = None
    tile = None
    type = None
    move_thread = False # so we can change direction
    log_utils = None
    pgu = None
        
    def __init__(self, log_utils, pgu, unit_type, tiles):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Unit() class") 
        grid_x = random.randint(Constants.SPAWN_GRID_X, Constants.SPAWN_SIZE)
        grid_y = random.randint(Constants.SPAWN_GRID_Y, Constants.SPAWN_SIZE)
        self.tile = tiles.GetTile(grid_x, grid_y) 
        self.name = Names.generate_name(self)
        self.type = unit_type
        self.pgu = pgu

        print(f"{self.name} has entered the field at XY:({self.tile.tile_rect_settings.x}x{self.tile.tile_rect_settings.y}), Grid:({self.tile.tile_rect_settings.grid_x}x{self.tile.tile_rect_settings.grid_y})") # just used for debugging

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def MoveUnitOverTime(self, tiles, end_x, end_y):
        self.log_utils.log.debug(f"Inside MoveUnitOverTime")
        return_msg = ""
        start = ""
        end = ""

        try:
            tile_width = tiles.GetTileWidth()            
            tile_coords = tiles.ConvertXYCoordToGridCoord(end_x, end_y)            
            gridx_end = tile_coords[0]
            gridy_end = tile_coords[1]          
            tile = tiles.GetTileByNodeCoord(gridx_end, gridy_end)  
            default_speed = .35 # higher is faster?
            speed = default_speed - (self.type.speed * .1)
            start = tiles.Grid.node(self.Grid_x, self.Grid_y)
            end = tiles.Grid.node(gridx_end, gridy_end)
            self.log_utils.log.info(f"{self.name}: Can I get from ({self.Grid_x}x{self.Grid_x}) to ({gridx_end}x{gridy_end})?")        
            tiles.Grid.cleanup()
            paths, runs = tiles.Finder.find_path(start, end, tiles.Grid)
            self.log_utils.log.info(f"operations: {runs}, path length: {len(paths)}")
            self.log_utils.log.info(tiles.Grid.grid_str(path=paths, start=start, end=end))
            if len(paths) < 1:
                return_msg = f"{self.name}: I can't get there"
            else:
                self.log_utils.log.debug(f"Moving {self.name} at {round(speed, 2)} speed from ({self.Grid_x}, {self.Grid_x}) to ({gridx_end}, {gridy_end}), journey will take {runs} steps")
                self.move_thread = True
                x = end_x
                y = end_y
                oldrect = None
                start = time.perf_counter()
                for path in paths:
                    newrect = pygame.Rect(end_x, end_y, tile_width, tile_width)
                    self.log_utils.log.debug(f"Sleeping: {round(speed, 2)} seconds before moving {self.name} again ({self})")
                    time.sleep(speed)
                    newrect.x = int(path[0] * tile_width)
                    newrect.y = int(path[1] * tile_width)
                    if oldrect is None:
                        self.log_utils.log.debug(f"{self.name} beginning travel to ({newrect.x}x{newrect.y})")
                    else:                        
                        self.log_utils.log.debug(f"Moving {self.name} from ({oldrect.x}x{oldrect.y}) to ({newrect.x}x{newrect.y})")
                    newrect = self.move_unit(pgu, oldrect, newrect, self.RectSettings.BgColor)
                    oldrect = newrect
                self.RectSettings.Rect = oldrect
                self.move_thread = False

                # add to tile
                # tile.Units.append(self)
                tiles.UpdateTile(tile)

                end = time.perf_counter()
                return_msg = f"{self.name} arrived and their destination (XY coords: {tile.x}x{tile.y}), Grid coords: {tile.Grid_x}x{tile.Grid_y}).  Commute took {round(end - start, 2)} second(s)"

        except:
            details = "find_path exception:"
            details += f"start: {str(start)}"
            details += f"end: {str(end)}"
            details += f"Grid: {str(tiles.Grid)}"
            self.log_utils.log.exception("An exception occured in MoveUnitOverTime: {details}")
        return return_msg

    def AddToArmy(self, player):
        # add to our army list
        found_unit = False
        for army_unit in player.army:
            if army_unit.Name == self.name:
                found_unit = True
                break
        if not found_unit:
            player.army.append(self)

        return player.army
    
    def DrawUnit(self, player):
        pygame.draw.rect(self.pgu.surface, player.selected_race.main_color, self.tile.tile_rect_settings.rect)

    def AttackTile(self, gridx, gridy):
        print(f"{self.name} is attacking tile ({gridx}x{gridy})")
        pass

    # moves rect x,y cords
    def move_unit(self, prevrect, newrect, bg_color):
        self.log_utils.log.debug(f"Inside move_unit")
        # previous
        if prevrect is not None:
            rs = self.pgu.RectSettings()
            rs.BgColor = Constants.Colors.GAME_MAP_COLOR
            rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
            rs.Rect = prevrect
            self.pgu.create_rect(rs)
            #pygame.display.update(prevrect)

        # new
        rs = self.pgu.RectSettings()
        rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
        rs.Rect = newrect
        rs.BgColor = bg_color
        self.pgu.create_rect(rs)

        pygame.display.update(newrect)
        return newrect
