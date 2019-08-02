#骑士救公主
import pygame
import pygame.locals as locals
import math

class player():
    pass

class enemy():
    pass


WINDOWS_WIDTH = 1024         #
WINDOWS_HEIGHT = 576        #
surface = pygame.display.set_mode((WINDOWS_WIDTH,WINDOWS_HEIGHT))
pygame.display.set_caption("勇士救公主")
background = pygame.image.load("../sources/image/background.png")
game_count = 0
# 角色静止
static = True
player_stand_img = []
player_stand_img_index = 0
player_stand_img.append(pygame.image.load("../sources/image/站立/stand1.png"))
player_stand_img.append(pygame.image.load("../sources/image/站立/stand2.png"))
player_stand_img.append(pygame.image.load("../sources/image/站立/stand3.png"))
player_stand_img.append(pygame.image.load("../sources/image/站立/stand4.png"))
player_stand_img.append(pygame.image.load("../sources/image/站立/stand5.png"))
player_stand_img.append(pygame.image.load("../sources/image/站立/stand6.png"))
# 角色奔跑
player_move_img = []
player_move_img_index = 0
player_move_img.append(pygame.image.load("../sources/image/移动/player_move1.png"))
player_move_img.append(pygame.image.load("../sources/image/移动/player_move2.png"))
player_move_img.append(pygame.image.load("../sources/image/移动/player_move3.png"))
player_move_img.append(pygame.image.load("../sources/image/移动/player_move4.png"))
player_move_img.append(pygame.image.load("../sources/image/移动/player_move5.png"))
#传送门
trans_door_img = []
trans_door_img_index = 0
trans_door_img.append(pygame.image.load("../sources/image/传送门/1-1.png"))
trans_door_img.append(pygame.image.load("../sources/image/传送门/1-2.png"))
trans_door_img.append(pygame.image.load("../sources/image/传送门/1-3.png"))
trans_door_img.append(pygame.image.load("../sources/image/传送门/1-4.png"))
trans_door_img.append(pygame.image.load("../sources/image/传送门/1-5.png"))

print(type(player_stand_img[0]))
#player = pygame.image.load("./
player = player_stand_img[0]
play_x = 0
play_y = 0
play_speed = 8
move = None
stop = None
# surface.blit(player,(play_x,play_y))

while True:
    game_count += 1
    if game_count == 1000000:
        game_count = 0
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            exit()
        if event.type == locals.MOUSEBUTTONDOWN:  # 按下鼠标触发
            left, wheel, right = pygame.mouse.get_pressed()
            if left == 1:
                print("鼠标左键按下")
                move = True
        if event.type == locals.MOUSEBUTTONUP:  # 抬起鼠标触发
            left, wheel, right = pygame.mouse.get_pressed()
            if left == 0:
                print(pygame.mouse.get_pos())
                print("鼠标左键抬起")
                move = False
            # if event.type == locals.KEYDOWN:
            #     if event.key == locals.K_b:
            #         super_boom()
    #更新背景位置信息
    #静态背景，无需更新
    #更新玩家位置信息
    if move:
        moveto_x, moveto_y = pygame.mouse.get_pos()
        x_len = moveto_x - play_x
        y_len = moveto_y - play_y
        s_len = math.sqrt(x_len ** 2 + y_len ** 2)
        times = s_len / play_speed
        if times > 1:
            x_speed = x_len / times
            y_speed = y_len / times
            play_x += x_speed
            play_y += y_speed
        else:
            play_x = moveto_x
            play_y = moveto_y
        #

        if player_move_img_index >= len(player_move_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
            player_move_img_index = 0
        player = player_move_img[player_move_img_index]
        if game_count % 10 == 0:  # 每多长时间显示一个爆炸图片
            player_move_img_index += 1
        #反向

    if not move:
        if player_stand_img_index >= len(player_stand_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
            player_stand_img_index = 0
        player = player_stand_img[player_stand_img_index]
        if game_count % 10 == 0:  # 每多长时间显示一个爆炸图片
            player_stand_img_index += 1
    #更新敌人位置信息

    #画背景
    surface.blit(background,(0,0))
    #画玩家
    surface.blit(player,(play_x,play_y))
 #   surface.blit(player,(play_x,play_y))
    #画敌人

    pygame.display.update()