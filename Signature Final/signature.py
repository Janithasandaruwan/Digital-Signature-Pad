#Author Janitha Sandaruwan

import pygame
import pymsgbox
import base64
import uuid


#For pygame display
background_color = (255,255,255)
pygame.init()
screen = pygame.display.set_mode((480,286))
pygame.display.set_caption("Digital Signature")
draw_on = False
write_active = False
last_pos = (0, 0)
radius = 1
screen.fill((background_color))

#For time processing
clock = pygame.time.Clock()
timer = pygame.time.get_ticks
timeout = 3000 # milliseconds
deadline = timer() + timeout

#For clear button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
width = screen.get_width()
height = screen.get_height()


#For display font
text1 = pygame.font.SysFont('Corbel',25)


def roundline(srf, color, start, end, radius):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.display.update(pygame.draw.circle(srf, color, (x, y), radius))

try:
    while True:
        now = timer()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise StopIteration
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = (0,0,0)
                pygame.draw.circle(screen, color, event.pos, radius)
                draw_on = True
                write_active = True
                #Clear when mouse clicked
                if 0 <= mouse[0] <= width and height-25 <= mouse[1] <= height:
                    screen.fill((background_color))
                    write_active = False

            if event.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            if event.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.display.update(pygame.draw.circle(screen, color, event.pos, radius))
                    roundline(screen, color, event.pos, last_pos,  radius)
                last_pos = event.pos

            if pygame.mouse.get_rel() != (0, 0):  # mouse moved within the pygame screen
                deadline = now + timeout  # reset the deadline
        if write_active == True:
            if now > deadline:
                write_active = False
                rect = pygame.Rect(0, 0, 480, 261)
                sub = screen.subsurface(rect)
                img_name = "Images/%s_%s_%s.jpg" % ("C3DSS","sign",str(uuid.uuid4()))
                pygame.image.save(sub,img_name)

                with open(img_name, "rb") as image_file:
                    data = base64.b64encode(image_file.read())

                f = open("sign.txt", "wb")
                f.write(data)
                f.close()
                #pymsgbox.alert('Signature was Submitted!', 'Alert')
                screen.fill((background_color))

        mouse = pygame.mouse.get_pos()

        if 0 <= mouse[0] <= width and height-25 <= mouse[1] <= height:
            pygame.draw.rect(screen, color_light, [0, height-25, width, 25])

        else:
            pygame.draw.rect(screen, color_dark, [0, height-25, width, 25])

        screen.blit(text1.render('Clear Screen', True,(0,187,14)), (170, 262))
        pygame.draw.line(screen, (0,142,14), (480, 230), (0, 230))
        pygame.display.flip()
        clock.tick(60)#set fps

except StopIteration:
    pass

pygame.quit()
