import pygame
from imagelist import ImageList
import debug
import time

SCREEN_WIDTH= 640
SCREEN_HEIGHT= 480


class MySprite():
    def __init__ (self, x, y, w, h, images, screen):
        valid = True    
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._xd = 0
        self._yd = 0
        self._images= images
        self._screen= screen
       
        # set default frame
        self._current_frame = 0
        self._start_frame = 0
        self._end_frame = 0
        self._delay = -1 # default to not animating
        self._repeat = False
        self._next_move = time.time()
        self._move_delay = 0

        if not valid:
            print("Invalid. Quit.")
            exit(0)




# internal get/set functions
    def get_x(self):
        return self._x
    def set_x(self, x):
        if x>=0 and x<= SCREEN_WIDTH:
            self._x = x
        elif x<0:
            self._x = 0
        else:
            self._x = SCREEN_WIDTH - 1

    def get_y(self):
        return self._y
    def set_y(self, y):
        if y>=0 and y<= SCREEN_HEIGHT:
            self._y = y
        elif y<0:
            self._y = 0
        else:
            self._y = SCREEN_HEIGHT - 1
   
    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def set_pos(self, x, y):
        self._x(x)
        self._y(y)
       
    def move(self, x_delta=None, y_delta=None, delay = None):
        # changing the vector if required
        if not x_delta is None:
            self._xd = x_delta
        if not y_delta is None:
            self._yd = y_delta
        if not delay is None:
            self._move_delay = delay
            if not delay == self._move_delay:
                self._next_move = time.time() + delay
       
        if time.time() > self._next_move:
            self.set_x(self._x + self._xd)
            self.set_y(self._y + self._yd)
            self._next_move = self._next_move + self._move_delay

    def collide(self, other_rect):
        if isinstance(other_rect, pygame.Rect):
            if not (self._x + self._w < other_rect.x or \
                self._y + self._h > other_rect.y or \
                self._x + self._w > other_rect.x or \
                self._y + self._h < other_rect.y):
                return True
            else:
                return False
        else:
            pass

    def set_animation(self, start_frame= 0, end_frame=0, delay=0, repeat=-1):
        if start_frame >=0 and len(self._images.images):
            self._start_frame = start_frame
        if end_frame >=0 and len(self._images.images) and start_frame <= end_frame:
            self._end_frame = end_frame
        if delay > 0:
            self._delay = delay
        if repeat:        
            self._repeat = True
        else:
            self._repeat = False

        self._next_frame = time.time() + delay

    def animate(self, reset_animation = False):
        if not self._delay == -1:
            # if we're resetting
            if reset_animation == True:
                self._current_frame = self._start_frame
            else:
                if time.time() > self._next_frame:
                    # go to our next frame
                    if self._current_frame < self._end_frame:
                        self._current_frame += 1
                    elif self._repeat == True:
                        self._current_frame = self._start_frame
                    self._next_frame = self._next_frame + self._delay
    def get_rect(self):
        return pygame.Rect (self._x, self._y, self._w, self._h)



    def draw(self):
        self._screen.blit(self._images.images[self._current_frame], self.get_rect())
       
# testing code
debug.DEBUG_LEVEL= 0
if __name__=="__main__":
    # starting up pygame
    pygame.init()
    # setting up window
    screen= pygame.display.set_mode((640,480), pygame.RESIZABLE)
    TEXT_X = 50
    TEXT_Y = 50
    TEXT_W = 50
    TEXT_H = 50
    # image list for sprite
    image_obj= ImageList("images\\test",64,64, "jpg")
    debug.dprint(1, "image list test class created")

    spritelist = []
    spritelist.append(MySprite(TEXT_X + TEXT_W, TEXT_Y, TEXT_W, TEXT_H, image_obj, screen))
    spritelist[-1].set_animation(0, 3, 0.1, True)
    quitting = False

    # main program loop
    while not quitting:
        # check event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        screen.fill(pygame.Color('black'))

        # draw, animate and move sprites in the list
        for sprite in spritelist:
            sprite.draw()
            sprite.animate()
            sprite.move(1, 0, 0.05)

        # show the new screen
        pygame.display.flip()
 
    pygame.quit()
    quit()        
       
       






#collide()
# size(h,w)
# color()
# move()
# direction()
# draw(surface)
# position()
# speed()
# image_Rect= pygame.Rect(TEXT_X,TEXT_Y,TEXT_W,TEXT_H) 
# sprite1= MySprite(TEXT_X, TEXT_Y, TEXT_H, TEXT_W)
