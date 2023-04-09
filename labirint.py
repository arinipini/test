from pygame import *
from time import sleep
w = 700
h = 700
back = (225, 237, 246)
window = display.set_mode((w,h))
win = transform.scale(image.load('finall.png'), (w, h))
lose = transform.scale(image.load('final.png'), (w, h))
display.set_caption('лабиринт')
run = True
finish = False
lives = 9
x1 = 480
x2 = 630
money = 0
bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, width, height, x, y, speed_x, speed_y):
        super().__init__(picture, width, height, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.speed_y
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        elif self.speed_y > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
    def fire(self):
        bullet = Bullet("bullet.png", 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= x1:
            self.direction = 'right'
        if self.rect.x >= x2:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, picture, width, height, x, y, speed ):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= w:
            self.kill()
wall_1 = GameSprite('platform_h.png', 350, 60, 130, 280)
wall_2 = GameSprite('platform_v.png', 60, 550, 430, 150)
player = Player('gato1.png', 80, 80, 5, 400, 0, 0)
final = GameSprite('7303-hehe.png', 80, 80, 600, 600)
enemy = Enemy('enemy.png', 80, 80, 480, 400, 2)
m1 = GameSprite("lapka.png", 40, 40, 50, 300)
m2 = GameSprite("lapka.png", 40,40, 400, 100)
m3 = GameSprite("lapka.png", 40,40, 300, 600)
m4 = GameSprite("lapka.png", 40,40, 600, 300)
m5 = GameSprite("lapka.png", 40,40, 100, 550)
m6 = GameSprite("lapka.png", 40,40, 250, 150)
m_gr = sprite.Group()
monsters = sprite.Group()
barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
m_gr.add(m1)
m_gr.add(m2)
m_gr.add(m3)
m_gr.add(m4)
m_gr.add(m5)
m_gr.add(m6)
monsters.add(enemy)

font.init()
font1 = font.SysFont('Arial', 30)
text_score = font1.render('Счет(^w^):'+str(money), True, (0,0,0))

while run:
    if finish != True:
        text_score = font1.render('Счет(^w^):'+str(money), True, (0,0,0))  
        window.fill(back)
        barriers.draw(window)
        player.reset()
        final.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        m_gr.draw(window)
        bullets.update()
        bullets.draw(window)
        window.blit(text_score, (40,40))
        time.delay(50)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0,0))
        if sprite.spritecollide(player,monsters,True):
            finish = True
            window.blit(lose, (0,0))
        if sprite.spritecollide(player, m_gr, True):
            money+=1
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y = -10
            if e.key == K_d:
                player.speed_x = 10
            if e.key == K_s:
                player.speed_y = 10
            if e.key == K_a:
                player.speed_x = -10
            if e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.speed_y = 0
            if e.key == K_d:
                player.speed_x = 0
            if e.key == K_s:
                player.speed_y = 0
            if e.key == K_a:
                player.speed_x = 0
    display.update()
sleep(30)