import pygame
from button import Button


class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self._build_menu()

    def _build_menu(self):
        btn_w, btn_h = 240, 60
        start_y = 200
        spacing = 85
        x_pos = (self.screen_w // 2) - (btn_w // 2)


        # We only pass labels here. No functions or app references.
        menu_items = ["Play", "Settings", "Exit"]
       
        for i, label in enumerate(menu_items):
            y_pos = start_y + (i * spacing)
            btn = Button(x_pos, y_pos, btn_w, btn_h, label)
            self.buttons.append(btn)


    def draw(self, surface):
        #Draws the main menu container and title heading
        surface.fill(pygame.Color('#750b6e'))
       
        # Header title
        title_font = pygame.font.Font('freesansbold.ttf', 48)
        title_surf = title_font.render("Snake Dash", True, pygame.Color('White'))
        title_rect = title_surf.get_rect(center=(self.screen_w // 2, 100))
        surface.blit(title_surf, title_rect)
       
        # Render custom buttons
        for btn in self.buttons:
            btn.draw(surface)




class Game:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My Game Engine")
       
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "menu"
       
        # Look: No app instance or self passed here anymore!
        self.main_menu = MainMenu(self.width, self.height)


    # Engine Core Loops
    def run(self):
        while self.running:
            coords = pygame.mouse.get_pos()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        self.running = False
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
                           
                            # Instead of running btn.click(), we read the text property directly
                            if was_down and was_over:
                                if btn._text == "Play":
                                    self.current_state = "playing"
                                elif btn._text == "Settings":
                                    self.current_state = "settings_screen"

                                elif btn._text == "Exit":
                                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_state = "menu"


            # Layout Switch Board
            if self.current_state == "menu":
                self.main_menu.draw(self.screen)
            elif self.current_state == "playing":
                self.screen.fill(pygame.Color('darkblue'))
            elif self.current_state == "settings_screen":
                self.screen.fill(pygame.Color('darkgray'))
            elif self.current_state == "highscore_screen":
                self.screen.fill(pygame.Color('purple'))


            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()




if __name__ == "__main__":
    game = Game()
    game.run()



