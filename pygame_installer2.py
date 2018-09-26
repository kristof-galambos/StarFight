
def install():
    try:
        import pygame
    except ImportError:
        import os
        os.system('pip install pygame')
