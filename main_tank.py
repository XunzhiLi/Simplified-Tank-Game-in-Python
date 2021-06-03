#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/15 15:38
# @Author  : Ryu
# @Site    : 
# @File    : main_tank.py
# @Software: PyCharm
'''
1.坦克(我方，敌方）
2.墙壁
3.子弹
4.爆炸效果
5.音效
6.主类
'''
#pygame的官方网站是  www.pygame.org

import pygame
import time
import random
from pygame.sprite import Sprite
SCREEN_WIDTH=750
SCREEN_HEIGHT=500
BG_COLOR=pygame.Color(0,0,0)
Font1_Color=pygame.Color(255,0,0)

#定义一个基类
class BaseItem(Sprite):
     def __init__(self,color,width,height):
         pygame.sprite.Sprite.__init__(self)
class Maingame():
    window=None
    my_tank=None
    #创建存储敌方坦克的列表
    EnemyTankList = []
    #定义敌方坦克的数量
    EnemyTankCount = 5
    #存储我方子弹的列表
    myBulletList = []
    #存储敌方子弹的列表
    enemyBulletList = []
    #存储爆炸效果的列表
    explodeList = []
    #存储墙壁的列表
    WallList = []
    def __init__(self):
        pass
    #开始游戏
    def startGame(self):

        pygame.display.init()#初始化窗口
        #设置窗口的大小和显示
        Maingame.window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #初始化墙壁
        self.creatWall()
        #初始化我方坦克
        self.creatmyTank()
        #初始化敌方坦克，并将敌方坦克添加到列表中
        self.createEnemyTank()
        #设置窗口标题
        pygame.display.set_caption("Tankgame!")
        while True:
            #使坦克移动速度慢一点
            time.sleep(0.02)
            pygame.display.update()#让窗口一直显示（没有这一条，窗口出现之后立即关闭）
            Maingame.window.fill(BG_COLOR)
            #执行获取事件（按右上角退出可以退出游戏）
            self.GetEvent()
            #调用绘制文字的方法
            Maingame.window.blit(self.getTextSurface('敌方坦克剩余数量%d'%len(Maingame.EnemyTankList)),(10,10))

            #如果坦克开关开启才能移动，关闭的话是停止
            if Maingame.my_tank and Maingame.my_tank.live:
                if not Maingame.my_tank.stop == True:
                    Maingame.my_tank.Move()
                    #检测我方坦克是否与墙壁发生碰撞
                    Maingame.my_tank.hitWall()
                    #检测我方坦克是否与敌方坦克发生碰撞
                    Maingame.my_tank.myTank_hit_enemyTank()

            # 调用坦克显示的方法
            if Maingame.my_tank and Maingame.my_tank.live:
                Maingame.my_tank.Display()
            else:
                del Maingame.my_tank
                Maingame.my_tank=None

            #调用函数：循环遍历敌方坦克列表，展示敌方坦克
            self.blitEnemyTank()

            #循环遍历显示我方坦克子弹
            self.blitMyBullet()

            #循环遍历显示敌方坦克子弹
            self.blitEnemyBullet()

            #循环遍历爆炸列表，展示爆炸效果
            self.blitexplode()

            #循环遍历墙壁列表，显示墙壁
            self.blitWalls()

    def creatmyTank(self):
        # 创建我方坦克的方法
        Maingame.my_tank = MyTank(350, 300)

        #创建初始音乐
        music=Music('img/music.mp3')
        music.play()
    #创建墙壁
    def creatWall(self):
        #初始化墙壁
        for i in range(6):
            Walls = Wall(i*130,220)
            #讲墙壁添加到墙壁列表中
            Maingame.WallList.append(Walls)

    # 初始化敌方坦克，并将敌方坦克添加到列表中
    def createEnemyTank(self):
        top = 100
        # 循环生成坦克
        for i in range(Maingame.EnemyTankCount):
            left = random.randint(0, 600)
            top = random.randint(0, 300)
            speed = 4
            enemy = EnemyTank(left, top, speed)
            Maingame.EnemyTankList.append(enemy)

    # 循环遍历爆炸列表，展示爆炸效果
    def blitexplode(self):
        for explode in Maingame.explodeList:
            #判断是否活着
            if explode.live:
                #展示
                explode.DisplayExplode()
            else:
                Maingame.explodeList.remove(explode)


    #循环遍历我方子弹存储列表
    def blitMyBullet(self):
         for myBullet in Maingame.myBulletList:
             #判定子弹的状态：如果状态为True，没有碰到墙才显示,否则从表中删除
             if myBullet.live:
                 myBullet.displayBullet()
                 myBullet.BulletMove()
                 #调用检测我方子弹是否与敌方坦克发生碰撞
                 myBullet.myBullet_hit_enemyTank()
                 # 检测我方子弹是否与墙壁碰撞
                 myBullet.hitWall()
             else:
                 Maingame.myBulletList.remove(myBullet)

    #循环遍历敌方子弹存储列表
    def blitEnemyBullet(self):
        for enemyBullet in Maingame.enemyBulletList:
            if enemyBullet.live:
                enemyBullet.displayBullet( )
                enemyBullet.BulletMove()
                # 调用检测敌方子弹是否与我方坦克发生碰撞
                enemyBullet.enemyBullet_hit_myTank()
                #检测敌方子弹是否与墙壁碰撞
                enemyBullet.hitWall()
            else:
                enemyBullet.enemyBullet_hit_myTank()
                Maingame.enemyBulletList.remove(enemyBullet)

    # 循环遍历敌方坦克列表，展示敌方坦克
    def blitEnemyTank(self):
        for EnemyTank in Maingame.EnemyTankList:
            #判断敌方坦克是否活着，活着才显示
            if EnemyTank.live:
                EnemyTank.Display()
                EnemyTank.randMove()
                #判断坦克是否撞墙
                EnemyTank.hitWall()
                if Maingame.my_tank and Maingame.my_tank.live:
                    #检测敌方坦克是否与我方坦克碰撞
                    EnemyTank.enemyTank_hit_myTank()
                # 发射子弹
                enemyBullet = EnemyTank.Shot()
                # 如果敌方子弹是否为None，如果不为None添加到敌方子弹列表中
                if enemyBullet:
                    # 把子弹存到列表里
                    Maingame.enemyBulletList.append(enemyBullet)
            else:#不活着，从列表中删除
                Maingame.EnemyTankList.remove(EnemyTank)
    def blitWalls(self):
        for Walls in Maingame.WallList:
            #判断一下，如果墙壁被打得没有了，即Wall.live小于等于0了就不存在了，否则才显示
            if Walls.live:
                #调用显示墙壁的方法
                Walls.DisplayWall()
            else:
                Maingame.WallList.remove(Walls)




    #结束游戏
    def endGame(self):
        print("Thanks for playing ,Welcome come back")
        exit()
    #左上角文字的绘制
    def getTextSurface(self,Tanknum):
        #初始化字体模块
        pygame.font.init()

        #查看所有能用的字体
        #print(pygame.font.get_fonts())

        #获取字体font对象
        font1=pygame.font.SysFont("kaiti",18)
        #绘制文字信息（render(文本，抗锯齿，颜色，背景）
        TextSurface=font1.render(Tanknum, True, Font1_Color)
        return TextSurface

    #获取事件
    def GetEvent(self):
        EventLsit=pygame.event.get()
        #遍历所有事件
        for event in EventLsit:
            #判断按下去的是什么键
            #如果按的是退出则关闭窗口
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                #当坦克不存在或者死亡时候
                if not Maingame.my_tank:
                    #判断的是按下的Ese键，让坦克重生
                    if event.key == pygame.K_ESCAPE:
                        #让坦克重生
                        self .creatmyTank()

                if Maingame.my_tank and Maingame.my_tank.live:
                    #判断按下的是上还是下还是左还是右
                    if event.key == pygame.K_LEFT:
                        Maingame.my_tank.direction='L'
                        #按下上下左右键之后修改坦克开关（T or F)
                        # Maingame.my_tank.Move()
                        Maingame.my_tank.stop = False
                        print("left！坦克向左移动")
                    elif event.key == pygame.K_RIGHT:
                        Maingame.my_tank.direction = 'R'
                        # Maingame.my_tank.Move()
                        Maingame.my_tank.stop = False
                        print("right！坦克向右移动")
                    elif event.key == pygame.K_UP:
                        Maingame.my_tank.direction = 'U'
                        # Maingame.my_tank.Move()
                        Maingame.my_tank.stop = False
                        print("up！坦克向上移动")
                    elif event.key == pygame.K_DOWN:
                        Maingame.my_tank.direction = 'D'
                        # Maingame.my_tank.Move()
                        Maingame.my_tank.stop = False
                        print("dowwn！坦克向下移动")
                    elif event.key ==pygame.K_SPACE:
                        print("发射子弹")
                        #创建子弹（调用函数）(我方坦克）
                        #通过子弹列表的大小来判断子弹数目，并设置最多只能发射三颗子弹
                        if len(Maingame.myBulletList) <3:
                            myBullet = Bullet(Maingame.my_tank)
                            Maingame.myBulletList.append(myBullet)
                            music=Music('img/shoot.mp3')
                            music.play()
            #松开方向键，坦克停止运动，stop值为True
            if event.type == pygame.KEYUP:
                #判断我们松开的键是不是发送子弹键，释放的SPACE的话不停止
                if not event.key == pygame.K_SPACE:
                    if Maingame.my_tank and Maingame.my_tank.live:
                        Maingame.my_tank.stop = True


