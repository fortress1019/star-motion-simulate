import pygame
import pyini
import os
import tkinter as tk
import tkinter.filedialog as fd
from math import isclose
from time import sleep, time
from threading import Thread
from typing import *
pygame.init()
pygame.key.set_repeat(1000, 50)

# Constant of gravitation
G = 6

class TrailPoint(tuple):
    def __init__(self, pos):
        tuple.__init__(self)
        self.pos = pos
        self.time = time()

    def __iter__(self):
        yield self.pos[0]
        yield self.pos[1]

    def get_time(self):
        return time() - self.time

class StarObject:
    def __init__(self, x, y, vx, vy, mass, locked=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.locked = locked


class Star(pygame.sprite.Sprite):
    def __init__(self,
            name: str,
            radius: int,
            color: Any,
            x: float,
            y: float,
            vx: float,
            vy: float,
            mass: float,
            locked=False):
        """
        A star
        :param name: name of star
        :param radius: radius of star
        :param color: color of star
        :param x: x pos of star
        :param y: y pos of star
        :param vx: x velocity of star
        :param vy: y velocity of star
        :param mass: mass of star
        :param locked: is star locked
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.locked = locked
        self.radius = radius
        self.color = color
        self.trail = []
        self.image = pygame.Surface((radius * 2, radius * 2)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)
        self.rect = self.image.get_rect()
        self.flush()

    def __repr__(self):
        return self.name

    __str__ = __repr__

    @property
    def info(self):
        return self.x, self.y, self.vx, self.vy, self.mass

    def flush(self):
        self.rect.centerx = (self.x + rel[0]) * scale
        self.rect.centery = (self.y + rel[1]) * scale

    def add_to_trail(self):
        self.trail.append(TrailPoint((self.x, self.y)))
        for point in self.trail:
            if point.get_time() > 1:
                self.trail.remove(point)

class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self._text = text
        self.flush(pos)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        pos = self.rect.topright
        self._text = text
        self.flush(pos)

    def flush(self, pos):
        self.image = font.render(self._text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos

def get_distance(sprite1, sprite2):
    x1, y1 = sprite1.star.x, sprite1.star.y
    x2, y2 = sprite2.star.x, sprite2.star.y
    dx = x2 - x1
    dy = y2 - y1
    return (dx ** 2 + dy ** 2) ** 0.5

def disappear_message(delay=1, interval=0.09):
    sleep(delay)
    while message.text and running:
        message.text = message.text[:-1]
        sleep(interval)

def move(t):
    sprites_to_delete = []
    for sprite1 in sprites:
        x1, y1, vx1, vy1, m1 = sprite1.info
        ax1, ay1 = 0, 0
        if sprite1 in sprites_to_delete:
            continue
        for sprite2 in sprites:
            if sprite1 in sprites_to_delete or sprite2 in sprites_to_delete:
                break
            if sprite1 is sprite2:
                continue
            x2, y2, vx2, vy2, m2 = sprite2.info
            dx = x2 - x1
            dy = y2 - y1
            r = get_distance(sprite1, sprite2)
            if is_collide(sprite1, sprite2):
                heavier = sprite1 if sprite1.mass > sprite2.mass else sprite2
                lighter = sprite2 if heavier is sprite1 else sprite1
                sprites_to_delete.append(lighter)
                heavier.star.vx += lighter.star.vx
                heavier.star.vy += lighter.star.vy
                message.text = language["star"]["collide"] % (heavier, lighter)
                Thread(target=disappear_message).start()
                break
            f = G * m1 * m2 / (r ** 2)
            if isclose(f, 0):
                continue
            accel = f / m1
            ax1 += accel * (dx / r)
            ay1 += accel * (dy / r)
        x, y = (
            x1 + vx1 * t + 0.5 * ax1 * (t ** 2),
            y1 + vy1 * t + 0.5 * ay1 * (t ** 2)
        )
        tempx, tempy = sprite1.x, sprite1.y
        if not sprite1.locked:
            sprite1.x, sprite1.y = x, y
            sprite1.vx = (x - tempx) / t
            sprite1.vy = (y - tempy) / t
        sprite1.flush()
    for sprite in sprites_to_delete:
        sprites.remove(sprite)
    for sprite in sprites:
        sprite.add_to_trail()

def is_collide(sprite1, sprite2):
    r1, r2 = sprite1.radius, sprite2.radius
    return r1 + r2 > get_distance(sprite1, sprite2)

def zoom(direction, each=0.02):
    global scale
    if direction > 0:
        scale += each
        if scale > 10:
            scale = 10
    elif direction < 0:
        scale -= each
        if scale < 0.02:
            scale = 0.02
    message.text = language["game"]["zoom"] % scale
    Thread(target=disappear_message).start()

def change_view(move_x, move_y):
    rel[0] += move_x
    rel[1] += move_y
    message.text = language["game"]["rel"] % str(tuple(rel))
    Thread(target=disappear_message).start()

with open("config/config.ini", "r", encoding="utf-8") as f:
    config = pyini.ConfigParser(f.read())

with open(f"config/language_{config['language']['default']}.ini", "r", encoding="utf-8") as f:
    language = pyini.ConfigParser(f.read())

size = width, height = (1000, 1000)

clock = pygame.time.Clock()
drag = False
rel = [0, 0]
scale = 1
paused = False

screen = pygame.display.set_mode(size)

movement = 10
pygame.display.set_icon(pygame.image.load(config["window"]["icon"]))
pygame.display.set_caption(language["game"]["title"])

with open(f"simulation/{config['simulation']['file']}.simulation", "r", encoding="utf-8") as f:
    sprites = eval(f.read())

font = pygame.font.SysFont("Microsoft YaHei UI", 20)
message = Message("", (width - 10, 10))

running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(30)
    if not paused:
        move(2)
    for sprite, trail in map(lambda xxx: (xxx, xxx.trail), sprites):
        if len(trail) < 2:
            continue
        trail = list(map(lambda point: ((point[0] + rel[0]) * scale, (point[1] + rel[1]) * scale), trail))
        pygame.draw.lines(screen, sprite.color, False, trail, 2)
    for sprite in sprites:
        sprite.flush()
        image = sprite.image
        image = pygame.transform.scale(image, (sprite.radius * 2 * scale,) * 2)
        screen.blit(image, sprite.rect)
    try:
        screen.blit(message.image, message.rect)
    except pygame.error:
        pass
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drag = False
            elif event.button == 4:
                zoom(1)
            elif event.button == 5:
                zoom(-1)
        elif event.type == pygame.MOUSEMOTION:
            if drag:
                change_view(*event.rel)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                root = tk.Tk()
                root.withdraw()
                filepath = fd.asksaveasfilename(
                    initialdir=os.path.dirname(__file__),
                    defaultextension=".png",
                    filetypes=(
                        (language["save"]["picture"] % "PNG", "*.png"),
                         language["save"]["other"], "*")
                )
                if filepath:
                    pygame.image.save(screen, filepath)
                root.destroy()
            elif event.key in (pygame.K_LEFT, pygame.K_KP_4):
                change_view(movement, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_KP_6):
                change_view(-movement, 0)
            elif event.key in (pygame.K_UP, pygame.K_KP_8):
                change_view(0, movement)
            elif event.key in (pygame.K_DOWN, pygame.K_KP_2):
                change_view(0, -movement)
            elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                zoom(1)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                zoom(-1)
pygame.quit()
