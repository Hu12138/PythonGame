import pygame
from pygame.locals import *
import Vector2D
from Vector2D import *
from random import randint,choice
#全局变量
#SCREEN_SIZE = (640,480 )
SCREEN_SIZE = (1400,788 )#改
NEST_POSITION = (320,340)
ANT_COUNT = 5
NEST_SIZE = 50
game_count = 0#改

World_Tag = 0#改
Make_World_Tag = 1#改,该世界是否已经创建对象
Spider_Anger = 25#改
Spider_R_health = 0
R_Spider_death = 0
R_Make_Spider = 0

Red_Boss = 0
Red_Boss_Health = 7
Has_Red = 0

trans_door_img_index = 0#改
FeiBiaoSpeed = 80
feibiao_ant_spider = 0
feibiao_tag = 0
feibiao_att_tag = 0
feibiao_location = Vector2D(0,0)
feibiao_destination =Vector2D(0,0)
#end
class State(object):
    def __init__(self, name):
        self.name = name
    def do_actions(self):
        pass
    def check_conditions(self):
        pass
    def entry_actions(self):
        pass
    def exit_actions(self):
        pass

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self,state):
        '''这里的states[state.name]=state不怎么懂'''
        self.states[state.name] = state
    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
    def set_state(self,new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()

class World(object):
    def __init__(self):
        self.flag=[]
        self.entities = {}
        self.entity_id = 0
        if World_Tag == 1:
            self.background = pygame.image.load("../sources/image/background.png")  # 加载背景
        elif World_Tag == 2:
            self.background = pygame.image.load("../sources/image/场景/场景2.png")  # 加载背景
        elif World_Tag == 3:
            self.background = pygame.image.load("../sources/image/场景/场景5.png")  # 加载背景
        # elif World_Tag == 4:
        #     self.background = pygame.image.load("../sources/image/场景/场景5.png")  # 加载背景
        #self.background = pygame.image.load("../sources/image/background.png")  # 加载背景
        # self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        # self.background.fill((255,255,255))
        #pygame.draw.circle(self.background,(200,255,200),NEST_POSITION,int(NEST_SIZE))
    def add_entity(self,entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self,entity):
        #del self.entities[entity.id]
        self.flag.append(entity.id)
    def get(self,entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        #global entity
        for entity in self.flag:
            if entity in self.entities:
                del self.entities[entity]
        self.flag=[]
        for entity in self.entities.values():
            entity.process(time_passed_seconds)

    def render(self,surface):
        surface.blit(self.background,(0,0))
        #画传送门
        if World_Tag == 3:
            image = pygame.image.load("../sources/image/princess.png")
            surface.blit(image, (SCREEN_SIZE[0] - 220, 0))
        else:
            trans_door(surface)
        for entity in self.entities.values():
            entity.render(surface)
    def get_closest_entity(self,name,location,range = 1000):
        distance = range
        id = None
        for entity in self.entities.values():
            if entity.name == name:
                t_dis = location.get_distance_to(entity.location)
                if t_dis < range:
                    if t_dis < distance:
                        id = entity
                        distance = t_dis
        if id is None:
            return None
        else:
            return id
    def get_close_entity(self, name, location, range=100.):
        location = Vector2D(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity
        return None
    #将画图片编程函数
    def img_split(self):
        pass
class start():
    def __init__(self):
        self.surface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.pos = None
        if World_Tag == 0:
            self.img = pygame.image.load("../sources/image/start.png").convert_alpha()
        elif World_Tag == 4:
            self.img = pygame.image.load("../sources/image/success.png").convert_alpha()
        elif World_Tag == 5:
            self.img = pygame.image.load("../sources/image/gameover.png").convert_alpha()
    def process(self,time_passed):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                left,wheel,right = pygame.mouse.get_pressed()
                if left == 1:
                    #print("in get left mouse")
                    self.pos = pygame.mouse.get_pos()
                    if self.pos[0] > 5 and self.pos[0] < 170 and self.pos[1] > (SCREEN_SIZE[1]-76) and self.pos[1] < SCREEN_SIZE[1]:
                        global World_Tag
                        World_Tag = 1
                        global Make_World_Tag
                        Make_World_Tag = 0
    def render(self,screen):
        self.surface.blit(self.img,(0,0))

class GameEntity(object):

    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2D(0, 0)
        self.destination = Vector2D(0, 0)
        self.speed = 0.
        self.brain = StateMachine()
        self.id = 0


    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, time_passed):
        self.brain.think()
        if self.speed > 0. and self.location.x != self.destination.x and self.location.y != self.destination.y:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_magnitude()
            #print(distance_to_destination)
            #print(vec_to_destination)
            heading = vec_to_destination.normalize()
            #print(heading)
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            #travel_distance = distance_to_destination
            if self.location.x >= SCREEN_SIZE[0]:
                self.location.x = SCREEN_SIZE[0]
            if self.location.x <= 0:
                self.location.x = 0
            if self.location.y >= SCREEN_SIZE[1]:
                self.location.y = SCREEN_SIZE[1]
            if self.location.y <= 0:
                self.location.y = 0

            self.location += heading * travel_distance

class Ant(GameEntity):
    #改开始
    #怪兽1
    player_stand_img = []
    player_stand_img_index = 0
    player_stand_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_1.png"))
    player_stand_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_2.png"))
    player_stand_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_3.png"))
    player_stand_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_4.png"))
    player_stand_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_5.png"))
    #怪兽1反向
    player_standr_img = []
    player_standr_img_index = 0
    player_standr_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_1r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_2r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_3r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_4r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/怪兽/怪兽1_5r.png"))
    #怪兽2
    player_stand2_img = []
    player_stand2_img_index = 0
    player_stand2_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_1.png"))
    player_stand2_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_2.png"))
    player_stand2_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_3.png"))
    player_stand2_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_4.png"))
    # 怪兽2反向
    player_stand2r_img = []
    player_stand2r_img_index = 0
    player_stand2r_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_1r.png"))
    player_stand2r_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_2r.png"))
    player_stand2r_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_3r.png"))
    player_stand2r_img.append(pygame.image.load("../sources/image/怪兽/怪兽2_4r.png"))
    # 怪兽3
    player_stand3_img = []
    player_stand3_img_index = 0
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_1.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_2.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_3.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_4.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_5.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_6.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_7.png"))
    player_stand3_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_8.png"))
    # 怪兽3反向
    player_stand3r_img = []
    player_stand3r_img_index = 0
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_1r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_2r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_3r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_4r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_5r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_6r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_7r.png"))
    player_stand3r_img.append(pygame.image.load("../sources/image/怪兽/怪兽3_8r.png"))
    #改结束
    def __init__(self, world, image,num):
        GameEntity.__init__(self, world, "ant", image)
        exploring_state = AntStateExploring(self)
        self.which_enemy = num  #怪物1，2，3
        if self.which_enemy == 1:
            self.health = 2
        elif self.which_enemy == 2:
            self.health = 5
        elif self.which_enemy == 3:
            self.health = 25
        hunting_state = AntStateHunting(self)
        self.dead_image = pygame.transform.flip(image, 0, 1)#死亡特效，没有做
        self.brain.add_state(exploring_state)
        self.re_tag = 0 #re_tag 用来表示是不是可以远程攻击
        #self.brain.add_state(seeking_state)
        #self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)
        #self.carry_image = None

    #def carry(self, image):
        #self.carry_image = image

    '''def drop(self, surface):
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))
            self.carry_image = None'''
    def ant_bitten2(self):
        self.health -= 4
        if self.health <= 0:
            self.speed = 0.
    def ant_bitten(self):
        global feibiao_att_tag
        #print(feibiao_att_tag)
        if feibiao_att_tag == 0:
            self.health -= 1
        elif feibiao_att_tag == 1:
            self.health -= 2
            #global feibiao_att_tag
            feibiao_att_tag = 0
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image

    def render(self, surface):
        #GameEntity.render(self, surface)
        #改
        if self.destination.x-self.location.x > 0:
            if self.which_enemy == 1:
                if self.player_stand_img_index >= len(self.player_stand_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_stand_img_index = 0
                self.image = self.player_stand_img[self.player_stand_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_stand_img_index += 1
            elif self.which_enemy == 2:
                if self.player_stand2_img_index >= len(self.player_stand2_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_stand2_img_index = 0
                self.image = self.player_stand2_img[self.player_stand2_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_stand2_img_index += 1
            elif self.which_enemy == 3:
                if self.player_stand3_img_index >= len(self.player_stand3_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_stand3_img_index = 0
                self.image = self.player_stand3_img[self.player_stand3_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_stand3_img_index += 1
        else:
            if self.which_enemy == 1:
                if self.player_standr_img_index >= len(self.player_standr_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_standr_img_index = 0
                self.image = self.player_standr_img[self.player_standr_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_standr_img_index += 1
            elif self.which_enemy == 2:
                if self.player_stand2r_img_index >= len(self.player_stand2r_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_stand2r_img_index = 0
                self.image = self.player_stand2r_img[self.player_stand2r_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_stand2r_img_index += 1
            elif self.which_enemy == 3:
                if self.player_stand3r_img_index >= len(self.player_stand3r_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
                    self.player_stand3r_img_index = 0
                self.image = self.player_stand3r_img[self.player_stand3r_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 4 == 0:  # 每多长时间显示一个怪兽图片
                    self.player_stand3r_img_index += 1
        # 画血条
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h / 2
        if self.which_enemy == 1:
            surface.fill((255, 0, 0), (bar_x, bar_y, 20, 4))  # 红条
        elif self.which_enemy == 2:
            surface.fill((255, 0, 0), (bar_x, bar_y, 50, 4))  # 红条
        elif self.which_enemy == 3:
            surface.fill((255, 0, 0), (bar_x, bar_y, 250, 4))  # 红条
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health*10, 4))  # 绿条
class feiBiao(GameEntity):
    #增加飞镖1图片
    player_stand_img = []
    player_stand_img_index = 0
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-1.png"))
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-2.png"))
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-3.png"))
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-4.png"))
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-5.png"))
    player_stand_img.append(pygame.image.load("../sources/image/技能/1-6.png"))

    player_feibiao1_img = []
    player_feibiao1_img_index = 0
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-1.png"))
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-2.png"))
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-3.png"))
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-4.png"))
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-5.png"))
    player_feibiao1_img.append(pygame.image.load("../sources/image/技能/2-6.png"))
    #增加结束
    def __init__(self,world,image):
        GameEntity.__init__(self,world,"feibiao",image)
        #self.clock = pygame.time.Clock()
        self.world = world
        self.hunting_state = FeiBiaoStateHunting(self)
        #self.brain.add_state(self.hunting_state)
        self.count = 0
        self.speed = 500.
        self.feibiao_ant_spider = 0
        self.spider_id = None
        self.ant_id = None
        self.arrive = False  # 改
        self.bomm_over = False  # 改
        self.anger_tag = 0#改
        #self.spider
    def process(self, time_passed):
        #print("begin")
        #print(self.location)
        #print(self.destination)
        #if self.location == self.destination:
        #    self.world.remove_entity(self)
        #    print("feibiao 消失")
        #    return
        #self.brain.states[].do_actions()
        #self.brain.think()
        #ant = self.world.get_close_entity("ant", self.location, 15)
        if self.feibiao_ant_spider == 0:
            ant = self.world.get_close_entity("ant", self.location, 90)
            if ant is not None:
                self.ant_id = ant.id
                global Spider_Anger
                self.anger_tag = 1
            self.hunting_state.do_actions()
            #self.count +=  1
            #print(self.count)
            if self.location.x == self.destination.x and self.location.y == self.destination.y:
                self.arrive = True#改
                #print("到了 100")
                if self.bomm_over:#改
                    self.player_stand_img_index = 0
                    self.world.remove_entity(self)
                #self.world.remove_entity(self)
                #print("feibiao 消失")
                return
            else:
                GameEntity.process(self,time_passed)
        elif self.feibiao_ant_spider == 1:
            spider = self.world.get_close_entity("spider",self.location,90)
            if spider is not None:
                self.spider_id = spider.id
            self.hunting_state.do_actions()
            #self.count += 1
            if self.location.x == self.destination.x and self.location.y == self.destination.y:
                #print("到了 100")
                self.world.remove_entity(self)
                #print("feibiao 消失")
                return
            else:
                GameEntity.process(self,time_passed)
    #增加render方法
    def render(self, surface):
        if not self.arrive :
            GameEntity.render(self, surface)
        else:
            if feibiao_att_tag == 0:
                if self.player_stand_img_index >= len(self.player_stand_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                    self.player_stand_img_index = len(self.player_stand_img) - 1
                    self.bomm_over = True
                    global Spider_Anger
                    if self.anger_tag == 1:
                        if Spider_Anger<25:
                            Spider_Anger += 1
                        self.anger_tag = 0
                    elif self.anger_tag == 0:
                        if Spider_Anger > 0:
                            Spider_Anger -= 1

                else:
                    self.image = self.player_stand_img[self.player_stand_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 2 == 0:  # 每多长时间显示一个爆炸图片
                    self.player_stand_img_index += 1
            else:
                if self.player_feibiao1_img_index >= len(self.player_feibiao1_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                    self.player_feibiao1_img_index = len(self.player_feibiao1_img) - 1
                    self.bomm_over = True
                else:
                    self.image = self.player_feibiao1_img[self.player_feibiao1_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 2 == 0:  # 每多长时间显示一个爆炸图片
                    self.player_feibiao1_img_index += 1

    #增加结束
class Spider(GameEntity):
    #增加
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
    #角色静止反向
    player_standr_img = []
    player_standr_img_index = 0
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand1r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand2r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand3r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand4r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand5r.png"))
    player_standr_img.append(pygame.image.load("../sources/image/站立/stand6r.png"))
    # 角色奔跑
    player_move_img = []
    player_move_img_index = 0
    player_move_img.append(pygame.image.load("../sources/image/移动/player_move1.png"))
    player_move_img.append(pygame.image.load("../sources/image/移动/player_move2.png"))
    player_move_img.append(pygame.image.load("../sources/image/移动/player_move3.png"))
    player_move_img.append(pygame.image.load("../sources/image/移动/player_move4.png"))
    player_move_img.append(pygame.image.load("../sources/image/移动/player_move5.png"))
    #角色奔跑反向
    player_mover_img = []
    player_mover_img_index = 0
    player_mover_img.append(pygame.image.load("../sources/image/移动/player_move1r.png"))
    player_mover_img.append(pygame.image.load("../sources/image/移动/player_move2r.png"))
    player_mover_img.append(pygame.image.load("../sources/image/移动/player_move3r.png"))
    player_mover_img.append(pygame.image.load("../sources/image/移动/player_move4r.png"))
    player_mover_img.append(pygame.image.load("../sources/image/移动/player_move5r.png"))
    # 角色释放技能
    player_skill_img = []
    player_skill_img_index = 0
    player_skill_img.append(pygame.image.load("../sources/image/放技能/skill1.png"))
    player_skill_img.append(pygame.image.load("../sources/image/放技能/skill2.png"))
    player_skill_img.append(pygame.image.load("../sources/image/放技能/skill3.png"))
    player_skill_img.append(pygame.image.load("../sources/image/放技能/skill4.png"))
    #角色释放技能反向
    player_skillr_img = []
    player_skillr_img_index = 0
    player_skillr_img.append(pygame.image.load("../sources/image/放技能/skill1r.png"))
    player_skillr_img.append(pygame.image.load("../sources/image/放技能/skill2r.png"))
    player_skillr_img.append(pygame.image.load("../sources/image/放技能/skill3r.png"))
    player_skillr_img.append(pygame.image.load("../sources/image/放技能/skill4r.png"))
    #角色近身攻击
    player_attack_img = []
    player_attack_img_index = 0
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou1.png"))
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou2.png"))
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou3.png"))
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou4.png"))
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou5.png"))
    player_attack_img.append(pygame.image.load("../sources/image/近身攻击/bodou6.png"))
    #角色近身攻击反向
    player_attackr_img = []
    player_attackr_img_index = 0
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou1r.png"))
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou2r.png"))
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou3r.png"))
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou4r.png"))
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou5r.png"))
    player_attackr_img.append(pygame.image.load("../sources/image/近身攻击/bodou6r.png"))
    #结束
    def __init__(self,world,image):
        GameEntity.__init__(self,world,"spider",image)
        self.Is_R = 0
        self.health = 100
        self.speed = 50.
        self.speed_ord = 50
        self.world = world
        self.speed_tag = 1
        self.speed_count = 0
        self.hunting_state = SpiderStateHunting(self)
        self.ant_id = None
        self.attak_count = 0
        self.att_tag = 0
        self.q_tag = 0
        self.q_count = 20
        self.e_tag = 70
        self.q_down = False  # 改
       #self.e_down = False  # 改
        #self.e_over = False  #
        self.e_ren_tag = 0
        self.reverse = False # 改 是否反向
        #()
    def bitten(self):
        self.health -= 1
        global Make_World_Tag
        global World_Tag
        if self.health == 0:
            Make_World_Tag = 0
            World_Tag = 5
    def spider_attack(self):
        ant = self.world.get_close_entity("ant", self.location, 200)
        if ant is not None:
            print("find ant")
            self.ant_id = ant.id
        self.hunting_state.do_actions()
        self.hunting_state = None
        self.hunting_state = SpiderStateHunting(self)
        self.ant = None
    def render(self, surface):
        self.surface = surface
        #GameEntity.render(self,surface)#原来
        #技能释放顺序有问题，应该为先抬手后释放
        if self.q_down :#k键动作完毕归零
            if pygame.mouse.get_pos()[0]-self.location.x>0:
                if self.player_skill_img_index >= len(self.player_skill_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                    self.player_skill_img_index = 0
                    self.q_down = False
                else:
                    self.image = self.player_skill_img[self.player_skill_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 2 == 0:  # 每多长时间显示一个释放技能动作
                    self.player_skill_img_index += 1
            else:
                #print("这里反向")
                if self.player_skillr_img_index >= len(self.player_skillr_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                    self.player_skillr_img_index = 0
                    self.q_down = False
                else:
                    self.image = self.player_skillr_img[self.player_skillr_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 2 == 0:  # 每多长时间显示一个爆炸图片
                    #print("in game_count")
                    self.player_skillr_img_index += 1
        elif self.e_ren_tag == 1:
            if game_count % 1 == 0:
                if not self.reverse:
                    if self.player_attack_img_index >= len(self.player_attack_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                        self.player_attack_img_index = 0
                        self.e_ren_tag = 0
                    else:
                        self.image = self.player_attack_img[self.player_attack_img_index]
                        #print(self.player_attack_img_index)
                        x, y = self.location
                        w, h = self.image.get_size()
                        surface.blit(self.image, (x - w / 2, y - h / 2))
                        self.player_attack_img_index = self.player_attack_img_index + 1
                    # if game_count % 10 == 0:  # 每多长时间显示一个爆炸图片
                else:
                    # print("这里反向")
                    if self.player_attackr_img_index >= len(self.player_attackr_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                        self.player_attackr_img_index = 0
                        self.e_ren_tag = 0
                    else:
                        self.e_down = True
                        self.image = self.player_attackr_img[self.player_attackr_img_index]
                        x, y = self.location
                        w, h = self.image.get_size()
                        surface.blit(self.image, (x - w / 2, y - h / 2))
                        self.player_attackr_img_index = self.player_attackr_img_index +1
        elif not self.q_down and not self.e_ren_tag and not self.static:
            if not self.reverse:
                if self.player_move_img_index >= len(self.player_move_img):  # 检查下表越界，如果等于移动图片数组大小，爆炸完毕，敌机死亡
                    self.player_move_img_index = 0
                self.image = self.player_move_img[self.player_move_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 10 == 0:  # 每多长时间显示一个移动图片
                    self.player_move_img_index += 1
            else:
                if self.player_mover_img_index >= len(self.player_mover_img):  # 检查下表越界，如果等于移动图片数组大小，爆炸完毕，敌机死亡
                    self.player_mover_img_index = 0
                self.image = self.player_mover_img[self.player_mover_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 10 == 0:  # 每多长时间显示一个移动图片
                    self.player_mover_img_index += 1
        elif self.static and not self.q_down and not self.e_ren_tag:
            # print("相等")
            #print(self.destination.x,self.location.x)
            if not self.reverse:
                if self.player_stand_img_index >= len(self.player_stand_img):  # 检查下表越界，如果等于站立图片数组大小，爆炸完毕，敌机死亡
                    self.player_stand_img_index = 0
                self.image = self.player_stand_img[self.player_stand_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 10 == 0:  # 每多长时间显示一个站立图片
                    self.player_stand_img_index += 1
            else:
                if self.player_standr_img_index >= len(self.player_standr_img):  # 检查下表越界，如果等于站立图片数组大小，爆炸完毕，敌机死亡
                    self.player_standr_img_index = 0
                self.image = self.player_standr_img[self.player_standr_img_index]
                x, y = self.location
                w, h = self.image.get_size()
                surface.blit(self.image, (x - w / 2, y - h / 2))
                if game_count % 10 == 0:  # 每多长时间显示一个站立图片
                    self.player_standr_img_index += 1

        #画血条
        x,y = self.location
        w,h = self.image.get_size()
        bar_x = x - 12
        bar_y = y +h/2
        bar_yr = bar_y + 6
        #红条
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        #绿条
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))
        #怒气蓝条
        surface.fill((0, 255, 255), (bar_x, bar_yr, 25, 4))
        surface.fill((255, 165, 0), (bar_x, bar_yr, Spider_Anger, 4))#橙色
    def make_feibiao(self,dest):
        #ew_feibaio = feiBiao(self.world,feibiao_image)

        #world.add_entity(new_feibaio)
        global feibiao_tag
        feibiao_tag = 1
        global feibiao_location
        feibiao_location= self.location
        global feibiao_destination
        feibiao_destination = dest
    def process(self, time_passed):
        x,y = self.location
        for event in pygame.event.get():
            #print("in spider")
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                left,wheel,right = pygame.mouse.get_pressed()
                #print("in get mouse")
                if left == 1:
                    #print("in get left mouse")
                    self.destination = pygame.mouse.get_pos()
                    self.destination = Vector2D(self.destination[0], self.destination[1])
                    if self.destination.x-self.location.x < 0:
                        self.reverse = True
                    else:
                        self.reverse = False
                    #print(self.destination)
            #pressed_keys = pygame.key.get_pressed()
            if event.type == KEYDOWN :
                #print("down")
                #print(pressed_keys[K_q])
                #self.K_q = pressed_keys[K_q]
                global feibiao_att_tag
                if  event.key == K_q and self.q_count >= 10:
                    self.q_down = True
                    self.q_count = 0
                    #print("q")
                #elif event.type == KEYUP :
                #print("up")
                #if self.K_q:
                   # print("q")
                    destination = pygame.mouse.get_pos()
                    destination = Vector2D(destination[0], destination[1])
                    self.make_feibiao(destination)
                    if self.att_tag >= 100:
                        feibiao_att_tag = 0
                        self.att_tag = 0
                    #feibiao_att_tag = 0
                    #i = 0
                    #while i<5000:
                    #    i+=1
                    #self.make_feibiao(destination)
                #global feibiao_att_tag
                #else:
                    #self.q_down = False
                if event.key == K_w:
                    if self.speed_tag == 1:
                        feibiao_att_tag = 1
                        self.speed = self.speed * 4
                        self.speed_tag = 0
                if event.key == K_e:
                    #print(self.e_tag)
                    if self.e_tag >= 70:
                        print("in e")
                        self.e_ren_tag = 1
                        self.spider_attack()
                        self.e_tag = 0
                if event.key == K_r:
                    if Spider_Anger >= 13:
                        global R_Make_Spider
                        R_Make_Spider = 1

                if event.key == K_b:
                    global World_Tag
                    global Make_World_Tag
                    if self.location.x > (SCREEN_SIZE[0] - 220) and self.location.x < SCREEN_SIZE[0] and self.location.y > 0 and self.location.y < 220:
                        if  World_Tag < 5:
                            World_Tag += 1
                            Make_World_Tag = 0
                        else:
                            World_Tag = 4
                        #World_Tag = 2
                #else:
                #    self.e_down = False
        #原逻辑
        # if  self.location != self.destination:
        #     vec_to_destination = self.destination - self.location
        #     distance_to_destination = vec_to_destination.get_magnitude()
        #     # print(distance_to_destination)
        #     # print(vec_to_destination)
        #     heading = vec_to_destination.normalize()
        #     # print(heading)
        #     travel_distance = min(distance_to_destination, time_passed * self.speed)
        #     # travel_distance = distance_to_destination
        #     self.location += heading * travel_distance

        # 重写此部分逻辑
        if self.location.x == self.destination.x and self.location.y == self.destination.y:
            self.static = True
            self.reverse = False
        else:
            self.static = False
            # self.static = False
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_magnitude()
            # print(distance_to_destination)
            # print(vec_to_destination)
            heading = vec_to_destination.normalize()
            # print(heading)
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            # travel_distance = distance_to_destination
            self.location += heading * travel_distance
        #结束

        if self.speed_tag == 0 and self.speed_count < 70:
            self.speed_count +=1
            #print("in more speed")
        elif self.speed_count >=70:
            #print(self.speed_count)
            #print("in cold")
            self.speed = self.speed_ord
            self.speed_count += 1
            if self.speed_count >= 140:
                #print(self.speed_count)
                self.speed_count = 0
                self.speed_tag = 1
        if feibiao_att_tag == 1:
            self.att_tag += 1
        if self.e_tag <= 70:
            self.e_tag += 1
        if self.q_count <= 10:
            self.q_count += 1
class RSpider(Spider):
    def __init__(self, world, image):
        Spider.__init__(self, world, image)
        self.Is_R = 1
        spider_r_exploring_state = RSpiderStateExploring(self)
        #self.brain = StateMachineR()
        self.brain.add_state(spider_r_exploring_state)
        spider_r_hunting_state = RSpiderStateHunting(self)
        self.brain.add_state(spider_r_hunting_state)
        #self.brain.set_state(spider_r_exploring_state)
        self.ratt_tag = 0
    def bitten(self):
        self.health -= 1

    def render(self, surface):
        self.surface = surface
        if self.ratt_tag == 0:
            if not self.static:
                if not self.reverse:
                    if self.player_move_img_index >= len(self.player_move_img):  # 检查下表越界，如果等于移动图片数组大小，爆炸完毕，敌机死亡
                        self.player_move_img_index = 0
                    self.image = self.player_move_img[self.player_move_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                    if game_count % 10 == 0:  # 每多长时间显示一个移动图片
                        self.player_move_img_index += 1
                else:
                    if self.player_mover_img_index >= len(self.player_mover_img):  # 检查下表越界，如果等于移动图片数组大小，爆炸完毕，敌机死亡
                        self.player_mover_img_index = 0
                    self.image = self.player_mover_img[self.player_mover_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                    if game_count % 10 == 0:  # 每多长时间显示一个移动图片
                        self.player_mover_img_index += 1
            if self.static:
                if not self.reverse:
                    if self.player_stand_img_index >= len(self.player_stand_img):  # 检查下表越界，如果等于站立图片数组大小，爆炸完毕，敌机死亡
                        self.player_stand_img_index = 0
                    self.image = self.player_stand_img[self.player_stand_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                    if game_count % 10 == 0:  # 每多长时间显示一个站立图片
                        self.player_stand_img_index += 1
                else:
                    if self.player_standr_img_index >= len(self.player_standr_img):  # 检查下表越界，如果等于站立图片数组大小，爆炸完毕，敌机死亡
                        self.player_standr_img_index = 0
                    self.image = self.player_standr_img[self.player_standr_img_index]
                    x, y = self.location
                    w, h = self.image.get_size()
                    surface.blit(self.image, (x - w / 2, y - h / 2))
                    if game_count % 10 == 0:  # 每多长时间显示一个站立图片
                        self.player_standr_img_index += 1
        elif self.ratt_tag == 1:
            if game_count % 1 == 0:
                if not self.reverse:
                    if self.player_attack_img_index >= len(self.player_attack_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                        self.player_attack_img_index = 0
                        self.e_ren_tag = 0
                    else:
                        self.image = self.player_attack_img[self.player_attack_img_index]
                        #print(self.player_attack_img_index)
                        x, y = self.location
                        w, h = self.image.get_size()
                        surface.blit(self.image, (x - w / 2, y - h / 2))
                        self.player_attack_img_index = self.player_attack_img_index + 1
                    # if game_count % 10 == 0:  # 每多长时间显示一个爆炸图片
                else:
                    # print("这里反向")
                    if self.player_attackr_img_index >= len(self.player_attackr_img):  # 检查下表越界，如果等于爆炸图片数组大小，爆炸完毕，敌机死亡
                        self.player_attackr_img_index = 0
                        self.e_ren_tag = 0
                    else:
                        self.e_down = True
                        self.image = self.player_attackr_img[self.player_attackr_img_index]
                        x, y = self.location
                        w, h = self.image.get_size()
                        surface.blit(self.image, (x - w / 2, y - h / 2))
                        self.player_attackr_img_index = self.player_attackr_img_index + 1
            self.ratt_tag = 0
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h / 2
        # 红条
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        # 绿条
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))
    def process(self, time_passed):
        #print("in process")
        #print(self.brain.states)
        self.brain.think()
        if self.speed > 0. and self.location.x != self.destination.x and self.location.y != self.destination.y:
            self.static = False
            if self.destination.x - self.location.x > 0:
                self.reverse = False
            else:
                self.reverse = True
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_magnitude()
            #print(distance_to_destination)
            #print(vec_to_destination)
            heading = vec_to_destination.normalize()
            #print(heading)
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            #travel_distance = distance_to_destination
            if self.location.x >= SCREEN_SIZE[0]:
                self.location.x = SCREEN_SIZE[0]
            if self.location.x <= 0:
                self.location.x = 0
            if self.location.y >= SCREEN_SIZE[1]:
                self.location.y = SCREEN_SIZE[1]
            if self.location.y <= 0:
                self.location.y = 0
            self.location += heading * travel_distance

class AntStateExploring(State):
    def __init__(self,ant):
        State.__init__(self, "exploring")
        self.ant = ant
        self.desti = None
    def random_destination(self):
        w = 20
        h = 20
        tag = 0

        #desti = Vector2D(randint(-w ,w),randint(-h,h))
        if randint(1,20) == 1:
            self.desti = Vector2D(randint(-w, w), randint(-h, h))
        #self.ant.destination = self.ant.location
        if self.desti is not None:
            self.ant.destination = self.ant.location + self.desti
        else:
            self.ant.destination = self.ant.location
        #print("ant's destination: " ,end ='')
        #print(self.ant.destination)
    def do_actions(self):
        if randint(1,20):
            self.random_destination()
    def check_conditions(self):
        if self.ant.re_tag == 1:
            spider = self.ant.world.get_close_entity("spider", self.ant.location, 1000)
        else:
            spider = self.ant.world.get_close_entity("spider", self.ant.location, 500)
        if spider is not None:
            self.ant.spider_id = spider.id
            return "hunting"
    def entry_actions(self):
        self.random_destination()
class RSpiderStateExploring(State):
    def __init__(self, spider):
        State.__init__(self, "r_exploring")
        self.spider = spider
        self.desti = None
    def random_destination(self):
        w = 20
        h = 20
        tag = 0

        #desti = Vector2D(randint(-w ,w),randint(-h,h))
        if randint(1, 20) == 1:
            self.desti = Vector2D(randint(-w, w), randint(-h, h))
        #self.ant.destination = self.ant.location
        if self.desti is not None:
            self.spider.destination = self.spider.location + self.desti
        else:
            self.spider.destination = self.spider.location
        #print("ant's destination: " ,end ='')
        #print(self.ant.destination)
    def do_actions(self):
        #print("in exploring")
        if randint(1, 10):
            self.random_destination()
    def check_conditions(self):
        ant = self.spider.world.get_closest_entity("ant", self.spider.location, 760)
        #print(ant.id)
        if ant is not None:
            self.spider.destination = ant.location
            self.spider.ant_id = ant.id
            return "r_hunting"
    def entry_actions(self):
        self.spider.speed = 300
        self.random_destination()

class FeiBiaoStateHunting(State):
    def __init__(self, feibiao):
        State.__init__(self, "hunting")
        self.feibiao = feibiao
        self.got_kill = False
        self.tag = 1
        self.re_tag = 1

    def do_actions(self):
        #print("feibiao doacthions")
        if self.feibiao.feibiao_ant_spider == 0:
            ant = self.feibiao.world.get(self.feibiao.ant_id)
            if ant is None:
                #print("ant is None")
                return
            #self.ant.destination = spider.location
            if self.feibiao.location.get_distance_to(ant.location) < 90.:
                if self.tag == 1:
                    ant.ant_bitten()
                    self.tag = 0
                    if ant.which_enemy == 3:
                        if ant.health <= Red_Boss_Health and Has_Red == 0:
                            global Red_Boss
                            Red_Boss = 1
                    if ant.health <= 0:
                        self.feibiao.world.remove_entity(ant)
                        self.got_kill = True
                        return
        elif self.feibiao.feibiao_ant_spider == 1:
            spider = self.feibiao.world.get(self.feibiao.spider_id)
            if spider is None:
                return
            if self.feibiao.location.get_distance_to(spider.location) < 90:
                if self.re_tag == 1:
                    spider.bitten()
                    self.re_tag = 0
                    if spider.health <= 0:
                        if spider.Is_R == 1:
                            self.spider.world.remove_entity(spider)
                        self.got_kill = True
                        return
class SpiderStateHunting(State):
    def __init__(self, spider):
        State.__init__(self, "hunting")
        self.spider = spider
        self.got_kill = False
        self.tag = 1

    def do_actions(self):
        #print("feibiao doacthions")
        ant = self.spider.world.get(self.spider.ant_id)
        if ant is None:
            print("ant is None")
            return
        #self.ant.destination = spider.location
        if self.spider.location.get_distance_to(ant.location) < 200.:
            if self.tag == 1:
                ant.ant_bitten2()
                self.tag = 0
                if ant.which_enemy == 3:

                    if ant.health <= Red_Boss_Health and Has_Red == 0:
                        global Red_Boss
                        Red_Boss = 1
                if ant.health <= 0:
                    self.spider.world.remove_entity(ant)
                    self.got_kill = True
                    return
class RSpiderStateHunting(State):
    def __init__(self, spider):
        State.__init__(self, "r_hunting")
        self.spider = spider
        self.got_kill = False
    def do_actions(self):
        ant = self.spider.world.get(self.spider.ant_id)
        if ant is None:
            return
        self.spider.destination = ant.location
        if self.spider.location.get_distance_to(ant.location) < 20.:
            if randint(1, 25) == 1:
                self.spider.ratt_tag = 1
                ant.ant_bitten2()
                if ant.which_enemy == 3:
                    if ant.health <= Red_Boss_Health and Has_Red == 0:
                        global Red_Boss
                        Red_Boss = 1
                if ant.health <= 0:
                    self.spider.world.remove_entity(ant)
                    self.got_kill = True
    def check_conditions(self):
        if self.got_kill:
            return "r_exploring"
        ant = self.spider.world.get(self.spider.ant_id)
        if ant is None:
            return "r_exploring"
        if ant.location.get_distance_to(self.spider.location) > NEST_SIZE * 3:
            return "r_exploring"
        return None
class AntStateHunting(State):
    def __init__(self,ant):
        State.__init__(self,"hunting")
        self.ant = ant
        self.got_kill = False
        #self.location = self.ant.location
    def make_feibiao(self,dest):
        #ew_feibaio = feiBiao(self.world,feibiao_image)

        #world.add_entity(new_feibaio)
        location = self.ant.location
        global feibiao_ant_spider
        feibiao_ant_spider = 1
        global feibiao_tag
        feibiao_tag = 1
        global feibiao_location
        feibiao_location= location
        global feibiao_destination
        feibiao_destination = dest
    def do_actions(self):
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return

        self.ant.destination = spider.location
        if self.ant.re_tag == 1:
            if self.ant.location.get_distance_to(spider.location) < 2000.:
                if randint(1, FeiBiaoSpeed) == 1:
                    #spider.bitten()
                    self.make_feibiao(spider.location)
                    if spider.health <= 0:
                        if spider.Is_R == 1:
                            self.ant.world.remove_entity(spider)
                        self.get_kill = True
        elif self.ant.re_tag == 0:
            if self.ant.location.get_distance_to(spider.location) < 15.:
                if randint(1,5) == 1:
                    spider.bitten()
                    if spider.health <= 0:
                        if spider.Is_R == 1:
                            self.ant.world.remove_entity(spider)
                        self.get_kill = True

    def check_conditions(self):
        if self.got_kill:
            return "over"
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return "exploring"
        return None
    def entry_actions(self):
        self.speed = 0 + randint(0,10)
    def exit_actions(self):
        self.get_kill =False



def trans_door(surface):
    trans_door_img = []
    global trans_door_img_index
    #trans_door_img_index = 0
    trans_door_img.append(pygame.image.load("../sources/image/传送门/1-1.png"))
    trans_door_img.append(pygame.image.load("../sources/image/传送门/1-2.png"))
    trans_door_img.append(pygame.image.load("../sources/image/传送门/1-3.png"))
    trans_door_img.append(pygame.image.load("../sources/image/传送门/1-4.png"))
    trans_door_img.append(pygame.image.load("../sources/image/传送门/1-5.png"))

    if trans_door_img_index >= len(trans_door_img):  # 检查下表越界，如果等于爆炸图片数组大小，怪兽一套完毕，敌机死亡
        trans_door_img_index = 0
    image = trans_door_img[trans_door_img_index]
    #x, y = self.location
    #w, h = image.get_size()
    #surface.blit(image, (x - w / 2, y - h / 2))
    surface.blit(image, (SCREEN_SIZE[0]-220,0 ))
    if game_count % 10 == 0:  # 每多长时间显示一个怪兽图片
        trans_door_img_index += 1

def make_Enemy(world,ant_image,num,x,y,speed,has_feibiao):
    ant = Ant(world, ant_image, num)  # 最后一个为类型
    ant.speed = speed
    ant.re_tag = has_feibiao
    ant.location = Vector2D(x, y)
    ant.brain.set_state("exploring")
    #ant.health = 5
    world.add_entity(ant)
    return ant


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("勇士救公主")  # 改
    world = start()
    #创建蜘蛛
    spider_image = pygame.image.load("../sources/image/站立/stand1.png").convert_alpha()
    #spider = Spider(world, spider_image)
    spider = None
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    while True:
        global World_Tag
        global Make_World_Tag
        global FeiBiaoSpeed
        if Make_World_Tag == 0:
            if World_Tag == 1:
                world = World()
                spider = Spider(world, spider_image)
                # ==============
                '''蚂蚁图片'''
                ant_image = pygame.image.load("../sources/image/怪兽/怪兽1_1.png").convert_alpha()
                '''蜘蛛图片'''
                #spider_image = pygame.image.load("../sources/image/站立/stand1.png").convert_alpha()
                #make_Enemy(world, ant_image, num, x, y, speed, has_feibiao)
                make_Enemy(world, ant_image, 1, (SCREEN_SIZE[0] - 220 - 120), 100, 0, 1)
                make_Enemy(world, ant_image, 1, (SCREEN_SIZE[0] - 220), 220, 0, 1)
                make_Enemy(world, ant_image, 1, SCREEN_SIZE[0]/2-100, 200, 50, 0)
                make_Enemy(world, ant_image, 1, SCREEN_SIZE[0]/2-100, 350, 50, 0)
                make_Enemy(world, ant_image, 1, SCREEN_SIZE[0]/2-100, 500, 50, 0)
                # 不发飞镖怪兽
                '''for ant_no in range(ANT_COUNT):
                    ant = Ant(world, ant_image, 1)  # 最后一个为类型
                    ant.location = Vector2D(randint(0, w), randint(0, h))
                    ant.brain.set_state("exploring")
                    world.add_entity(ant)'''
                # 发飞镖怪物
                '''for ant_no in range(5):
                    ant = Ant(world, ant_image)
                    ant.re_tag = 1
                    ant.health = 1
                    ant.location = Vector2D(randint(0, w), randint(0, h))
                    ant.brain.set_state("exploring")
                    world.add_entity(ant)'''
                #spider = Spider(world, spider_image)
                spider.location = Vector2D(200, 300)
                spider.destination = Vector2D(200., 300.)
                world.add_entity(spider)
                # 基础子弹
                '''飞镖图片'''
                feibiao_image = "../sources/image/技能/1-1.png"
                feibiao_image = pygame.image.load(feibiao_image).convert_alpha()
                # 另一种子弹 未替换
                leaf_image = "../sources/image/技能/2-1.png"
                feibiao_image1 = pygame.image.load(leaf_image).convert_alpha()
                # 怪兽飞镖
                feibiao_image2 = pygame.image.load("../sources/image/技能/3.png").convert_alpha()
                Make_World_Tag = 1#世界创建好
            elif World_Tag == 2:
                world = World()
                FeiBiaoSpeed = 50
                # 添加对象
                # ==============
                '''蚂蚁图片'''
                ant_image = pygame.image.load("../sources/image/怪兽/怪兽1_1.png").convert_alpha()
                '''蜘蛛图片'''
                #spider_image = pygame.image.load("../sources/image/站立/stand1.png").convert_alpha()
                make_Enemy(world, ant_image, 2, (SCREEN_SIZE[0] - 220 - 120), 100, 0, 1)
                make_Enemy(world, ant_image, 2, (SCREEN_SIZE[0] - 220), 220, 0, 1)
                make_Enemy(world, ant_image, 2, SCREEN_SIZE[0] / 2 - 100, 200, 50, 0)
                make_Enemy(world, ant_image, 2, SCREEN_SIZE[0] / 2 - 100, 350, 50, 0)
                make_Enemy(world, ant_image, 2, SCREEN_SIZE[0] / 2 - 100, 500, 50, 0)
                #spider = Spider(world, spider_image)
                spider.location = Vector2D(200, 300)
                spider.destination = Vector2D(200., 300.)

                '''这里必须将world重新改变，放弃旧世界，QAQ'''
                spider.world = world
                world.add_entity(spider)
                # 基础子弹
                '''飞镖图片'''
                feibiao_image = "../sources/image/技能/1-1.png"
                feibiao_image = pygame.image.load(feibiao_image).convert_alpha()
                # 另一种子弹 未替换
                leaf_image = "../sources/image/技能/2-1.png"
                feibiao_image1 = pygame.image.load(leaf_image).convert_alpha()
                # 怪兽飞镖
                feibiao_image2 = pygame.image.load("../sources/image/技能/3.png").convert_alpha()
                # world = start()
                Make_World_Tag = 1  # 世界创建好
            elif World_Tag == 3:
                world = World()
                FeiBiaoSpeed = 20
                # 添加对象
                '''蚂蚁图片'''
                ant_image = pygame.image.load("../sources/image/怪兽/怪兽1_1.png").convert_alpha()
                '''蜘蛛图片'''
                #spider_image = pygame.image.load("../sources/image/站立/stand1.png").convert_alpha()
                ant = make_Enemy(world, ant_image, 3, 1100, 220, 100, 1)
                # make_Enemy(world, ant_image, 3, (SCREEN_SIZE[0] - 220), 220, 0, 1)
                # make_Enemy(world, ant_image, 3, (SCREEN_SIZE[0] - 220 - 240), 0, 0, 0)
                # make_Enemy(world, ant_image, 3, (SCREEN_SIZE[0] - 220 - 240), 220, 0, 0)
                # make_Enemy(world, ant_image, 3, (SCREEN_SIZE[0] - 220), 220 + 120, 0, 0)
                #spider = Spider(world, spider_image)
                spider.location = Vector2D(200, 300)
                spider.destination = Vector2D(200., 300.)
                spider.world = world
                world.add_entity(spider)
                # 基础子弹
                '''飞镖图片'''
                feibiao_image = "../sources/image/技能/1-1.png"
                feibiao_image = pygame.image.load(feibiao_image).convert_alpha()
                # 另一种子弹 未替换
                leaf_image = "../sources/image/技能/2-1.png"
                feibiao_image1 = pygame.image.load(leaf_image).convert_alpha()
                # 怪兽飞镖
                feibiao_image2 = pygame.image.load("../sources/image/技能/3.png").convert_alpha()
                Make_World_Tag = 1  # 世界创建好
            elif World_Tag == 4:#游戏成功，结束
                world = start()
                # 添加对象
                Make_World_Tag = 1  # 世界创建好
            elif World_Tag == 5:#游戏失败，重新开始
                world = start()
                # 添加对象
                Make_World_Tag = 1  # 世界创建好
        global game_count
        game_count += 1
        if game_count == 1000000:
            game_count = 0
        time_passed = clock.tick(30)
        if World_Tag < 4 and World_Tag > 0:
            global R_Make_Spider
            global Spider_Anger
            if R_Make_Spider == 1:
                r_spider = RSpider(world, spider_image)
                pos = pygame.mouse.get_pos()
                r_spider.location = Vector2D(pos[0], pos[1])
                r_spider.destination = r_spider.location
                r_spider.health = Spider_Anger
                r_spider.brain.set_state("r_exploring")
                world.add_entity(r_spider)
                R_Make_Spider = 0
                Spider_Anger = 0

            global Red_Boss
            global Has_Red
            if Red_Boss == 1:
                ant_image = pygame.image.load("../sources/image/怪兽/怪兽1_1.png").convert_alpha()
                ant = make_Enemy(world, ant_image, 1, randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]), 30, 1)

                ant_image = pygame.image.load("../sources/image/怪兽/怪兽2_1.png").convert_alpha()
                ant = make_Enemy(world, ant_image, 2, randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]), 100, 0)

                Has_Red = 1
                Red_Boss = 0

            global feibiao_tag
            global feibiao_ant_spider
            if feibiao_tag == 1:
                if feibiao_ant_spider == 1:
                    # new_feibiao = feiBiao(world, feibiao_image)
                    # 此处怪兽飞镖
                    new_feibiao = feiBiao(world, feibiao_image2)
                    new_feibiao.location = feibiao_location
                    new_feibiao.destination = feibiao_destination
                    new_feibiao.feibiao_ant_spider = 1
                    feibiao_ant_spider = 0
                elif feibiao_ant_spider == 0:
                    if feibiao_att_tag == 1:
                        new_feibiao = feiBiao(world, feibiao_image1)
                    elif feibiao_att_tag == 0:
                        new_feibiao = feiBiao(world, feibiao_image)
                    new_feibiao.location = feibiao_location
                    new_feibiao.destination = feibiao_destination
                    # global feibiao_ant_spider
                    if feibiao_ant_spider == 1:
                        new_feibiao.feibiao_ant_spider = 1
                        feibiao_ant_spider = 0
                world.add_entity(new_feibiao)
                feibiao_tag = 0


        world.process(time_passed)
        world.render(screen)
        pygame.display.update()#画图

if __name__ == "__main__":
    run()