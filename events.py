import concurrent.futures
import time
import pygame

class Events(object):
    executor = None
    unit_moving_threads = []
    showing_grid = False

    def __init__(self):
        self.log_utils.log.info("Initializing Events() class")
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.executor._max_workers = 1

    def scan_for_slow_events(self):
        self.log_utils.log.info(f"scan_for_slow_events: enter")
        scan_for_slow_events_start = time.perf_counter()

        # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_left_single_event(event, self.player, self.ut, self.game_data, self.game_data)
                if event.button == 2:
                    self.mouse_middle_single_event(event)
                if event.button == 3:
                    self.mouse_right_single_event(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.log_utils.log.debug(f"mouse up: {event}")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_game_menu_loop()
                    if self.running == False:
                        self.main_game_running = False
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.main_game_running = False
                self.running = False
        scan_for_slow_events_end = time.perf_counter()
        self.log_utils.log.info(f"scan_for_slow_events: exit, timings: {round((scan_for_slow_events_end - scan_for_slow_events_start), 2)} second(s)")

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

    def check_for_fast_events(self):
        self.log_utils.log.info(f"check_for_fast_events: enter")
        check_for_fast_events_start = time.perf_counter()

        # keyboard
        key = pygame.key.get_pressed()            
        if key[pygame.K_a] or key[pygame.K_LEFT] == True:
            self.log_utils.log.info(f"left key: {key} pressed")
        elif key[pygame.K_d] or key[pygame.K_RIGHT] == True:
            self.log_utils.log.info(f"right key: {key} pressed")
        elif key[pygame.K_w] or key[pygame.K_UP] == True:
            self.log_utils.log.info(f"up key: {key} pressed")
        elif key[pygame.K_s] or key[pygame.K_DOWN] == True:
            self.log_utils.log.info(f"down key: {key} pressed")

        # mouse
        mouse = pygame.mouse.get_pressed()            
        if mouse[0] == True:
            self.log_utils.log.info("quick mouse 0 click")
        elif mouse[1] == True:
            self.log_utils.log.info("quick mouse 1 click")
        elif mouse[2] == True:
            self.log_utils.log.info("quick mouse 2 click")

        check_for_fast_events_end = time.perf_counter()
        self.log_utils.log.info(f"check_for_fast_events: exit, timings: {round((check_for_fast_events_end - check_for_fast_events_start), 2)} second(s)")

    def mouse_left_single_event(self, event, player, ut, tiles, gamedata):
        self.log_utils.log.info("mouse_0_single_event")  
        self.log_utils.log.info(f"mouse down event: {event}")

        mouse_pos = self.pg.update_mouse()

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
        self.log_utils.log.info("mouse_1_single_event (middle)")  
        if self.show_grid == True:
            self.show_grid = False # just disable it
        else:
            self.show_grid = True 

    def mouse_right_single_event(self, event):
        self.log_utils.log.info("mouse_2_single_event")
        self.pgu.loop_fonts(self.pgu)