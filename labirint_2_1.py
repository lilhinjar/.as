import pygame
import pygame_widgets
import random
import time
import sys

pygame.init()
font1 = pygame.font.SysFont("comicsansms", 49, True)
font2 = pygame.font.SysFont("comicsansms", 150, True)
font3 = pygame.font.SysFont("comicsansms", 28, True)
from pygame_widgets.button import Button

wallWidth = 8

screenWidth = 400
screenHeigth = 400
screen = pygame.display.set_mode((900, 900))
green = (0, 255, 0)

levels = {
    1: {
        "screen": {
            "width": 400,
            "length": 400
        },
        "labirintSize": 12
    },
    2: {
        "screen": {
            "width": 600,
            "length": 600
        },
        "labirintSize": 18
    },
    3: {
        "screen": {
            "width": 800,
            "length": 800
        },
        "labirintSize": 24
    }
}


def our_snake(snake_block, snake_list):
    for x in snake_list:
        print(snake_list)
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])


def get_time(hours, minutes, seconds):
    if len(str(hours)) > 1:
        a = str(hours)
    else:
        a = "0" + str(hours)

    if len(str(minutes)) > 1:
        b = str(minutes)
    else:
        b = "0" + str(minutes)

    if len(str(seconds)) > 1:
        c = str(seconds)
    else:
        c = "0" + str(seconds)

    return a + ":" + b + ":" + c


def draw_time(start_time, pause_time):
    hours = 0
    minutes = 0
    seconds = 0
    current_time = time.time() - pause_time - start_time
    if current_time > 3600:
        while True:
            if current_time - 3600 > 0:
                hours += 1
                current_time -= 3600
            else:
                while True:
                    if current_time - 60 > 0:
                        minutes += 1
                        current_time -= 60
                    else:
                        seconds += int(current_time)
                        break
                break

    else:
        while True:
            if current_time - 60 > 0:
                minutes += 1
                current_time -= 60
            else:
                seconds += int(current_time)
                break

    return [font1.render(get_time(hours, minutes, seconds), True, (0, 0, 0), (255, 255, 255)),
            get_time(hours, minutes, seconds)]


class cell:
    def __init__(self, up, down, left, right):
        self.visited = False
        self.walls = [up, down, left, right]


class labyrinth:
    def __init__(self, id, level):
        self.id = id
        self.walls = []
        self.maze_walls = []
        self.cells = []

        x = 0
        t = 0

        for f in range(levels[level]["labirintSize"]):
            for s in range(levels[level]["labirintSize"]):
                if not (f in (0, 1, 2) and s > levels[level]["labirintSize"]):
                    self.cells.append(cell((x + wallWidth, t, 25, wallWidth), (x + wallWidth, t + 33, 25, wallWidth),
                                           (x, t + wallWidth, wallWidth, 25), (x + 33, t + wallWidth, wallWidth, 25)))
                x += 33
            x = 0
            t += 33

        for v in self.cells[0].walls:
            self.maze_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while len(self.walls) > 0:
            wall = random.choice(self.walls)
            divided_cells = []
            for u in self.cells:
                if wall in u.walls:
                    divided_cells.append(u)

            if len(divided_cells) > 1 and (not ((divided_cells[0].visited and divided_cells[1].visited) or (
                    (not divided_cells[0].visited) and (not divided_cells[1].visited)))):
                for k in divided_cells:
                    k.walls.remove(wall)

                    if k.visited == False:
                        k.visited = True

                    for q in k.walls:
                        if not q in self.walls:
                            self.walls.append(q)

                        if not q in self.maze_walls:
                            self.maze_walls.append(q)

                    if wall in self.maze_walls:
                        self.maze_walls.remove(wall)

            self.walls.remove(wall)

        for j in range(0, levels[level]["screen"]["width"], 33):
            for i in range(0, levels[level]["screen"]["length"], 33):
                self.maze_walls.append((i, j, wallWidth, wallWidth))

    def draw(self, goal):
        screen.fill((0, 0, 0))

        for k in self.maze_walls:
            pygame.draw.rect(screen, color, pygame.Rect(k[0], k[1], k[2], k[3]))

        pygame.draw.rect(screen, (0, 255, 0), goal)


id = 0
running = True


