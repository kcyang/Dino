import sys  #시스템 기본 라이브러리
import os  #OS 에 접근하기 위한 라이브러리 (폴더)
import math  #수학함수가 들어있는 라이브러리 (수학공식)
import random  #무작위로 숫자를 만들어내기 위한 라이브러리
import pygame  #게임을 만들기 위한 기본 라이브러리

#먼저, 게임화면의 넓이를 지정합니다.
WIDTH = 623
HEIGHT = 150

#게임을 초기화 해줍니다.
pygame.init()
pygame.mixer.init()
#게임의 화면을 정의해 줍니다. ?set_mode 
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
#게임의 타이틀을 줍니다.
pygame.display.set_caption('Dino')


#배경화면을 정의하는 클래스.
class BG:

    #클래스 초기화 (?초기화의 개념을 알려줘야 함)
    #클래스 생성자에, Parameter 를 입력합니다.
    #여기 parameter는 현재 화면의 좌표를 받아서, 배경을 적절하게 표시하기 위함입니다.
    def __init__(self, x) -> None:
        self.width = WIDTH #배경화면의 넓이를 정의.
        self.height = HEIGHT  #배경화면의 높이를 정의.
        self.x = x  #현재 화면이 업데이트 되고 있는 X 좌표를 정의.
        self.y = 0  #현재 화면이 업데이트 되고 있는 Y 좌표를 정의.(y값은 변하지 않을 것이므로)
        self.set_texture() #텍스쳐를 정의합니다.
        self.show() #배경화면을 정의한대로 보여줍니다.

    #배경화면의 좌표를 업데이트 해주는 함수.
    def update(self, dx):
        self.x += dx  #좌표를 dx 만큼 움직여줍니다. (+ 면 오른쪽, - 면 왼쪽으로 배경이 움직입니다.)
        # 만약 현재 좌표가 배경화면과 같거나 적으면 (완전히 화면을 벗어나면,)
        if self.x <= -WIDTH:
            self.x = WIDTH  #좌표를 처음과 같이 만들어 줍니다.현재 화면 다음에 재위치 시킵니다.#...|...|#..|

    def show(self):
        #게임의 화면을 정의한 screen 에 보여주라는 뜻.
        #아래의 경우, texture 를 좌표 0,0 에서 보여주라는 이야기입니다.
        screen.blit(self.texture, (self.x,self.y))

    #텍스쳐를 정의하는 함수.
    def set_texture(self):
        path = os.path.join('assets/images/bg.png') #이미지가 있는 곳을 찾아서,
        self.texture = pygame.image.load(path)  #게임안에 이미지를 불러옵니다.
        #?transform.scale 기능에 대해서 알아보기.
        self.texture = pygame.transform.scale(self.texture, (self.width,self.height)) #게임화면 안에 맞도록 조정합니다.

