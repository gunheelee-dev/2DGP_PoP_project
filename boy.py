from pico2d import *

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, UP_UP,UP_DOWN,STOPPING_TIMER, STOPPING_TIMER_L,SHIFT_DOWN,SHIFT_UP = range(10)
isPressedRight, isPressedLeft, isPressedUP, isPressedShift=False, False, False, False
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP,SDLK_UP):UP_UP,
    (SDL_KEYDOWN,SDLK_UP):UP_DOWN,
    (SDL_KEYDOWN,SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP,SDLK_LSHIFT):SHIFT_UP
}

start_time = 0
wait_time = 0.1 #딜레이 타임

# Boy States
class LeftStoppingState: # 왼쪽방향 제동
    @staticmethod
    def enter(boy,event):
        boy.sprite = Boy.SPRITE_STOPPING
        boy.velocity=boy.dir*10

    @staticmethod
    def exit(boy, event):
        boy.velocity=0
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >= 7:
            boy.frame = 0
            boy.add_event(STOPPING_TIMER)
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.velocity>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)

class RightStoppingState: #오른쪽방향 제동
    @staticmethod
    def enter(boy,event):
        boy.sprite = Boy.SPRITE_STOPPING
        boy.velocity=boy.dir*10

    @staticmethod
    def exit(boy, event):
        boy.velocity=0
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >= 7:
            boy.frame = 0
            boy.add_event(STOPPING_TIMER)
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.velocity>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)

class IdleState: #대기상태
    @staticmethod
    def enter(boy, event):
        boy.sprite = Boy.SPRITE_STOPPED
        if event == RIGHT_DOWN:
            boy.velocity += 15
        elif event == LEFT_DOWN:
            boy.velocity -= 15

    @staticmethod
    def exit(boy, event):
        boy.velocity=0
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        if boy.dir>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)

class readyWalkState: #걷기 대기상태(대기상태랑 같음
    @staticmethod
    def enter(boy, event):
        boy.sprite = Boy.SPRITE_STOPPED
        if event == RIGHT_DOWN:
            boy.velocity += 15
        elif event == LEFT_DOWN:
            boy.velocity -= 15


    @staticmethod
    def exit(boy, event):
        boy.velocity=0
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        if boy.dir>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)
class RunState: # 달리기 상태(기본 이동 동작)
    @staticmethod
    def enter(boy, event):
        boy.sprite=Boy.SPRITE_RUN
        if event == RIGHT_DOWN:
            boy.velocity += 15
        elif event == LEFT_DOWN:
            boy.velocity -= 15

        if boy.velocity>0:
            boy.dir=1
        else:
            boy.dir=-1

    @staticmethod
    def exit(boy, event):
        boy.velocity=0

        boy.frame=0
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >= 13:
            boy.frame = 5
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.velocity>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)
class TurnRunState: # 달리기 중 방향전환 시
    def enter(boy, event):
        boy.sprite = Boy.SPRITE_RUNTURN
        if event == RIGHT_DOWN:
            boy.velocity -= 10
            boy.dir=-1
        elif event == LEFT_DOWN:
            boy.velocity += 10
            boy.dir=1

    @staticmethod
    def exit(boy, event):
        boy.velocity*=-15/10
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >= 9:
            boy.add_event(STOPPING_TIMER)
            boy.dir *= -1
        #if boy.frame==4:

        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)
    @staticmethod
    def draw(boy):
        if boy.velocity>0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100,0,'h',boy.x,boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)
class RunJumpState: # 달리기 중 점프 시
    @staticmethod
    def enter(boy,event):
        boy.sprite=Boy.SPRITE_RUNJUMP
        boy.velocity=boy.dir*30

    @staticmethod
    def exit(boy, event):
        boy.velocity=0
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >=11:
            if boy.velocity>0:
                boy.add_event(STOPPING_TIMER)
                boy.frame=0
            else:
                boy.add_event(STOPPING_TIMER_L)
                boy.frame=0
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.velocity > 0:
            boy.image.clip_composite_draw(boy.frame * 110, 1500 - boy.sprite, 110, 100, 0, 'h', boy.x, boy.y, 110, 100)
        else:
            boy.image.clip_draw(boy.frame * 110, 1500 - boy.sprite, 110, 100, boy.x, boy.y)

class JumpState: #제자리에서 점프시
    @staticmethod
    def enter(boy, event):
        boy.sprite = Boy.SPRITE_JUMP

    @staticmethod
    def exit(boy, event):
        boy.velocity = 0
        pass

    @staticmethod
    def do(boy):
        boy.frame += 1
        if boy.frame >= 17:
            if boy.dir > 0:
                boy.add_event(STOPPING_TIMER)
                boy.frame=0
            else:
                boy.add_event(STOPPING_TIMER_L)
                boy.frame=0
        if boy.frame==7:
            if boy.dir>0:
                boy.velocity=20
            else:
                boy.velocity=-20

        elif boy.frame==12:
            if boy.dir>0:
                boy.velocity=5
            else:
                boy.velocity=-5
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_composite_draw(boy.frame * 110, 1500 - boy.sprite, 110, 100, 0, 'h', boy.x, boy.y, 110, 100)
        else:
            boy.image.clip_draw(boy.frame * 110, 1500 - boy.sprite, 110, 100, boy.x, boy.y)

