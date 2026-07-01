
import pygame
import math
import random
import os


# SETTINGS & COLORS
# Window sizing to fit everything cleanly
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 620

# Color palette from the UI design mockup
BG_PASTEL_PURPLE = pygame.Color('#D3B5E5')
GAME_DARK_PURPLE = pygame.Color('#A855F7')
GRID_LIGHT_PURPLE = pygame.Color('#C084FC')

BTN_NORMAL = pygame.Color('#B18FCF')
BTN_HOVER = pygame.Color('#9A73BE')
BTN_TEXT_COLOR = pygame.Color('#EADBFF')
BTN_ICON_COLOR = pygame.Color('#6F4A9E')

TEXT_DARK_GRAY = pygame.Color('#374151')

# BUTTON CLASS FOR INTERACTIVE MENUS
class Button:
    def __init__(self, x, y, width, height, text, icon_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon_type = icon_type
        
        # Hover and click states
        self.is_hovered = False
        self.is_pressed = False

    def check_hover(self, mouse_x, mouse_y):
        # Built-in rect collision to check if mouse is over the button
        self.is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

    def handle_click_event(self, event):
        # Checks if left mouse button clicked down or up on the button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.is_pressed
            self.is_pressed = False
            # Only trigger action if clicked down AND released on the button
            if was_pressed and self.is_hovered:
                return True
        return False

    def draw(self, surface):
        # Use hover color if mouse is over, otherwise use normal color
        button_color = BTN_HOVER if self.is_hovered else BTN_NORMAL
        
        # Dynamic border radius makes it pill-shaped
        pygame.draw.rect(surface, button_color, self.rect, border_radius=self.rect.height // 2)
        
        # Draw the button label text
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_surface = font.render(self.text, True, BTN_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.left = self.rect.left + 25
        text_rect.centery = self.rect.centery
        surface.blit(text_surface, text_rect)
        
        # Center points for the right-hand icon slots
        icon_x = self.rect.right - 35
        icon_y = self.rect.centery
        
        # Draw manual shapes for icons so the program doesn't need external icon assets
        if self.icon_type == "play":
            triangle_points = [(icon_x - 10, icon_y - 12), (icon_x - 10, icon_y + 12), (icon_x + 15, icon_y)]
            pygame.draw.polygon(surface, BTN_ICON_COLOR, triangle_points)
            
        elif self.icon_type == "settings":
            pygame.draw.circle(surface, BTN_ICON_COLOR, (icon_x, icon_y), 12)
            pygame.draw.circle(surface, button_color, (icon_x, icon_y), 5)
            for i in range(8):
                angle = i * (math.pi / 4)
                nx = icon_x + int(14 * math.cos(angle))
                ny = icon_y + int(14 * math.sin(angle))
                pygame.draw.circle(surface, BTN_ICON_COLOR, (nx, ny), 3)
                
        elif self.icon_type == "leaderboard":
            pygame.draw.rect(surface, BTN_ICON_COLOR, (icon_x - 10, icon_y - 12, 20, 14), border_radius=3)
            pygame.draw.rect(surface, BTN_ICON_COLOR, (icon_x - 3, icon_y + 2, 6, 8))
            pygame.draw.rect(surface, BTN_ICON_COLOR, (icon_x - 12, icon_y + 10, 24, 4))
            
        elif self.icon_type == "exit":
            pygame.draw.line(surface, BTN_ICON_COLOR, (icon_x - 10, icon_y - 10), (icon_x + 10, icon_y + 10), 4)
            pygame.draw.line(surface, BTN_ICON_COLOR, (icon_x - 10, icon_y + 10), (icon_x + 10, icon_y - 10), 4)



# BRIGHTNESS SLIDER CONTROL FOR SETTINGS

class Slider:
    def __init__(self, x, y, width, initial_val):
        self.rect = pygame.Rect(x, y, width, 10)
        self.val = initial_val  # Float scale from 0.0 to 1.0
        self.radius = 12
        self.is_dragging = False

    def draw(self, surface):
        # Draw slider track line
        pygame.draw.rect(surface, BTN_NORMAL, self.rect, border_radius=5)
        # Find where handle sits based on current value percentage
        handle_x = self.rect.x + int(self.val * self.rect.w)
        handle_y = self.rect.centery
        pygame.draw.circle(surface, BTN_ICON_COLOR, (handle_x, handle_y), self.radius)

    def process_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_x = self.rect.x + int(self.val * self.rect.w)
            handle_y = self.rect.centery
            mx, my = event.pos
            # Distance formula check to see if mouse clicked the slider knob
            if math.hypot(mx - handle_x, my - handle_y) <= self.radius:
                self.is_dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            mx, my = event.pos
            # Clamp the slider positions within boundary limits
            if mx < self.rect.x:
                mx = self.rect.x
            if mx > self.rect.right:
                mx = self.rect.right
            # Convert pixel spot to a percentage decimal value
            self.val = (mx - self.rect.x) / self.rect.w


# MAIN MENU DRAWING AND ASSET HANDLING

class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        
        # Load custom large background canvas snake graphic if available
        self.menu_snake_img = None
        if os.path.exists("menu_snake.png"):
            try:
                raw_img = pygame.image.load("menu_snake.png").convert_alpha()
                self.menu_snake_img = pygame.transform.scale(raw_img, (200, 200))
            except:
                print("Failed loading menu_snake.png placeholder")
                
        self.setup_menu_buttons()

    def setup_menu_buttons(self):
        w, h = 280, 60
        start_y = 320 # Room for the logo header and graphic elements
        gap = 70
        x = (self.screen_w // 2) - (w // 2)
        
        items = [("Play", "play"), ("Settings", "settings"), ("Leaderboard", "leaderboard"), ("Exit", "exit")]
        for i, (label, type_id) in enumerate(items):
            y = start_y + (i * gap)
            self.buttons.append(Button(x, y, w, h, label, type_id))

    def draw(self, surface):
        surface.fill(BG_PASTEL_PURPLE)
        
        # Render decorative snake layout image
        if self.menu_snake_img:
            img_rect = self.menu_snake_img.get_rect(center=(self.screen_w // 2, 130))
            surface.blit(self.menu_snake_img, img_rect)
        
        # Overlapping titles from the layout guide
        title_font = pygame.font.Font('freesansbold.ttf', 56)
        dash_font = pygame.font.Font('freesansbold.ttf', 72)
        
        snake_text = title_font.render("Snake", True, pygame.Color('#7D5BA6'))
        surface.blit(snake_text, (self.screen_w // 2 - 160, 110))
        
        dash_text = dash_font.render("Dash", True, pygame.Color('#3A41A4'))
        surface.blit(dash_text, (self.screen_w // 2 - 10, 150))
        
        for btn in self.buttons:
            btn.draw(surface)


# MAIN SNAKE GAMEPLAY ENGINE LOOP

class SnakeGameplay:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Grid variables matching 16x16 playing area dimensions
        self.cols = 16
        self.rows = 16
        self.cell_size = 28
        
        # Calculate offset values to cleanly center grid playspace on display
        self.grid_x = (self.screen_w - (self.cols * self.cell_size)) // 2
        self.grid_y = 110
        
        # Top right menu escape cross boundary dimensions
        self.close_btn = pygame.Rect(self.screen_w - 65, 30, 35, 35)
        
        # Top 3 High Score slots leaderboard file simulation
        self.high_scores = [0, 0, 0]
        self.score = 0
        

        # Dynamic runtime image loading routines 
        self.apple_img = self.get_scaled_image("apple.png")
        self.head_imgs = {
            "up": self.get_scaled_image("snake_up.png"),
            "down": self.get_scaled_image("snake_down.png"),
            "left": self.get_scaled_image("snake_left.png"),
            "right": self.get_scaled_image("snake_right.png")
        }
        
        self.start_new_match()

    def get_scaled_image(self, file_path):
        # Helper to load and handle images safely without breaking if file is missing
        if os.path.exists(file_path):
            try:
                loaded_surface = pygame.image.load(file_path).convert_alpha()
                return pygame.transform.scale(loaded_surface, (self.cell_size, self.cell_size))
            except:
                print(f"Error reading asset file: {file_path}")
        return None

    def start_new_match(self):
        self.score = 0
        # Initialize standard multi-cell grid coordinate lists for the snake body
        self.snake = [[7, 12], [6, 12], [5, 12], [4, 12]]
        self.direction = [1, 0] # X, Y vector (default moving East/Right)
        self.next_direction = [1, 0]
        
        self.game_over = False
        self.score_logged = False
        self.generate_food_coordinates()

    def generate_food_coordinates(self):
        while True:
            self.food = [random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)]
            # Redo loop execution if food lands on snake or inside line blockades
            if self.food in self.snake or self.hit_obstacle_walls(self.food):
                continue
            break

    def hit_obstacle_walls(self, block_coord):
        # Standard lookup checker map tracking maze grid cells manually from layout
        bx, by = block_coord[0], block_coord[1]
        
        if bx == 2 and (3 <= by <= 7): return True
        if by == 3 and (2 <= bx <= 7): return True
        if by == 7 and (2 <= bx <= 7): return True
       
        if bx == 15 and (3 <= by <= 6): return True
        if by == 6 and (11 <= bx <= 15): return True
       
        if (bx == 7 or bx == 10) and (7 <= by <= 10): return True
        if (by == 7 or by == 10) and (7 <= bx <= 10): return True
       
        if bx == 2 and (11 <= by <= 14): return True
        if by == 14 and (2 <= bx <= 7): return True
       
        if bx == 13 and (11 <= by <= 15): return True
        if bx == 11 and (14 <= by <= 15): return True
        if by == 14 and (11 <= bx <= 15): return True

        return False

    def trigger_tick_update(self):
        if self.game_over:
            if not self.score_logged:
                self.save_score_entry()
            return

        self.direction = self.next_direction
        
        # Extrapolate new head block position indices
        new_head_block = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
        
        # Grid boundaries containment checking logic
        if new_head_block[0] < 0 or new_head_block[0] >= self.cols or new_head_block[1] < 0 or new_head_block[1] >= self.rows:
            self.game_over = True
            return
           
        # Self collision monitoring
        if new_head_block in self.snake:
            self.game_over = True
            return
           
        # Maze map lines impact tracking
        if self.hit_obstacle_walls(new_head_block):
            self.game_over = True
            return

        # Add piece ahead of current coordinate list array positions
        self.snake.insert(0, new_head_block)

        # Handle food digestion score updates
        if new_head_block == self.food:
            self.score += 1
            self.generate_food_coordinates()
        else:
            # Delete tail cell if it didn't eat an apple to simulate sliding movement
            self.snake.pop()

    def save_score_entry(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:3] # Splice array down to best 3 matches
        self.score_logged = True

    def draw(self, surface):
        surface.fill(GAME_DARK_PURPLE)
        font = pygame.font.Font('freesansbold.ttf', 24)
       
        # Core UI labels
        score_surface = font.render(f"Score: {self.score}", True, TEXT_DARK_GRAY)
        surface.blit(score_surface, (45, 35))
       
        # Procedural vector Trophy design shapes
        tx, ty = 170, 30
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (tx, ty + 8, 18, 14), border_radius=3)
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (tx + 6, ty + 22, 6, 6))
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (tx + 2, ty + 26, 14, 3))
        
        hs_surface = font.render(f": {self.high_scores[0]}", True, TEXT_DARK_GRAY)
        surface.blit(hs_surface, (195, 35))
       
        # Header close window cross tracking layout lines
        pygame.draw.line(surface, TEXT_DARK_GRAY, (self.close_btn.left, self.close_btn.top), (self.close_btn.right, self.close_btn.bottom), 5)
        pygame.draw.line(surface, TEXT_DARK_GRAY, (self.close_btn.left, self.close_btn.bottom), (self.close_btn.right, self.close_btn.top), 5)

        # Alternating Checkerboard tile processing engine loops
        for r in range(self.rows):
            for c in range(self.cols):
                cx = self.grid_x + (c * self.cell_size)
                cy = self.grid_y + (r * self.cell_size)
                cell_box = pygame.Rect(cx, cy, self.cell_size, self.cell_size)
                
                tile_color = GRID_LIGHT_PURPLE if (r + c) % 2 == 0 else GAME_DARK_PURPLE
                pygame.draw.rect(surface, tile_color, cell_box)

        self.draw_maze_lines(surface)

        # Draw Target Objective Fruit
        food_pixel_x = self.grid_x + (self.food[0] * self.cell_size)
        food_pixel_y = self.grid_y + (self.food[1] * self.cell_size)
        
        if self.apple_img:
            surface.blit(self.apple_img, (food_pixel_x, food_pixel_y))
        else:
            # Vector fallback shapes if apple.png file path string error triggers
            fallback_cx = food_pixel_x + self.cell_size // 2
            fallback_cy = food_pixel_y + self.cell_size // 2
            pygame.draw.circle(surface, pygame.Color('#DC2626'), (fallback_cx, fallback_cy), 10)
            pygame.draw.circle(surface, pygame.Color('#22C55E'), (fallback_cx + 4, fallback_cy - 10), 3)

        # Multi-segment Snake element drawer engine parsing
        for index, block in enumerate(self.snake):
            bx = self.grid_x + (block[0] * self.cell_size)
            by = self.grid_y + (block[1] * self.cell_size)
            block_rect = pygame.Rect(bx, by, self.cell_size, self.cell_size)
           
            if index == 0: # HEAD EVALUATION STATE
                head_asset = None
                if self.direction == [0, -1]: head_asset = self.head_imgs["up"]
                elif self.direction == [0, 1]: head_asset = self.head_imgs["down"]
                elif self.direction == [1, 0]: head_asset = self.head_imgs["right"]
                elif self.direction == [-1, 0]: head_asset = self.head_imgs["left"]

                if head_asset:
                    surface.blit(head_asset, (bx, by))
                else:
                    # Fallback head block drawing style with eye center dot markers
                    pygame.draw.rect(surface, pygame.Color('#EC4899'), block_rect)
                    pygame.draw.circle(surface, pygame.Color('black'), (block_rect.centerx, block_rect.centery), 4)
            else: # BODY RENDERING SECTION
                # Procedural system generating pink mesh segments to link to image heads cleanly
                pygame.draw.rect(surface, pygame.Color('#F472B6'), block_rect)
                pygame.draw.rect(surface, pygame.Color('#EC4899'), block_rect, 1)

        # Dead crash announcement display layer window banner overlays
        if self.game_over:
            go_font = pygame.font.Font('freesansbold.ttf', 40)
            go_text = go_font.render("GAME OVER", True, pygame.Color('#EF4444'))
            surface.blit(go_text, go_text.get_rect(center=(self.screen_w // 2, self.screen_h // 2)))
           
            sub_font = pygame.font.Font('freesansbold.ttf', 18)
            sub_text = sub_font.render("Press R to Respawn / Restart Match", True, pygame.Color('white'))
            surface.blit(sub_text, sub_text.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 45)))

    def draw_maze_lines(self, surface):
        wall_color = pygame.Color('#111827')
        thickness = 4
        cs = self.cell_size
        gx, gy = self.grid_x, self.grid_y

        # Top-Left Maze Path
        pygame.draw.line(surface, wall_color, (gx + 2*cs, gy + 3*cs), (gx + 7*cs, gy + 3*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 2*cs, gy + 3*cs), (gx + 2*cs, gy + 7*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 2*cs, gy + 7*cs), (gx + 7*cs, gy + 7*cs), thickness)

        # Top-Right Maze Path
        pygame.draw.line(surface, wall_color, (gx + 11*cs, gy + 6*cs), (gx + 15*cs, gy + 6*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 15*cs, gy + 3*cs), (gx + 15*cs, gy + 6*cs), thickness)

        # Center Grid Box Cutout Path lines
        pygame.draw.line(surface, wall_color, (gx + 7*cs, gy + 7*cs), (gx + 7*cs, gy + 10*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 7*cs, gy + 7*cs), (gx + 10*cs, gy + 7*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 10*cs, gy + 7*cs), (gx + 10*cs, gy + 10*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 7*cs, gy + 10*cs), (gx + 10*cs, gy + 10*cs), thickness)

        # Bottom-Left Maze Path
        pygame.draw.line(surface, wall_color, (gx + 2*cs, gy + 11*cs), (gx + 2*cs, gy + 14*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 2*cs, gy + 14*cs), (gx + 7*cs, gy + 14*cs), thickness)

        # Bottom-Right Maze Path Intersections
        pygame.draw.line(surface, wall_color, (gx + 11*cs, gy + 14*cs), (gx + 15*cs, gy + 14*cs), thickness)
        pygame.draw.line(surface, wall_color, (gx + 13*cs, gy + 11*cs), (gx + 13*cs, gy + 15*cs), thickness)



# CENTRAL COORDINATOR CLASS (SYSTEM MAIN WINDOW MANAGER)

class MainAppController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Dash")
        
        # Transparent overlay mask container surface object for brightness sliders
        self.dimmer_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dimmer_surface.fill((0, 0, 0))
       
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Core execution window states tracker switch flag ("menu", "playing", "settings", "leaderboard")
        self.global_state = "menu"
        
        self.game_speed_mode = "Normal"
        self.audio_status = True
        
        # Custom user event acting as game engine physics updates clock step
        self.MOVE_TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_TICK, 160) # Moves position cells every 160ms interval
       
        # Setup view controller sub modules classes
        self.main_menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.game_play = SnakeGameplay(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Setting sub panel navigation controls buttons objects configuration variables
        self.back_to_menu_settings = Button(WINDOW_WIDTH//2 - 140, 500, 280, 55, "Back to Menu", "exit")
        self.back_to_menu_leaderboard = Button(WINDOW_WIDTH//2 - 140, 480, 280, 55, "Back to Menu", "exit")
        
        self.speed_toggle_btn = Button(WINDOW_WIDTH//2 - 140, 200, 280, 55, "Speed: Normal", "settings")
        self.sound_toggle_btn = Button(WINDOW_WIDTH//2 - 140, 275, 280, 55, "Sound: On", "play")
        self.intensity_slider = Slider(WINDOW_WIDTH//2 - 100, 390, 200, 1.0) # Full brightness initialization

    def run_main_loop(self):
        while self.is_running:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                   
                # STATE MACHINE CONTROLS ROUTING TRACKS 
                if self.global_state == "menu":
                    for btn in self.main_menu.buttons:
                        btn.check_hover(mx, my)
                        if btn.handle_click_event(event):
                            if btn.text == "Play":
                                self.game_play.start_new_match()
                                self.global_state = "playing"
                            elif btn.text == "Settings":
                                self.global_state = "settings"
                            elif btn.text == "Leaderboard":
                                self.global_state = "leaderboard"
                            elif btn.text == "Exit":
                                self.is_running = False
                               
                elif self.global_state == "playing":
                    # Redirect event payloads straight into snake direction logic engines
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.game_play.direction != [0, 1]:
                            self.game_play.next_direction = [0, -1]
                        elif event.key == pygame.K_DOWN and self.game_play.direction != [0, -1]:
                            self.game_play.next_direction = [0, 1]
                        elif event.key == pygame.K_LEFT and self.game_play.direction != [1, 0]:
                            self.game_play.next_direction = [-1, 0]
                        elif event.key == pygame.K_RIGHT and self.game_play.direction != [-1, 0]:
                            self.game_play.next_direction = [1, 0]
                        # Keyboard hotkey checking if snake died to reset scene matches
                        elif self.game_play.game_over and event.key == pygame.K_r:
                            self.game_play.start_new_match()
                            
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Monitor if close boundary corner buttons was tapped
                        if self.game_play.close_btn.collidepoint(event.pos):
                            self.game_play.save_score_entry()
                            self.global_state = "menu"
                            
                    # Process moving frames updates ticks timers
                    if event.type == self.MOVE_TICK:
                        self.game_play.trigger_tick_update()
                       
                elif self.global_state == "settings":
                    self.intensity_slider.process_mouse(event)
                    self.back_to_menu_settings.check_hover(mx, my)
                    self.speed_toggle_btn.check_hover(mx, my)
                    self.sound_toggle_btn.check_hover(mx, my)
                    
                    if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                        if self.back_to_menu_settings.handle_click_event(event):
                            self.global_state = "menu"
                        if self.speed_toggle_btn.handle_click_event(event):
                            if self.game_speed_mode == "Normal":
                                self.game_speed_mode = "Fast"
                                pygame.time.set_timer(self.MOVE_TICK, 90) # Accelerated millisecond refresh frame clocks
                            else:
                                self.game_speed_mode = "Normal"
                                pygame.time.set_timer(self.MOVE_TICK, 160)
                            self.speed_toggle_btn.text = f"Speed: {self.game_speed_mode}"
                        if self.sound_toggle_btn.handle_click_event(event):
                            self.audio_status = not self.audio_status
                            self.sound_toggle_btn.text = "Sound: On" if self.audio_status else "Sound: Off"

                elif self.global_state == "leaderboard":
                    self.back_to_menu_leaderboard.check_hover(mx, my)
                    if self.back_to_menu_leaderboard.handle_click_event(event):
                        self.global_state = "menu"

                # Global escape key shortcut listener mapping back to home panel options
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.global_state = "menu"

            #DISPLAY RENDER ROUTER LAYER DRAWER PIPELINES 
            if self.global_state == "menu":
                self.main_menu.draw(self.screen)
            elif self.global_state == "playing":
                self.game_play.draw(self.screen)
            elif self.global_state == "settings":
                self.screen.fill(pygame.Color('#5C3D99'))
                header_font = pygame.font.Font('freesansbold.ttf', 44)
                text_label = header_font.render("SETTINGS", True, BTN_TEXT_COLOR)
                self.screen.blit(text_label, text_label.get_rect(center=(WINDOW_WIDTH//2, 100)))
                
                self.speed_toggle_btn.draw(self.screen)
                self.sound_toggle_btn.draw(self.screen)
                
                label_font = pygame.font.Font('freesansbold.ttf', 20)
                caption = label_font.render(f"Brightness: {int(self.intensity_slider.val * 100)}%", True, BTN_TEXT_COLOR)
                self.screen.blit(caption, caption.get_rect(center=(WINDOW_WIDTH//2, 360)))
                self.intensity_slider.draw(self.screen)
                self.back_to_menu_settings.draw(self.screen)
                
            elif self.global_state == "leaderboard":
                self.screen.fill(pygame.Color('#311B57'))
                header_font = pygame.font.Font('freesansbold.ttf', 44)
                text_label = header_font.render("LEADERBOARD", True, BTN_TEXT_COLOR)
                self.screen.blit(text_label, text_label.get_rect(center=(WINDOW_WIDTH//2, 120)))
                
                rank_font = pygame.font.Font('freesansbold.ttf', 28)
                for index, record in enumerate(self.game_play.high_scores):
                    score_label = rank_font.render(f"Rank {index+1}:   {record} pts", True, BTN_NORMAL)
                    self.screen.blit(score_label, (WINDOW_WIDTH//2 - 100, 220 + index * 50))
                self.back_to_menu_leaderboard.draw(self.screen)

            # Apply tinted overlay surfaces mask to modify global window visual brightness alpha values
            brightness_pct = int((1.0 - self.intensity_slider.val) * 220)
            if brightness_pct > 0:
                self.dimmer_surface.set_alpha(brightness_pct)
                self.screen.blit(self.dimmer_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game_controller = MainAppController()
    game_controller.run_main_loop()