# 공룡을 표시하기 위해 공룡클래스를 정의함.
class Dino:

    #공룡 클래스의 생성자.
    def __init__(self) -> None:
        #공룡의 이미지 크기
        self.width = 44
        self.height = 44
        #공룡이 화면에 위치할 좌표 정의
        #pygame 에서 좌표의 0,0 은 맨 왼쪽 위를 뜻한다.
        self.x = 10
        self.y = 80
        self.dy = 3  #공룡이 점프하는 정도, y 의 좌표 설정.
        self.gravity = 1.2  #공룡이 사용할 중력의 값을 설정. (떨어지는 속도?)
        self.onground = True #공룡이 땅에 닿았는지 여부.
        self.jumping = False  #공룡이 점프중인지 여부.
        self.jump_stop = 10  #공룡이 점프하는 높이를 정의함.
        self.falling = False  #공룡이 떨어지고 있는 중인지 여부.
        self.fall_stop = self.y  #공룡의 원래 위치.
        #공룡의 이미지는 여러개이므로, 여러개를 표시하기 위한 번호정의
        self.texture_num = 0
        self.set_sound()
        #공룡의 이미지를 셋팅하고,
        self.set_texture()
        #공룡을 화면상에 표시한다.
        self.show()

    def update(self, loops):
        #공룡이 점프할때 정의
        if self.jumping:  #점프의 상태인가?
            self.y -= self.dy  #공룡의 좌표를 dy 만큼씩 줄인다. 즉, dy 만큼씩 위로 올라감(하늘로 올라감)
            if self.y <= self.jump_stop:  #공룡의 좌표가 jump_stop 에 닿으면,
                self.fall()  #공룡은 떨어져야 함.

        #공룡이 떨어질 때 정의.
        elif self.falling:  #떨어지고 있는 중인가?
            self.y += self.gravity * self.dy  #공룡의 좌표가 늘어난다. 즉, dy 만큼씩 아래로 떨어짐(땅으로 떨어짐) -> 그냥떨어지지 않고, 중력값을 줌.(gravity)
            if self.y >= self.fall_stop:  #공룡이 원래 있던자리에 닿으면.
                self.stop()  #공룡은 맘춰야 함.

        #공룡이 걸을 때 정의.
        #공룡의 이미지가 너무 빠르게 회전하므로,
        #공룡의 이미지가 바뀌는 속도를 조절하기 위해, 숫자를 입력함.
        #숫자가 높을수록, 공룡의 이미지가 천천히 바뀜(다리가 느려짐)
        elif self.onground and loops % 5 == 0:
            self.texture_num = (self.texture_num + 1) % 3  #텍스쳐의 번호를 바꿈 (공룡이 움직이는 것처럼 보임/실제로는 이미지가 바뀌는 것)
            self.set_texture()  #바뀐 텍스처 번호로 이미지를 바꿈.

    #공룡을 화면상에 표시하기.
    def show(self):
        screen.blit(self.texture, (self.x,self.y))  #바뀐 공룡의 이미지로 셋팅된 좌표에 보여줌.

    #공룡의 소리를 셋업.
    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')  #공룡이 점프하는 소리의 위치를 가지고 있음.
        self.sound = pygame.mixer.Sound(path)  #소리를 가져와서 가지고 있음.

    #공룡의 이미지를 게임상에 불러오기.
    def set_texture(self):
        path = os.path.join(f'assets/images/dino{self.texture_num}.png') #이미지가 있는 곳을 찾아서,
        self.texture = pygame.image.load(path)  #게임안에 이미지를 불러옵니다.
        self.texture = pygame.transform.scale(self.texture, (self.width,self.height)) #게임화면 안에 맞도록 조정합니다.

    #공룡이 점프하면
    def jump(self):
        self.sound.play()  #점프하는 소리를 냅니다.
        self.jumping = True  #공룡의 상태를 점프하는 중이라고 저장합니다.
        self.onground = False  #공룡의 상태를 땅이 아니라고 저장합니다.

    #공룡이 떨어지면
    def fall(self):
        self.jumping = False  #공룡의 상태를 점프하는 중이 아니라고 저장합니다.
        self.falling = True  #공룡의 상태를 떨어지는 중이라고 저장합니다.

    #공룡이 멈추면
    def stop(self):
        self.falling = False  #공룡의 상태를 떨어지는 중이 아니라고 저장합니다.
        self.onground = True  #공룡의 상태를 현재 땅에 있다고 저장합니다.

#장애물 -> 선인장을 선언하는 클래스.
class Cactus:

    def __init__(self, x) -> None:
        #선인장의 넓이와 높이.
        self.width = 34
        self.height = 44
        #선인장의 위치 좌표값.
        self.x = x  #선인장의 X 좌표값은 값을 받아서 줌.
        self.y = 80  #선인장의 높이는 고정값으로 줌.
        self.set_texture()  #선인장의 그림을 설정(위치와 그림)하고.
        self.show()  #선인장을 화면상에 보여줌.
        
    #선인장의 위치를 업데이트 함.
    def update(self, dx):
        self.x += dx  #선인장의 좌표값을 받아서 위치를 업데이트 함.

    #선인장을 실제 화면상에 보여주는 함수.
    def show(self):
        screen.blit(self.texture, (self.x, self.y))  #선인장의 이미지를 좌표상에 보여줌.

    def set_texture(self):
        path = os.path.join('assets/images/cactus.png') #이미지가 있는 곳을 찾아서,
        self.texture = pygame.image.load(path)  #게임안에 이미지를 불러옵니다.
        #?transform.scale 기능에 대해서 알아보기.
        self.texture = pygame.transform.scale(self.texture, (self.width,self.height)) #게임화면 안에 맞도록 조정합니다.

#충돌을 정의하는 클래스.
class Collision:

    #객체 1(공룡)과 객체 2(선인장)의 위치를 판단하는 함수.
    def between(self, obj1, obj2):
        #각 객체의 좌표값을 받아서 둘 사이의 위치값을 받아옴 (이 공식은 두 물체의 위치를 계산하는 수학공식을 적용함.)
        distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
        #두 물체간의 거리가 35 보다 작으면 True 를 리턴합니다.
        #왜 35보다 작으면 인가? -> 두 물체간에 적절한 거리값임. 숫자를 조정해 보면 이해할 수 있음.(클 수록-멀수록 조금만 건들여도 죽음/작을수록-가까울수록 많이 닿아야 함)
        return distance < 35

