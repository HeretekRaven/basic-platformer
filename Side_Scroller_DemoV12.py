import pygame
import random

W = 1000
H = 800

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
off_white_f = (220, 0, 200)
off_white_w = (200, 0, 100)

pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("Demo V9")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("PUTINV2.png")
        self.image = pygame.Surface((30,30))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400
        self.grav = 10
        self.direct = 1
        self.timer = 0
        self.respawn = False
        self.x = 500
        self.y = 400
        self.ammo = 200
        self.mag = 15
        self.wep = (1, 15, 20, 20)
        self.rtimer = 0
        self.rel = False
        self.stimer = 0
        self.s = 5
    def update(self):
        self.change_x = 0
        self.change_y = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.direct = 1
            self.change_x = -15
            self.rect.x += 15
            collision = pygame.sprite.spritecollide(self, all_sprites, False)
            if collision:
                self.rect.x -= 15
                if self.change_x == -15:
                    self.change_x = 0
            else:
                self.rect.x -= 15
        if key[pygame.K_a]:
            self.direct = 2
            self.change_x = 15
            self.rect.x -= 15
            collision = pygame.sprite.spritecollide(self, all_sprites, False)
            if collision:
                self.rect.x += 15
                if self.change_x == 15:
                    self.change_x = 0
            else:
                self.rect.x += 15
        if self.timer < 4:
            self.timer += 1
        if key[pygame.K_SPACE] and self.timer == 4 and self.mag > 0 and self.rel == False:
            self.shoot(self.wep[0])
            self.mag += -1
            self.timer = 0
        if key[pygame.K_r] and self.mag != self.wep[1] and self.ammo + self.mag - self.wep[1] >= 0 and self.rel == False:
            self.ammo += self.mag - self.wep[1]
            self.rel = True
        if self.rel == True and self.rtimer < self.wep[2]:
            self.rtimer += 1
        if self.rtimer == self.wep[2]:
            self.mag = self.wep[1]
            self.rel = False
            self.rtimer = 0
            
            

        self.change_y -= self.grav
        global jump
        if jump <= 30 and jump > 21:
            self.change_y += 20
            jump -= 1
        if jump <= 21 and jump > 15:
            self.change_y += 15
            jump -= 1
        if jump <= 15 and jump > 10:
            jump -= 1
        if jump <= 10:
            jump = 0


        hit = pygame.sprite.spritecollide(self, epew, False)
        if hit:
            self.s += -1
            if self.s < 0:
                game.respawn()

        if self.stimer != 40:
            self.stimer += 1
        if self.stimer == 40:
            if self.s < 5:
                self.s += 1
            self.stimer = 0


        global jnum
        self.rect.y += 10
        floored = pygame.sprite.spritecollide(self, all_sprites, False)
        if floored:
            self.rect.y += -10
            if self.change_y <= 0:
                self.change_y = 0
            if jnum != 1:
                jnum = 1

        else:
            self.rect.y += -10

        self.rect.y += 10
        flooredM = pygame.sprite.spritecollide(self, mov_sprites, False)
        if flooredM:
            self.rect.y += -10
            if self.change_y <= 0:
                self.change_y = 0
                self.change_x += -wall0.moveX()
            if jnum != 1:
                jnum = 1
        else:
            self.rect.y += -10

        get = pygame.sprite.spritecollide(self, item, True)
        if get:
            self.ammo += 30


        if self.respawn == True:
            self.change_x = self.rect.x - self.x
            self.change_y = self.rect.y - self.y
            self.respawn = False
        self.x += self.change_x
        self.y += self.change_y

       
    def moveX(self):
        x = self.change_x
        return x
    def moveY(self):
        x = self.change_y
        return x
    def check(self):
        self.respawn = True
    def setcheck(self, pos):
        self.checkpoint = pos
        self.x = self.checkpoint[0]
        self.y = self.checkpoint[1]
    def shoot(self, wep):
        self.i = wep
        rngy = random.randint(-1 * self.wep[3], self.wep[3])
        if self.i == 1:
            e = Bullet((self.rect.x, self.rect.y + rngy), self.direct)
            pew.add(e)
        
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size = (500, 30)):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("PUTINV2.png")
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()
        
        hit = pygame.sprite.spritecollide(self, epew, True)
        hit2 = pygame.sprite.spritecollide(self, pew, True)

        self.rect.x += self.change_x
        self.rect.y += self.change_y