class Tank(BaseItem):
    #距离左边，上面的距离
    def __init__(self,left,top):
        #保存加载的图片
        self.images={
            'U':pygame.image.load('img/tank_top.gif'),
            'D': pygame.image.load('img/tank_down.gif'),
            'L': pygame.image.load('img/tank_left.gif'),
            'R': pygame.image.load('img/tank_right.gif'),
        }
        self.direction = 'D'
        # 根据当前图片的方向获取图片
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left值和top值
        self.rect.left = left
        self.rect.top = top
        # 速度，决定了移动的快慢
        self.speed = 4
        # 坦克移动的开关
        self.stop = True
        #坦克状态 ：是否活着
        self.live=True
        #新增属性：原来的坐标
        self.OldLeft = self.rect.left
        self.OldTop = self.rect.top
    #坦克的移动
    def Move(self):
        #移动之后要记录原来的坐标
        self.OldLeft = self.rect.left
        self.OldTop = self.rect.top
        #判断坦克的方向来进行移动
        if self.direction =='L':
            if self.rect.left >=10:
                self.rect.left=self.rect.left-self.speed
        elif self.direction =='U':
            if self.rect.top >= 10:
                self.rect.top=self.rect.top-self.speed
        elif self.direction =='D':
            if self.rect.top+self.rect.height <=SCREEN_HEIGHT:
                self.rect.top=self.rect.top+self.speed
        elif self.direction =='R':
            if self.rect.left +self.rect.height <= SCREEN_WIDTH:
                self.rect.left=self.rect.left+self.speed

    #坦克的设计
    def Shot(self):
        return Bullet(self)
    #检测坦克是否和墙壁发生了碰撞

    # stay方法
    def stay(self):
        self.rect.left = self.OldLeft
        self.rect.top = self.OldTop

    def hitWall(self):
        for wall in Maingame.WallList:
            if pygame.sprite.collide_rect(self,wall):
               #撞击墙壁后坦克调用stay方法，坦克不动
                self.stay()

    #展示坦克
    def Display(self):
        #获取展示的对象
        self.image=self.images[self.direction]
        #调用blit方法展示
        Maingame.window.blit(self.image,self.rect)
