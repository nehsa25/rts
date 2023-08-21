import pygame
from constants import Constants

class Menu(object):
    border_rect = None
    side_panel_rect = None

    def __init__(self):
        self.log_utils.log.info("Initializing Menu() class")

    # def draw_map_select_menu(self, pgu):
    #     left_side_rs = pgu.RectSettings()
    #     left_side_rs.x = Constants.MAP_MENU_LEFT_WIDTH_PX
    #     right_side_rect = None
    #     map_view_rect = None

    def create_border(self):
        self.log_utils.log.debug(f"Inside create_border")
        rect = pygame.Rect(0, 0, Constants.SCREEN_WIDTH_PX, Constants.SCREEN_HEIGHT_PX) 
        self.border_rect = pygame.draw.rect(self.surface, Constants.Colors.GAME_BORDER_COLOR, rect, Constants.BORDER_SIZE_PX, border_radius=2)


    # create sides panel with army troop buttons
    def draw_side_panel(self, player, really_draw=True):
        self.log_utils.log.debug(f"Inside draw_side_panel")
        rect = pygame.Rect(0, 0, Constants.SIDE_PANEL_WIDTH_PX, Constants.SCREEN_HEIGHT_PX) 
        self.side_panel_rect = pygame.draw.rect(self.surface, Constants.Colors.GAME_BORDER_COLOR, rect, Constants.BORDER_SIZE_PX, border_radius=2)

        # # also draw guys..
        # if really_draw:
        #     i = 1
        #     unit_button_list = []
        #     for unit in player.selected_race.units:
        #         unit_x = (Constants.SIDE_PANEL_WIDTH_PX / 2) / 2
        #         unit_y = 60 * i
        #         unit_width = Constants.SIDE_PANEL_WIDTH_PX / 2
        #         unit_height = unit_width
        #         rs = pgu.RectSettings()
        #         rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
        #         rs.background_color = player.selected_race.main_color
        #         rs.BorderColor = player.selected_race.secondary_color
        #         rs.Text = unit["Name"]
        #         rs.HintName = "unit button text"
        #         rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE_PX
        #         rs.Font = pygame.font.SysFont(Constants.TROOP_FONT, rs.FontSize)
        #         pgu.create_rect(rs)

        #         # update our list to pass back
        #         unit_button_list.append(rs)
        #         i = i + 1

        #     if mouse_pos is not None:
        #         for unit_btn_rectsettings in unit_button_list:
        #             if unit_btn_rectsettings.Rect.collidepoint(mouse_pos):
        #                 self.unit_button_highlighted(pgu, player, unit_btn_rectsettings)