class Ammokit(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("PUTINV2.png")
        self.image = pygame.Surface((10,10))
        self.image.fill(off_white_f)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()


        self.rect.x += self.change_x
        self.rect.y += self.change_y

class WallM(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("PUTINV2.png")
        self.image = pygame.Surface((300,30))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timer = 0
        self.speed = 0
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()

        if self.timer != 200:
            self.timer += 1
        if self.timer <= 100 and self.timer >= 0:
            self.speed = 10
            self.change_x += self.speed
        if self.timer <= 200 and self.timer > 100:
            self.speed = -10
            self.change_x += self.speed
        if self.timer == 200:
            self.timer = 0

        hit = pygame.sprite.spritecollide(self, epew, True)
        hit2 = pygame.sprite.spritecollide(self, pew, True)

        self.rect.x += self.change_x
        self.rect.y += self.change_y
    def moveX(self):
        x = self.speed
        return x

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direct):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direct = direct
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()
        if self.direct == 1:
            self.change_x += 25
        if self.direct == 2:
            self.change_x += -25
        if self.rect.x > 1000 or self.rect.x < 0:
            self.kill()
        if self.rect.y > 800 or self.rect.y < 0:
            self.kill()
            
        self.rect.x += self.change_x
        self.rect.y += self.change_y

class Turret(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.health = 5
        self.timer = 0
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()

        hit = pygame.sprite.spritecollide(self, pew, True)
        if hit:
            self.health -= 1
        if self.health <= 0:
            drop = random.randint(1,2)
            if drop == 2:
                a = Ammokit((self.rect.x, self.rect.y + 20))
            self.kill()

        if self.timer != 50:
             self.timer += 1
        if self.timer == 3:
            if player.rect.x < self.rect.x:
                self.direct = 2
            if player.rect.x > self.rect.x:
                self.direct = 1
            self.shoot(self.direct)
        if self.timer == 6:
            if player.rect.x < self.rect.x:
                self.direct = 2
            if player.rect.x > self.rect.x:
                self.direct = 1
            self.shoot(self.direct)
        if self.timer == 9:
            if player.rect.x < self.rect.x:
                self.direct = 2
            if player.rect.x > self.rect.x:
                self.direct = 1
            self.shoot(self.direct)
        if self.timer == 12:
            if player.rect.x < self.rect.x:
                self.direct = 2
            if player.rect.x > self.rect.x:
                self.direct = 1
            self.shoot(self.direct)
        if self.timer == 50:
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
    def shoot(self, direct):
        rngy = random.randint(-15, 15)
        e = Bullet((self.rect.x, self.rect.y + rngy), direct)
        epew.add(e)
        
class Trooper(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.health = 10
        self.timer = 0
        self.dir = 1
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()

        hit = pygame.sprite.spritecollide(self, pew, True)
        if hit:
            self.health -= 1
        if self.health <= 0:
            drop = random.randint(1,2)
            if drop == 2:
                a = Ammokit((self.rect.x, self.rect.y + 20))
            self.kill()

        if self.timer != 25:
             self.timer += 1
        if self.timer == 25:
            if player.rect.x < self.rect.x:
                self.direct = 2
            if player.rect.x > self.rect.x:
                self.direct = 1
            self.shoot(self.direct)
            self.timer = 0

        if self.dir == 1:
            self.change_x -= 5
        if self.dir == 2:
            self.change_x += 5
        

        if self.dir == 1:
            self.rect.x -= 50
            self.rect.y += 10 
            floored = pygame.sprite.spritecollide(self, all_sprites, False)
            if floored:
                self.rect.x += 50
                self.rect.y -= 10
            else:
                self.rect.x += 50
                self.rect.y -= 10
                self.dir = 2
        if self.dir == 2:
            self.rect.x += 50
            self.rect.y += 10 
            floored = pygame.sprite.spritecollide(self, all_sprites, False)
            if floored:
                self.rect.x -= 50
                self.rect.y -= 10
            else:
                self.rect.x -= 50
                self.rect.y -= 10
                self.dir = 1
                
                

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
    def shoot(self, direct):
        e = Bullet((self.rect.x, self.rect.y - 15), direct)
        epew.add(e)
        e = Bullet((self.rect.x, self.rect.y), direct)
        epew.add(e)
        e = Bullet((self.rect.x, self.rect.y + 15), direct)
        epew.add(e)


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(off_white_w)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        hit = pygame.sprite.spritecollide(self, player_inst, False)
        if hit:
            player.setcheck((self.rect.x, self.rect.y))
            

class Door1(pygame.sprite.Sprite):
    def __init__(self, pos, locked = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill(off_white_w)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.state = locked
        self.opening = False
        self.timer = 0
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()

        self.rect.x += 30
        self.rect.y += 50
        hit = pygame.sprite.spritecollide(self, player_inst, False)
        if hit and self.state == False:
            self.rect.x += -30
            self.rect.y += -50
            self.opening = True
        else:
            self.rect.x += -30
            self.rect.y += -50
        self.rect.x += -30
        self.rect.y += 50
        hit = pygame.sprite.spritecollide(self, player_inst, False)
        if hit and self.state == False:
            self.rect.x += 30
            self.rect.y += -50
            self.opening = True
        else:
            self.rect.x += 30
            self.rect.y += -50
        if self.opening == True and self.timer != 5:
            self.timer += 1
            self.change_y += -10
        hitp = pygame.sprite.spritecollide(self, pew, True)
        if hitp and self.state == True:
            self.opening = True
        hit2 = pygame.sprite.spritecollide(self, epew, True)
        
            

        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Door2(pygame.sprite.Sprite):
    def __init__(self, pos, locked = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill(off_white_w)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.state = locked
        self.opening = False
        self.timer = 0
    def update(self):
        self.change_x = player.moveX()
        self.change_y = player.moveY()
        
        self.rect.x += 30
        hit = pygame.sprite.spritecollide(self, player_inst, False)
        if hit and self.state == False:
            self.rect.x += -30
            self.opening = True
        else:
            self.rect.x += -30
        self.rect.x += -30
        hit = pygame.sprite.spritecollide(self, player_inst, False)
        if hit and self.state == False:
            self.rect.x += 30
            self.opening = True
        else:
            self.rect.x += 30
        if self.opening == True and self.timer != 5:
            self.timer += 1
            self.change_y += 10
        hitp = pygame.sprite.spritecollide(self, pew, True)
        if hitp and self.state == True:
            self.opening = True
        hit2 = pygame.sprite.spritecollide(self, epew, True)
        
            

        self.rect.x += self.change_x
        self.rect.y += self.change_y    




        

class Game():
    def __init__(self):
        self.O2 = 100
        self.health = 10
        self.shield = 5
        self.lvl = 1
        self.menu = 0
    def lvlclr(self):
        all_sprites.empty()
        mov_sprites.empty()
        pew.empty()
        epew.empty()
        enemies.empty()
        player.kill()
        self.menu = 1
    def lvl_1(self):
        global gen
        gen = 1
    def lvl_2(self):
        global gen
        gen = 2
    def respawn(self):
        player.check()
    #def lvl_1(self):
        #Generate all of zone 1
    
        

font = pygame.font.SysFont("Times New Roman", 20)        
gen = 0
jump = 0
jnum = 0
game = Game()
game.lvl_2()


all_sprites = pygame.sprite.Group()
mov_sprites = pygame.sprite.Group()
player_inst = pygame.sprite.Group()
pew = pygame.sprite.Group()
epew = pygame.sprite.Group()
enemies = pygame.sprite.Group()
item = pygame.sprite.Group()
if gen == 1:
    player = Player()
    player_inst.add(player)

    wall = Wall((400, 600))
    all_sprites.add(wall)
    tur = Turret((600, 570))
    enemies.add(tur)
    wall = Wall((250, 800))
    all_sprites.add(wall)
    wall0 = WallM((100, 900))
    mov_sprites.add(wall0)
    wall = Wall((450, 750))
    all_sprites.add(wall)
    wall = Wall((550, 620))
    all_sprites.add(wall)
    d1 = Door1((500, 500))
    all_sprites.add(d1)
    d2 = Door2((500, 550))
    all_sprites.add(d2)
    c1 = Checkpoint((450, 570))
    enemies.add(c1)
if gen == 2:
    player = Player()
    player_inst.add(player)

    wall = Wall((400, 600))
    all_sprites.add(wall)
    wall = Wall((950, 700))
    all_sprites.add(wall)
    c1 = Checkpoint((1200, 670))
    enemies.add(c1)
    tur = Turret((1100, 670))
    enemies.add(tur)
    wall = Wall((1150, 550))
    all_sprites.add(wall)
    tur = Turret((1700, 420))
    enemies.add(tur)
    wall = Wall((1600, 450))
    all_sprites.add(wall)
    wall0 = WallM((2150, 450))
    mov_sprites.add(wall0)
    wall = Wall((3500, 450))
    all_sprites.add(wall)
    Tr = Trooper((3600, 420))
    enemies.add(Tr)
   

Quit = False
while not Quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and jump == 0 and jnum > 0:
                jump = 30
                jnum += -1
            if event.key == pygame.K_q:
                game.respawn()
    Scoreboard = font.render("Ammo: " + str(player.mag) + "/" + str(player.ammo), True, white)
    board = font.render("Shield: " + player.s * " [X] ", True, white)
    player_inst.update()
    item.update()
    pew.update()
    epew.update()
    all_sprites.update()
    mov_sprites.update()
    enemies.update()
    win.fill(black)
    player_inst.draw(win)
    item.draw(win)
    pew.draw(win)
    epew.draw(win)
    win.blit(Scoreboard, (50, 10))
    win.blit(board, (50, 40))
    all_sprites.draw(win)
    mov_sprites.draw(win)
    enemies.draw(win)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
quit()
            