#점수를 기록하고 보여주기 위한 클래스.
class Score:
    
    def __init__(self, hs) -> None:
        self.hs = hs  #최고기록을 받아서 저장함.
        self.act = 0  #현재기록, 초기값은 0
        self.font = pygame.font.SysFont('monospace', 18)  #기록을 보여줄 폰트정의
        self.color = (0,0,0)  #폰트의 색을 정의 0,0,0 -> 검은색.
        self.set_sound()  #소리를 설정함.
        self.show()  #기록(점수)를 보여줌.

    def update(self, loops):
        self.act = loops // 10  #loops 값을 받아서, 10번에 한번 점수를 1씩 올려줌.
        self.check_hs()  #최고기록을 보고, 현재기록이 최고기록을 갱신하면, 현재기록을 최고기록에 저장함.
        self.check_sound()  #현재 기록이 100을 넘으면, 소리를 냄.(띠리링!)

    def show(self):
        self.lbl = self.font.render(f'HI {self.hs} {self.act}', 1, self.color)  #폰트를 셋업해서,
        lbl_width = self.lbl.get_rect().width  #폰트의 크기만큼.
        screen.blit(self.lbl,(WIDTH - lbl_width - 10, 10))  #화면에 보여줌.

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')  #소리를 불러와서
        self.sound = pygame.mixer.Sound(path)  #소리를 저장해 놓음.

    def check_sound(self):
        if self.act % 100 == 0 and self.act != 0:  #점수가 100이 될때마다
            self.sound.play()  #소리를 냄.

    def check_hs(self):
        if self.act >= self.hs:  #현재기록이 최고기록보다 높으면
            self.hs = self.act  #현재기록을 최고기록값에 저장함.

