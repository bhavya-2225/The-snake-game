import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):

        self.body= [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)
        self.new_block= False

        self.head_up= pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down= pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_left= pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_right= pygame.image.load('Graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        #create rectangle
        #still be needing this so as to place image n get position
        for index,block in enumerate(self.body):
            x_pos=int(block.x*cell_size)
            y_pos=int(block.y*cell_size)
            block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            #draw rectangle
            #which part is head n tail n what is head's direction
            if index==0:#head
                screen.blit(self.head,block_rect)
            
            elif index == len(self.body)-1:#tail
                screen.blit(self.tail,block_rect)
            else:#rest body
                previous_block= self.body[index+1]-block
                next_block= self.body[index-1]-block
                
                if(previous_block.x==next_block.x):
                    screen.blit(self.body_vertical,block_rect)
                elif(previous_block.y==next_block.y):
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if(previous_block.x==-1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==-1): screen.blit(self.body_tl,block_rect)
                    elif(previous_block.x==1 and next_block.y==1 or previous_block.y==1 and next_block.x==1): screen.blit(self.body_br,block_rect)
                    elif(previous_block.x==-1 and next_block.y==1 or previous_block.y==1 and next_block.x==-1): screen.blit(self.body_bl,block_rect)
                    elif(previous_block.x==1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==1): screen.blit(self.body_tr,block_rect)

    def update_tail_graphics(self):
        tail_relation=self.body[len(self.body)-2]-self.body[len(self.body)-1]

        if tail_relation == Vector2(1,0): self.tail=self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail=self.tail_right
        elif tail_relation == Vector2(0,1): self.tail=self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail=self.tail_down

    def update_head_graphics(self):
        head_relation= self.body[1]-self.body[0]

        if head_relation==Vector2(1,0): self.head=self.head_left
        elif head_relation==Vector2(-1,0): self.head=self.head_right
        elif head_relation==Vector2(0,1): self.head=self.head_up
        elif head_relation==Vector2(0,-1): self.head=self.head_down

    def move_snake(self):
        if self.new_block == True:
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body=body_copy[:]
            self.new_block=False
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body=body_copy[:]

    def addBlock(self):
        self.new_block= True

    def reset(self):
        self.body= [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)


class FRUIT:
    def __init__(self):
        self.randomize()
        # #create an x and y position
        # self.x = random.randint(0, cell_number-1)
        # self.y = random.randint(0, cell_number-1)
        # #store this in list or vector. Vector being the better option
        # self.pos= Vector2(self.x,self.y)
        
    def draw_fruit(self):
        # create rectangle
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)    #x cord, y coord, width, height
        #draw rectangle :  surface, color, rectangle
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        
        self.pos= Vector2(self.x,self.y)


class MAIN:
    def __init__(self):
        self.snake=SNAKE()
        self.fruit=FRUIT()

    def update(self):
        self.snake.move_snake() 
        self.check_collision() 
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #print('EAT')
            #reposition the fruit
            self.fruit.randomize()
            #add another blosk to snake
            self.snake.addBlock()

        for block in self.snake.body[1:]:
            if(block== self.fruit.pos):
                self.fruit.randomize()

    def check_fail(self):
        #collision with wall
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        #hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()   

    def draw_grass(self):
        grass_color=(160,200,40)
        for row in range(cell_number):
            if row%2==0:
                for col in range(cell_number):
                    if col%2==0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col%2!=0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
                
    def draw_score(self):
        score_text= "Score: "
        score= str(len(self.snake.body) - 3)
        score_surface= game_font.render(score,True,(56,74,12))   #text, anti aliasing(more smoother text), color
        score_x= int(cell_number*cell_size -60)
        score_y= int(cell_number*cell_size -40)
        score_rect= score_surface.get_rect(center=(score_x,score_y))
        score_text_surface=game_font.render(score_text,True,(56,74,12))
        score_text_rect= score_text_surface.get_rect(midright=(score_rect.left,score_rect.centery))
        apple_rect= apple.get_rect(midright=(score_text_rect.left,score_text_rect.centery))
        bg_rect= pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width+ score_rect.width+ score_text_rect.width+ 5 ,apple_rect.height)  #x,y,w,h
        
        pygame.draw.rect(screen,(150,200,50),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        screen.blit(score_text_surface,score_text_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)
        #screen.blit()



pygame.init()

cell_size=40
cell_number=20

screen= pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size)) 
clock= pygame.time.Clock()     

apple= pygame.image.load('Graphics/apple.png').convert_alpha()

game_font= pygame.font.Font('font/Copyduck.ttf',25)

fruit=FRUIT()
snake=SNAKE()
main_game=MAIN()

SCREEN_UPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    #draw all our elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()  
             sys.exit()   
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction=Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction=Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction=Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction=Vector2(1,0)

    #screen.fill(pygame.Color('gold'))
    screen.fill(pygame.Color((175,215,70)))  
    main_game.draw_elements()
    pygame.display.update()    
    clock.tick(60)  

    


