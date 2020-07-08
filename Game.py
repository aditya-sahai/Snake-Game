import pygame
from Snake import Snake
from Map import Map


class Game:
    def __init__(self):
        self.WIDTH = 500
        self.HEIGHT = 500

        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.FPS = 15
        self.game_over = False

        self.SCORE_FONT = pygame.font.Font('game_over.ttf', 250)
        self.HEADING_FONT = pygame.font.Font('game_over.ttf', 300)
        self.LENGTH_FONT = pygame.font.Font('game_over.ttf', 50)
        self.selected_layout_number = 0

        self.COLORS = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "red": (255, 50, 50),
            "green": (50, 255, 50),
            "light-blue": (200, 200, 255),
            "background-color": (20, 20, 20),
            "walls-color": (26, 8, 130),
        }

        self.MENU_PLAY_BUTTON_RECT = pygame.Rect(300, 210, 170, 100)
        self.menu_play_button_color = self.COLORS["green"]
        self.play_button_is_pressed = False

        self.BUTTON_FONT = pygame.font.Font("game_over.ttf", 75)

        self.MENU_CONTROL_BUTTON_RECT = pygame.Rect(300, 340, 170, 100)
        self.menu_control_button_color = self.COLORS["green"]
        self.control_button_is_pressed = False

        self.CONTROLS_TEXT_IMAGE = pygame.image.load("Images/controls.png")
        self.CONTROLS_FONT = pygame.font.Font("game_over.ttf", 50)
        self.CONTROLS_HOME_BUTTON_RECT = pygame.Rect(50, 400, 100, 50)
        self.controls_home_button_color = self.COLORS["green"]

        self.NOTE_FONT = pygame.font.Font("game_over.ttf", 50)

        self.Snake = Snake(self.win, self.WIDTH, self.HEIGHT)
        self.Map = Map()

    def check_event_loop(self):
        """Checks the event loop for quitting."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def check_menu_event_loop(self):
        """Checks the event loop."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.selected_layout_number > 0:
                    self.selected_layout_number -= 1
                elif event.key == pygame.K_RIGHT and self.selected_layout_number < 3:
                    self.selected_layout_number += 1
                elif event.key == pygame.K_SPACE or event.key == 13:
                    self.play_button_is_pressed = True
                elif event.key == pygame.K_c:
                    self.control_button_is_pressed = True

    def check_controls_event_loop(self):
        """Checks the menu event loop."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return True
        return False

    def check_game_event_loop(self):
        """Checks the event loop."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8:
                    self.Snake.y_change = -1 * self.Snake.size
                    self.Snake.x_change = 0
                    self.Snake.direction = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP5:
                    self.Snake.y_change = self.Snake.size
                    self.Snake.x_change = 0
                    self.Snake.direction = "down"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4:
                    self.Snake.y_change = 0
                    self.Snake.x_change = -1 * self.Snake.size
                    self.Snake.direction = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6:
                    self.Snake.y_change = 0
                    self.Snake.x_change = self.Snake.size
                    self.Snake.direction = "right"

    def write_center_text(self, font, message, rect, color):
        """Writes the text in the center of the given rectangle."""

        text = font.render(message.strip(), True, color)
        text_rect = text.get_rect()
        text_rect.center = rect.center
        self.win.blit(text, (text_rect[0], text_rect[1]))

    def make_button_responsive(self, button_rect):
        """Returns true if button is pressed and the color of the button."""

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return (True, self.COLORS["red"])
            else:
                return (False, self.COLORS["red"])
        else:
            return (False, self.COLORS["green"])

    def draw_menu_window(self):
        """Draws the menu window."""

        self.win.fill(self.COLORS["light-blue"])
        self.write_center_text(self.HEADING_FONT, "Snake", pygame.Rect(0, 0, self.WIDTH, 150), self.COLORS["black"])
        pygame.draw.rect(self.win, self.menu_play_button_color, self.MENU_PLAY_BUTTON_RECT)
        pygame.draw.rect(self.win, self.menu_control_button_color, self.MENU_CONTROL_BUTTON_RECT)
        self.write_center_text(self.BUTTON_FONT, "Play", self.MENU_PLAY_BUTTON_RECT, self.COLORS["black"])
        self.write_center_text(self.BUTTON_FONT, "Controls", self.MENU_CONTROL_BUTTON_RECT, self.COLORS["black"])
        self.write_center_text(self.NOTE_FONT, "Note: Use Arrow Keys To Change Layout", pygame.Rect(0, 445, self.WIDTH, 55), self.COLORS["black"])
        self.win.blit(self.Map.LAYOUT_IMAGES[self.selected_layout_number], (50, 200))

        pygame.display.update()

    def draw_controls_window(self):
        """Draws the controls window."""

        self.check_controls_event_loop()
        self.win.fill(self.COLORS["light-blue"])
        self.win.blit(self.CONTROLS_TEXT_IMAGE, (0, 0))
        pygame.draw.rect(self.win, self.controls_home_button_color, self.CONTROLS_HOME_BUTTON_RECT)
        self.write_center_text(self.BUTTON_FONT, "Home", self.CONTROLS_HOME_BUTTON_RECT, self.COLORS["black"])
        pygame.display.update()

    def draw_map(self):
        """Draws the walls."""

        for row_num, row in enumerate(self.Map.selected_layout):
            for col_num, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.win, self.COLORS["walls-color"], (col_num * self.Map.WALLTHICKNESS, row_num * self.Map.WALLTHICKNESS, self.Map.WALLTHICKNESS, self.Map.WALLTHICKNESS))
                elif col == 2:
                    pygame.draw.rect(self.win, self.COLORS["red"], (col_num * self.Map.WALLTHICKNESS, row_num * self.Map.WALLTHICKNESS, self.Map.WALLTHICKNESS, self.Map.WALLTHICKNESS))
                    # self.win.blit(self.Map.APPLE_IMAGE, (col_num * self.Map.WALLTHICKNESS, row_num * self.Map.WALLTHICKNESS))

    def draw_game_window(self):
        """Draws the game window."""
        self.win.fill(self.COLORS["background-color"])
        self.Snake.draw_snake()

        self.draw_map()
        self.write_center_text(self.LENGTH_FONT, f"Length: {self.Snake.length}", pygame.Rect(0, 0, self.WIDTH, self.Map.WALLTHICKNESS), self.COLORS["white"])

        pygame.display.update()

    def draw_score_window(self):
        """After dying displays the score of the player."""
        self.win.fill(self.COLORS["black"])
        self.write_center_text(self.SCORE_FONT, f"Score: {self.Snake.length - 1}", pygame.Rect(0, 0, self.WIDTH, self.HEIGHT), self.COLORS["white"])
        pygame.display.update()

    def menu_loop(self):
        """The menu loop which would display the play button and show map options."""

        while True:
            self.play_button_is_pressed, self.menu_play_button_color = self.make_button_responsive(self.MENU_PLAY_BUTTON_RECT)
            self.control_button_is_pressed, self.menu_control_button_color = self.make_button_responsive(self.MENU_CONTROL_BUTTON_RECT)
            self.check_menu_event_loop()

            if self.play_button_is_pressed:
                self.Snake = Snake(self.win, self.WIDTH, self.HEIGHT)
                self.Map = Map()
                self.Map.selected_layout = self.Map.LAYOUTS[self.selected_layout_number]
                self.Map.generate_apple()
                return "play"

            elif self.control_button_is_pressed:
                return "controls"

            self.draw_menu_window()
            self.clock.tick(self.FPS)

    def controls_loop(self):
        """Controls loop which would only display the controls."""

        while True:
            pressed_home_key = self.check_controls_event_loop()
            pressed_home_button, self.controls_home_button_color = self.make_button_responsive(self.CONTROLS_HOME_BUTTON_RECT)

            if pressed_home_key or pressed_home_button:
                break

            self.draw_controls_window()
            self.clock.tick(self.FPS)

    def game_loop(self):
        """Game loop."""

        while not self.game_over:
            self.check_game_event_loop()
            snake_apple_collide = self.Snake.move(self.Map.selected_layout, self.Map.WALLTHICKNESS)

            if snake_apple_collide:
                self.Map.generate_apple()

            self.game_over = self.Snake.check_collision(self.Map.selected_layout, self.Map.WALLTHICKNESS)
            self.draw_game_window()
            self.clock.tick(self.FPS)

        start_time = pygame.time.get_ticks()
        spent_time = pygame.time.get_ticks() - start_time

        self.draw_score_window()

        while spent_time < 2500:
            self.check_event_loop()
            spent_time = pygame.time.get_ticks() - start_time
            self.clock.tick(self.FPS)

    def main(self):
        """Main game."""

        while True:
            pressed_button = self.menu_loop()

            if pressed_button == "play":
                self.game_loop()

            elif pressed_button == "controls":
                self.controls_loop()

            self.game_over = False
        pygame.quit()


if __name__ == "__main__":
    SnakeGame = Game()
    SnakeGame.main()