def start_game(level):
    global screen, color, running, id, menuDone
    menuDone = False
    screen.fill((0, 0, 0))
    while running:
        screen = pygame.display.set_mode((levels[level]["screen"]["width"], levels[level]["screen"]["length"]))
        done = False
        color = (0, 128, 255)
        x = 16
        y = 16
        clock = pygame.time.Clock()
        id += 1
        maze = labyrinth(id, level)
        goal = pygame.Rect(levels[level]["screen"]["width"] - 30, levels[level]["screen"]["length"] - 30, 25, 25)
        victory = False
        speed = 4
        pause = False
        pause_time = 0
        x_change = 0
        y_change = 0
        moving_up = False
        moving_down = False
        moving_left = False
        moving_right = False
        isStart = False

        print(x, y)

        while not done:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    done = True
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        if pause:
                            pause = False
                            pause_time += time.time() - pause_time_start
                        else:
                            pause = True
                            pause_time_start = time.time()

                    if event.key == pygame.K_RETURN:
                        done = True

            if pause:
                showMenu()

            if not victory and not pause:
                move_up = True
                move_down = True
                move_left = True
                move_right = True

                pressed = pygame.key.get_pressed()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        isStart = True
                        moving_up = True
                        y_change = -speed
                        x_change = 0



                    elif event.key == pygame.K_DOWN:
                        isStart = True

                        moving_down = True
                        y_change = speed
                        x_change = 0


                    elif event.key == pygame.K_LEFT:
                        isStart = True

                        moving_left = True
                        x_change = -speed
                        y_change = 0



                    elif event.key == pygame.K_RIGHT:
                        isStart = True

                        moving_right = True
                        x_change = speed
                        y_change = 0

                if goal.colliderect((x, y, 10, 10)):
                    victory = True
                maze.draw(goal)
            player = pygame.Rect(x, y - speed, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                    move_up = False
                    break
            player = pygame.Rect(x, y - speed, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                    move_down = False
                    break

            player = pygame.Rect(x - speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                    move_left = False
                    break

            player = pygame.Rect(x + speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                    move_right = False
                    break

            isMove = ((moving_right and move_right) or (moving_up and move_up) or (moving_left and move_left) or (
                        moving_down and move_down))

            print(isMove)
            if (not (isMove) and isStart):
                showMenu()
            x += x_change
            y += y_change

            pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x, y, 10, 10))

            if victory:
                screen.fill((0, 0, 0))
                showMenu()

            pygame.display.flip()
            pygame.display.update()
            clock.tick(15)
        pygame.quit()


def showMenu():
    global screen, running, menuDone
    screen = pygame.display.set_mode((900, 900))
    screen.fill((0, 0, 0))

    menuDone = False

    while running:
        while not menuDone:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    menuDone = True
                    running = False
            pygame_widgets.update(event)
            pygame.display.update()

            Button(
                screen,
                900 / 2 - 75,
                900 / 2 - 225,
                150,
                90,

                text='Level 1',
                fontSize=50,
                margin=20,
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=lambda: start_game(1)
            )
            Button(
                screen,
                900 / 2 - 75,
                900 / 2 - 125,
                150,
                90,

                text='Level 2',
                fontSize=50,
                margin=20,
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=lambda: start_game(2)
            )
            Button(
                screen,
                900 / 2 - 75,
                900 / 2 - 25,
                150,
                90,

                text='Level 3',
                fontSize=50,
                margin=20,
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=lambda: start_game(3)
            )
            Button(
                screen,
                900 / 2 - 75,
                900 / 2 + 175,
                150,
                90,
                text='Выход',
                fontSize=50,
                margin=20,
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=quitGame
            )
            Button(
                screen,
                900 / 2 - 75,
                900 / 2 + 75,
                150,
                90,
                text='Правила', 
                fontSize=50,
                margin=20,
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=show_rules 
            )
    pygame.quit()


def show_rules():
    screen = pygame.display.set_mode((1400, 900))

    screen.fill((0, 0, 0))  

    
    rules_text = [
        "Цель игры: Вашей целью является управление змейкой и прохождение через лабиринт,",
        "избегая столкновений со стенами и собственным хвостом.",
        "Управление змейкой:",
        "Вы можете управлять змейкой, используя стрелки на клавиатуре (вверх, вниз, влево, вправо).",
        "Избегание столкновений:",
        "Избегайте столкновений со стенами лабиринта",
        "и собственным хвостом. Столкновение приводит к поражению.",
        "Цель и победа: Вашей целью является пройти через лабиринт.",
        "Если вы дошли до выхода, это означает вашу победу.",
        "Уровни сложности:",
        "Игра предоставляет несколько уровней сложности,",
        "с различными размерами лабиринта и скоростью змейки.",
        "Завершение игры:",
        "Игра может быть завершена, если вы проигрываете",
        "(сталкиваетесь со стенами или собственным хвостом)",
        "или вы выигрываете (проходите лабиринт).",
        "Победа и поражение:",
        "если вы проходите лабиринт, это считается вашей победой.",
        "Если вы не можете сделать это и сталкиваетесь со стенами или хвостом,",
        "это означает ваше поражение."
    ]


    text_y = 50  
    for line in rules_text:
        text_surface = font3.render(line, False, (255, 255, 255))
        screen.blit(text_surface, (0, text_y))
        text_y += 30

    pygame.display.flip()  


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.display.set_mode((900, 900))
                screen.fill((0, 0, 0))  
            elif event.type == pygame.KEYDOWN:
                waiting = False
                pygame.display.set_mode((900, 900))
                screen.fill((0, 0, 0)) 


def quitGame():
    pygame.quit()
    sys.exit()


showMenu()
