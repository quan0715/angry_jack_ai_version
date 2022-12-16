import time
import pygame
from pygame.locals import *
import sys
from logic import Snake, Food, Boarder


class Game:
    def __init__(self):
        pygame.init()
        self.isGameover=False
        self.boarder=Boarder(1200,780,20)
        self.screen=pygame.display.set_mode((self.boarder.boarderWidth,self.boarder.boarderHeight))
        self.background=pygame.Surface((self.boarder.boarderWidth,self.boarder.boarderHeight))
        self.background.fill((0,0,0))
        pygame.display.set_caption("Snake")
        self.whoWin=0
        self.scoreFont=pygame.font.SysFont("Roboto",25)
        self.snake1=Snake(self.boarder.cellWidthNum,self.boarder.cellHeightNum)
        self.snake2=Snake(self.boarder.cellWidthNum,self.boarder.cellHeightNum)
        self.food=Food(self.boarder.cellWidthNum,self.boarder.cellHeightNum,self.snake1,self.snake2)

    def drawSnake(self,snake,color):
        tailColor=()
        for i in range(3):
            if color[i]!=0:
                tailColor=tailColor+(150,)
            else:
                tailColor=tailColor+(0,)
        s=pygame.Rect(snake.head['x']*self.boarder.cellWidth,snake.head['y']*self.boarder.cellWidth,self.boarder.cellWidth,self.boarder.cellWidth)
        pygame.draw.rect(self.screen,color,s)
        for x,y in snake.tail:
            s=pygame.Rect(x*self.boarder.cellWidth,y*self.boarder.cellWidth,self.boarder.cellWidth,self.boarder.cellWidth)
            pygame.draw.rect(self.screen,tailColor,s)

    def drawFood(self):
        f=pygame.Rect(self.food.position['x']*self.boarder.cellWidth,self.food.position['y']*self.boarder.cellWidth,self.boarder.cellWidth,self.boarder.cellWidth)
        pygame.draw.rect(self.screen,(255,0,0),f)

    def drawScore(self,text,posi):
        surface=self.scoreFont.render(text,True,(100,100,100))
        self.screen.blit(surface,posi)

    def restart(self):
        self.isGameover=False
        self.whoWin=0
        self.snake1=Snake(self.boarder.cellWidthNum,self.boarder.cellHeightNum)
        self.snake2=Snake(self.boarder.cellWidthNum,self.boarder.cellHeightNum)
        self.food.changePosition()

    def run(self):
        self.gameClock=pygame.time.Clock()
        self.isGameover=False
        while True:
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYDOWN:
                    if event.type==pygame.K_ESCAPE:
                        sys.exit()
                    if not self.isGameover:
                        if event.key==K_RIGHT:
                            self.snake1.changeDirection='r'
                            if not self.snake1.direction=='l':
                                self.snake1.direction=self.snake1.changeDirection
                        if event.key==K_LEFT:
                            self.snake1.changeDirection='l'
                            if not self.snake1.direction=='r':
                                self.snake1.direction=self.snake1.changeDirection
                        if event.key==K_UP:
                            self.snake1.changeDirection='u'
                            if not self.snake1.direction=='d':
                                self.snake1.direction=self.snake1.changeDirection
                        if event.key==K_DOWN:
                            self.snake1.changeDirection='d'
                            if not self.snake1.direction=='u':
                                self.snake1.direction=self.snake1.changeDirection
                        if event.key==K_d:
                            self.snake2.changeDirection='r'
                            if not self.snake2.direction=='l':
                                self.snake2.direction=self.snake2.changeDirection
                        if event.key==K_a:
                            self.snake2.changeDirection='l'
                            if not self.snake2.direction=='r':
                                self.snake2.direction=self.snake2.changeDirection
                        if event.key==K_w:
                            self.snake2.changeDirection='u'
                            if not self.snake2.direction=='d':
                                self.snake2.direction=self.snake2.changeDirection
                        if event.key==K_s:
                            self.snake2.changeDirection='d'
                            if not self.snake2.direction=='u':
                                self.snake2.direction=self.snake2.changeDirection
                    else:
                        if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE:
                            self.restart()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.isGameover:
                        self.restart()
                        
            if self.isGameover==False and (self.snake1.checkHeadHitTail() or self.snake1.checkHitWall() or self.snake1.checkTouchSnake(self.snake2)):
                self.isGameover=True
                self.whoWin=2
            elif self.isGameover==False and (self.snake2.checkHeadHitTail() or self.snake2.checkHitWall() or self.snake2.checkTouchSnake(self.snake1)):
                self.isGameover=True
                self.whoWin=1

            whoIsGrow=0
            if self.snake1.headTouchFood(self.food.position['x'],self.food.position['y']):
                whoIsGrow=1
                self.snake1.score+=1
                self.food.changePosition()
            elif self.snake2.headTouchFood(self.food.position['x'],self.food.position['y']):
                whoIsGrow=2
                self.snake2.score+=1
                self.food.changePosition()
            
            self.screen.blit(self.background,(0,0))
            self.drawFood()

            if not self.isGameover:
                if whoIsGrow==1:
                    self.snake1.snakeMove(True)
                    self.snake2.snakeMove(False)
                elif whoIsGrow==2:
                    self.snake2.snakeMove(True)
                    self.snake1.snakeMove(False)
                else:
                    self.snake1.snakeMove(False)
                    self.snake2.snakeMove(False)
            self.drawSnake(self.snake1,(0,255,0))
            self.drawSnake(self.snake2,(0,0,255))

            self.drawScore(f"{self.snake1.score}",(30,30))
            self.drawScore(f"{self.snake2.score}",(1000,30))
            self.gameClock.tick(10)
            pygame.display.flip()


if __name__ == '__main__':
    Game().run()