import pygame
from random import randint

pygame.init()
pygame.font.init()

#screen dimensions
WIDTH = 700
HEIGHT = 500
TILE_SIZE = 20

#set framerate
clock = pygame.time.Clock()
FPS = 60

#create and name the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CUSTOM_GREEN = (103, 255, 79)

#rows, columns and offset's settings
SIDE_OFFSET = 50
VERTICAL_OFFSET = 50
OFFSET_COLOR = BLACK
COLUMNS = (WIDTH - 2 * SIDE_OFFSET) // TILE_SIZE
ROWS = (HEIGHT - 2 * VERTICAL_OFFSET) // TILE_SIZE

def centeredx_text(surface, y, font, color, string, height):
    format = pygame.font.SysFont(font, height)
    text = format.render(string, True, color)
    surface.blit(text, ((surface.get_width() -text.get_width())/2, y))

def draw_bg():
    #draw the screen
    screen.fill(CUSTOM_GREEN)
    #draw the side rectangles
    pygame.draw.rect(screen, OFFSET_COLOR, (0, 0, SIDE_OFFSET, HEIGHT))
    pygame.draw.rect(screen, OFFSET_COLOR, (WIDTH - SIDE_OFFSET, 0, SIDE_OFFSET, HEIGHT))
    #draw the vertical rectangles
    pygame.draw.rect(screen, OFFSET_COLOR, (0, 0, WIDTH, VERTICAL_OFFSET))
    pygame.draw.rect(screen, OFFSET_COLOR, (0, HEIGHT - VERTICAL_OFFSET, WIDTH, VERTICAL_OFFSET))

def draw_grid():
    #draw te grid
    grid = []
    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            rect = pygame.Rect((SIDE_OFFSET + TILE_SIZE * j, VERTICAL_OFFSET + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, WHITE, rect, 1)
            row.append(rect)
        grid.append(row)

class Snake:
    def __init__(self, start_body_lenght, head_color, body_color, x, y, wait):
        self.start_body_lenght = start_body_lenght
        self.head_color = head_color
        self.body_color = body_color
        self.x = x
        self.y = y
        self.wait = wait
        self.alive = True
        self.moving = False
        self.cooldown = pygame.time.get_ticks()
        self.x_vel = 0
        self.y_vel = 0

        self.head_rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self.body_rects = []
        for i in range(self.start_body_lenght):
            body_rect = pygame.Rect(self.x, self.y + TILE_SIZE*(i+1), TILE_SIZE, TILE_SIZE)
            self.body_rects.append(body_rect)

    #draw every piece of the snake
    def draw(self):
        for rect in self.body_rects:
            pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.head_color, self.head_rect)
        pygame.draw.rect(screen, WHITE, self.head_rect, 1)

    #changing the direction
    def move(self):
        self.keys = pygame.key.get_pressed()
        if self.x_vel != 0 or self.y_vel != 0:
            self.moving = True

        if self.keys[pygame.K_a] and self.x_vel != 1:
            self.x_vel = -1
            self.y_vel = 0
        if self.keys[pygame.K_d] and self.x_vel != -1:
            self.x_vel = 1
            self.y_vel = 0
        if self.keys[pygame.K_w] and self.y_vel != 1:
            self.y_vel = -1
            self.x_vel = 0
        if self.keys[pygame.K_s] and self.y_vel != -1:
            self.y_vel = 1
            self.x_vel = 0

        #every piece of the body gets the position of the previous one
        if pygame.time.get_ticks() - self.cooldown >= self.wait and self.moving and self.alive:
            if len(self.body_rects) > 1:
                self.body_rects[-1:0:-1] = self.body_rects[-2::-1]
                self.body_rects[0] = pygame.Rect(self.head_rect[0], self.head_rect[1], TILE_SIZE, TILE_SIZE)
            elif len(self.body_rects) == 1:
                self.body_rects[0] = pygame.Rect(self.head_rect[0], self.head_rect[1], TILE_SIZE, TILE_SIZE)

            self.head_rect.x += self.x_vel*TILE_SIZE
            self.head_rect.y += self.y_vel * TILE_SIZE
            self.cooldown = pygame.time.get_ticks()

    def eat(self, target):
        self.target = target

        if self.head_rect.colliderect(self.target):

            #check where to place the new body rectangle
            if len(self.body_rects) == 0:
                self.new_rect = pygame.Rect(self.head_rect[0], self.head_rect[1], TILE_SIZE, TILE_SIZE)
                if self.x_vel == -1:
                    self.new_rect.x += TILE_SIZE
                elif self.x_vel == 1:
                    self.new_rect.x -= TILE_SIZE
                if self.y_vel == -1:
                    self.new_rect.y += TILE_SIZE
                elif self.y_vel == 1:
                    self.new_rect.y -= TILE_SIZE

            else:
                self.new_rect = self.body_rects[-1]

                if len(self.body_rects) >= 2:
                    if self.body_rects[-1].x == self.body_rects[-2].x - TILE_SIZE:
                        self.new_rect.x += TILE_SIZE
                    elif self.body_rects[-1].x == self.body_rects[-2].x + TILE_SIZE:
                        self.new_rect.x -= TILE_SIZE
                    if self.body_rects[-1].y == self.body_rects[-2].y - TILE_SIZE:
                        self.new_rect.y += TILE_SIZE
                    elif self.body_rects[-1].y == self.body_rects[-2].y + TILE_SIZE:
                        self.new_rect.y -= TILE_SIZE

            self.body_rects.append(self.new_rect)

    #check the collison betweeen the head and the border
    def border_collision(self):
        if self.head_rect.right > WIDTH - SIDE_OFFSET or self.head_rect.left < SIDE_OFFSET \
            or self.head_rect.bottom > HEIGHT - VERTICAL_OFFSET or self.head_rect.top < VERTICAL_OFFSET:
            self.alive = False

    #check collision between the head and the body
    def body_collision(self):
        for body_rect in self.body_rects:
            if self.head_rect == body_rect:
                self.alive = False