#게임을 정의하는 클래스
class Game:

    def __init__(self, hs=0) -> None:
        self.bg = [BG(x=0), BG(x=WIDTH)]  #배경화면을 0,0 좌표에서 시작하는거 하나,화면 밖에서 시작하는거 하나.
        self.dino = Dino()  #공룡 인스턴스를 생성함(공룡이 만들어짐)
        self.obstacles = []  #장애물 목록.
        self.collision = Collision()  #충돌을 정의하는 클래스의 인스턴스
        self.score = Score(hs)  #기록을 보여주는 점수 클래스의 인스턴스
        self.speed = 3  #기본 좌표가 움직이는 길이를 정의함.숫자가 높을수록 빨리 움직임(좌표가 많이 움직임)
        self.playing = False  #현재 게임중인가를 저장하는 값. 시작할 때 스페이스바를 누르면 바뀔 값.
        self.set_sound()  #소리를 설정하고
        self.set_labels()  #화면에 보여줄 레이블(게임오버) 설정하고
        self.spawn_cactus()  #선인장을 생성합니다.

    #게임이 끝나면, GAME OVER를 보여주는 글자를 정의하는 곳.
    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_lbl = big_font.render(f'G A M E  O V E R', 1, (0,0,0))
        self.small_lbl = small_font.render(f'press r to restart', 1, (0,0,0))

    #죽었을 때 죽는 소리를 정의하는 곳.
    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    #게임을 시작하면, 게임중이라는 상태값을 '참'으로 설정하는 곳.
    def start(self):
        self.playing = True

    #게임이 끝나면 무엇을 할지 정의하는 곳.
    def over(self):
        self.sound.play()  #게임이 끝나는 소리를 내고,
        screen.blit(self.big_lbl, (WIDTH // 2 - self.big_lbl.get_width() // 2, HEIGHT // 4))  #게임오버를 보여줌. GAME OVER
        screen.blit(self.small_lbl, (WIDTH//2 - self.small_lbl.get_width() // 2, HEIGHT // 2))  #게임오버를 보여줌. Please r button
        self.playing = False  #게임중인가? 아니오로 변경.

    #선인장을 생성하는 주기를 정의함.
    def tospawn(self, loops):
        return loops % 100 == 0  #loops 의 값이 100일 때마다.참을 리턴함.

    #선인장을 무작위의 좌표에 생성함.
    def spawn_cactus(self):
        #이미 선인장이 있으면,
        if len(self.obstacles) > 0:
            prev_cactus = self.obstacles[-1]  #바로이전 선인장을 가져와서,
            # 공룡의 몸체보다는 넓게 그리고, 최소한 선인장만큼은 건너뛰어서 랜덤하게 좌표를 생성함.
            x = random.randint(prev_cactus.x + self.dino.width + 84, WIDTH + prev_cactus.x + self.dino.width + 84)
        #선인장이 없으면,
        else:
            #새로운 선인장을 생성할 좌표를 만듦.
            x = random.randint(WIDTH + 100, 1000)

        #새로운 위치(x) 에 선인장을 생성한다.
        cactus = Cactus(x)
        self.obstacles.append(cactus)

    #새로 시작하는 경우에,
    def restart(self):
        self.__init__(hs=self.score.hs)  #이전에 진행한 최고 기록을 다시 넘겨줌.

#메인 함수를 정의해 줍니다.
#여기가 실제 게임이 실행되는 곳. 순서대로 진행 됨.
def main():

    game = Game()  #게임을 정의한 클래스의 인스턴스 (새로운 게임이 만들어짐)
    dino = game.dino  #게임인스턴스에서 초기화 된 공룡 인스턴스를 가져옴.

    clock = pygame.time.Clock()  #적절한 움직임을 위한 시간을 정의합니다.
    loops = 0  #공룡의 이미지가 바뀌는 속도조절.
    over = False  #게임이 끝났는지 여부 (처음 시작은 '거짓')

    #메인 루프 -> 프로그램이 실행되는 동안 계속 꺼지지 않고 실행할 부분을 정의합니다.
    #조건이 참인경우에 계속 -> 프로그램의 거짓인 경우는 없으므로, 실행되는 동안 계속이라는 이야기.
    while True:
        if game.playing:  #게임이 플레이하는 중인가? (게임이 over 될 때까지 계속 실행함.)

            loops += 1  #게임이 플레이하는 중에 한바퀴 돌때마다 1씩 증가함.

            #game.bg.update(-game.speed)  #좌표를 음수로 줘서 배경이 왼쪽으로 움직이게 합니다.
            #game.bg.show()  #움직인 배경을 화면상에 보여줍니다.
            #game.bg 에 정의된 배경화면이 0,0에서 시작하는 것 1개
            #화면밖에서 시작하는 WIDTH,0 에서 시작하는 것 1개를 무한으로 돌면서 보여줍니다.
            #그럼, 화면은 계속 업데이트가 되면서 무한으로 화면 2개를 번갈아 보여줍니다.
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # Dino
            dino.update(loops)  #공룡의 이미지를 loops 값에따라서 계속 바꿔줌.
            dino.show()  #바뀐 공룡이미지를 계속 보여줌.

            # Cactus
            if game.tospawn(loops):  #선인장이 생성되는 주기마다 (loops 값을 받아서 True 일때마다)
                game.spawn_cactus()  #무작위로 생성된 좌표에 선인장이미지를 설정함.

            for cactus in game.obstacles:  #생성된 선인장의 목록을 불러와서
                cactus.update(-game.speed)  #특정 숫자만큼 좌표를 이동하면서
                cactus.show()  #선인장을 화면상에 보여줌.

                #충돌
                if game.collision.between(dino,cactus):  #공룡과 선인장의 거리가 설정한 값보다 작으면(충돌하면)
                    over = True  #게임이 끝남.

            if over:  #게임이 끝나면,
                game.over()  #게임이 끝났을때 실행하는 함수를 진행합니다.
            #Score        
            game.score.update(loops)  #점수를 업데이트하고
            game.score.show()  #점수를 화면에 보여줍니다.

        #파이게임안에서 생기는 이벤트(사건)들을 가져옵니다. (?이벤트를 가져오는 방식에 대해서 설명이 필요함.)
        for event in pygame.event.get():
            #만약 게임을 종료하겠다는 이벤트가 오면, 게임을 종료하고, 프로그램도 종료합니다.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #만약, 키보드를 누르면,
            if event.type == pygame.KEYDOWN:
                #키보드를 눌었을 때 스페이스바가 눌렸으면,
                if event.key == pygame.K_SPACE:
                    if not over:  #게임이 끝난게 아니라면,
                        if dino.onground:  #공룡이 땅에 있다면,
                            dino.jump()  #공룡을 점프시킵니다.          

                        if not game.playing:  #만약 게임이 끝난게 아니라면,
                            game.start()  #새로 게임을 시작합니다.

                if event.key == pygame.K_r:  #r 키를 누르면,
                    game.restart()  #게임을 재시작합니다.
                    dino = game.dino  #새로운 공룡으로 
                    loops = 0  #새로운 게임의 시작값.
                    over = False  #게임은 시작됩니다.

        clock.tick(80)  #적절한 시간이 지난 후에...
        #게임의 화면을 계속 업데이트 합니다.(화면을 모두 움직인 다음에, 실제 모니터에 결과를 보여줍니다)
        pygame.display.update()  #계속 화면을 업데이트 합니다.
        
#만들어 놓은 메인함수를 실행합니다.
main()
