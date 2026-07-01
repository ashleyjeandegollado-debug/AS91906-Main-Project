import pygame
import math

# Initialize Pygame text engine
pygame.font.init()


# BUTTON CLASS 

class Button:
    def __init__(self, x, y, w, h, text, icon_type):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon_type = icon_type
        
        self._mouse_over = False
        self._button_down = False
        
        # Color Palette
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
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._button_down = False
        return False

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
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy - 10), (icon_cx + 10, icon_cy + 10), 5)
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy + 10), (icon_cx + 10, icon_cy - 10), 5)
        elif self.icon_type == "back":
            # Draw a left pointing arrow
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy), (icon_cx + 10, icon_cy), 4)
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy), (icon_cx, icon_cy - 8), 4)
            pygame.draw.line(surface, self.icon_color, (icon_cx - 10, icon_cy), (icon_cx, icon_cy + 8), 4)



# SETTINGS MENU CLASS

class SettingsMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Core Game Setting States
        self.volume_on = True
        self.brightness = 0.8  # Value between 0.0 and 1.0
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.diff_index = 1    # Defaults to "Medium"
        
        # UI Alignment Layout
        self.content_x = self.screen_w // 2 - 50
        self.label_x = self.screen_w // 2 - 180
        
        # Interactive UI Objects
        self.vol_rect = pygame.Rect(self.content_x, 235, 80, 40)
        self.slider_rect = pygame.Rect(self.content_x, 320, 200, 12)
        self.diff_rect = pygame.Rect(self.content_x, 385, 160, 40)
        self.back_button = Button(self.screen_w // 2 - 140, 490, 280, 60, "Back", "back")
        
        # State tracking for drag physics
        self.dragging_slider = False
        
        # Custom complementary colors
        self.ui_dark = pygame.Color('#6F4A9E')
        self.ui_light = pygame.Color('#EADBFF')
        self.ui_accent = pygame.Color('#3A41A4')

    def mouse_move(self, mx, my):
        self.back_button.mouse_move(mx, my)
        
        # Handle dragging logic for Brightness Slider
        if self.dragging_slider:
            # Clamp value between the slider tracks bounding box
            relative_x = max(0, min(mx - self.slider_rect.x, self.slider_rect.width))
            self.brightness = relative_x / self.slider_rect.width

    def mouse_click(self, event):
        mx, my = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1. Volume Toggle Button clicked
            if self.vol_rect.collidepoint(mx, my):
                self.volume_on = not self.volume_on
            
            # 2. Brightness Slider clicked
            elif self.slider_rect.inflate(0, 20).collidepoint(mx, my): # Inflate broadens vertical click target
                self.dragging_slider = True
                relative_x = max(0, min(mx - self.slider_rect.x, self.slider_rect.width))
                self.brightness = relative_x / self.slider_rect.width
                
            # 3. Difficulty Cycle Button clicked
            elif self.diff_rect.collidepoint(mx, my):
                self.diff_index = (self.diff_index + 1) % len(self.difficulties)
                
            # 4. Back Button Action
            if self.back_button.mouse_click(event):
                return "main_menu"
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_slider = False
            self.back_button.mouse_click(event)
            
        return "settings"

    def draw(self, surface):
        # Base Menu Background 
        surface.fill(pygame.Color('#D3B5E5'))
        
        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 52)
        title_surf = title_font.render("Settings", True, self.ui_accent)
        surface.blit(title_surf, (self.screen_w // 2 - title_surf.get_width() // 2, 80))
        
        label_font = pygame.font.Font('freesansbold.ttf', 24)
        value_font = pygame.font.Font('freesansbold.ttf', 20)
        

        # 1. RENDER VOLUME ROW
   
        vol_label = label_font.render("Volume", True, self.ui_dark)
        surface.blit(vol_label, (self.label_x, self.vol_rect.centery - vol_label.get_height() // 2))
        
        # Draw pill container background for Volume
        vol_bg = pygame.Color('#B18FCF') if self.volume_on else pygame.Color('#9581A6')
        pygame.draw.rect(surface, vol_bg, self.vol_rect, border_radius=10)
        
        # Dynamic Text Status
        vol_txt = "ON" if self.volume_on else "OFF"
        vol_surf = value_font.render(vol_txt, True, self.ui_light)
        surface.blit(vol_surf, (self.vol_rect.centerx - vol_surf.get_width() // 2, self.vol_rect.centery - vol_surf.get_height() // 2))
        
    
        # 2. RENDER BRIGHTNESS ROW
    
        bright_label = label_font.render("Brightness", True, self.ui_dark)
        surface.blit(bright_label, (self.label_x, self.slider_rect.centery - bright_label.get_height() // 2))
        
        # Draw Slider Background Track
        pygame.draw.rect(surface, pygame.Color('#9581A6'), self.slider_rect, border_radius=4)
        
        # Draw Slider Fill Track (representing progress value)
        fill_width = int(self.slider_rect.width * self.brightness)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y, fill_width, self.slider_rect.height)
            pygame.draw.rect(surface, self.ui_light, fill_rect, border_radius=4)
            
        # Draw Slider Circular Handle (Knob)
        knob_x = self.slider_rect.x + fill_width
        pygame.draw.circle(surface, self.ui_dark, (knob_x, self.slider_rect.centery), 10)
        
      
        # 3. RENDER DIFFICULTY ROW

        diff_label = label_font.render("Difficulty", True, self.ui_dark)
        surface.blit(diff_label, (self.label_x, self.diff_rect.centery - diff_label.get_height() // 2))
        
        # Draw button frame
        pygame.draw.rect(surface, pygame.Color('#B18FCF'), self.diff_rect, border_radius=10)
        
        # Print string state
        current_diff = self.difficulties[self.diff_index]
        diff_surf = value_font.render(current_diff, True, self.ui_light)
        surface.blit(diff_surf, (self.diff_rect.centerx - diff_surf.get_width() // 2, self.diff_rect.centery - diff_surf.get_height() // 2))


        # 4. BACK BUTTON

        self.back_button.draw(surface)



# MAIN MENU CLASS
class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self._build_menu()

    def _build_menu(self):
        btn_w, btn_h = 280, 60
        start_y = 240
        spacing = 80
        x_pos = (self.screen_w // 2) - (btn_w // 2)

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
       
        title_font = pygame.font.Font('freesansbold.ttf', 56)
        dash_font = pygame.font.Font('freesansbold.ttf', 72)
        
        snake_surf = title_font.render("Snake", True, pygame.Color('#7D5BA6'))
        surface.blit(snake_surf, (self.screen_w // 2 - 160, 90))
        
        dash_surf = dash_font.render("Dash", True, pygame.Color('#3A41A4'))
        surface.blit(dash_surf, (self.screen_w // 2 - 10, 110))
        
        for btn in self.buttons:
            btn.draw(surface)

# EXECUTABLE GAME LOOP ENTRY POINT

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Dash - Menu System")
    clock = pygame.time.Clock()
    
    # State tracking variable: "main_menu" or "settings"
    current_state = "main_menu"
    
    main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    settings_menu = SettingsMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.get_event_loop():
            if event.type == pygame.QUIT:
                running = False
                
            if current_state == "main_menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in main_menu.buttons:
                        if btn.rect.collidepoint(mx, my):
                            if btn.icon_type == "settings":
                                current_state = "settings"
                            elif btn.icon_type == "exit":
                                running = False
                                
            elif current_state == "settings":
                # Settings changes state back if user hits "Back"
                current_state = settings_menu.mouse_click(event)

        # Send structural mouse location updates
        if current_state == "main_menu":
            for btn in main_menu.buttons:
                btn.mouse_move(mx, my)
        elif current_state == "settings":
            settings_menu.mouse_move(mx, my)
            
        # Rendering Screen pass
        if current_state == "main_menu":
            main_menu.draw(screen)
        elif current_state == "settings":
            settings_menu.draw(screen)
            
            # Application of Brightness to screen view:
            # Overlays a dark filter to change screen brightness levels based on setting
            if settings_menu.brightness < 1.0:
                darkness = int((1.0 - settings_menu.brightness) * 180)
                dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                dim_overlay.fill((0, 0, 0))
                dim_overlay.set_alpha(darkness)
                screen.blit(dim_overlay, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()

