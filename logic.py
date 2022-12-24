import random

class Snake():
    def __init__(self,cellWidthNum,cellHeightNum):
        self.score=0
        self.cellWidthNum=cellWidthNum
        self.cellHeightNum=cellHeightNum
        self.head={'x':random.randint(0,cellWidthNum-1), 'y':random.randint(0,cellHeightNum-1)}
        self.tail=[(0,0)]
        self.direction='r'
        if self.head['x']>cellWidthNum/2:
            self.direction='l'

    def checkHeadTail(self,foodX,foodY):
        if self.head['x']==foodX and self.head['y']==foodY:
            return True
        for x,y in self.tail:
            if x==foodX and y==foodY:
                return True
        return False

    def checkHitWall(self):
        if self.head['x']<0 or self.head['y']<0:
            return True
        elif self.head['x']>self.cellWidthNum-1 or self.head['y']>self.cellHeightNum-1:
            return True
        return False
    
    def headTouchFood(self,foodX,foodY):
        if foodX==self.head['x'] and foodY==self.head['y']:
            return True

    def checkHeadHitTail(self):
        for x,y in self.tail:
            if x==self.head['x'] and y==self.head['y']:
                return True
        return False

    def snakeMove(self,isGrow):
        if not isGrow:
            self.tail.pop()
        self.tail.insert(0,(self.head['x'],self.head['y']))
        if self.direction=='u':
            self.head['y']=self.head['y']-1
        elif self.direction=='d':
            self.head['y']=self.head['y']+1
        elif self.direction=='l':
            self.head['x']=self.head['x']-1
        elif self.direction=='r':
            self.head['x']=self.head['x']+1

    def checkTouchSnake(self,snake):
        if snake.head['x']==self.head['x'] and snake.head['y']==self.head['y']:
            return True
        for x,y in snake.tail:
            if self.head['x']==x and self.head['y']==y:
                return True
        return False


class Food:
    def __init__(self,cellWidthNum,cellHeightNum,snake1,snake2):
        self.snake1=snake1
        self.snake2=snake2
        self.cellWidthNum=cellWidthNum
        self.cellHeightNum=cellHeightNum
        self.position={'x':0, 'y':0}
        self.changePosition()

    def changePosition(self):
        x,y=random.randint(0,self.cellWidthNum-1), random.randint(0,self.cellHeightNum-1)
        while self.snake1.checkHeadTail(x,y) or self.snake2.checkHeadTail(x,y):
            x,y=random.randint(0,self.cellWidthNum-1), random.randint(0,self.cellHeightNum-1)
        self.position['x']=x
        self.position['y']=y

class Boarder:
    def __init__(self,boarderWidth,boarderHeight,cellLength):
        self.boarderWidth=boarderWidth
        self.boarderHeight=boarderHeight
        self.cellWidthNum=boarderWidth/cellLength
        self.cellHeightNum=boarderHeight/cellLength
        self.cellWidth=cellLength