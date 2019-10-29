import random
import json
import os

from pico2d import *

import game_framework


from boy import Boy



name = "MainState"

boy = None
font = None



def enter():
    global boy
    boy = Boy()


def exit():
    global boy
    del boy




def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)



def update():
    boy.update()

def draw():
    clear_canvas()
    boy.draw()
    update_canvas()






