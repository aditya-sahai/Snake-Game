import pygame
import sys
import random

pygame.init()

wall_thickness = 25
width = 500 + 2 * wall_thickness
height = 500 + 2 * wall_thickness

red_head_img = pygame.image.load('red_head.png')
green_head_img = pygame.image.load('green_head.png')
blue_head_img = pygame.image.load('blue_head.png')
yellow_head_img = pygame.image.load('yellow_head.png')
magenta_head_img = pygame.image.load('magenta_head.png')
head_images = [red_head_img, green_head_img, blue_head_img, yellow_head_img, magenta_head_img]

map_1_img = pygame.image.load('map_1.png')
map_2_img = pygame.image.load('map_2.png')
map_3_img = pygame.image.load('map_3.png')
map_4_img = pygame.image.load('map_4.png')
map_images = [map_1_img, map_2_img, map_3_img, map_4_img]

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
magenta = (200, 0 ,200)
white = (255, 255, 255)
black = (0, 0, 0)
color_list = [red, green, blue, yellow, magenta]

game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
pygame.display.set_icon(green_head_img)

heading_font = pygame.font.Font('game_over.ttf', 250)
box_font = pygame.font.Font('game_over.ttf', 75)
score_font = pygame.font.Font('game_over.ttf',60)

def MakeColorButtons(snake_size):
    color_button_list = []
    for y in range(62, 476, 100):
        color_button_list.append(pygame.Rect(100, y, snake_size[0], snake_size[1]))
    return color_button_list

def GenerateApple(apple_size, width, height, wall_thickness, map):
    apple_x = random.randrange(wall_thickness, width - (apple_size + 1), apple_size)
    apple_y = random.randrange(wall_thickness, height - (apple_size + 1), apple_size)
    for rect in map:
        if rect.colliderect((apple_x, apple_y, apple_size, apple_size)):
            apple_y += apple_size
    return apple_x, apple_y

def EatApple(head_rect, apple_rect, width, height, length, wall_thickness, wall_rects):
    if head_rect.colliderect(apple_rect):
        apple_x, apple_y = GenerateApple(apple_size, width, height, wall_thickness, wall_rects)
        length += 1
        return length, apple_x, apple_y
    return length, apple_rect[0], apple_rect[1]

def MoveSnake(snake, x_change, y_change, lead_x, lead_y, snake_length, size, wall_rects):
    for rect in wall_rects:
        if pygame.Rect(snake[-1][0], snake[-1][1], size, size).colliderect(rect):
            return lead_x, lead_y, snake, True

    lead_x += x_change
    lead_y += y_change
    head = (lead_x, lead_y)
    snake.append(head)

    if len(snake) > snake_length:
        del snake[0]
    for segment in snake[:-1]:
        if segment == head:
            return lead_x, lead_y, snake, True
    return lead_x, lead_y, snake, False

def CheckClick(buttons):
    mouse_pos = pygame.mouse.get_pos()
    for button_num, button in enumerate(buttons):
        if button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            return (button_num, False)
    return (None, True)

def DrawButtons(win, width, height, buttons, color1, color2, box_width, box_height):
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.collidepoint(mouse_pos):
            pygame.draw.rect(win, color2, button)
        elif not button.collidepoint(mouse_pos):
            pygame.draw.rect(win, color1, button)

def WriteText(win, rectangle, message, font, color):
    text = font.render(str(message), True, color)
    text_rect = text.get_rect()
    text_rect.center = rectangle.center
    win.blit(text, (text_rect[0], text_rect[1]))

def DrawIntroWindow(win, width, height, buttons, color1, color2, box_width, box_height):
    win.fill(white)
    heading_y = int(((height / 2) / 2) / 2)
    heading_rect = pygame.Rect(0, 0, width, int(height / 2))
    WriteText(win, heading_rect, 'Snake', heading_font, black)
    DrawButtons(win, width, height, buttons, color1, color2, box_width, box_height)
    WriteText(win, buttons[0], 'Play', box_font, black)
    WriteText(win, buttons[1], 'Snake Color', box_font, black)
    WriteText(win, buttons[2], 'Change Map', box_font, black)
    pygame.display.update()