#我方坦克
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank, self).__init__(left,top)

    #检测我方坦克和敌方坦克发生碰撞
    def myTank_hit_enemyTank(self):
        #循环便利敌方坦克列表
        for enemyTank in Maingame.EnemyTankList:
            if pygame.sprite.collide_rect(self,enemyTank):
                self.stay()

#敌方坦克
class EnemyTank(Tank):
    def __init__(self,top,left,speed):
        #调用父类的初始化方法，
        super(EnemyTank, self).__init__(left,top)
        #加载敌方坦克
        self.images = {
            'U': pygame.image.load('img/enemy_top1.gif'),
            'D': pygame.image.load('img/enemy_down1.gif'),
            'L': pygame.image.load('img/enemy_left1.gif'),
            'R': pygame.image.load('img/enemy_right1.gif'),
        }
        #方向,随机生成敌方坦克的方向
        self.direction = self.randDirection()
        # 根据当前图片的方向获取图片
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left值和top值
        self.rect.left = left
        self.rect.top = top
        self.speed =speed
        #移动开关
        self.flag=True
        #新增一个步数变量
        self.step=40

    def randDirection(self):
           num = random.randint(1,4)
           if num ==1:
               return 'U'
           elif num == 2:
               return 'D'
           elif num == 3:
               return 'L'
           elif num == 4:
               return 'R'
    #敌方坦克的随即移动方法
    def randMove(self):
        if self.step <=0:
            self.direction=self.randDirection()
            #让步数复位
            self.step=40
        else:
            self.Move()
            #步数递减
            self.step-=1
    #重写Shot()
    def Shot(self):
        #随机生成100以内的数字
        num =random.randint(1,100)
        if num<10:
            return Bullet(self)
    #敌方坦克与我方坦克的碰撞
    def enemyTank_hit_myTank(self):
        if pygame.sprite.collide_rect(self,Maingame.my_tank):
            self.stay()
