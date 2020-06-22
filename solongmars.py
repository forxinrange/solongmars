## So Long Mars Source 1.0.0.1 ##
#
#
## Created by - Michael Bradley 2020 ##

import pygame
import random
import math
import time
import os

#os.environ['SDL_VIDEODRIVER'] = 'directx'
pygame.init()

class sound():

    def __init__(self):
        self.music = ''
        self.soundBank = []

    def loadMusic(self,track):
        self.music = track
        print(self.music)
        pygame.mixer.music.load(self.music)
    
    def loadEffect(self,effect):
        self.soundBank.append(pygame.mixer.Sound(effect))
    
    def playMusic(self, looping):
        if(looping == False):
            pygame.mixer.music.play()
        elif(looping == True):
            pygame.mixer.music.play(-1)

    def getMusicPlayTime(self):
        return pygame.mixer.music.get_pos()

    def triggerSound(self, ID):
        self.soundBank[int(ID)].play()

    def stopMusic(self):
        pygame.mixer.music.stop()

class sprite():

    def __init__(self,spritePath):
        self.xPos = 0
        self.yPos = 0
        self.xMod = 0
        self.yMod = 0
        self.speed = 1
        self.topSpeed = 10
        self.friction = 1
        self.sprite = pygame.image.load(spritePath)
    
    def setPosition(self, x, y):
        self.xPos = x
        self.yPos = y

    def boundary(self, s_x, s_y):
        if(self.xPos > s_x):
            self.xPos = s_x
        elif(self.xPos < 0):
            self.xPos = 0
        
        if(self.yPos > s_y):
            self.yPos = s_y
        elif(self.yPos < 0):
            self.yPos = 0

class planet(sprite):

    def __init__(self, spritePath, name):
        super().__init__(spritePath)
        self.visible = True
        self.name = name


class enemy(sprite):

    def __init__(self, spritePath, name):
        super().__init__(spritePath)
        self.visible = True
        self.moving = True
        self.bossName = name

    def setSpeed(self, level):
        self.speed = int(level)

    def chaseTarget(self, t_x, t_y):
        if(self.moving == True):
            if(self.xPos < t_x):
                self.xPos = self.xPos + self.speed
            elif(self.xPos > t_x):
                self.xPos = self.xPos - self.speed
            
            if(self.yPos < t_y):
                self.yPos = self.yPos + self.speed
            elif(self.yPos > t_y):
                self.yPos = self.yPos - self.speed

class asteroid(sprite):

    def __init__(self, spritePath, maxX, maxY):
        super().__init__(spritePath)
        self.visible = True
        self.moving = True
        self.hit = False
        self.maxX = maxX
        self.maxY = maxY
        self.topSpeed = 4
        self.xDirection = 1
        self.yDirection = 1
        self.respawn = True
        self.randomPosition()
        self.determineDirection()
        #self.setDirection()
        self.randomSpeed()
        self.angle = random.randint(0, 359)
        self.angleSteps = 360
        self.spriteCache = []
        self.initSpriteCache()

    def initSpriteCache(self):
        origImg = self.sprite.copy()
        for x in range(self.angleSteps):
            self.spriteCache.append(pygame.transform.rotate(origImg, x))


    def setSpeed(self, level):
        self.speed = int(level)

    def rotateAsteroid(self):
        if(self.angle == 359):
            self.angle = 0
        else:
            self.angle = self.angle + 1

        self.sprite = self.spriteCache[self.angle]
    
    def randomSpeed(self):
        self.speed = round(random.uniform(0.5, self.topSpeed), 2)

    def randomPosition(self):

        self.xDirection = round(random.uniform(self.speed/4, self.speed*4), 2)
        self.yDirection = round(random.uniform(self.speed/4, self.speed*4), 2)

        edgeSpawn = random.randint(0, 3)

        # LEFT SIDE
        if(edgeSpawn == 0):
            self.xPos = random.randint(-150, -20)
            self.yPos = random.randint(0, self.maxY)
        
        # TOP SIDE
        if(edgeSpawn == 1):
            self.xPos = random.randint(0, self.maxX)
            self.yPos = random.randint(-150, -20)
        
        # RIGHT SIDE
        if(edgeSpawn == 2):
            self.xPos = random.randint(self.maxX + 20, self.maxX + 150)
            self.yPos = random.randint(0, self.maxY)
        
        # BOTTOM SIDE
        if(edgeSpawn == 3):
            self.xPos = random.randint(0, self.maxX)
            self.yPos = random.randint(self.maxY + 20, self.maxY + 150)

    def determineDirection(self):
        upDown = random.randint(0, 1)

        if(self.xPos < 0):
            self.xDirection = self.speed
        else:
            self.xDirection = self.speed = self.speed - (self.speed * 2)
        
        if(upDown == 1):
            self.yDirection = self.speed
        else:
            self.yDirection = self.speed = self.speed - (self.speed * 2)

    def moveAsteroid(self):
        self.xPos = self.xPos + self.xDirection
        self.yPos = self.yPos + self.xDirection
        if(self.xPos < -100 or self.xPos > (self.maxX + 100)):
            self.resetAsteroid()

        if(self.yPos < -150 or self.yPos > (self.maxY + 150)):
            self.resetAsteroid()

        self.rotateAsteroid()
        #print(self.xPos, self.yPos, self.xDirection, self.yDirection)

    def resetAsteroid(self):
        if(self.respawn == True):
            self.randomPosition()
            self.determineDirection()
        #self.setDirection()
        #print("RESET")
    
    def collisionCheck(self, x2, y2):
        xCol = bool(self.xPos >= x2-20 and self.xPos <= x2+20)
        yCol = bool(self.yPos >= y2-20 and self.yPos <= y2+20)
        if(xCol and yCol):
            self.hit = True
        else:
            self.hit = False



