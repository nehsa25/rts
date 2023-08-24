import inspect
from time import sleep
import pygame

# our stuff
from constants import Constants

class Utility(object):
    screen_border_rs = None # border
    sp_menu_rs = None # side panel
    spawn_rs = None # spawn point
    spawn_points = None
    obstacles = None

    def __init__(self):
        self.log_utils.log.info("Initializing Utility() class")    
    
    # creates section of the map free for units spawn
    def draw_spawn_points(self):
        self.log_utils.log.debug(f"Inside draw_spawn_points")
        spawn_x = Constants.SIDE_PANEL_WIDTH_PX + Constants.SPAWN_GD_X * Constants.TILE_WIDTH_PX
        spawn_y = Constants.SPAWN_GD_Y * Constants.TILE_HEIGHT_PX
        spawn_width = Constants.SPAWN_SIZE * Constants.TILE_WIDTH_PX 
        spawn_height = Constants.SPAWN_SIZE * Constants.TILE_HEIGHT_PX 
        rect = pygame.Rect(spawn_x, spawn_y, spawn_width, spawn_height) 
        self.side_panel_rect = pygame.draw.rect(self.surface, Constants.Colors.SPAWN_COLOR, rect, Constants.BORDER_SIZE_PX, border_radius=2)

    def update_selected_units_list(self, unit):
        self.log_utils.log.debug(f"Inside update_selected_units_list")
        newlist = self.selected_units
        unit_already_added = False
        for selected_unit in self.selected_units:
            if selected_unit.Name == unit.Name:
                unit_already_added = True
                break

        if unit_already_added:
            # newlist.remove(unit) # this is wrong
            pass
        else:
            newlist.append(unit)

        return newlist

    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self, player):
        self.log_utils.log.debug(f"Inside create_bottom_panel")
        rs = self.pgu.RectSettings()
        rs.background_color = Constants.Colors.COCOA
        rs.BorderColor = Constants.Colors.GAME_BORDER_COLOR
        rs.BorderSides = [Constants.BorderSides.TOP, Constants.BorderSides.LEFT]
        rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE_PX
        nudge = 2
        rs.x = Constants.SIDE_PANEL_WIDTH_PX  + nudge # start at end of SP panel
        rs.y = Constants.SCREEN_HEIGHT_PX - Constants.BP_HEIGHT_PX
        rs.Width = Constants.SCREEN_WIDTH_PX - Constants.SIDE_PANEL_WIDTH_PX - nudge
        rs.Height = self.pgu.surface.get_height()
        rs.HintName = "bottom panel main"
        self.pgu.create_rect(rs)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in player.army:
            unit_x = Constants.SIDE_PANEL_WIDTH_PX + Constants.PANEL_BUTTON_SPACING_PX
            unit_y = rs.y + Constants.PANEL_BUTTON_SPACING_PX
            unit_width = Constants.SIDE_PANEL_WIDTH_PX / 2
            unit_height = unit_width
            rs = self.pgu.RectSettings()
            rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rs.background_color = player.selected_race.main_color
            rs.BorderColor = player.selected_race.secondary_color
            rs.Text = unit.Name
            rs.HintName = "unit button text"
            rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE_PX
            self.pgu.create_rect(rs)

            # update our list to pass back
            unit_button_list.append(rs)
            i = i + 1

        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, player, rs):
        self.log_utils.log.debug(f"Inside unit_button_highlighted")
        rs.FontColor = player.selected_race.hover_text_color
        rs.background_color = player.selected_race.hover_color
        self.pgu.create_rect(rs, really_draw=True)
        self.pgu.update_mouse()

    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, unit):
        self.log_utils.log.debug(f"Inside select_unit")
        unit.RectSettings.BorderColor = Constants.Colors.RANDOM
        unit.RectSettings = self.pgu.create_rect(unit.RectSettings)
        return unit
