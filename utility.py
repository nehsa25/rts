import random
from time import sleep
import time
import traceback
import pygame

# our stuff
from constants import Constants
from pygameutility import PygameUtilities
from names import Names
from unit import Unit
from tile import Tiles

class Utility:
    screen_border_rs = None # border
    sp_menu_rs = None # side panel
    spawn_rs = None # spawn point
    MenuTiles = []
    spawn_points = None
    obstacles = None

    def __init__(self):
        self.MapTiles = Tiles()

    def create_border(self, pgu):
        if self.screen_border_rs is None:
            # create border
            self.screen_border_rs = pgu.RectSettings()
            self.screen_border_rs.Width = Constants.SCREEN_WIDTH
            self.screen_border_rs.Height = Constants.SCREEN_HEIGHT
            self.screen_border_rs.BgColor = Constants.Colors.ROYAL_PURPLE
            self.screen_border_rs.BorderColor = Constants.Colors.AQUA
            self.screen_border_rs.BorderWidth = Constants.BORDER_SIZE
        self.screen_border_rs = pgu.create_rect(self.screen_border_rs, ignore_side_panel=True, really_draw=True)

    # creates section of the map free for units spawn
    def draw_spawn_points(self, pgu, really_draw=True):
        pgu.update_mouse()

        if self.spawn_rs is None:
            spawn_point_rect = pgu.RectSettings()
            spawn_point_rect.BgColor = Constants.Colors.SPAWN_COLOR
            spawn_point_rect.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            spawn_point_rect.BorderColor = Constants.Colors.PLUM
            spawn_point_rect.Rect = pygame.Rect(Constants.SPAWN_X, Constants.SPAWN_Y, Constants.SPAWN_WIDTH, Constants.SPAWN_HEIGHT)
            self.spawn_rs = spawn_point_rect
        self.spawn_rs = pgu.create_rect(self.spawn_rs, ignore_side_panel=True, really_draw=really_draw)

    def update_selected_units_list(self, unit):
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

    # create sides panel with army troop buttons
    def draw_side_panel(self, pgu, player, really_draw=True):
        mouse_pos = pgu.update_mouse()
        if self.sp_menu_rs is None:
            sp_menu_rs = pgu.RectSettings()
            sp_menu_rs.BgColor = Constants.Colors.POOP_BROWN
            sp_menu_rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            sp_menu_rs.Width = Constants.SP_WIDTH
            sp_menu_rs.Height = pgu.surface.get_height()
            sp_menu_rs.BorderColor = Constants.Colors.GAME_BORDER_COLOR
            sp_menu_rs.BorderSides = [Constants.BorderSides.RIGHT]
            self.sp_menu_rs = sp_menu_rs
        self.sp_menu_rs = pgu.create_rect(self.sp_menu_rs, ignore_side_panel=True, really_draw=really_draw)

        # also draw guys..
        if really_draw:
            i = 1
            unit_button_list = []
            for unit in player.selected_race.units:
                unit_x = (Constants.SP_WIDTH / 2) / 2
                unit_y = 60 * i
                unit_width = Constants.SP_WIDTH / 2
                unit_height = unit_width
                rs = pgu.RectSettings()
                rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
                rs.BgColor = player.selected_race.main_color
                rs.BorderColor = player.selected_race.secondary_color
                rs.Text = unit["Name"]
                rs.HintName = "unit button text"
                rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
                rs.Font = pygame.font.Font(None, rs.FontSize)
                pgu.create_rect(rs, ignore_side_panel=True)

                # update our list to pass back
                unit_button_list.append(rs)
                i = i + 1

            if mouse_pos is not None:
                for unit_btn_rectsettings in unit_button_list:
                    if unit_btn_rectsettings.Rect.collidepoint(mouse_pos):
                        self.unit_button_highlighted(pgu, player, unit_btn_rectsettings)

    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self, pgu, player):
        rs = pgu.RectSettings()
        rs.BgColor = Constants.Colors.COCOA
        rs.BorderColor = Constants.Colors.GAME_BORDER_COLOR
        rs.BorderSides = [Constants.BorderSides.TOP, Constants.BorderSides.LEFT]
        rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        nudge = 2
        rs.x = Constants.SP_WIDTH  + nudge # start at end of SP panel
        rs.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rs.Width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH - nudge
        rs.Height = pgu.surface.get_height()
        rs.HintName = "bottom panel main"
        pgu.create_rect(rs, ignore_side_panel=True)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in player.army:
            unit_x = Constants.SP_WIDTH + Constants.PANEL_BUTTON_SPACING
            unit_y = rs.y + Constants.RECT_SIZE
            unit_width = Constants.SP_WIDTH / 2
            unit_height = unit_width
            rs = pgu.RectSettings()
            rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rs.BgColor = player.selected_race.main_color
            rs.BorderColor = player.selected_race.secondary_color
            rs.Text = unit.Name
            rs.HintName = "unit button text"
            rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            pgu.create_rect(rs, ignore_side_panel=True)

            # update our list to pass back
            unit_button_list.append(rs)
            i = i + 1

        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, pgu, player, rs):
        rs.FontColor = player.selected_race.hover_text_color
        rs.BgColor = player.selected_race.hover_color
        pgu.create_rect(rs, ignore_side_panel=True, really_draw=True)
        pgu.update_mouse()

    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, pgu, unit):
        unit.RectSettings.BorderColor = Constants.Colors.RANDOM
        unit.RectSettings = pgu.create_rect(unit.RectSettings)
        return unit

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, pgu, player, unit_type, unit = None):
        if unit is None:
            unit = Unit()
            unit.RectSettings = pgu.RectSettings()
            unit.RectSettings.BgColor = player.selected_race.main_color
            unit.RectSettings.BorderColor = player.selected_race.secondary_color
            unit.RectSettings.x = random.randint(Constants.SPAWN_X, Constants.SPAWN_X + (Constants.SPAWN_WIDTH - Constants.UNIT_SIZE))
            unit.RectSettings.y = random.randint(Constants.SPAWN_Y, Constants.SPAWN_Y + (Constants.SPAWN_HEIGHT - Constants.UNIT_SIZE))
            unit.RectSettings.Width = Constants.UNIT_SIZE
            unit.RectSettings.Height = Constants.UNIT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
            unit.RectSettings.HintName = f"army unit on field: {unit.Name}" # just used for debugging

        # create new unit for this guy
        unit.RectSettings = pgu.create_rect(unit.RectSettings)

        # add to our army list
        found_unit = False
        for army_unit in player.army:
            if army_unit.Name == unit.Name:
                found_unit = True
                break
        if not found_unit:
            player.army.append(unit)

        return unit