class asteroidField():

    def __init__(self, noAsteroids, maxXScale, maxYScale):
        self.noAsteroids = noAsteroids
        self.maxXScale = maxXScale
        self.maxYScale = maxYScale

    def initAsteroids(self, reset):
        if(reset == True): 
            self.Asteroids = []
        for _ in range(self.noAsteroids):
            self.Asteroids.append(asteroid('asteroidS.png', self.maxXScale, self.maxYScale))

    def changeAsteroidSpeed(self, newSpeedFactor):
        for x in range(len(self.Asteroids)):
            self.Asteroids[x].speed = newSpeedFactor
        
    def moveAsteroids(self):
        for x in range(len(self.Asteroids)):
            self.Asteroids[x].moveAsteroid()

    def drawAsteroids(self, screen):
        for x in range(len(self.Asteroids)):
            tempRect = self.Asteroids[x].sprite.get_rect()
            tempRect.center = (self.Asteroids[x].xPos, self.Asteroids[x].yPos)
            screen.blit(self.Asteroids[x].sprite, tempRect)

    def asteroidsHit(self, x2, y2):
        for x in range(len(self.Asteroids)):
            self.Asteroids[x].collisionCheck(x2, y2)

    def asteroidsRespawn(self, toggle):
        for x in self.Asteroids:
            x.respawn = toggle

    def checkHits(self):
        hitDetect = False
        for x in self.Asteroids:
            if x.hit == True:
                hitDetect = True
                break
            else:
                continue
        
        return hitDetect

class player(sprite):

    def __init__(self, spritePath, spritePath2, spritePath3):
        super().__init__(spritePath)
        self.playerName = "Player 1"
        self.friction = 0.20
        self.spriteExplode = pygame.image.load(spritePath2)
        self.spriteNoEngine = pygame.image.load(spritePath3)
        self.engineOut = True
    
    def processMovement(self):
        keys = pygame.key.get_pressed()
        # Right
        if keys[pygame.K_RIGHT]:
            self.xMod += self.speed
        elif(self.xMod > 0 and not keys[pygame.K_RIGHT]):
            self.xMod = self.xMod - self.friction

        # Left
        if keys[pygame.K_LEFT]:
            self.xMod += -self.speed
        elif(self.xMod < 0 and not keys[pygame.K_LEFT]):
            self.xMod = self.xMod + self.friction
        
        # Down
        if keys[pygame.K_DOWN]:
            #self.engineOut = True
            self.yMod += self.speed
        elif(self.yMod > 0 and not keys[pygame.K_DOWN]):
            #self.engineOut = False
            self.yMod = self.yMod - self.friction
        
        # Up
        if keys[pygame.K_UP]:
            self.yMod += -self.speed
        elif(self.yMod < 0 and not keys[pygame.K_UP]):
            self.yMod = self.yMod + self.friction

        # Speed limiter

        # X Limiter
        if(self.xMod >= self.topSpeed):
            self.xMod = self.topSpeed
        elif(self.xMod <= -self.topSpeed):
            self.xMod = -self.topSpeed

        # Y Limiter
        if(self.yMod >= self.topSpeed):
            self.yMod = self.topSpeed
        elif(self.yMod <= -self.topSpeed):
            self.yMod = -self.topSpeed

        # Move
        self.xPos += self.xMod
        self.yPos += self.yMod

        #print(self.xPos, self.yPos)