class WalkState: #걷기 상태
    @staticmethod
    def enter(boy, event):
        boy.sprite= Boy.SPRITE_WALKING
        if event == RIGHT_DOWN:
            boy.dir=1
        elif event == LEFT_DOWN:
            boy.dir=-1

    def exit(boy, event):
        boy.velocity=0

    def do(boy):
        boy.frame += 1
        if boy.frame >= 12:
            boy.add_event(STOPPING_TIMER)
            boy.frame=0

        if boy.frame==7:
            boy.velocity=boy.dir*7
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1000 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_composite_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, 0, 'h', boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_draw(boy.frame * 100, 1500 - boy.sprite, 100, 100, boy.x, boy.y)



next_state_table = {
    IdleState:{RIGHT_UP: IdleState, LEFT_UP: IdleState,
               RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
               UP_DOWN:JumpState,UP_UP:IdleState,SHIFT_DOWN:readyWalkState,SHIFT_UP:IdleState},

    RunState:{RIGHT_UP: RightStoppingState, LEFT_UP: LeftStoppingState,
              LEFT_DOWN: TurnRunState, RIGHT_DOWN: TurnRunState,
              UP_DOWN: RunJumpState, SHIFT_DOWN:RunState, SHIFT_UP: RunState},

    LeftStoppingState:{STOPPING_TIMER: IdleState, LEFT_UP: IdleState,
                       RIGHT_DOWN:TurnRunState, RIGHT_UP: RunState,
                       LEFT_DOWN: RunState,UP_DOWN:JumpState, UP_UP:LeftStoppingState,
                       SHIFT_DOWN:LeftStoppingState, SHIFT_UP:LeftStoppingState},

    RightStoppingState:{STOPPING_TIMER: IdleState, LEFT_UP: IdleState,
                   RIGHT_DOWN:RunState, RIGHT_UP: IdleState,
                   LEFT_DOWN: TurnRunState,UP_DOWN:JumpState, UP_UP:RightStoppingState,
                    SHIFT_DOWN:RightStoppingState, SHIFT_UP:RightStoppingState},

    TurnRunState:{STOPPING_TIMER: RunState, LEFT_UP:LeftStoppingState, RIGHT_DOWN:IdleState
                  ,LEFT_DOWN: IdleState, RIGHT_UP:RightStoppingState, UP_DOWN:RunJumpState,
                  SHIFT_DOWN:TurnRunState, SHIFT_UP:TurnRunState},

    RunJumpState:{STOPPING_TIMER: RightStoppingState, STOPPING_TIMER_L: LeftStoppingState,
                  RIGHT_DOWN:RunJumpState, RIGHT_UP: RunJumpState, UP_UP:RunJumpState,
                  LEFT_DOWN:RunJumpState, LEFT_UP: RunJumpState, UP_DOWN:RunJumpState,
                  SHIFT_DOWN:RunJumpState, SHIFT_UP:RunJumpState},

    JumpState:{STOPPING_TIMER: IdleState, STOPPING_TIMER_L: IdleState,
               RIGHT_DOWN: JumpState, RIGHT_UP: JumpState, UP_UP: JumpState,
               LEFT_DOWN: JumpState, LEFT_UP: JumpState, UP_DOWN: JumpState,
               SHIFT_DOWN:JumpState, SHIFT_UP:JumpState},

    readyWalkState:{LEFT_DOWN:WalkState, LEFT_UP:WalkState, RIGHT_UP:WalkState, RIGHT_DOWN:WalkState,
                    UP_UP:JumpState, UP_DOWN:JumpState,SHIFT_DOWN:readyWalkState,SHIFT_UP:IdleState},

    WalkState:{STOPPING_TIMER:readyWalkState}
}

class Boy:
    SPRITE_RUN = 400
    SPRITE_STOPPING = 300
    SPRITE_STOPPED = 100
    SPRITE_RUNTURN = 200
    SPRITE_RUNJUMP= 1050
    SPRITE_WALKING= 1150
    SPRITE_JUMP=950
    image=None

    def __init__(self):
        self.sprite = self.SPRITE_STOPPED
        self.x, self.y = 800 // 2, 90
        self.dir = 1
        self.velocity = 0
        self.event_que =[]
        self.frame=0
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        if self.image==None:
            Boy.image = load_image('sprite.png')

    def update_state(self):
        global start_time
        global wait_time
        start_time=get_time()
        if len(self.event_que)>0:
            event= self.event_que.pop()
            self.cur_state.exit(self,event)
            self.cur_state=next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)
            start_time=get_time()

    def change_state(self,  state):
        # fill here
        pass

    def add_event(self, event):
        self.event_que.insert(0,event)

    def update(self):
        global start_time, wait_time
        if get_time()-start_time>wait_time:
            self.cur_state.do(self)
            start_time=get_time()
        if len(self.event_que)>0:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)
        print(self.velocity,self.dir,self.cur_state)

    def draw(self):
        self.cur_state.draw(self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type,event.key)]
            if key_event == RIGHT_DOWN:
                isPressedRight=True
            elif key_event == LEFT_DOWN:
                isPressedLeft=True
            elif key_event == UP_DOWN:
                isPressedUP=True
            elif key_event == SHIFT_DOWN:
                isPressedShift=True
            elif key_event== RIGHT_UP:
                isPressedRight=False
            elif key_event== LEFT_UP:
                isPressedLeft=False
            elif key_event== UP_UP:
                isPressedUP=False
            elif key_event == SHIFT_UP:
                isPressedShift=False
            if(self.cur_state!=JumpState and self.cur_state!=WalkState):
                self.add_event(key_event)

