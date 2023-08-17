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
    Moving_Thread = False # so we can change direction
    logutils = None
    Grid_y = None
    Grid_x = None
        
    def __init__(self, logutils, pgu, player, unit_type, tiles):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Unit() class") 
        self.Grid_x = random.randint(Constants.SPAWN_GRID_X, Constants.SPAWN_SIZE)
        self.Grid_y = random.randint(Constants.SPAWN_GRID_Y, Constants.SPAWN_SIZE)
        unit_tile = tiles.GetTile(self.Grid_x, self.Grid_y) 
        self.RectSettings = pgu.RectSettings()
        self.RectSettings.BgColor = player.selected_race.main_color
        self.RectSettings.BorderColor = player.selected_race.secondary_color
        self.RectSettings.x = unit_tile.x
        self.RectSettings.y = unit_tile.y
        self.RectSettings.Width = unit_tile.Width
        self.RectSettings.Height = unit_tile.Height
        self.Name = Names.generate_name(self)
        self.Type = unit_type
        self.RectSettings.HintName = f"{self.Name} has entered the field at XY:({unit_tile.x}x{unit_tile.y}), Grid:({self.Grid_x}x{self.Grid_y})" # just used for debugging
        print(self.RectSettings.HintName)

        # create new unit for this guy
        self.RectSettings = pgu.create_rect(self.RectSettings)

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def MoveUnitOverTime(self, pgu, tiles, end_x, end_y):
        self.logutils.log.debug(f"Inside MoveUnitOverTime: {inspect.currentframe().f_code.co_name}")
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
            speed = default_speed - (self.Type.speed * .1)
            start = tiles.Grid.node(self.Grid_x, self.Grid_y)
            end = tiles.Grid.node(gridx_end, gridy_end)
            self.logutils.log.info(f"{self.Name}: Can I get from ({self.Grid_x}x{self.Grid_x}) to ({gridx_end}x{gridy_end})?")        
            tiles.Grid.cleanup()
            paths, runs = tiles.Finder.find_path(start, end, tiles.Grid)
            self.logutils.log.info(f"operations: {runs}, path length: {len(paths)}")
            self.logutils.log.info(tiles.Grid.grid_str(path=paths, start=start, end=end))
            if len(paths) < 1:
                return_msg = f"{self.Name}: I can't get there"
            else:
                self.logutils.log.debug(f"Moving {self.Name} at {round(speed, 2)} speed from ({self.Grid_x}, {self.Grid_x}) to ({gridx_end}, {gridy_end}), journey will take {runs} steps")
                self.Moving_Thread = True
                x = end_x
                y = end_y
                oldrect = None
                start = time.perf_counter()
                for path in paths:
                    newrect = pygame.Rect(end_x, end_y, tile_width, tile_width)
                    self.logutils.log.debug(f"Sleeping: {round(speed, 2)} seconds before moving {self.Name} again ({self})")
                    time.sleep(speed)
                    newrect.x = int(path[0] * tile_width)
                    newrect.y = int(path[1] * tile_width)
                    if oldrect is None:
                        self.logutils.log.debug(f"{self.Name} beginning travel to ({newrect.x}x{newrect.y})")
                    else:                        
                        self.logutils.log.debug(f"Moving {self.Name} from ({oldrect.x}x{oldrect.y}) to ({newrect.x}x{newrect.y})")
                    newrect = self.move_unit(pgu, oldrect, newrect, self.RectSettings.BgColor)
                    oldrect = newrect
                self.RectSettings.Rect = oldrect
                self.Moving_Thread = False

                # add to tile
                # tile.Units.append(self)
                tiles.UpdateTile(tile)

                end = time.perf_counter()
                return_msg = f"{self.Name} arrived and their destination (XY coords: {tile.x}x{tile.y}), Grid coords: {tile.Grid_x}x{tile.Grid_y}).  Commute took {round(end - start, 2)} second(s)"

        except:
            details = "find_path exception:"
            details += f"start: {str(start)}"
            details += f"end: {str(end)}"
            details += f"Grid: {str(tiles.Grid)}"
            self.logutils.log.exception("An exception occured in MoveUnitOverTime: {details}")
        return return_msg

    def AddToArmy(self, player):
        # add to our army list
        found_unit = False
        for army_unit in player.army:
            if army_unit.Name == self.Name:
                found_unit = True
                break
        if not found_unit:
            player.army.append(self)

        return player.army
    
    def DrawUnit(self, pgu):
        pygame.draw.rect(pgu.surface, self.RectSettings.BgColor, self.RectSettings.Rect)

    def AttackTile(self, gridx, gridy):
        print(f"{self.Name} is attacking tile ({gridx}x{gridy})")
        pass

    # moves rect x,y cords
    def move_unit(self, pgu, prevrect, newrect, bg_color):
        self.logutils.log.debug(f"Inside move_unit: {inspect.currentframe().f_code.co_name}")
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
