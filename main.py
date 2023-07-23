import pygame
pygame.init()

########## 可更改：引力的大小 ##########
引力常数 = 10

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
        self.rect.center = self.天体.x, self.天体.y

    def 刷新rect属性(self):
        self.rect.centerx = self.天体.x + rel[0]
        self.rect.centery = self.天体.y + rel[1]

def get距离(天体精灵1, 天体精灵2):
    x1, y1, x速度1, y速度1, 质量1 = 天体精灵1.天体.基本信息
    x2, y2, x速度2, y速度2, 质量2 = 天体精灵2.天体.基本信息
    x距离 = x2 - x1
    y距离 = y2 - y1
    return (x距离 ** 2 + y距离 ** 2) ** 0.5

def is碰撞(天体精灵1, 天体精灵2):
    半径1, 半径2 = 天体精灵1.image.get_width(), 天体精灵2.image.get_height()
    return 半径1 + 半径2 > get距离(天体精灵1, 天体精灵2)

def 移动全部天体(时间):
    要删除的天体 = []
    for 天体精灵1 in 天体动画精灵列表:
        天体1 = 天体精灵1.天体
        if 天体1 in 要删除的天体:
            continue
        x1, y1, x速度1, y速度1, 质量1 = 天体1.基本信息
        x加速度1, y加速度1 = 0, 0
        for 天体精灵2 in 天体动画精灵列表:
            天体2 = 天体精灵2.天体
            if 天体2 in 要删除的天体:
                continue
            if 天体1 is 天体2:
                continue
            x2, y2, x速度2, y速度2, 质量2 = 天体2.基本信息
            x距离 = x2 - x1
            y距离 = y2 - y1
            距离 = get距离(天体精灵1, 天体精灵2)
            if is碰撞(天体精灵1, 天体精灵2):
                重天体 = 天体精灵1 if 天体1.质量 > 天体2.质量 else 天体精灵2
                轻天体 = 天体精灵1 if 重天体 is 天体2 else 天体精灵2
                要删除的天体.append(轻天体)
                重天体.天体.x速度 += 轻天体.天体.x速度
                重天体.天体.y速度 += 轻天体.天体.y速度
                continue
            力 = 引力常数 * 质量1 * 质量2 / (距离 ** 2)
            加速度 = 力 / 质量1
            x加速度1 += 加速度 * (x距离 / 距离)
            y加速度1 += 加速度 * (y距离 / 距离)
        x, y = (
            x1 + x速度1 * 时间 + 0.5 * x加速度1 * (时间 ** 2),
            y1 + y速度1 * 时间 + 0.5 * y加速度1 * (时间 ** 2)
        )
        临时x, 临时y = 天体1.x, 天体1.y
        天体1.x, 天体1.y = x, y
        天体1.x速度 = (x - 临时x) / 时间
        天体1.y速度 = (y - 临时y) / 时间
        天体精灵1.刷新rect属性()
    for 动画精灵 in 天体动画精灵列表:
        if 动画精灵 in 要删除的天体:
            天体动画精灵列表.remove(动画精灵)

screen = pygame.display.set_mode((900, 900))

天体动画精灵列表 = [
    天体动画精灵(天体("planet1", 100, 100, 0, 2, 500), 10, "green"),
    天体动画精灵(天体("planet2", 800, 450, 0, -2, 500), 10, "blue"),
    天体动画精灵(天体("planet3", 450, 850, 0, -1, 1000), 10, "cyan")
]

clock = pygame.time.Clock()
drag = False
rel = [0, 0]
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
        elif event.type == pygame.MOUSEMOTION:
            rel[0] += event.rel[0]
            rel[1] += event.rel[1]
    ########## 可更改：天体移动速度 ##########
    移动全部天体(1)
    for 天体动画精灵 in 天体动画精灵列表:
        screen.blit(天体动画精灵.image, 天体动画精灵.rect)
    pygame.display.flip()
