import pygame
import math
import random




# BUTTON CLASS
class Button:
    def __init__(self, x, y, w, h, text, icon_type):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon_type = icon_type
       
        self._mouse_over = False
        self._button_down = False
       
        self.base_color = pygame.Color('#B18FCF')  
        self.hover_color = pygame.Color('#9A73BE')
        self.text_color = pygame.Color('#EADBFF')  
        self.icon_color = pygame.Color('#6F4A9E')  


    def mouse_move(self, mx, my):
        self._mouse_over = self.rect.collidepoint(mx, my)


    def mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._mouse_over:
                self._button_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._button_down = False


    def draw(self, surface):
        current_color = self.hover_color if self._mouse_over else self.base_color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.rect.height // 2)
       
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_surf = font.render(self.text, True, self.text_color)
       
        text_rect = text_surf.get_rect()
        text_rect.left = self.rect.left + 35
        text_rect.centery = self.rect.centery
        surface.blit(text_surf, text_rect)
       
        icon_cx = self.rect.right - 45
        icon_cy = self.rect.centery
       
        if self.icon_type == "play":
            points = [(icon_cx - 10, icon_cy - 12), (icon_cx - 10, icon_cy + 12), (icon_cx + 15, icon_cy)]
            pygame.draw.polygon(surface, self.icon_color, points)
        elif self.icon_type == "settings":
            pygame.draw.circle(surface, self.icon_color, (icon_cx, icon_cy), 12)
            pygame.draw.circle(surface, current_color, (icon_cx, icon_cy), 5)
            for i in range(8):
                angle = i * (math.pi / 4)
                nx = icon_cx + int(14 * math.cos(angle))
                ny = icon_cy + int(14 * math.sin(angle))
                pygame.draw.circle(surface, self.icon_color, (nx, ny), 3)
        elif self.icon_type == "leaderboard":
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 10, icon_cy - 12, 20, 14), border_radius=3)
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 3, icon_cy + 2, 6, 8))
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 12, icon_cy + 10, 24, 4))
        elif self.icon_type == "exit":
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy - 10), (icon_cx + 10, icon_cy + 10), 4)
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy + 10), (icon_cx + 10, icon_cy - 10), 4)






# MAIN MENU CLASS


