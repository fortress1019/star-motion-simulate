import pygame
import pyini
from time import sleep
from threading import Thread
pygame.init()
pygame.key.set_repeat(1000, 50)

G = 6

class StarObject:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass

    @property
    def info(self):
        return self.x, self.y, self.vx, self.vy, self.mass

class StarSprite(pygame.sprite.Sprite):
    def __init__(self, name, star, radius, color):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.star = star
        self.radius = radius
        self.color = color
        self.trail = []
        self.image = pygame.Surface((radius * 2, radius * 2)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.star.x, self.star.y

    def flush(self):
        self.rect.centerx = (self.star.x + rel[0]) * scale
        self.rect.centery = (self.star.y + rel[1]) * scale
        self.trail.append((self.star.x, self.star.y))

    def __repr__(self):
        return self.name

    __str__ = __repr__

class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self._text = text
        self.image = font.render(text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        pos = self.rect.topright
        self._text = text
        self.image = font.render(text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos

def get_distance(sprite1, sprite2):
    x1, y1 = sprite1.star.x, sprite1.star.y
    x2, y2 = sprite2.star.x, sprite2.star.y
    dx = x2 - x1
    dy = y2 - y1
    return (dx ** 2 + dy ** 2) ** 0.5

def disappear_message(delay=2, interval=0.09):
    sleep(delay)
    while message.text:
        message.text = message.text[:-1]
        sleep(interval)

def move(t):
    sprites_to_delete = []
    for sprite1 in sprites:
        star1 = sprite1.star
        x1, y1, vx1, vy1, m1 = star1.info
        ax1, ay1 = 0, 0
        if sprite1 in sprites_to_delete:
            continue
        for sprite2 in sprites:
            star2 = sprite2.star
            if sprite1 in sprites_to_delete or sprite2 in sprites_to_delete:
                break
            if star1 is star2:
                continue
            x2, y2, vx2, vy2, m2 = star2.info
            dx = x2 - x1
            dy = y2 - y1
            r = get_distance(sprite1, sprite2)
            if is_collide(sprite1, sprite2):
                heavier = sprite1 if star1.mass > star2.mass else sprite2
                lighter = sprite2 if heavier is star2 else sprite1
                sprites_to_delete.append(lighter)
                heavier.star.vx += lighter.star.vx
                heavier.star.vy += lighter.star.vy
                message.text = language["star"]["collide"] % (heavier, lighter)
                Thread(target=disappear_message).start()
                break
            f = G * m1 * m2 / (r ** 2)
            accel = f / m1
            ax1 += accel * (dx / r)
            ay1 += accel * (dy / r)
        x, y = (
            x1 + vx1 * t + 0.5 * ax1 * (t ** 2),
            y1 + vy1 * t + 0.5 * ay1 * (t ** 2)
        )
        tempx, tempy = star1.x, star1.y
        star1.x, star1.y = x, y
        star1.vx = (x - tempx) / t
        star1.vy = (y - tempy) / t
        sprite1.flush()
    for sprite in sprites_to_delete:
        sprites.remove(sprite)

def is_collide(sprite1, sprite2):
    r1, r2 = sprite1.radius, sprite2.radius
    return r1 + r2 > get_distance(sprite1, sprite2)

with open("config/config.ini", "r", encoding="utf-8") as f:
    config = pyini.ConfigParser(f.read())

with open(f"config/{config['language']['default']}", "r", encoding="utf-8") as f:
    language = pyini.ConfigParser(f.read())

size = width, height = (1000, 1000)
screen = pygame.display.set_mode((1000, 1000))

sprites = [
    StarSprite("planet1", StarObject(100, 100, 2, 0, 1000), 10, "green"),
    StarSprite("planet2", StarObject(800, 100, 0, 2, 1000), 10, "blue"),
    StarSprite("planet3", StarObject(800, 800, -2, 0, 1000), 10, "cyan"),
    StarSprite("planet4", StarObject(100, 800, 0, -2, 1000), 10, "yellow")
]

font = pygame.font.SysFont("Microsoft YaHei UI", 30)
message = Message("", (width - 10, 10))

clock = pygame.time.Clock()
drag = False
rel = [0, 0]
scale = 1
paused = False
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
        elif event.type == pygame.MOUSEMOTION:
            if drag:
                rel[0] += event.rel[0]
                rel[1] += event.rel[1]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                scale += 0.01
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                scale -= 0.01
    if not paused:
        move(2)
    for sprite, trail in map(lambda xxx: (xxx, xxx.trail), sprites):
        if len(trail) < 2:
            continue
        trail = list(map(lambda point: ((point[0] + rel[0]) * scale, (point[1] + rel[1]) * scale), trail))
        pygame.draw.lines(screen, sprite.color, False, trail, 2)
    for sprite in sprites:
        image = sprite.image
        image = pygame.transform.scale(image, (sprite.radius * 2 * scale, ) * 2)
        screen.blit(image, sprite.rect)
    screen.blit(message.image, message.rect)
    pygame.display.flip()
pygame.quit()