#墙壁
class Wall():
    def __init__(self,left,top):
        #加载墙壁图片
        self.image = pygame.image.load('img/Wall.gif')
        #获取墙壁的区域
        self.rect = self.image.get_rect()
        #设置位置
        self.rect.left = left
        self.rect.top = top
        #是否活着
        self.live=True
        #设置一个墙壁生命值
        self.hp=10

    #展示墙壁的方法
    def DisplayWall(self):
        Maingame.window.blit(self.image,self.rect)

#子弹
class Bullet(BaseItem):
    def __init__(self,tank):
        #加载子弹图片
        self.image=pygame.image.load('img/Bullet.gif')
        #坦克的方向决定了子弹的方向
        self.direction=tank.direction
        #获取区域
        self.rect=self.image.get_rect()
        #子弹的left和top与方向有关
        if self.direction =='U':
            self.rect.left = tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top = tank.rect.top-self.rect.height
        elif self.direction =='D':
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top = tank.rect.top+tank.rect.height
        elif self.direction =='L':
            self.rect.left=tank.rect.left-tank.rect.width/2+self.rect.width
            self.rect.top = tank.rect.top+tank.rect.width/2-self.rect.width/2
        elif self.direction =='R':
            self.rect.left=tank.rect.left+tank.rect.width+self.rect.width*0.5
            self.rect.top = tank.rect.top+tank.rect.width/2-self.rect.width/2
        #子弹的速度
        self.speed =6
        #子弹的状态：即碰到墙壁则修改此状态
        self.live=True
     #子弹的移动
    def BulletMove(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-= self.speed
            else:
                #修改状态
                self.live=False
        elif self.direction == 'D':
            if self.rect.top+self.rect.height< SCREEN_HEIGHT:
                self.rect.top+= self.speed
            else:
                # 修改状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left +self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改状态
                self.live = False
    #子弹是否碰撞墙壁
    def hitWall(self):
        #循环遍历墙壁列表
        for wall in Maingame.WallList:
            if pygame.sprite.collide_rect(self,wall):
                #修改子弹的状态，让子弹消失
                self.live=False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live=False


    #子弹的展示
    def displayBullet(self):
        #将图片surface加载在主窗口里
        Maingame.window.blit(self.image,self.rect)

    #我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        #遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in Maingame.EnemyTankList:
            if pygame.sprite.collide_rect(enemyTank,self):
                #修改敌方坦克的状态和我方子弹的状态
                enemyTank.live=False
                self.live=False
                #创建爆炸对象
                explode=Explode(enemyTank)
                Maingame.explodeList.append(explode)

    #敌方子弹和我方坦克的碰撞
    def enemyBullet_hit_myTank(self):
        if Maingame.my_tank and Maingame.my_tank.live:
            if pygame.sprite.collide_rect(Maingame.my_tank, self):
                # 产生爆炸对象
                explode = Explode(Maingame.my_tank)
                # 讲爆炸对象添加到列表中
                Maingame.explodeList.append(explode)
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                Maingame.my_tank.live = False

#爆炸效果
class Explode():
    def __init__(self,tank):
        #爆炸的位置，由当前子弹打中的坦克位置决定
        self.rect=tank.rect
        self.image=pygame.image.load('img/boom.gif')
        self.live=True

    #显示爆炸
    def DisplayExplode(self):

        Maingame.window.blit(self.image,self.rect)
        self.live=False


#音效
class Music():
    def __init__(self,filename):
        self.file = filename
        #初始化音乐混合器
        pygame.mixer.init()
        #加载音乐
        pygame.mixer.music.load(self.file)
    #播放音乐
    def play(self):
        pygame.mixer.music.play()

if __name__ == '__main__':
    Maingame().startGame()