class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self._build_menu()


    def _build_menu(self):
        btn_w, btn_h = 280, 60
        start_y = 260
        spacing = 80
        x_pos = (self.screen_w // 2) - (btn_w // 2)
        #list of menu items
        menu_items = [
            ("Play", "play"),
            ("Settings", "settings"),
            ("Leaderboard", "leaderboard"),
            ("Exit", "exit")
        ]
       
        for i, (label, icon) in enumerate(menu_items):
            y_pos = start_y + (i * spacing)
            btn = Button(x_pos, y_pos, btn_w, btn_h, label, icon)
            self.buttons.append(btn)


    def draw(self, surface):
        surface.fill(pygame.Color('#D3B5E5'))
       
        # "Snake Dash" Heading Design
        title_font = pygame.font.Font('freesansbold.ttf', 56)
        dash_font = pygame.font.Font('freesansbold.ttf', 72)#font sytle of each word of the heading
        #design of the word snake and rendering it
        snake_surf = title_font.render("Snake", True, pygame.Color('#7D5BA6'))
        surface.blit(snake_surf, (self.screen_w // 2 - 160, 100))
        #rendering the word Dash of the heading
        dash_surf = dash_font.render("Dash", True, pygame.Color('#3A41A4'))
        surface.blit(dash_surf, (self.screen_w // 2 - 10, 120))
       
        for btn in self.buttons:
            btn.draw(surface)




# SNAKE GAMEPLAY  
class SnakeGameplay:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
       
        # Grid Setup (16x16 board)
        self.grid_cols = 16
        self.grid_rows = 16
        self.cell_size = 28
       
        # Center the grid on screen horizontally, push down for header UI
        self.grid_x = (self.screen_w - (self.grid_cols * self.cell_size)) // 2
        self.grid_y = 110
       
        # UI Top Exit Button
        self.exit_btn_rect = pygame.Rect(self.screen_w - 65, 30, 35, 35)
       
        self.high_score = 0
        self.reset_game()


    def reset_game(self):
        self.score = 0
       
        # Starting positioning: Facing right towards the bottom half
        self.snake = [
            [7, 12], # Head
            [6, 12],
            [5, 12],
            [4, 12]  # Tail
        ]
        self.direction = [1, 0] # Moving Right
        self.next_direction = [1, 0]
       
        self.spawn_food()
        self.game_over = False


    def spawn_food(self):
        while True:
            self.food = [random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1)]
           
            # Check if food spawned inside the snake
            if self.food in self.snake:
                continue
               
            # Verify food doesn't clip directly through custom map line walls
            # keeping it clear of obstacle boundaries
            break


    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != [0, 1]:
                self.next_direction = [0, -1]
            elif event.key == pygame.K_DOWN and self.direction != [0, -1]:
                self.next_direction = [0, 1]
            elif event.key == pygame.K_LEFT and self.direction != [1, 0]:
                self.next_direction = [-1, 0]
            elif event.key == pygame.K_RIGHT and self.direction != [-1, 0]:
                self.next_direction = [1, 0]
               
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.exit_btn_rect.collidepoint(event.pos):
                return "menu"
        return "playing"


    def update(self):
        if self.game_over:
            return


        self.direction = self.next_direction
       
        # Calculate new head position
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
       
        # 1. Boundary Wall Collision Checks
        if new_head[0] < 0 or new_head[0] >= self.grid_cols or new_head[1] < 0 or new_head[1] >= self.grid_rows:
            self.game_over = True
            return
           
        # 2. Self Collision Checks
        if new_head in self.snake:
            self.game_over = True
            return
           
        # 3. Custom Line Wall Maze Collisions (Hardcoded to match image layout positions)
        if self.check_obstacle_collision(new_head):
            self.game_over = True
            return


        # Advance snake
        self.snake.insert(0, new_head)


        # 4. Food Collection Logic
        if new_head == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.spawn_food()
        else:
            self.snake.pop()


    def check_obstacle_collision(self, head):
        hx, hy = head[0], head[1]
       
        # Top-Left Loop Wall
        if hx == 2 and (3 <= hy <= 6): return True
        if hy == 3 and (2 <= hx <= 6): return True
        if hy == 6 and (2 <= hx <= 6): return True
       
        # Top-Right Angle Wall
        if hx == 14 and (2 <= hy <= 6): return True
        if hy == 6 and (11 <= hx <= 14): return True
       
        # Bottom-Left Angle Wall
        if hx == 2 and (11 <= hy <= 13): return True
        if hy == 13 and (2 <= hx <= 6): return True
       
        # Bottom-Right Intersecting Wall Structures
        if hx == 12 and (11 <= hy <= 14): return True
        if hy == 13 and (10 <= hx <= 14): return True


        return False


    def draw(self, surface):
           # Main background fill
        surface.fill(pygame.Color('#A855F7')) # True solid layout background tone
        # TOP BANNER PANEL (Scores & Exit Controls)
        font = pygame.font.Font('freesansbold.ttf', 24)
       
        # Render "Score: X"
        score_txt = font.render(f"Score: {self.score}", True, pygame.Color('#374151'))
        surface.blit(score_txt, (45, 35))
       
        # Trophy Graphic Placeholder
        trophy_x, trophy_y = 170, 30
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (trophy_x, trophy_y + 8, 18, 14), border_radius=3)
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (trophy_x + 6, trophy_y + 22, 6, 6))
        pygame.draw.rect(surface, pygame.Color('#EAB308'), (trophy_x + 2, trophy_y + 26, 14, 3))
        # High Score Value text output next to trophy
        hs_txt = font.render(f": {self.high_score}", True, pygame.Color('#374151'))
        surface.blit(hs_txt, (195, 35))
       
        # Cross Exit Button Icon Layout
        pygame.draw.line(surface, pygame.Color('#374151'), (self.exit_btn_rect.left, self.exit_btn_rect.top), (self.exit_btn_rect.right, self.exit_btn_rect.bottom), 5)
        pygame.draw.line(surface, pygame.Color('#374151'), (self.exit_btn_rect.left, self.exit_btn_rect.bottom), (self.exit_btn_rect.right, self.exit_btn_rect.top), 5)


       
        # CHECKERBOARD PLAYSPACE GRID
     
        color_light = pygame.Color('#C084FC')
        color_dark = pygame.Color('#A855F7')
       
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell_rect = pygame.Rect(self.grid_x + (c * self.cell_size), self.grid_y + (r * self.cell_size), self.cell_size, self.cell_size)
                current_cell_color = color_light if (r + c) % 2 == 0 else color_dark
                pygame.draw.rect(surface, current_cell_color, cell_rect)


     
        # DRAW MAZE LINE OBSTACLES
       
        self.draw_maze_lines(surface)


       
        # DRAW GAME FRUIT (Apple)
       
        food_rx = self.grid_x + (self.food[0] * self.cell_size) + self.cell_size // 2
        food_ry = self.grid_y + (self.food[1] * self.cell_size) + self.cell_size // 2
        pygame.draw.circle(surface, pygame.Color('#DC2626'), (food_rx, food_ry), 10) # Base Red
        pygame.draw.circle(surface, pygame.Color('#22C55E'), (food_rx + 4, food_ry - 10), 3) # Little Leaf


       
        # DRAW PINK MESH SNAKE
     
        for idx, segment in enumerate(self.snake):
            seg_x = self.grid_x + (segment[0] * self.cell_size)
            seg_y = self.grid_y + (segment[1] * self.cell_size)
            seg_rect = pygame.Rect(seg_x, seg_y, self.cell_size, self.cell_size)
           
            # Pink base body shade matching your Canva-textured snake layout
            pygame.draw.rect(surface, pygame.Color('#F472B6'), seg_rect)
            pygame.draw.rect(surface, pygame.Color('#EC4899'), seg_rect, 1) # Mesh grid framing
           
            # Head detail additions (Eyes)
            if idx == 0:
                eye_radius = 4
                # Dynamically offset eyes depending on travel direction
                if self.direction == [1, 0] or self.direction == [-1, 0]: # Horizontal
                    pygame.draw.circle(surface, pygame.Color('black'), (seg_rect.centerx, seg_rect.top + 7), eye_radius)
                    pygame.draw.circle(surface, pygame.Color('black'), (seg_rect.centerx, seg_rect.bottom - 7), eye_radius)
                else: # Vertical
                    pygame.draw.circle(surface, pygame.Color('black'), (seg_rect.left + 7, seg_rect.centery), eye_radius)
                    pygame.draw.circle(surface, pygame.Color('black'), (seg_rect.right - 7, seg_rect.centery), eye_radius)


        # Game Over Banner Overlay
        if self.game_over:
            go_font = pygame.font.Font('freesansbold.ttf', 40)
            go_surf = go_font.render("GAME OVER", True, pygame.Color('#EF4444'))
            go_rect = go_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2))
           
            sub_font = pygame.font.Font('freesansbold.ttf', 18)
            sub_surf = sub_font.render("Press R to Respawn / Restart Match", True, pygame.Color('white'))
            sub_rect = sub_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 45))
           
            surface.blit(go_surf, go_rect)
            surface.blit(sub_surf, sub_rect)


    def draw_maze_lines(self, surface):
        black = pygame.Color('#111827')
        w = 3 # Match line weight thickness
        cs = self.cell_size
        gx, gy = self.grid_x, self.grid_y


        # Top-Left Loop Wall
        pygame.draw.line(surface, black, (gx + 2*cs, gy + 3*cs), (gx + 7*cs, gy + 3*cs), w)
        pygame.draw.line(surface, black, (gx + 2*cs, gy + 3*cs), (gx + 2*cs, gy + 7*cs), w)
        pygame.draw.line(surface, black, (gx + 2*cs, gy + 7*cs), (gx + 7*cs, gy + 7*cs), w)


        # Top-Right Angle Wall
        pygame.draw.line(surface, black, (gx + 11*cs, gy + 6*cs), (gx + 15*cs, gy + 6*cs), w)
        pygame.draw.line(surface, black, (gx + 15*cs, gy + 3*cs), (gx + 15*cs, gy + 6*cs), w)

        # Bottom-Left Angle Wall
        pygame.draw.line(surface, black, (gx + 2*cs, gy + 11*cs), (gx + 2*cs, gy + 14*cs), w)
        pygame.draw.line(surface, black, (gx + 2*cs, gy + 14*cs), (gx + 7*cs, gy + 14*cs), w)


        # Bottom-Right Intersecting Wall Structures
        pygame.draw.line(surface, black, (gx + 11*cs, gy + 14*cs), (gx + 13*cs, gy + 14*cs), w)
        pygame.draw.line(surface, black, (gx + 13*cs, gy + 11*cs), (gx + 13*cs, gy + 15*cs), w)
        pygame.draw.line(surface, black, (gx + 11*cs, gy + 14*cs), (gx + 11*cs, gy + 15*cs), w)
        pygame.draw.line(surface, black, (gx + 13*cs, gy + 14*cs), (gx + 15*cs, gy + 14*cs), w)






