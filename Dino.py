import sys
import os
import pygame

#먼저, 게임화면의 넓이를 지정합니다.
WIDTH = 623
HEIGHT = 150

#게임을 초기화 해줍니다.
pygame.init()
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

#게임을 정의하는 클래스
class Game:

    def __init__(self) -> None:
        self.bg = [BG(x=0), BG(x=WIDTH)]  #배경화면을 0,0 좌표에서 시작하는거 하나,화면 밖에서 시작하는거 하나.
        self.speed = 2  #기본 좌표가 움직이는 길이를 정의함.숫자가 높을수록 빨리 움직임(좌표가 많이 움직임)

#메인 함수를 정의해 줍니다.
def main():

    game = Game()

    clock = pygame.time.Clock()  #적절한 움직임을 위한 시간을 정의합니다.
    #메인 루프 -> 프로그램이 실행되는 동안 계속 꺼지지 않고 실행할 부분을 정의합니다.
    #조건이 참인경우에 계속 -> 프로그램의 거짓인 경우는 없으므로, 실행되는 동안 계속이라는 이야기.
    while True:

        #game.bg.update(-game.speed)  #좌표를 음수로 줘서 배경이 왼쪽으로 움직이게 합니다.
        #game.bg.show()  #움직인 배경을 화면상에 보여줍니다.
        #game.bg 에 정의된 배경화면이 0,0에서 시작하는 것 1개
        #화면밖에서 시작하는 WIDTH,0 에서 시작하는 것 1개를 무한으로 돌면서 보여줍니다.
        #그럼, 화면은 계속 업데이트가 되면서 무한으로 화면 2개를 번갈아 보여줍니다.
        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        #파이게임안에서 생기는 이벤트(사건)들을 가져옵니다. (?이벤트를 가져오는 방식에 대해서 설명이 필요함.)
        for event in pygame.event.get():
            #만약 게임을 종료하겠다는 이벤트가 오면, 게임을 종료하고, 프로그램도 종료합니다.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(80)  #적절한 시간이 지난 후에...
        #게임의 화면을 계속 업데이트 합니다.(화면을 모두 움직인 다음에, 실제 모니터에 결과를 보여줍니다)
        pygame.display.update()
        
#만들어 놓은 메인함수를 부릅니다.
main()
