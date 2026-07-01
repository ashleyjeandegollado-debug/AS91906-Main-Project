import pygame
import math



# BUTTON CLASS

class Button:
    def __init__(self, x, y, w, h, text, icon_type):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon_type = icon_type
        
        # State tracking for mouse interaction
        self._mouse_over = False
        self._button_down = False
        
        # Color Palette matching the image
        self.base_color = pygame.Color('#B18FCF')  # Pastel Lavender
        self.hover_color = pygame.Color('#9A73BE') # Slightly darker for hover
        self.text_color = pygame.Color('#EADBFF')  # Very light purple/white text
        self.icon_color = pygame.Color('#6F4A9E')  # Deep purple for icons

    def mouse_move(self, mx, my):
        """Checks if the mouse is hovering over the button."""
        self._mouse_over = self.rect.collidepoint(mx, my)

    def mouse_click(self, event):
        """Tracks click down and release states."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._mouse_over:
                self._button_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._button_down = False

    def draw(self, surface):
        """Draws the pill-shaped button, text, and its corresponding icon."""
        # Visual feedback for hover
        current_color = self.hover_color if self._mouse_over else self.base_color
        
        # Draw rounded button (border_radius makes it pill-shaped)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.rect.height // 2)
        
        # Load font and render text
        font = pygame.font.Font('freesansbold.ttf', 26)
        text_surf = font.render(self.text, True, self.text_color)
        
        # Position text on the left side of the button
        text_rect = text_surf.get_rect()
        text_rect.left = self.rect.left + 35
        text_rect.centery = self.rect.centery
        surface.blit(text_surf, text_rect)
        
        # Draw stylized icons on the right side of the button
        icon_cx = self.rect.right - 45
        icon_cy = self.rect.centery
        
        if self.icon_type == "play":
            # Draw a Right-pointing Triangle
            points = [
                (icon_cx - 10, icon_cy - 12),
                (icon_cx - 10, icon_cy + 12),
                (icon_cx + 15, icon_cy)
            ]
            pygame.draw.polygon(surface, self.icon_color, points)
            
        elif self.icon_type == "settings":
            # Draw a simplified Settings Gear
            pygame.draw.circle(surface, self.icon_color, (icon_cx, icon_cy), 12)
            pygame.draw.circle(surface, current_color, (icon_cx, icon_cy), 5) # Inner cutout
            # Small notches around the gear
            for i in range(8):
                angle = i * (math.pi / 4)
                nx = icon_cx + int(14 * math.cos(angle))
                ny = icon_cy + int(14 * math.sin(angle))
                pygame.draw.circle(surface, self.icon_color, (nx, ny), 3)
                
        elif self.icon_type == "leaderboard":
            # Draw a Golden/Deep Purple Trophy shape
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 10, icon_cy - 12, 20, 14), border_radius=3)
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 3, icon_cy + 2, 6, 8))
            pygame.draw.rect(surface, self.icon_color, (icon_cx - 12, icon_cy + 10, 24, 4))
            
        elif self.icon_type == "exit":
            # Draw an 'X' shape
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy - 10), (icon_cx + 10, icon_cy + 10), 5)
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy + 10), (icon_cx + 10, icon_cy - 10), 5)



# MAIN MENU CLASS

class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self._build_menu()

    def _build_menu(self):
        # Adjusted sizes to match the layout proportions of the image
        btn_w, btn_h = 280, 60
        start_y = 240
        spacing = 80
        x_pos = (self.screen_w // 2) - (btn_w // 2)

        # Labels mapped to their respective drawn icons
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
        """Draws the background color, title typography, and menu buttons."""
        # Soft pastel purple background matching your layout image
        surface.fill(pygame.Color('#D3B5E5'))
       
        
        # TITLE DESIGN 
       
        title_font = pygame.font.Font('freesansbold.ttf', 56)
        dash_font = pygame.font.Font('freesansbold.ttf', 72)
        
        # 1. "Snake" Text (Left side, medium purple)
        snake_surf = title_font.render("Snake", True, pygame.Color('#7D5BA6'))
        surface.blit(snake_surf, (self.screen_w // 2 - 160, 90))
        
        # 2. "Dash" Text (Slightly lower, overlapping right side, darker blue/purple)
        dash_surf = dash_font.render("Dash", True, pygame.Color('#3A41A4'))
        surface.blit(dash_surf, (self.screen_w // 2 - 10, 110))
        
        # Render all menu buttons
        for btn in self.buttons:
            btn.draw(surface)



# GAME ENGINE CORE

class Game:
    #screen size of the game
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 650
        # screen display
        self.screen = pygame.display.set_mode((self.width, self.height))
        #caption of the game
        pygame.display.set_caption("Snake Dash - Main Menu")
       
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "menu"
       
        self.main_menu = MainMenu(self.width, self.height)

    def run(self):
        while self.running:
            coords = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # direction of mouse in buttons
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
                           # Stating the clicked button
                            btn.mouse_click(event)
                           
                            # State switcher evaluation based on text properties
                            if was_down and was_over:
                                if btn.text == "Play":
                                    self.current_state = "playing"
                                elif btn.text == "Settings":
                                    self.current_state = "settings_screen"
                                elif btn.text == "Leaderboard":
                                    self.current_state = "highscore_screen"
                                elif btn.text == "Exit":
                                    self.running = False
                               
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_state = "menu"

            # Layout Switch Board rendering
            if self.current_state == "menu":
                self.main_menu.draw(self.screen)
            elif self.current_state == "playing":
                self.screen.fill(pygame.Color('#4A2E80')) # State transitions use thematic colors
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
