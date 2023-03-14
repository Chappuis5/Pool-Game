import pygame
import random
import math
from objects import Ball, find_ball, Hole

DEBUG = False


FPS = 60
WIDTH = 800
HEIGHT = 400

# colours 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (29, 110, 50)

# initialisation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('8 ball pool')
screen.fill(BACKGROUND)
clock = pygame.time.Clock() # For syncing the FPS
font = pygame.font.SysFont(None, 24)


message = {"time_to_live": 0, "text": "", "color": (0, 0, 0)}


balls = []
for i in range(16):
    size = 10
    x = random.randint(size, WIDTH - size)
    y = random.randint(size, HEIGHT - size)
    color = BLUE
    ball_object = Ball(x, y, size, color)
    balls.append(ball_object)


holes = [
    Hole(0,0, 30),
    Hole(WIDTH/2, 0, 30),
    Hole(WIDTH, 0, 30),
    Hole(0, HEIGHT, 30),
    Hole(WIDTH/2, HEIGHT, 30),
    Hole(WIDTH, HEIGHT, 30)
]



running = True
selected_ball = None
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_ball = find_ball(balls, mouseX, mouseY)
            if selected_ball:
                selected_ball.color = RED
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_ball :
                selected_ball.color = BLUE
                selected_ball = None
    
    screen.fill(BACKGROUND)

    # update
    for index, i in enumerate(balls):
        if i != selected_ball:
            i.move()
            i.bounce()
            for i2 in balls:
                if i != i2:
                    i.collide(i2)
            
            for hole in holes:
                if hole.isInHole(i):
                    balls.remove(i)
                    message["text"] = "Ball {} has been removed".format(index)
                    message["color"] = WHITE
                    message["time_to_live"] = FPS * 3
                    break
        else : 
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selected_ball.x
            dy = mouseY - selected_ball.y
            selected_ball.angle = (math.atan2(dy, dx) + 0.5*math.pi)+math.pi
            selected_ball.speed = math.hypot(dx, dy) * 0.1
            selected_ball.speed = min(selected_ball.speed, 20)


            end_line_x = selected_ball.x + selected_ball.speed * math.cos(selected_ball.angle - math.pi/2)*10
            end_line_y = selected_ball.y + selected_ball.speed * math.sin(selected_ball.angle - math.pi/2)*10
            # change the color of the line based on the speed of the selected ball.
            colorShifter = selected_ball.speed/20
            color = (255, 255-int(255*colorShifter), 255-int(255*colorShifter))
            # draw a line that goes from the ball in direction of selected_ball.angle, length selected_ball.speed
            pygame.draw.line(screen, color, (selected_ball.x, selected_ball.y), (end_line_x, end_line_y), max(1,int(selected_ball.speed/3)))
            # draw a text showing the lenght of the line above the ball
            text = font.render(str(int(selected_ball.speed)), True, color)
            screen.blit(text, (selected_ball.x+10, selected_ball.y))    
            if DEBUG :
                # draw a text showing the color of the line above the ball
                text = font.render(str(color), True, color)
                screen.blit(text, (selected_ball.x+10, selected_ball.y-20)) 
        
        
        
        # draw
        i.display()
    
    # draw
    for h in holes : 
        h.display()
    
    if message["time_to_live"] > 0:
        message["time_to_live"] -= 1
        text = font.render(message["text"], True, message["color"])
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))


    # flip
    pygame.display.flip()