class star():

    def __init__(self, size, color, maxX):
        self.size = size
        self.color = color
        self.velocity = size * 1
        self.maxX = maxX
        self.randomXPos()
        self.randomYPos()
    
    def randomYPos(self):
        self.yPos = random.randint(-self.maxX, -5)

    def randomXPos(self):
        self.xPos = random.randint(0, self.maxX)

    def setCol(self, newColor):
        self.color = newColor

    def setPos(self, x, y):
        self.xPos = x
        self.yPos = y

    def drawStar(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.xPos), int(self.yPos)), self.size)

class starfield():
    
    def __init__(self, bgCol, noStars, maxStarSize, starColor, maxXScale, maxYScale):
        self.bgCol = bgCol
        self.noStars = noStars
        self.maxStarSize = maxStarSize
        self.starColor = starColor
        self.maxXScale = maxXScale
        self.maxYScale = maxYScale
        self.speedFactor = 1
        self.repeatStars = True
        self.visible = True

    def initStars(self):
        self.stars = []
        for _ in range(self.noStars):
            self.stars.append(star(random.randint(1, self.maxStarSize), self.starColor, self.maxXScale))

    def changeStarSpeed(self, newSpeedFactor):
        self.speedFactor = newSpeedFactor
        for x in range(self.noStars):
            self.stars[x].velocity = self.stars[x].size * self.speedFactor

    def moveStars(self):
        for x in range(len(self.stars)):
            if((self.stars[x].yPos > self.maxYScale + self.stars[x].size) and self.repeatStars == True):
                self.stars[x].randomXPos()
                self.stars[x].randomYPos()
            else:
                self.stars[x].setPos(self.stars[x].xPos, (self.stars[x].yPos) + self.stars[x].velocity)

    def sparkleStars(self, color):
        for x in range(len(self.stars)):
            chance = random.randint(0, 1)
            if(chance == 1):
                self.stars[x].setCol(color)

    def colorStars(self, color):
        for x in self.stars:
            x.setCol(color)

    def rainbowStars(self):
        for x in range(len(self.stars)):
            ranRGB = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
            self.stars[x].setCol(ranRGB)
    
    def drawStars(self, screen):
        for x in range(len(self.stars)):
            self.stars[x].drawStar(screen)

## MAIN GAME CLASS ##

