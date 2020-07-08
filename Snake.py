import pygame


class Snake:
    def __init__(self, game_win, width, height):
        self.game_win = game_win
        self.size = 25

        self.direction = "right"

        self.x_change = 25
        self.y_change = 0
        self.x = width // 2 - self.size
        self.y = height // 2 - self.size

        self.snake_list = [(self.x, self.y, self.size, self.size)]
        self.length = 1

        self.HEAD_IMG = pygame.image.load("Images/snake-head.png")
        self.rotated_head_img = self.HEAD_IMG

    def check_collision(self, walls, wallthickness):
        """Checks for collision with the given list of rects."""
        snake_head = pygame.Rect(self.snake_list[-1])

        for row_num, row in enumerate(walls):
            for col_num, col in enumerate(row):
                if col == 1:
                    wall_rect =  pygame.Rect(col_num * wallthickness, row_num * wallthickness, wallthickness, wallthickness)
                    if snake_head.colliderect(wall_rect):
                        return True

        for segment in self.snake_list[:-1]:
            if segment == snake_head:
                return True

        return False

    def move(self, walls, wallthickness):
        """Moves the snake."""

        self.x += self.x_change
        self.y += self.y_change
        self.snake_list.append((self.x, self.y, self.size, self.size))


        if len(self.snake_list) > self.length:
            del self.snake_list[0]

        return self.check_apple_pos(walls, wallthickness)

    def rotate_snake_head(self):
        """Rotates the head of the snake according to the direction."""

        if self.direction == "up":
            self.rotated_head_img = self.HEAD_IMG

        elif self.direction == "down":
            self.rotated_head_img = pygame.transform.rotate(self.HEAD_IMG, 180)

        elif self.direction == "left":
            self.rotated_head_img = pygame.transform.rotate(self.HEAD_IMG, 90)

        elif self.direction == "right":
            self.rotated_head_img = pygame.transform.rotate(self.HEAD_IMG, -90)

    def draw_snake(self):
        """Draws the snake on the screen."""

        self.rotate_snake_head()

        for segment in self.snake_list[:-1]:
            pygame.draw.rect(self.game_win, (50, 255, 50), segment)

        self.game_win.blit(self.rotated_head_img, (self.x, self.y))

    def get_apple_pos(self, walls, wallthickness):
        """Returns the rect of the apple."""

        for row_num, row in enumerate(walls):
            for col_num, col in enumerate(row):
                if col == 2:
                    apple_rect = pygame.Rect((col_num * wallthickness, row_num * wallthickness, wallthickness, wallthickness))
                    return apple_rect

    def check_apple_pos(self, walls, wallthickness):
        """Checks if the snake's head collides with the apple."""
        snake_head = pygame.Rect(self.snake_list[-1])
        apple_rect = self.get_apple_pos(walls, wallthickness)

        if snake_head.colliderect(apple_rect):
            self.length += 1
            return True

        return False


if __name__ == "__main__":
    Player = Snake()
