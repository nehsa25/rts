import time
import pygame
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants

class GridUtilities:
    finder = None
    grid = None

    def __init__(self):
        self.finder = AStarFinder()

    def load_grid(self, pgu, ut, player, load_env = True):
        #  refresh side panel / highlight a unit that's hovered over
        self.side_panel_rects = ut.draw_side_panel(pgu, player, really_draw=False)

        # spawn points
        self.spawn_points = ut.draw_spawn_points(pgu, really_draw=False)

        usable_map = False

        # get grid of screen based on unit size
        self.grid = self.get_empty_grid()
        while not usable_map:
            # generate our obstacles
            obstacles = []
            if load_env:
                menu_list = []
                menu_list.append(dict(rects=self.side_panel_rects, walkable=False))
                menu_list.append(dict(rects=self.spawn_points, walkable=True))
                obstacles, self.grid = ut.create_terrain(self.grid, menu_list)

                # # update grid with nodes we cannot walk on
                self.grid = ut.update_grid_with_terrain(self.grid, obstacles)

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
            self.grid.cleanup()

        print(f"usable_map: {usable_map}, runs: {runs}")        
        return self.grid, obstacles
    
    def get_empty_grid(self):
        get_empty_start = time.perf_counter()   
        print(f"Generating grid based on {Constants.SCREEN_WIDTH}x{Constants.SCREEN_HEIGHT}")
        matrix = []      
        for y in range(0, Constants.SCREEN_HEIGHT, Constants.UNIT_SIZE):
            x_line = []
            for x in range(0, Constants.SCREEN_WIDTH, Constants.UNIT_SIZE):
                x_line.append(1)
            matrix.append(x_line)

        print("get_empty_grid: Generating pathfinding grid...")
        grid =  Grid(matrix = matrix)
        grid.walkable = True

        for node in grid.nodes:
            for item in node:   
                item.walkable = True

        print("get_empty_grid: Done...")
        get_empty_end = time.perf_counter()
        print(f"get_empty_grid timings: {round(60 - (get_empty_end - get_empty_start), 2)} second(s)")
        return grid

    def show_grid(self, pgu):     
        show_grid_start = time.perf_counter()  
        print("Showing grid")   
        mouse_pos = self.update_mouse()       
        tile_details = ""
        for node in self.grid.nodes:
            for item in node:                
                rs = pgu.RectSettings()
                rs.x = int(item.x * Constants.UNIT_SIZE)
                rs.y = int(item.y * Constants.UNIT_SIZE)
                tile = [i for i in self.tiles if i["coord"]==(rs.x,rs.y)]
                rs.Font = pygame.font.SysFont('Arial', 8)
                mouse_x = int(mouse_pos[0] / Constants.UNIT_SIZE)
                mouse_y = int(mouse_pos[1] / Constants.UNIT_SIZE)
                if item.x == mouse_x and item.y == mouse_y: 
                    tile_details = f"Coordinates: ({rs.x}, {rs.y})\n"
                    tile_details += f"Grid node: ({item.x}, {item.y})\n"
                    tile_details += f"walkable: {False}\n"
                    if len(tile) > 0:
                        tile_details += f"Type: {tile[0]['name']}\n"
                if item.walkable:
                    rs.BgColor = Constants.Colors.GREEN_DARK
                else:
                    rs.BgColor = Constants.Colors.BURNT_ORANGE
                rs.BorderColor = Constants.Colors.NEON_GREEN
                rs.BorderSize = 1
                pgu.create_rect(rs, True)
        show_grid_end = time.perf_counter()
        self.update_mouse(details_text=tile_details)    
        print(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")

