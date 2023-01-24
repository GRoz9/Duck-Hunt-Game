import pygame

def scale_image(img, factor):   #Can chnage the size of an asset if need by the factor e.g 2x
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)