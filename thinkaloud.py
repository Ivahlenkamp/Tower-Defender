#Video Follow along part 1 https://www.youtube.com/watch?v=BTqLJlfFE0M
#Video Follow along part 2 https://www.youtube.com/watch?v=glah2YjuY2A
#Video Follow along part 3 https://www.youtube.com/watch?v=vaGv2Pa-oWA
#Video Follow along part 4 https://www.youtube.com/watch?v=ZB4_x28dFCw&t=2s
#Video Follow along part 5 https://www.youtube.com/watch?v=Q6Wm-8ecL-o 
#Video Follow along part 6 https://www.youtube.com/watch?v=Y_ldIQgM3CU 
#Video Follow along part 7 https://www.youtube.com/watch?v=N0VvHLm6cK0 
#import libraries
#images link https://github.com/russs123/Castle_Defender/blob/main/Castle_Defender.zip
#install [pip install pygame]
import pygame
import math
from enemy import Enemy


#initialize pygame
pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

"""Create game window"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Can be called to add images
pygame.display.set_caption('Castle defender')

clock= pygame.time.Clock()    #Sets frames so it doesnt max out constantly
fps = 60                      #Sets fps

#define game variables
MAX_ENEMIES = 10
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks
enemies_alive = 0

"""load images, Folder attached possible that your path is not the same"""
bg = pygame.image.load('img/bg.png').convert_alpha() #background photo
#castle image
castle_img_100 = pygame.image.load('img\castle\castle_100.png').convert_alpha() #object oriented
castle_img_50 = pygame.image.load('img\castle\castle_50.png').convert_alpha() #object oriented
castle_img_25 = pygame.image.load('img\castle\castle_25.png').convert_alpha() #object oriented

#bullet image
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * .075), int(b_h * .075)))

# load enemies images
#setting your global parameters using lists
enemy_animations = []
enemy_types = ['knight']
enemy_health = [75]

animation_types = ['walk', 'attack', 'death']
for enemy in enemy_types:
      #load animation
      animation_list = []
      # makes it so it goes through that list of walk attack and death
      for animation in animation_types:
            #resettemporary list of images
            temp_list = []
            #define number of frames
            num_of_frames = 20
            #0-19 which is our number of images for the motions
            for i in range(num_of_frames):
                  img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
                  # enemt image length and width
                  e_w = img.get_width()
                  e_h = img.get_height()
                  img = pygame.transform.scale(img, (int(e_w * .2), int(e_h * .2)))
                  #temp list houses images in folder
                  temp_list.append(img)
            animation_list.append(temp_list)
      enemy_animations.append(animation_list)



"""define colors"""
WHITE= (255,255,255)

#castle class
class castle():  #object/constructor
      def __init__(self, image100, image50, image25, x, y, scale): #Scale because size changes, different factors to track
            self.health = 1000
            self.max_health = self.health
            self.fired = False
            self.money= 0
            self.score = 0

            width= image100.get_width()   #defined but dont need/transformed
            height= image100.get_height()

            self.image100 = pygame.transform.scale(image100, (int(width*scale), (int(height * scale))))
            self.image50 = pygame.transform.scale(image50, (int(width*scale), (int(height * scale))))
            self.image25 = pygame.transform.scale(image25, (int(width*scale), (int(height * scale))))
            self.rect = self.image100.get_rect()  #Create rectangle around it to create position to move it
            self.rect.x = x
            self.rect.y = y

      def shoot(self):
            pos = pygame.mouse.get_pos()
            x_dist = pos[0] - self.rect.midleft[0]
            y_dist = -(pos[1] - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))
            #get mouseclick
            if pygame.mouse.get_pressed()[0] and self.fired == False:# three values to access 0,1,2 0 is the left
                  self.fired = True
                  bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                  bullet_group.add(bullet)
            #reset mouseclick
            if pygame.mouse.get_pressed()[0] ==False:
                  self.fired = False

      def draw(self):   #method within
            #check which image to use based pon health
            if self.health <+ 250:
                  self.image = self.image25
            elif self.health <=500:
                  self.image = self.image50
            else:
                  self.image = self.image100

            screen.blit(self.image, self.rect) #Calling rectangle you created

#bullet class
class Bullet(pygame.sprite.Sprite): #sprite built in pygame functionality
      def __init__(self, image, x, y, angle):
            pygame.sprite.Sprite.__init__(self)
            self.image= image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.angle = math.radians(angle)#convert input to radians
            self.speed = 40
            #calculate the horizontal and vertical speeds based on the angle
            self.dx = math.cos(self.angle) * self.speed
            self.dy = -(math.sin(self.angle) * self.speed)

      def update(self):
            #check if bullet has gone off screen
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom <0 or self.rect.top > SCREEN_HEIGHT:
                  self.kill()

            #move bullet
            self.rect.x += self.dx
            self.rect.y += self.dy

class Crosshair():
      def __init__(self, scale):
            image = pygame.image.load('img/crosshair.png').convert_alpha()
            width = image.get_width()
            height = image.get_height()

            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()

            pygame.mouse.set_visible(False)

      def draw(self):
            mx, my = pygame.mouse.get_pos()
            self.rect.center = (mx, my)
            screen.blit(self.image, self.rect)



#create castle, call all the arguments
castle = castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, .2) #.2 is percentage of image size

#Create Crosshair
crosshair = Crosshair(.025)

"""Groups"""
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()



#game loop
run = True
while run:
      clock.tick(fps)         

      #Background image called
      screen.blit(bg, (0,0)) #(0,0) is location of image

      #Draw castle
      castle.draw()
      castle.shoot()

      #draw crosshair
      crosshair.draw()


      #draw bullet
      bullet_group.update()
      bullet_group.draw(screen)
      #print(len(bullet_group))

      #draw enemies
      enemy_group.update(screen, castle, bullet_group)

      #create enemies
      #check if max number of enemies had been reached
      if len(enemy_group) < MAX_ENEMIES:
            """Create Enemies"""
      
            #our class and passing the enemies through it all
            enemy= Enemy(enemy_health[0], enemy_animations[0], -100, SCREEN_HEIGHT - 100, 1)
            #groups have built in update and draw methods
            enemy_group.add(enemy)
            #reset enemy timer
            last_enemy = pygame.time.get_ticks()

      #event handler 
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  run = False

      #update display window
      pygame.display.update()

pygame.quit()
