from pygame import *
from random import randint

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'

score = 0
lost = 0
goal = 10
max_lost = 30

mixer.init()
mixer.music.load('space.ogg')

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 36)
win = font1.render('ПОБЕДА', True, (245, 239, 66))
lose = font1.render('ПРОИГРЫШ', True, (245, 81, 66))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load (player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0 
            lost = lost + 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

width = 700
height = 500
display.set_caption('Урок математики в 7 Бе)')
window = display.set_mode((width, height))
backgraund = transform.scale(image.load(img_back), (width, height))

ship = Player(img_hero, 5, height - 100, 50, 100, 3)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, width - 80), -10, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
start = True 

while start:
    for e in event.get():
        if e.type == QUIT:
            start = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finish:
        window.blit(backgraund, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (74, 247, 172))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущенно:' + str(lost), 1, (66, 135, 245))
        window.blit(text_lose, (10, 50))

        ship.update()
        bullets.update()
        monsters.update()
        ship.reset() 
        bullets.draw(window)
        monsters.draw(window) 

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1 
            monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster) 



        if score >= goal:
            finish = True
            window.blit(win, (200, 200))   

        display.update()
time.delay(2)  