class game():

    def __init__(self):
        self.icon = pygame.image.load('rockit3.png')
        self.xWindow = 1280
        self.yWindow = 720
        self.asteroidCount = 10
        self.fps = 60
        self.timeTick = 0
        self.screen = pygame.display.set_mode((self.xWindow, self.yWindow), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("So long Mars | 1.0.0.1 | © 2020 Michael J. Bradley")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.soundEng = sound()
        self.bigFont = pygame.font.Font('freesansbold.ttf', 64)
        self.menuStars = starfield((0, 0, 0), 1000, 2, (255, 255, 255), self.xWindow, self.yWindow)
        self.initMenu()
        self.starField1 = starfield((0, 0, 0), 1000, 3, (255, 255, 255), self.xWindow, self.yWindow)
        self.starField2 = starfield((0,0,0), 100, 3, (255,255,255), self.xWindow, self.yWindow)
        self.asteroidField1 = asteroidField(self.asteroidCount, self.xWindow, self.yWindow)
        self.mainLoop = True
        self.gameOver = False
        self.gameWon = False
        self.menu = True
        self.mainRun()

    def initMenu(self):
        self.menuStars.initStars()
        self.menuStars.changeStarSpeed(0.25)
        for _ in range(1400):
            self.menuStars.moveStars()
        #self.menuStars.sparkleStars((0, 0, 255))

    def loadObjects(self):

        # Init starfield #
        self.starField1.initStars()
        self.starField1.repeatStars = True

        self.starField2.initStars()
        self.starField2.visible = False
        self.starField2.repeatStars = True
        self.starField2.sparkleStars((255,165,0))

        # Player object 
        self.PLAYER = player('rockit3.png', 'explode.png', 'rockitne.png')
        self.PLAYER.engineOut = True
        self.PLAYER.sprite = self.scaleSprite(self.PLAYER.sprite, round(self.xWindow/30), round(self.xWindow/30))
        self.PLAYER.spriteExplode = self.scaleSprite(self.PLAYER.spriteExplode, round(self.xWindow/20), round(self.xWindow/20))
        self.PLAYER.spriteNoEngine = self.scaleSprite(self.PLAYER.spriteNoEngine, round(self.xWindow/30), round(self.xWindow/30))
        self.PLAYER.setPosition(int(self.xWindow / 2), int(self.yWindow / 2))

        # Load Mars
        self.MARS = planet('mars.png', "mars")
        self.MARS.sprite = self.scaleSprite(self.MARS.sprite, self.xWindow, self.xWindow)
        self.MARS.setPosition(int(self.xWindow/2), int(self.yWindow + (self.yWindow/5)))
        self.MARS.speed = 0.25

        # Load Earth
        self.EARTH = planet('earth.png', "earth")
        self.EARTH.sprite = self.scaleSprite(self.EARTH.sprite, self.xWindow, self.xWindow)
        self.EARTH.setPosition(int(self.xWindow/2), int(-self.yWindow + (self.yWindow/5)))
        self.EARTH.speed = 1.5

        # Init asteroid field
        self.asteroidField1.initAsteroids(True)
        for x in range(len(self.asteroidField1.Asteroids)):
            self.asteroidField1.Asteroids[x].sprite = self.scaleSprite(self.asteroidField1.Asteroids[x].sprite, round(self.xWindow/20), round(self.xWindow/20))
            for y in range(len(self.asteroidField1.Asteroids[x].spriteCache)):
                self.asteroidField1.Asteroids[x].spriteCache[y] = self.scaleSprite(self.asteroidField1.Asteroids[x].spriteCache[y], round(self.xWindow/20), round(self.xWindow/20))

    def initSoundBank(self):
        # ID 0 - EXPLOSION SOUND
        self.soundEng.loadEffect('exp.wav')
    
    def scaleSprite(self, sprite, x, y):
        return pygame.transform.scale(sprite, (x, y))

    def drawObjects(self):

        self.marsRect = self.MARS.sprite.get_rect()
        self.marsRect.center = (self.MARS.xPos, self.MARS.yPos)
        self.screen.blit(self.MARS.sprite, self.marsRect)

        self.earthRect = self.EARTH.sprite.get_rect()
        self.earthRect.center = (self.EARTH.xPos, self.EARTH.yPos)
        self.screen.blit(self.EARTH.sprite, self.earthRect)

        # Draw player #
        self.playerRect = self.PLAYER.sprite.get_rect()
        self.playerRect.center = (self.PLAYER.xPos, self.PLAYER.yPos)
        self.PLAYER.boundary(self.xWindow, self.yWindow)

        self.explodeRect = self.PLAYER.spriteExplode.get_rect()
        self.explodeRect.center = (self.PLAYER.xPos, self.PLAYER.yPos)

        self.engineOutRect = self.PLAYER.spriteNoEngine.get_rect()
        self.engineOutRect.center = (self.PLAYER.xPos, self.PLAYER.yPos)

        if(self.gameOver == True):
            self.screen.blit(self.PLAYER.spriteExplode, self.explodeRect)
        elif(self.PLAYER.engineOut == True):
            self.screen.blit(self.PLAYER.spriteNoEngine, self.engineOutRect)
        else:
            self.screen.blit(self.PLAYER.sprite, self.playerRect)

        # Draw asteroid #
        self.asteroidField1.drawAsteroids(self.screen)

    def resetEventTriggers(self):
        self.eventFirstLauch = True
        self.eventFirstBreather = True
        self.eventSecondLaunch = True
        self.eventSecondBreather = True


    ##### Main Game Loop #####
    def mainRun(self):

        while self.mainLoop:

            while self.menu:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                # Menu elements
                self.screen.fill((0, 0, 0))
                self.menuStars.drawStars(self.screen)
                self.menuStars.moveStars()
                self.menuStars.repeatStars = True
                self.menuTitle = "SO LONG MARS"
                self.menuTitleObj = self.bigFont.render(self.menuTitle, True, (0, 255, 255))
                self.menuRectObj = self.menuTitleObj.get_rect()
                self.menuRectObj.center = (self.xWindow // 2, self.yWindow // 2)
                self.screen.blit(self.menuTitleObj, self.menuRectObj)
                self.clock.tick(self.fps)
                pygame.display.flip()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.initSoundBank()
                    self.loadObjects()
                    self.resetEventTriggers()
                    self.gameOver = False
                    self.gameWon = False
                    self.menu = False

            
            self.soundEng.loadMusic('us3.mp3')
            self.soundEng.playMusic(False)
            
            while(self.gameOver == False and self.gameWon == False):

                # Store music time
                musicPos = self.soundEng.getMusicPlayTime()

                # Hide menu stars
                self.menuStars.visible = False

                # Pygame event listener #
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                # Blank screen every frame
                self.screen.fill((0, 0, 0))

                # Draw starfield
                if(self.starField1.visible == True):
                        self.starField1.drawStars(self.screen)
                        self.starField1.moveStars()

                if(self.starField2.visible == True):
                        self.starField2.drawStars(self.screen)
                        self.starField2.moveStars()

                if(self.MARS.yPos > 0):
                    self.MARS.setPosition(self.MARS.xPos, (self.MARS.yPos + self.MARS.speed))

                

                ## TIMED EVENTS ##

                # First launch
                if(musicPos > 14500 and self.eventFirstLauch == True):
                    self.PLAYER.engineOut = False
                    self.starField1.sparkleStars((0, 255, 255))
                    self.starField1.changeStarSpeed(5)
                    self.MARS.speed = 7
                    self.eventFirstLauch = False

                #Breather
                if(musicPos > 60000 and self.eventFirstBreather == True):
                    self.PLAYER.engineOut = True
                    self.starField1.repeatStars = False
                    self.starField2.visible = True
                    self.asteroidField1.asteroidsRespawn(False)
                    self.eventFirstBreather = False


                # Final push double the asteroids 96000
                if(musicPos > 97000 and self.eventSecondLaunch == True):
                    self.PLAYER.engineOut = False
                    self.asteroidField1.initAsteroids(False)
                    self.starField1.repeatStars = True
                    self.starField2.repeatStars = False
                    self.starField2.visible = False
                    self.asteroidField1.asteroidsRespawn(True)
                    self.eventSecondLaunch = False

                # Back to Earth 112000
                if(musicPos > 112500 and self.eventSecondBreather == True):
                    self.PLAYER.engineOut = True
                    self.starField1.colorStars((255, 255, 255))
                    self.starField1.changeStarSpeed(1)
                    self.starField1.repeatStars = False
                    self.asteroidField1.asteroidsRespawn(False)
                    self.eventSecondBreather = False

                if(musicPos > 112500):
                    self.EARTH.setPosition(self.EARTH.xPos, (self.EARTH.yPos + self.EARTH.speed))
                
                if(musicPos > 120000):
                    self.gameWon = True

                # Logic for player movement #
                if(musicPos > 14500):
                    self.PLAYER.processMovement()

                # Asteroid Logic #
                if(musicPos > 14500):
                    self.asteroidField1.moveAsteroids()

                # Check Asteroid Collision
                self.asteroidField1.asteroidsHit(self.PLAYER.xPos, self.PLAYER.yPos)
                self.gameOver = self.asteroidField1.checkHits()

                # BANG! #
                if(self.gameOver == True):
                    self.soundEng.stopMusic()
                    self.soundEng.triggerSound(0)

                # Draw Objects
                self.drawObjects()

                # Update screen
                pygame.display.flip()
                self.clock.tick(self.fps)
                #print(self.timeTick / 60)

            while self.gameOver:

                pygame.time.delay(3000)
                self.gameOver = False
                self.gameWon = False
                self.menu = True

            while self.gameWon:

                pygame.time.delay(3000)
                self.gameOver = False
                self.gameWon = False
                self.menu = True



if __name__ == "__main__":
    game()
    quit()
