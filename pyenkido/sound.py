## Project: pyEnkido
## Module: None (audio utilities)
## Author: Salwan A. AlHelaly

import os, sys, pygame

def load_sound(path, filename):
    return pygame.mixer.Sound(os.path.join(path,filename))

