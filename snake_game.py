import pygame
import sys
import random

pygame.init()

wall_thickness = 10
width = 500 + 2 * wall_thickness
height = 500 + 2 * wall_thickness

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
background_image = pygame.image.load('wall.png')
heading_font = pygame.font.Font('game_over.ttf', 250)
box_font = pygame.font.Font('game_over.ttf', 75)

def GenerateApple(apple_size, width, height):
    apple_x = random.randrange(10, width - (apple_size + 1), apple_size)
    apple_y = random.randrange(10, height - (apple_size + 1), apple_size)
    return apple_x, apple_y

def EatApple(head_rect, apple_rect, width, height, length):
    if head_rect.colliderect(apple_rect):
        apple_x, apple_y = GenerateApple(apple_size, width, height)
        length += 1
        return length, apple_x, apple_y
    return length, apple_rect[0], apple_rect[1]

def MoveSnake(snake, x_change, y_change, lead_x, lead_y, snake_length, size):
    if (lead_x + x_change < wall_thickness or lead_x + size + x_change > width - wall_thickness) or (lead_y + y_change < wall_thickness or lead_y + size + y_change > height - wall_thickness):
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
    for button_num, button in enumerate(button_list):
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

def WriteText(win, rectangle, message, font, ):
    text = font.render(str(message), True, black)
    text_rect = text.get_rect()
    text_rect.center = rectangle.center
    win.blit(text, (text_rect[0], text_rect[1]))

def DrawIntroWindow(win, width, height, buttons, color1, color2, box_width, box_height):
    win.fill(white)
    heading_y = int(((height / 2) / 2) / 2)
    heading_rect = pygame.Rect(0, 0, width, int(height / 2))
    WriteText(win, heading_rect, 'Snake', heading_font)
    DrawButtons(win, width, height, buttons, color1, color2, box_width, box_height)
    WriteText(win, buttons[0], 'Play', box_font)
    WriteText(win, buttons[1], 'Snake Color', box_font)
    WriteText(win, buttons[2], 'Map Color', box_font)
    pygame.display.update()

def DrawGameWindow(win, width, height, bgcolor, snake, snake_size, snake_color, apple_rect, wall_thickness):
    win.blit(background_image, (0, 0))
    pygame.draw.rect(win, red, apple_rect)
    for box in snake:
        pygame.draw.rect(win, snake_color, (box[0], box[1], snake_size, snake_size))
    pygame.draw.rect(win, blue, (0, 0, width, height), wall_thickness)
    pygame.display.update()

button_box_width = 300
button_box_height = 50
button_list = [
    pygame.Rect(int((width - button_box_width) / 2), 225, button_box_width, button_box_height),
    pygame.Rect(int((width - button_box_width) / 2), 325, button_box_width, button_box_height),
    pygame.Rect(int((width - button_box_width) / 2), 425, button_box_width, button_box_height),
    ]

running = True
game_over = True
pressed_button = 0#None

clock = pygame.time.Clock()
'''
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_button, running = CheckClick(button_list)
    DrawIntroWindow(game_window, width, height, button_list, green, red, button_box_width, button_box_height)

    clock.tick(10)
'''
if pressed_button == 0:
    game_over = False

snake_size = 25
x_change = 0
y_change = snake_size
snake_x = int((width - 2 * wall_thickness) / 2) + 10
snake_y = int((height - 2 * wall_thickness) / 2) + 10
snake_length = 1
snake_list = [(snake_x,snake_y)]
head = snake_list[-1]

apple_size = snake_size
apple_x, apple_y = GenerateApple(apple_size, width, height)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_change = -snake_size
                x_change = 0
            elif event.key == pygame.K_DOWN:
                y_change = snake_size
                x_change = 0
            elif event.key == pygame.K_LEFT:
                y_change = 0
                x_change = -snake_size
            elif event.key == pygame.K_RIGHT:
                y_change = 0
                x_change = snake_size
            elif event.key == pygame.K_SPACE:
                snake_length += 1

    snake_x, snake_y, snake_list, game_over = MoveSnake(snake_list, x_change, y_change, snake_x, snake_y, snake_length, snake_size)
    snake_length, apple_x, apple_y = EatApple(pygame.Rect(snake_x, snake_y, snake_size, snake_size), pygame.Rect(apple_x, apple_y, apple_size, apple_size), width, height, snake_length)
    apple_rect = pygame.Rect(apple_x, apple_y, apple_size, apple_size)
    DrawGameWindow(game_window, width, height, black, snake_list, snake_size, green, apple_rect, wall_thickness)

    clock.tick(10)

pygame.quit()
sys.exit()
