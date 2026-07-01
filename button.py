import pygame

class Button():
    # class defaults
    MIN_BUTTON_W = 100
    MIN_BUTTON_H = 50
    CLICK_OFFSET = 5

    DEFAULT_FONT = 'freesansbold.ttf'
    DEFAULT_FONT_SIZE = 20

    FONT_COLOR = pygame.Color('Black')
    HIGHLIGHT_COLOR = pygame.Color('darkgrey')
    BG_COLOR = pygame.Color('Purple')
    BORDER_COLOR = pygame.Color('Black')

    def __init__(self, x, y, w, h, text, font = None, font_color = FONT_COLOR, highlight_color = HIGHLIGHT_COLOR, bg_color = BG_COLOR, border_color = BORDER_COLOR):
        # init internal variables
        self._mouse_over = False
        self._button_down = False
        self._disabled = False  # need to make property for this.
        self._border = 4        # border width. not configurable yet 

        if w < Button.MIN_BUTTON_W:
            self._w = Button.MIN_BUTTON_W
        else:
            self._w = w
        if h < Button.MIN_BUTTON_H:
            self._h = Button.MIN_BUTTON_H
        else:
            self._h = h
        self._x = x
        self._y = y
        self._text = text
        if font is None:
            self._font = pygame.font.Font( Button.DEFAULT_FONT, self.DEFAULT_FONT_SIZE)
        else: 
            self._font = font
        self._font_color = font_color
        self._bg_color = bg_color
        self._border_color = border_color
        self._highlight_color = highlight_color
        self._down = False
        self._action = None


    def click(self):
        if self._action == None:
            print("No action function set for button:", self._text)
        else:
            self._action()

    def contains(self, x, y):
        return self.get_rect().collidepoint(x, y)
    
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)
    def mouse_move(self, x, y):
        if not self._disabled:
            if self.contains( x, y):
                self._mouse_over = True
            else:
                self._mouse_over = False

    def mouse_click(self, event):
        if not self._disabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._mouse_over:
                    self._button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._button_down and self._mouse_over:
                    if not self._action is None:
                        self._action() # I'm clicked
                    else:
                        print("button", self._text, "has no function set")
                self._button_down = False

    def set_action(self, action_function):
        if type(action_function).__name__ == 'function':
            self._action = action_function
    def get_action(self):
        return self._action
    action = property(get_action, set_action)

    def draw(self, screen):
        # draw rectangle
        pygame.draw.rect(screen, self._border_color, self.get_rect())
        pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x + self._border, self._y + self._border, self._w - self._border*2, self._h - self._border*2))

        # draw the text
        color = self._font_color
        offset = 0
        if self._mouse_over:
            if self._button_down:
                offset = Button.CLICK_OFFSET
            else:
                color = self._highlight_color
        
        # create the rendered text as a surface
        rendered_text = self._font.render(self._text, True, color, self._bg_color)
        # get the rectangle for this new surface
        rendered_text_rect = rendered_text.get_rect() 
        # set the centre of this rectangle to the centre of this button (self)
        rendered_text_rect.center = (self._x + self._w / 2 + offset, self._y + self._h / 2 + offset)
        screen.blit(rendered_text, rendered_text_rect)
        
# Testing Code
if __name__ == "__main__":\
    # a few constants for testing
    TEST_X = 50
    TEST_Y = 50
    TEST_W = 200
    TEST_H = 100
    BLUE = pygame.Color("blue")

    # a simple sample function to set for the button action
    def test_click():
        print("The test button was clicked")

    # init pygame and open the window
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    quitting = False
    
    my_button = Button(TEST_X, TEST_Y+TEST_H, TEST_W, TEST_H, "OK", border_color=BLUE)
    my_button.action = test_click

    while not quitting:
        coords = pygame.mouse.get_pos()
        # check the even queue for messages
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True

            # tell the button about mouse events
            if event.type == pygame.MOUSEMOTION:
                my_button.mouse_move(coords[0], coords[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                my_button.mouse_click(event)
            if event.type == pygame.MOUSEBUTTONUP:
                my_button.mouse_click(event)
        #Clear The Screen
        screen.fill(pygame.Color('Violet'))

        # draw my button
        my_button.draw(screen)

        # make the new screen visible
        pygame.display.flip()

    pygame.quit()
    quit()
        