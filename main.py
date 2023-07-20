import pygame
pygame.init()

引力常数 = 6

class 天体:
    def __init__(self, 名称, x, y, x速度, y速度, 质量):
        self.名称 = 名称
        self.x = x
        self.y = y
        self.x速度 = x速度
        self.y速度 = y速度
        self.质量 = 质量

    @property
    def 基本信息(self):
        return self.x, self.y, self.x速度, self.y速度, self.质量

class 天体动画精灵(pygame.sprite.Sprite):
    def __init__(self, 天体, 半径, 颜色):
        pygame.sprite.Sprite.__init__(self)
        self.天体 = 天体
        self.image = pygame.Surface((半径 * 2, 半径 * 2)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, 颜色, (半径, 半径), 半径, 0)
        self.rect = self.image.get_rect()
        self.刷新rect属性()

    def 刷新rect属性(self):
        self.rect.topleft = self.天体.x, self.天体.y

def 移动全部天体(时间):
    for 天体sprite1 in 天体动画精灵列表:
        天体1 = 天体sprite1.天体
        x1, y1, x速度1, y速度1, 质量1 = 天体1.基本信息
        x加速度1, y加速度1 = 0, 0
        for 天体2 in 天体动画精灵列表:
            天体2 = 天体2.天体
            if 天体1 != 天体2:
                x2, y2, x速度2, y速度2, 质量2 = 天体2.基本信息
                x距离 = x2 - x1
                y距离 = y2 - y1
                距离 = (x距离 ** 2 + y距离 ** 2) ** 0.5
                力 = 引力常数 * 质量1 * 质量2 / (距离 ** 2)
                加速度 = 力 / 质量1
                x加速度1 += 加速度 * (x距离 / 距离)
                y加速度1 += 加速度 * (y距离 / 距离)
        x, y = (
            x1 + x速度1 * 时间 + 0.5 * x加速度1 * (时间 ** 2),
            y1 + y速度1 * 时间 + 0.5 * y加速度1 * (时间 ** 2)
        )
        天体1.x = x
        天体1.y = y
        天体sprite1.刷新rect属性()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

天体动画精灵列表 = [
    天体动画精灵(天体("planet1", 0, 0, 1, 1, 10), 50, "orange"),
    天体动画精灵(天体("planet2", 5, 5, -1, -1, 5), 10, "blue")
]

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    移动全部天体(1)
    for 天体动画精灵 in 天体动画精灵列表:
        screen.blit(天体动画精灵.image, 天体动画精灵.rect)
    pygame.display.flip()
