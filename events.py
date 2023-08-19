import concurrent.futures
import pygame

class Events:
    executor = None
    pgu = None
    log_utils = None
    unit_moving_threads = []

    def __init__(self, log_utils, pgu):
        self.log_utils = log_utils
        self.pgu = pgu
        self.log_utils.log.debug("Initializing Events() class")     
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.executor._max_workers = 1

    def check_on_troop_movement(self):
        self.log_utils.log.debug("check_on_troop_movement")
        # check units done moving threads..
        for future in self.unit_moving_threads:
            state = future._state     
            if state == "PENDING":
                state = "INITIALIZING"
            elif state == "RUNNING":
                state = "LOADING"
            elif state == "FINISHED":                        
                state = "COMPLETE"
                self.log_utils.log.info(f"unit_moving_threads future state: {state}")
                result = future.result()
                self.log_utils.log.info(f"Unit moving result: {result}, removing thread from unit_moving_threads list")
                self.unit_moving_threads.remove(future)

    def check_for_events(self, tiles):
        self.log_utils.log.debug("check_for_events")

        # keyboard
        key = pygame.key.get_pressed()            
        if key[pygame.K_a] or key[pygame.K_LEFT] == True:
            print(f"left key: {key} pressed")
        elif key[pygame.K_d] or key[pygame.K_RIGHT] == True:
            print(f"right key: {key} pressed")
        elif key[pygame.K_w] or key[pygame.K_UP] == True:
            print(f"up key: {key} pressed")
        elif key[pygame.K_s] or key[pygame.K_DOWN] == True:
            print(f"down key: {key} pressed")

        # mouse
        mouse = pygame.mouse.get_pressed()            
        if mouse[0] == True:
            print("quick mouse 0 click")
        elif mouse[1] == True:
            # print("quick mouse 1 click")
            tiles.show_grid(self.pgu)
        elif mouse[2] == True:
            print("quick mouse 2 click")

    def mouse_left_single_event(self, event, player, ut, tiles, gamedata):
        print("mouse_0_single_event")  
        print(f"mouse down event: {event}")

        mouse_pos = self.pgu.update_mouse()

        # scan unit for select      
        selected_new_unit = False
        for unit in player.army:
            if unit.RectSettings.Rect.collidepoint(mouse_pos):                        
                self.selected_units = [] # if we clicked a different troop unit and only used left mouse (not CTRL for example), start over                
                self.selected_units.append(unit)
                selected_new_unit = True

                # if we any unit selected, show it in the bottom window and indicate it's selected with border
                if len(self.selected_units) > 0:
                    ut.select_unit(self.pgu, unit)
                    ut.create_bottom_panel(self.pgu, gamedata.Player)

        # if we selected something new cool, if not, then the order it to move..
        if not selected_new_unit and len(self.selected_units) > 0:
            for army_unit in self.selected_units:
                if army_unit.Moving_Thread is False:
                    dest_x = mouse_pos[0]
                    dest_y = mouse_pos[1]
                    self.unit_moving_threads.append(self.executor.submit(army_unit.MoveUnitOverTime, self.pgu, tiles, dest_x, dest_y))

    def mouse_middle_single_event(self, event):
        print("mouse_1_single_event")  

    def mouse_right_single_event(self, event):
        print("mouse_2_single_event")
        self.pgu.loop_fonts(self.pgu)