def DrawGameWindow(win, width, height, bgcolor, snake, snake_size, snake_color, apple_rect, wall_rects, score, head_img):
    win.fill(black)
    for wall in wall_rects:
        pygame.draw.rect(win, blue  , wall)
    pygame.draw.rect(win, red, apple_rect)
    win.blit(head_img, (snake[-1]))
    for box in snake[:-1]:
        pygame.draw.rect(win, snake_color, (box[0], box[1], snake_size, snake_size))
    score_rect = wall_rects[1]#pygame.Rect(width - int(width / 3), height - int(height / 5), int(width / 4), int(height / 4))
    WriteText(win, score_rect, 'Score: ' + str(score), score_font, white)
    pygame.display.update()

def DrawColorWindow(win, width, height, color_buttons, color_list, snake_head_images, wall_rects):
    win.fill(black)
    for wall in wall_rects[:4]:
        pygame.draw.rect(win, blue, wall)

    for index, snake in enumerate(color_buttons):
        pygame.draw.rect(win, color_list[index], snake)
        rotated_img = pygame.transform.rotate(snake_head_images[index], -90)
        win.blit(rotated_img, (snake[0] + (snake[2] - snake[3]), snake[1]))
    pygame.display.update()

def DrawMapWindow(win, map_images):
    win.fill(black)
    win.blit(map_images[0], (0, 0))
    win.blit(map_images[1], (275, 0))
    win.blit(map_images[2], (0, 275))
    win.blit(map_images[3], (275, 275))
    pygame.draw.line(win, white, (int(width / 2), 0), (int(width / 2), height))
    pygame.draw.line(win, white, (0, int(height / 2)), (width, int(height / 2)))
    pygame.display.update()

button_box_width = 300
button_box_height = 50
main_button_list = [
    pygame.Rect(int((width - button_box_width) / 2), 225, button_box_width, button_box_height),
    pygame.Rect(int((width - button_box_width) / 2), 325, button_box_width, button_box_height),
    pygame.Rect(int((width - button_box_width) / 2), 425, button_box_width, button_box_height),
    ]

snake_size = 25
x_change = snake_size
y_change = 0
snake_x = int(width / 2)
snake_y = int(height / 2)
direction = 'right'
snake_length = 1
snake_list = [(snake_x,snake_y)]
head = snake_list[-1]

map_1 = [
    pygame.Rect(0, 0, wall_thickness, height),
    pygame.Rect(0, 0, width, wall_thickness),
    pygame.Rect(width - wall_thickness, 0, wall_thickness, height),
    pygame.Rect(0, height - wall_thickness, width, wall_thickness),
    pygame.Rect(0, snake_y, int((width - 2 * wall_thickness) / 2) - snake_size, wall_thickness),
    pygame.Rect(snake_x + 3 * snake_size, snake_y - 3 * snake_size, int(width / 2 - wall_thickness), wall_thickness)
    ]

map_2 = [
    pygame.Rect(0, 0, wall_thickness, height),
    pygame.Rect(0, 0, width, wall_thickness),
    pygame.Rect(width - wall_thickness, 0, wall_thickness, height),
    pygame.Rect(0, height - wall_thickness, width, wall_thickness),
    ]

map_3 = [
    pygame.Rect(0, 0, wall_thickness, height),
    pygame.Rect(0, 0, width, wall_thickness),
    pygame.Rect(width - wall_thickness, 0, wall_thickness, height),
    pygame.Rect(0, height - wall_thickness, width, wall_thickness),
    pygame.Rect(wall_thickness, 200, 250, wall_thickness),
    pygame.Rect(350, 200, 175, wall_thickness),
    pygame.Rect(wall_thickness, 350, 50, wall_thickness),
    pygame.Rect(150, 350, 375, wall_thickness),
    ]

map_4 = [
    pygame.Rect(0, 0, wall_thickness, height),
    pygame.Rect(0, 0, width, wall_thickness),
    pygame.Rect(width - wall_thickness, 0, wall_thickness, height),
    pygame.Rect(0, height - wall_thickness, width, wall_thickness),
    pygame.Rect(100, 125, 350, wall_thickness),
    pygame.Rect(150, 300, 250, wall_thickness),
    pygame.Rect(100, 400, 350, wall_thickness),
    ]