# GAME ENGINE CORE SWITCHBOARD


class Game:
    def __init__(self):
        pygame.init()
        self.width = 540
        self.height = 620
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Dash")
       
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "menu"
       
        # Frame-rate tick management for step limits on game loop update
        self.SNAKE_UPDATE_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.SNAKE_UPDATE_EVENT, 160) # Moves every 160ms
       
        self.main_menu = MainMenu(self.width, self.height)
        self.gameplay = SnakeGameplay(self.width, self.height)


    def run(self):
        while self.running:
            coords = pygame.mouse.get_pos()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                   
                # MENU ENVIRONMENT LOGIC HANDLERS
                if self.current_state == "menu":
                    if event.type == pygame.MOUSEMOTION:
                        for btn in self.main_menu.buttons:
                            btn.mouse_move(coords[0], coords[1])
                           
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for btn in self.main_menu.buttons:
                            btn.mouse_click(event)
                           
                    if event.type == pygame.MOUSEBUTTONUP:
                        for btn in self.main_menu.buttons:
                            was_down = btn._button_down
                            was_over = btn._mouse_over
                            btn.mouse_click(event)
                           
                            if was_down and was_over:
                                if btn.text == "Play":
                                    self.gameplay.reset_game()
                                    self.current_state = "playing"
                                elif btn.text == "Settings":
                                    self.current_state = "settings_screen"
                                elif btn.text == "Leaderboard":
                                    self.current_state = "highscore_screen"
                                elif btn.text == "Exit":
                                    self.running = False
                               
                # RUNNING SNAKE GAMEPLAY LOGIC HANDLERS
                elif self.current_state == "playing":
                    next_state = self.gameplay.handle_input(event)
                    if next_state == "menu":
                        self.current_state = "menu"
                   
                    # Keyboard action handling if dead to restart game instance
                    if self.gameplay.game_over and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.gameplay.reset_game()
                           
                    # Game speed tick execution loop trigger
                    if event.type == self.SNAKE_UPDATE_EVENT:
                        self.gameplay.update()
                       
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_state = "menu"


            # Layout Switch Board Rendering Engine Router
            if self.current_state == "menu":
                self.main_menu.draw(self.screen)
            elif self.current_state == "playing":
                self.gameplay.draw(self.screen)
            elif self.current_state == "settings_screen":
                self.screen.fill(pygame.Color('#5C3D99'))
            elif self.current_state == "highscore_screen":
                self.screen.fill(pygame.Color('#311B57'))


            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()




if __name__ == "__main__":
    game = Game()
    game.run()