#food class
class Food:
    def __init__(self, color, wait, target):
        self.color = color
        self.wait = wait
        self.target = target
        self.alive = True
        self.cooldown = pygame.time.get_ticks()
        self.x = randint(0, COLUMNS - 1)
        self.y = randint(0, ROWS - 1)

        self.rect = pygame.Rect(self.x*TILE_SIZE + SIDE_OFFSET, self.y*TILE_SIZE + VERTICAL_OFFSET, TILE_SIZE, TILE_SIZE)

    #if the food is eaten, generate another one
    def eat(self):
        if self.target.colliderect(self.rect):
            self.x = randint(0, COLUMNS - 1)
            self.y = randint(0, ROWS - 1)
            self.rect = pygame.Rect(self.x * TILE_SIZE + SIDE_OFFSET, self.y * TILE_SIZE + VERTICAL_OFFSET,
                                    TILE_SIZE, TILE_SIZE)
            self.alive = False
            self.cooldown = pygame.time.get_ticks()

    #if enough time is passed since the last food is eaten, create another one
    def spawn(self):
        if self.alive == False and pygame.time.get_ticks() - self.cooldown >= self.wait:
            self.alive = True

    #draw the food
    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)

#main function
def main():

    run = True
    gameover = False

    #snake instance
    snake = Snake(4, RED, BLACK, SIDE_OFFSET + 10*TILE_SIZE, VERTICAL_OFFSET + 5*TILE_SIZE, 150)

    #food instance
    food = Food(BLUE, 1000, snake.head_rect)

    while run:

        #use the choosen framerate
        clock.tick(FPS)

        # on-screen variables
        body_lenght = len(snake.body_rects)
        food_eaten = len(snake.body_rects) - snake.start_body_lenght
        
        if gameover == False:

            #draw all the game window
            draw_bg()
            draw_grid()

            #snake
            snake.draw()
            snake.move()
            snake.eat(food)
            snake.border_collision()
            snake.body_collision()

            #food
            food.spawn()
            food.eat()
            food.draw()

            centeredx_text(screen, 15, "rockwellnova", WHITE, "BODY LENGHT: " + str(body_lenght), 20)
            centeredx_text(screen, HEIGHT - 40, "rockwellnova", WHITE, "FOOD EATEN: " + str(food_eaten), 20)

            if snake.alive == False:
                gameover = True

        #gameover settings
        if gameover:
            #screen.fill(BLACK)
            centeredx_text(screen, HEIGHT // 2 - 150, "rockwellnova", RED, "YOU LOST", 50)
            centeredx_text(screen, HEIGHT // 2 - 50, "rockwellnova", RED, "PRESS SPACE TO PLAY AGAIN", 30)

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                gameover = False
                snake = Snake(4, RED, BLACK, SIDE_OFFSET + 10 * TILE_SIZE, VERTICAL_OFFSET + 5 * TILE_SIZE, 150)
                food = Food(BLUE, 1000, snake.head_rect)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #update the screen
        pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()
