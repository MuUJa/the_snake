import random
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    position: tuple[int, int]
    body_color: tuple[int, int, int]

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инициализация игрового объекта.

        :param body_color: цвет объекта (R, G, B)
        """
        self.body_color = body_color
        self.position = position

    def draw(self, display):
        """
        Отрисовывает объект на экране.

        :param display: поверхность для отрисовки
        """
        pass

    @staticmethod
    def _to_screen(position: tuple[int, int], cell=GRID_SIZE):
        assert len(position) == 2
        return position[0] * cell, position[1] * cell


class Snake(GameObject):
    """Класс для объекта 'Змейка'."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """
        Инициализация змейки.

        :param position: начальная позиция змейки (x, y)
        :param body_color: цвет змейки
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку в направлении движения."""
        head_x, head_y = self.position
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT
        )

        self.position = new_head
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        self.length += 1

    def draw(self, display):
        """
        Отрисовывает змейку на экране.

        :param display: поверхность для отрисовки
        """
        for position in self.positions:
            rect = pygame.Rect(GameObject._to_screen(position),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(display, self.body_color, rect)
            pygame.draw.rect(display, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.position

    def reset(self, position):
        """Сбрасывает состояние змейки в исходное."""
        self.length = 1
        self.position = position
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Класс для объекта 'Яблоко'."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        """
        Инициализация яблока.

        :param position: начальная позиция яблока (x, y)
        :param body_color: цвет яблока
        """
        super().__init__(position, body_color)
        self.body_color = body_color
        self.randomize_position()

    def draw(self, display):
        """
        Отрисовывает яблоко на экране.

        :param display: поверхность для отрисовки
        """
        rect = pygame.Rect(GameObject._to_screen(self.position),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(display, self.body_color, rect)
        pygame.draw.rect(display, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake: Snake = None):
        """Устанавливает произвальную позицию яблоку.

        :param snake: Используется для выбора незанятых змеёй клеток
        """
        if snake is None:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            return

        cells = [[0 for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        for x, y in snake.positions:
            cells[x][y] = 1
        empty_cells = [(i, j)
                       for i in range(GRID_WIDTH)
                       for j in range(GRID_HEIGHT)
                       if cells[i][j] == 0
                       ]

        self.position = random.choice(empty_cells)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления змейки.

    :param snake: объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """
    Главная функция игры.

    Инициализирует объекты и запускает игровой цикл.
    """
    pygame.init()

    snake = Snake(GRID_CENTER)
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset(GRID_CENTER)

        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            3
        )

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
