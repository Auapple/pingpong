import pygame as pg,random, math
pg.init()

lscore = 0
rscore = 0

class Ball(pg.sprite.Sprite):
	dx = 0         #x位移量
	dy = 0         #y位移量
	x = 0          #球x坐標
	y = 0          #球y坐標
	direction = 0  #球移動方向
	speed = 0      #球移動速度

	def __init__(self, sp, srx, sry, radium, color):
		pg.sprite.Sprite.__init__(self)
		self.speed = sp
		self.x = srx
		self.y = sry

		#繪製球體
		self.image = pg.Surface([radium*2, radium*2])  
		self.image.fill((255,255,255))
		pg.draw.circle(self.image, color, (radium,radium), radium, 0)
		self.rect = self.image.get_rect()  #取得球體區域
		self.rect.center = (srx,sry)       #初始位置
		self.direction = random.randint(40,70)  #移動角度

         #球體移動 
	def update(self):         
		radian = math.radians(self.direction)    #角度轉為弳度
		self.dx = self.speed * math.cos(radian)  #球水平運動速度
		self.dy = -self.speed * math.sin(radian) #球垂直運動速度or 
		self.x += self.dx     #計算球新坐標
		self.y += self.dy
		self.rect.x = self.x  #移動球圖形
		self.rect.y = self.y
        #到達左右邊界
		if(self.rect.left <= 0):
			self.x = 300
			self.y = 200
		if(self.rect.right >= screen.get_width()-10):
			self.x = 300
			self.y = 200
		elif(self.rect.top <= 10):  #到達上邊界
			self.rect.top = 10
			self.bounceup()
		if(self.rect.bottom >= screen.get_height()-10):  #到達下邊界出界
			self.bounceup()
		else:
			return False


	def bounceup(self):
		self.direction = 360 - self.direction
	
	def bouncelr(self):
		self.direction = (180 - self.direction) % 360

screen = pg.display.set_mode((600, 400))
pg.display.set_caption("Ping Pong Game")
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))
allsprite = pg.sprite.Group()
ball = Ball(15, 300, 350, 10, (255,123,188))
allsprite.add(ball)
keys = pg.key.get_pressed()

class Ltab(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([25,100])
		self.image.fill((230,230,230))
		self.rect = self.image.get_rect()
		self.rect.x = 25
		self.rect.y = 150

	def update(self):
		if keys[pg.K_w]:
			self.rect.y += 10
		if keys[pg.K_s]:
			self.rect.y -= 10
	def move_up(self):
		self.rect.y -= 10

	def move_down(self):
		self.rect.y += 10

class Rtab(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([25,100])
		self.image.fill((230,230,230))
		self.rect = self.image.get_rect()
		self.rect.x = 550
		self.rect.y = 150

	def update(self):
		if keys[pg.K_UP]:
			self.rect.y += 10
		if keys[pg.K_DOWN]:
			self.rect.y -= 10
	def move_up(self):
		self.rect.y -= 10

	def move_down(self):
		self.rect.y += 10	


Ltab = Ltab()
Rtab = Rtab()
allsprite.add(Ltab)
allsprite.add(Rtab)

clock = pg.time.Clock()        
downmsg = "Press Left Click Button to start game!"  #起始訊息
playing = False  #開始時球不會移動
running = True
tab_key = True
#運行的程式碼
while running:
	clock.tick(30)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
	buttons = pg.mouse.get_pressed()  #檢查滑鼠按鈕
	if buttons[0]:            #按滑鼠左鍵後球可移動       
		playing = True
       
    #遊戲進行中
	if playing == True:  
		screen.blit(background, (0,0))  #清除繪圖視窗
		fail = ball.update()  #移動球體

		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			Ltab.move_up()
		if keys[pg.K_s]:
			Ltab.move_down()
		if keys[pg.K_UP]:
			Rtab.move_up()
		if keys[pg.K_DOWN]:
			Rtab.move_down()
		#if tab_key:
		#	Ltab.update()
		#	Rtab.update()
		if ball.rect.right >= 590:
			lscore += 1
		if ball.rect.left <= 0:
			rscore += 1
		if lscore >= 8:
			font = pg.font.SysFont("Arial",50)
			win = font.render('LEFT  WINS!!!', True, (212,201,106), (255,255,255))
			ball.rect.y = 0
			ball.speed = 0
			tab_key = False
			screen.blit(win, (175,175))
			playing = False
		if rscore >= 8:
			font = pg.font.SysFont("Arial",50)
			win = font.render('RIGHT  WINS!!!', True, (212,201,106), (255,255,255))
			ball.rect.y = 0
			ball.speed = 0
			tab_key = False
			screen.blit(win, (175,175))
			playing = False
		Lhitpad = pg.sprite.collide_rect(ball, Ltab)
		Rhitpad = pg.sprite.collide_rect(ball, Rtab)
		if Lhitpad:
			ball.bouncelr()
		if Rhitpad:
			ball.bouncelr()
		allsprite.draw(screen)
	pg.display.update()
pg.quit()