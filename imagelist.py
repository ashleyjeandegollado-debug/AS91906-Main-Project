from os.path import exists
import debug
import pygame


class ImageList():
    def __init__(self, filename, width, height, image_type = 'jpg'):
        self._images=[]
        count = 0
        debug.dprint(2, "filename" + filename + str(count) + '.' + image_type)
        while exists(filename + str(count) + '.' + image_type):
            image = pygame.image.load(filename + str(count) + '.' + image_type)
            debug.dprint(2, "image" + filename + str(count) + '.' + image_type + "loaded")
            scaled = pygame.transform.smoothscale(image, [width,height])
            self._images.append(scaled)
            debug.dprint(2, self._images[-1] )
            count+=1

        if count == 0:
            debug.dprint(0, f"Images with prefix {filename} failed to load")

    def get_images(self):
        return self._images
    images = property(get_images, None, None)


# testing
debug.DEBUG_LEVEL = 0
if __name__ =="__main__":
    TEST_X = 50
    TEST_Y = 50
    TEST_W = 64
    TEST_H= 64
    image_obj= ImageList("images\\test",64,64, "jpg")
    pygame.init()
    screen = pygame.display.set_mode((640,480),pygame.RESIZABLE)
    debug.dprint(1, "image list test class created")
    quitting = False
    # main program loop
    while not quitting:
        # check event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True

        count = 0 
        while count < len(image_obj.images):
            image_Rect = pygame.Rect(TEST_X + ( count*TEST_W), TEST_Y, TEST_W, TEST_H)
            screen.blit(image_obj.images[count],image_Rect)
            count += 1
        pygame.display.flip()


    pygame.quit()
    quit()
