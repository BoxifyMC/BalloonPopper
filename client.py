import pygame
import os
from random import randint as rand
from playsound import playsound
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from pygame.locals import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Player:
    def __init__(self):
        self.texture = pygame.transform.scale(pygame.image.load('player.png'), (200, 200))
        self.weapon = ['Bare Hands', 40]
        self.x = 0
        self.y = 200
    def render(self):
        global root
        self.character = root.blit(self.texture, (self.x, self.y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += 10
        if keys[pygame.K_LEFT]:
            self.x -= 10
class Balloon:
    def __init__(self, startpos=None):
        if startpos != None:
            self.pos = [startpos, 200]
        else:
            self.pos = [1000, 200]
        self.colour = (rand(0, 255), rand(0, 255), rand(0, 255))
        self.popped = False
    def render(self):
        global root
        if not self.popped:
            pygame.draw.line(root, (0, 0, 0), (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1] + 100))
            self.character = pygame.draw.circle(root, self.colour, (self.pos[0], self.pos[1] - 50), 50)
        if self.pos[0] < -100:
            self.pos[0] = 1100
            self.colour = (rand(0, 255), rand(0, 255), rand(0, 255))
            self.popped = False
        else:
            self.pos[0] -= 20
def playAgain():
    global score
    global hooray
    score = 0
    hooray.destroy()
def killGame():
    global running
    global hooray
    running = False
    hooray.destroy()
def congratulateWin():
    global score
    global hooray
    hooray = Tk()
    Label(hooray, text='Well done, you won the game!').pack()
    Button(hooray, text='Quit', command= lambda: killGame()).pack()
    Button(hooray, text='Play Again', command=lambda: resetGame()).pack()
    hooray.title('Well done, you won the game!')
def warnNoMoney():
    window = Tk()
    exit = Button(window, text='OK', command= lambda: window.destroy())
    message = Label(window, text='You do not have enough points to upgrade your weapon!')
    message.pack()
    exit.pack()
    window.title('Warning')
    window.mainloop()
def popBalloon(arg):
    global player
    global score
    chance = player.weapon[1]
    chance += 1
    if chance > rand(1, 100):
        arg.popped = True
        score += 1
        playsound('popped.mp3')
    else:
        playsound('not_popped.mp3')
def upgradeWeapon():
    global upgraded
    global player
    upgraded = True
    player.weapon = ['Needle', 80]
def updateWindow():
    global root
    global clock
    global fps
    pygame.display.update()
    pygame.time.delay(100)
    clock.tick(60)
    fps = clock.get_fps()
def clearWindow():
    global root
    root.fill((50, 205, 50))
def checkEvents():
    global balloons
    global running
    global upgrader
    global upgrader_text
    global score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for balloon in balloons:
                if balloon.character.collidepoint(mouse_x, mouse_y):
                    popBalloon(balloon)
            if not upgraded:
                if upgrader.collidepoint(mouse_x, mouse_y) or upgrader_text.collidepoint(mouse_x, mouse_y):
                    if score > 31:
                        upgradeWeapon()
                    else:
                        warnNoMoney()
    if score > 100:
        congratulateWin()
def redrawSprites():
    global root
    global upgrader
    global upgrader_text
    global balloons
    global player
    global score
    global fps
    global text
    global upgraded
    root.blit(pygame.image.load('sky.png'), (0, 0))
    root.blit(pygame.image.load('sky.png'), (0, 100))
    for balloon in balloons:
        balloon.render()
    root.blit(text.render("FPS: " + str(int(fps)), True, (0, 0, 0)), (0, 0))
    root.blit(text.render(str(score), True, (0, 0, 0)), (920, 0))
    root.blit(text.render("Weapon: " + player.weapon[0], True, (0, 0, 0)), (550, 0))
    if not upgraded:
        upgrader = pygame.draw.rect(root, (255, 255, 255), (200, 0, 260, 40))
        upgrader_text = root.blit(text.render("Upgrade Weapon", True, (0, 0, 0)), (200, 0))
    player.render()
def setupGame():
    global root
    global text
    global running
    global fps
    global score
    global balloons
    global clock
    global player
    global upgraded
    pygame.init()
    root = pygame.display.set_mode((1000, 400))
    text = pygame.font.SysFont('Courier', 30)
    running = True
    fps = 0
    upgraded = False
    score = 0
    balloons = []
    clock = pygame.time.Clock()
    player = Player()
    pygame.display.set_caption('Balloon Popper')
    for time in range(1, 14):
        if time%2 == 0:
            x = time*100
            balloons.append(Balloon(startpos=x))
def playGame():
    global running
    setupGame()
    while running:
        updateWindow()
        clearWindow()
        checkEvents()
        redrawSprites()
        pygame.event.pump()
    pygame.display.quit()
    pygame.quit()
playGame()
