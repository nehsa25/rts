import time
import random
from enum import Enum

# our stuff
from constants import Constants

class Terrain:
    class Level(Enum):
        Subterranean = 0
        Ground = 1
        Air = 2
        Sea = 3
        
    class Type(Enum):
        Lava = dict(BgColor=Constants.Colors.LAVA)
        Mountain = dict(BgColor=Constants.Colors.WHITE_MISTY)
        Water = dict(BgColor=Constants.Colors.AQUA)
        Rain = dict(BgColor=Constants.Colors.WATER)
        Fog = dict(BgColor=Constants.Colors.GRAY_IRON_MOUNTAIN)
        Forest = dict(BgColor=Constants.Colors.HUNTER_GREEN)
        Swamp = dict(BgColor=Constants.Colors.GREEN_DARK)
        Basic = dict(BgColor=Constants.Colors.SANDY_BROWN) # nothing special
        Fire = dict(BgColor=Constants.Colors.BURNT_ORANGE)

    def create_random_tiles(pgu, grid, tiles, terrain_type, type_num):
        start = time.perf_counter()
        body_num_tiles = 0
        for num_complete in range(type_num):
            print(f"create_random_tiles ({terrain_type.name}) % Complete: {round(((num_complete / type_num) * 100), 2)}")
            num_tiles_remaining = type_num

            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            grid_x = rand_cord.x
            grid_y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            body_size = 0
            if size == "tiny":
                body_size = random.randint(1, 2)
            elif size == "small":
                body_size = random.randint(2, 6)
            elif size == "medium":
                body_size = random.randint(6, 10)
            elif size == "large":
                body_size = random.randint(10, 30)
            elif size == "huge":
                body_size = random.randint(30, 100)

            while body_num_tiles <= body_size:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    grid_x += -1
                elif side == "right":
                    grid_x += 1
                elif side == "top":
                    grid_y += -1
                elif side == "bottom":
                    grid_y += 1

                item = tiles.GetTile(grid_x, grid_y)

                # ensure we don't get off track
                if item is None:
                    break

                if item.Type == Terrain.Type.Basic:
                    coords = item.ConvertGridCoordToXYCoord()
                    print(f"picked {terrain_type} tile placement: {grid_x}x{grid_y} ({coords[0]}x{coords[1]})")
                    t = tiles.CreateTile(pgu, gridx=grid_x, gridy=grid_y)
                    t.Type = terrain_type
                    t.Walkable = False
                    t.RectSettings = pgu.RectSettings(t)
                    t.RectSettings = pgu.create_rect(t.RectSettings) # update with .Rect
                    tiles.UpdateTile(t)
                    body_num_tiles += 1
                    num_tiles_remaining -= 1

                if num_tiles_remaining <= 0:
                    break

            print(f"Wanted tiles for water density {size}: {body_size}, got: {body_num_tiles}")
            if num_tiles_remaining <= 0:
                break

            # start next "body" of water
            body_num_tiles = 0

        end = time.perf_counter()
        print(f"create_random_tiles ({terrain_type.name}): {round(60 - (end - start), 2)} second(s)")
        return tiles.MapTiles

