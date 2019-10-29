from pico2d import *
import Character

open_canvas(1000,600)
gameRunning=True
player = Character.Character()


def handle_event():

    global player
    global gameRunning

    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if player.vector <= 0 and player.isRunning:
                    player.status = player.STAT_TURNBACKR
                elif player.status!=player.STAT_STOPPING:
                    player.status = player.STAT_MOVE_RIGHT
            elif event.key == SDLK_LEFT:
                if player.vector >= 0 and player.isRunning:
                    player.status = player.STAT_TURNBACKR
                elif player.status != player.STAT_STOPPING:
                    player.status = player.STAT_MOVE_LEFT
            elif event.key == SDLK_ESCAPE:
                gameRunning = False
        elif event.type == SDL_KEYUP:
            if player.isRunning and ((event.key == SDLK_LEFT and player.vector<=0) or  (event.key== SDLK_RIGHT and player.vector>=0)):
                player.status = player.STAT_STOPPING
                player.init_frame()



print("gameRun")
delay_time=get_time()
while gameRunning:
    wait_time=0.1
    if get_time()-delay_time >= wait_time:
        delay_time=get_time()
        clear_canvas()
        player.draw_character()
        update_canvas()
        player.move_character()
        print(player.x , player.y)
    handle_event()

print("gameover")

close_canvas()