import time
import pygame
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants
from tile import Tiles

class GridUtilities:
    Finder = None
    Grid = None
    Tiles = None
    GridMatrix = None

    def __init__(self):
        self.Finder = AStarFinder()
        self.Tiles = Tiles()

    def load_grid(self, pgu, ut, player, load_env = True):
        #  refresh side panel / highlight a unit that's hovered over
        ut.draw_side_panel(pgu, player, really_draw=False)

        # spawn points
        ut.draw_spawn_points(pgu, really_draw=False)

        usable_map = False

        # get grid of screen based on unit size
        self.Grid, self.Tiles.MapTiles = self.get_empty_grid(pgu)
        while not usable_map:
            # generate our obstacles
            if load_env:
                # menu_list = []
                # menu_list.append(dict(rects=self.side_panel_rects, walkable=False))
                # menu_list.append(dict(rects=self.spawn_points, walkable=True))
                self.Tiles.MapTiles  = ut.create_terrain(pgu, self.Grid, self.Tiles)

                # # update grid with nodes we cannot walk on
                # self.update_grid_with_terrain()

            usable_map = True
            runs = 0

            # # ensure usable map - also ensure we have a route to the other side of screen
            # unit_spawn_x = int(Constants.UNIT_SPAWN_X / Constants.UNIT_SIZE)
            # unit_spawn_y = int(Constants.UNIT_SPAWN_Y / Constants.UNIT_SIZE)
            # start = grid.node(unit_spawn_x, unit_spawn_y)
            # end_cord_x = int((Constants.SCREEN_WIDTH-Constants.BORDER_SIZE) / Constants.UNIT_SIZE)
            # end_cord_y = int((Constants.SCREEN_HEIGHT-Constants.BORDER_SIZE) / Constants.UNIT_SIZE)
            # end = grid.node(end_cord_x, end_cord_y)
            # paths, runs = self.finder.find_path(start, end, grid)

            # if len(paths) > 1:
            #     usable_map = True
            # else:
            #     usable_map = False

            print(f"Map created is: {usable_map}")
            self.Grid.cleanup()

        return "usable_map: {usable_map}, runs: {runs}"
    
    def get_empty_grid(self, pgu):
        get_empty_start = time.perf_counter()   
        print(f"Generating grid based on {Constants.SCREEN_WIDTH}x{Constants.SCREEN_HEIGHT}")
        matrix = []      
        for y in range(0, Constants.SCREEN_HEIGHT, Constants.UNIT_SIZE):
            x_line = []
            for x in range(0, Constants.SCREEN_WIDTH, Constants.UNIT_SIZE):
                x_line.append(1)
            matrix.append(x_line)

        print("get_empty_grid: Generating pathfinding grid...")
        self.GridMatrix = matrix
        grid =  Grid(matrix = self.GridMatrix)
        # grid.walkable = True

        self.Tiles = Tiles()
        for node in grid.nodes:
            for item in node:   
                # item.walkable = True

                t = self.Tiles.CreateTile(pgu, gridx=item.x, gridy=item.y)
                print(f"get_empty_grid: created basic tile: ({t.x}x{t.y})")
                self.Tiles.MapTiles.append(t)

        print("get_empty_grid: Done...")
        get_empty_end = time.perf_counter()
        print(f"get_empty_grid timings: {round(60 - (get_empty_end - get_empty_start), 2)} second(s)")
        return grid, self.Tiles.MapTiles

    def show_grid(self, pgu, ut):     
        show_grid_start = time.perf_counter()  
        print("Showing grid")   
        mouse_pos = pgu.update_mouse()   
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]    
        
        tile_details = ""
        
        gridcord = self.Tiles.ConvertXYCoordToGridCoord(mouse_x, mouse_y)
        details_node = self.Tiles.GetTile(gridcord[0], gridcord[1])
        print(f"show_grid tile: {details_node}")
        tile_details = f"Coordinates: ({details_node.x}, {details_node.y})\n"
        tile_details += f"Grid node: ({details_node.Grid_x}, {details_node.Grid_y})\n"
        tile_details += f"walkable: {details_node.Walkable}\n"
        tile_details += f"Type: {details_node.Type}\n"
        details_node.RectSettings.Text = tile_details
        pgu.update_mouse(details_text=tile_details)   

        for tile in self.Tiles.MapTiles:
            print(f"tile.x == mouse_pos[0]: {tile.x == mouse_pos[0]}, tile.y == mouse_pos[1]: {tile.y == mouse_pos[1]}")
 
            #rs = pgu.RectSettings()

            # rs.x = int(item.x * Constants.UNIT_SIZE)
            # rs.y = int(item.y * Constants.UNIT_SIZE)
            # tile = [i for i in ut.self.Tiles if i["coord"]==(rs.x,rs.y)]
            # rs.Font = pygame.font.SysFont('Arial', 8)
            # mouse_x = int(mouse_pos[0] / Constants.UNIT_SIZE)
            # mouse_y = int(mouse_pos[1] / Constants.UNIT_SIZE)
            # if item.x == mouse_x and item.y == mouse_y: 
            #     tile_details = f"Coordinates: ({rs.x}, {rs.y})\n"
            #     tile_details += f"Grid node: ({item.x}, {item.y})\n"
            #     tile_details += f"walkable: {False}\n"
            #     if len(tile) > 0:
            #         tile_details += f"Type: {tile[0]['name']}\n"
            # if item.walkable:
            #     rs.BgColor = Constants.Colors.GREEN_DARK
            # else:
            #     rs.BgColor = Constants.Colors.BURNT_ORANGE
            # rs.BorderColor = Constants.Colors.NEON_GREEN
            # rs.BorderSize = 1
            # pgu.create_rect(rs, True)
        show_grid_end = time.perf_counter()
        
        print(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")

    def update_grid_with_terrain(self):
        get_grid_start = time.perf_counter()
        print("get_grid: Updating pathfinding grid with terrain...")
        UNIT_CANNOT_MOVE = False

        collisions = [i for i in self.Tiles.MapTiles if i.Walkable == False]
        for node in self.Grid.nodes:
            for item in node:
                rect = pygame.Rect(item.x * Constants.UNIT_SIZE, item.y * Constants.UNIT_SIZE, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collide = rect.collidelist(collisions)
                if collide != -1:
                    item.walkable = UNIT_CANNOT_MOVE

        get_grid_end = time.perf_counter()
        print(f"get_grid timings: {round(60 - (get_grid_end - get_grid_start), 2)} second(s)")