maps = [map_1, map_2, map_3, map_4]

map_rects = [
    pygame.Rect(0, 0, int(width / 2), int(height / 2)),
    pygame.Rect(int(width / 2), 0, int(width / 2), int(height / 2)),
    pygame.Rect(0, int(height / 2), int(width / 2), int(height / 2)),
    pygame.Rect(int(width / 2), int(height / 2), int(width / 2), int(height / 2)),
    ]

color_button_list = MakeColorButtons((width - 100 * 2,snake_size))

game_exit = False
intro_running = True
game_over = True
color_running = False
map_running = False
pressed_button = None
pressed_color_button = 1
pressed_map_button = 0
snake_head_img = head_images[pressed_color_button]

apple_size = snake_size
apple_x, apple_y = GenerateApple(apple_size, width, height, wall_thickness, maps[pressed_map_button])

clock = pygame.time.Clock()

while not game_exit:

    while intro_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                game_over = True
                intro_running = False

        if intro_running == True:
            pressed_button, intro_running = CheckClick(main_button_list)
        DrawIntroWindow(game_window, width, height, main_button_list, green, red, button_box_width, button_box_height)

        clock.tick(10)

    if pressed_button == 0 and game_over == False:
        game_over = False
        color_running = False
        map_running = False
    elif pressed_button == 1:
        color_running = True
        game_over = True
        map_running = False
    elif pressed_button == 2:
        game_over = True
        color_running = False
        map_running = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -snake_size
                    x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    y_change = snake_size
                    x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    y_change = 0
                    x_change = -snake_size
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    y_change = 0
                    x_change = snake_size
                    direction = 'right'

        if direction == 'up':
            rotated_head_img = pygame.transform.rotate(snake_head_img, 0)
        elif direction == 'down':
            rotated_head_img = pygame.transform.rotate(snake_head_img, 180)
        elif direction == 'left':
            rotated_head_img = pygame.transform.rotate(snake_head_img, 90)
        elif direction == 'right':
            rotated_head_img = pygame.transform.rotate(snake_head_img, -90)

        if game_over == False:
            snake_x, snake_y, snake_list, game_over = MoveSnake(snake_list, x_change, y_change, snake_x, snake_y, snake_length, snake_size, maps[pressed_map_button])
        snake_head_rect = pygame.Rect(snake_x, snake_y, snake_size, snake_size)
        apple_rect = pygame.Rect(apple_x, apple_y, apple_size, apple_size)
        snake_length, apple_x, apple_y = EatApple(snake_head_rect, apple_rect, width, height, snake_length, wall_thickness, maps[pressed_map_button])
        DrawGameWindow(game_window, width, height, black, snake_list, snake_size, color_list[pressed_color_button], apple_rect, maps[pressed_map_button], snake_length - 1, rotated_head_img)

        if game_over == True:
            i = 1
            while i <= 20:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_exit = True
                        color_running = False
                        intro_running = False

                if game_exit:
                    break

                game_window.fill(black)
                WriteText(game_window, pygame.Rect(wall_thickness, wall_thickness, width - wall_thickness * 2, height - wall_thickness * 2), 'Score: ' + str(snake_length - 1), heading_font, white)
                pygame.display.update()

                i += 1
                clock.tick(10)

        clock.tick(10)

    while color_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                intro_running = False
                game_over = True
                color_running = False

        if color_running == True:
            pressed_color_button, color_running = CheckClick(color_button_list)
        DrawColorWindow(game_window, width, height, color_button_list, color_list, head_images, map_1)
        clock.tick(10)

    while map_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                map_running = False
                intro_running = False
                game_over = True
                game_exit = True

        if map_running:
            pressed_map_button, map_running = CheckClick(map_rects)
        DrawMapWindow(game_window, map_images)
        clock.tick(10)

    game_over = False
    intro_running = True
    color_running = False
    pressed_button = None

    snake_head_img = head_images[pressed_color_button]

    x_change = snake_size
    y_change = 0
    snake_x = int(width / 2)
    snake_y = int(height / 2)
    direction = 'right'
    snake_length = 1
    snake_list = [(snake_x,snake_y)]
    head = snake_list[-1]

pygame.quit()
sys.exit()
