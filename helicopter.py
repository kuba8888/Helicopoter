import pygame
import random
import os

pygame.init()

sWidth = 800
sHeight = 800
screen = pygame.display.set_mode((sWidth, sHeight))
display = "menu"


def writeMid(text, fontSize):
    f = pygame.font.SysFont("JetBrainsMono Nerd Font", fontSize)
    rend = f.render(text, 1, (255, 100, 100))
    x = (sWidth - rend.get_rect().width) / 2
    y = (sHeight - rend.get_rect().height) / 2
    screen.blit(rend, (x, y))
    pygame.display.update()

def write(text, x, y, fontSize):
    f = pygame.font.SysFont("JetBrainsMono Nerd Font", fontSize)
    rend = f.render(text, 1, (255, 100, 100))
    screen.blit(rend, (x, y))
    pygame.display.update()

prevHeightUp = 200
heightUpCount = 0

class Obstacle():
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.yUp = 0
        self.space = 150
        global heightUpCount

        if heightUpCount >= 40:
           global prevHeightUp
           prevHeightUp = random.randint((prevHeightUp - 30), (prevHeightUp + 30))
           while prevHeightUp <= 10 or prevHeightUp >= (sHeight - (self.space + 10)):
               prevHeightUp = random.randint((prevHeightUp - 30), (prevHeightUp + 30))
        else:
            heightUpCount = heightUpCount + 1

        self.heightUp = prevHeightUp
        self.yDown = self.heightUp + self.space
        self.heightDown = sHeight - self.yDown
        self.color = (160, 140, 190)
        self.shapeUp = pygame.Rect(self.x, self.yUp, self.width, self.heightUp)
        self.shapeDown = pygame.Rect(self.x, self.yDown, self.width, self.heightDown)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.shapeUp, 0)
        pygame.draw.rect(screen, self.color, self.shapeDown, 0)
    
    def move(self, v):
        self.x = self.x - v
        self.shapeUp = pygame.Rect(self.x, self.yUp, self.width, self.heightUp)
        self.shapeDown = pygame.Rect(self.x, self.yDown, self.width, self.heightDown)

    def collision(self, player):
        if self.shapeUp.colliderect(player) or self.shapeDown.colliderect(player):
            return True
        else:
            return False

class Player():
    def __init__(self, x, y, hei, wid):
        self.x = x
        self.y = y
        self.height = hei
        self.width = wid
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load(os.path.join("helicopter.png"))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

obstacles = []

def obstacleDraw():
    for i in range(21):
        obstacles.append(Obstacle(i * sWidth / 20, sWidth / 20))

heli = Player(250, 300, 32, 62)
dy = 0
dyCount = 0
up = 0
down = 0
points = 0
vo = 2

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -1
            if event.key == pygame.K_DOWN:
                dy = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                dy = 0
            if event.key == pygame.K_DOWN:
                dy = 0

            if event.key == pygame.K_SPACE:
                if display != "gameplay":
                    heli = Player(250, 300, 32, 62)
                    dy = 0
                    display = "gameplay"
                    points = 0
                    heightUpCount = 0
                    prevHeightUp = 200
                    obstacles.clear()
                    obstacleDraw()


    screen.fill((0,0,0))

    if display == "menu":
        writeMid("Press space to start :))", 20)

    elif display == "gameplay":
        for o in obstacles:

            # if points%100 == 0:
                # vo *= 2

            o.move(vo)
            o.draw()

            if o.collision(heli.shape):
                display = "end"
                dy = 0

        if up == 1:
            dyCount = dyCount + 1
            if dyCount == 2:
                dy = -1
                dyCount = 0
        elif down == 1:
            dyCount = dyCount + 1
            if dyCount == 2:
                dy = 1
                dyCount = 0
        
        for o in obstacles:
            if o.x <= -o.width:
                obstacles.remove(o)
                obstacles.append((Obstacle(sWidth, sWidth / 20)))
                # obstacles.append((Obstacle(sWidth+ o.x + o.width, sWidth / 20)))
                points = points + 1
                

        heli.draw()
        heli.move(dy)
        write(str(points), 5, 5, 15)
    
    elif display == "end":
        writeMid("You lose, press space to try again", 20)
        write(str(points), 5, 5, 15)
        heli = Player(250, 300, 32, 62)

