import random
from pydantic import BaseModel
import pygame

class Teleporter(BaseModel):
    x: int
    y: int
    target_x: int
    target_y: int

class FireBall(BaseModel):
    x: int
    y: int
    damage: int
    direction: str

class Skeleton(BaseModel):
    x: int
    y: int
    damage: int
    direction: str
    health: int = 3

class Boss(BaseModel):
    x: int
    y: int
    damage: int
    direction: str
    health: float = 3.0

class Snake(BaseModel):
    x: int
    y: int
    damage: int
    direction: str
    health: int = 5

class DamageIcon(BaseModel):
    x: int
    y: int
    # image: str
    counter: int
    text: str

class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    fireballs: list[FireBall] = []
    skeletons: list[Skeleton] = []
    snakes: list[Snake] = []
    boss: list[Boss] = []

class DungeonGame(BaseModel):
    status: str = "running"
    x: int = 8
    y: int = 1
    coins: int = 0
    health: int = 1
    items: list[str] = []  # inventory
    current_level: Level
    level_number: int = 0
    damages: list[DamageIcon] = []
    armor: int = 0
    sword: int = 0

def move_player(game, direction: str) -> None:
    new_x, new_y = get_next_position(game.x, game.y, direction)

    can_walk_through = ".td€a"
    if game.current_level.level[new_y][new_x] in can_walk_through:
        game.x = new_x
        game.y = new_y

    if game.current_level.level[new_y][new_x] == "x":
        game.level_number += 1
        if game.level_number < len(LEVELS):
        # move to next level
            game.current_level = LEVELS[game.level_number]
        else:
        # no more levels left
            game.status = "finished"

    if game.current_level.level[new_y][new_x] == "€":
        game.current_level.level[new_y][new_x] = "."
        soundObj = pygame.mixer.Sound("coin.mp3")
        soundObj.play()
        game.coins += 1

    if game.current_level.level[new_y][new_x] == "a":
        game.current_level.level[new_y][new_x] = "."
        game.armor += 1

    if game.current_level.level[new_y][new_x] == "s":
        game.current_level.level[new_y][new_x] = "."
        game.sword += 1

    if game.current_level.level[new_y][new_x] == "c":
        game.current_level.level[new_y][new_x] = "."
        item = "key"
        if item == "key":
            game.items.append("key")

    if game.current_level.level[new_y][new_x] == "t":
        if "key" in game.items:
            game.items.remove("key")
        if game.armor > 0:
            game.armor -= 1
        else:
            game.health -= 1

        damage = DamageIcon(
            x=new_x,
            y=new_y,
            # image = random.choice(["prompt_no", "prompt_yes"]),
            counter=100,
            text = "Ouch!",
        )
        game.damages.append(damage)

    # collecting key
    collect_key = "k"
    if game.current_level.level[new_y][new_x] in collect_key:
        game.current_level.level[new_y][new_x] = "."
        game.items.append("key")
        game.x = new_x
        game.y = new_y

    # health potion
    if game.current_level.level[new_y][new_x] == "p":
        game.current_level.level[new_y][new_x] = "."
        game.health += 1

    if game.current_level.level[new_y][new_x] == "y":
        game.current_level.level[new_y][new_x] = "."
        game.coins += 100

    # open closed door
    if "key" in game.items and game.current_level.level[new_y][new_x] == "D":
        game.items.remove("key")  # key can be used once
        game.current_level.level[new_y][new_x] = "d"  # opens closed door

def parse_level(level):
    return [list(row) for row in level]

LEVEL_ONE = Level(
    level = parse_level(
        [
            "#############",
            "#........t..#",
            "#...t....a..#",
            "#..#.#..#s#t#",
            "#k.D.#..#.#t#",
            "#..#..t.#.#t#",
            "#.##p.#€€.#t#",
            "#.#t..###D#t#",
            "#.....k....x#",
            "#############",
        ]
    ),

    teleporters = [Teleporter(x = 4, y = 3, target_x = 6, target_y = 8)],

    fireballs = [
        FireBall(x = 1, y = 2, direction = "right", damage = 1),
        FireBall(x = 1, y = 8, direction = "left", damage = 1),
    ],

    skeletons = [
        Skeleton(x = 4, y = 8, direction = "left", damage = 1),
        Skeleton(x = 7, y = 8, direction = "up", damage = 1),
    ],
)

LEVEL_TWO = Level(
    level = parse_level(
        [
            "#############",
            "#.D...tttt.x#",
            "#.#.#.##.p.##",
            "#.#.#.###..##",
            "#.#.#...##.##",
            "#.#.###....##",
            "#.#..########",
            "#€##....#####",
            "#y#####.....#",
            "#############",
        ]
    ),

    fireballs = [
        FireBall(x = 1, y = 1, direction = "down", damage = 1),
    ],

    snakes = [
        Snake(x = 4, y = 6, direction = "left", damage = 2),
        Snake(x = 10, y = 3, direction = "up", damage = 2),
    ],
)

LEVEL_THREE = Level(
    level = parse_level(
        [
            "#############",
            "#.tttttttt..#",
            "#.########.##",
            "#.#........##",
            "#.#......####",
            "#.#..c.a.#t##",
            "#.#......#t##",
            "#.#D######t##",
            "#..........x#",
            "#############",
        ]
    ),
    
    teleporters = [Teleporter(x = 3, y = 3, target_x = 1, target_y = 8)],
    
    fireballs = [
        FireBall(x = 1, y = 8, direction = "down", damage = 1),
    ],

    skeletons = [
        Skeleton(x = 1, y = 8, direction = "up", damage = 1),
        Skeleton(x = 7, y = 8, direction = "left", damage = 1),
    ],
    
    snakes = [
        Snake(x = 3, y = 6, direction = "right", damage = 1),
        Snake(x = 8, y = 6, direction = "left", damage = 1),
    ],
)

LEVEL_FOUR = Level(
    level = parse_level(
        [
            "#############",
            "#y.........x#",
            "#tt..#.#..tt#",
            "#t.###.###.t#",
            "#t.#.....#.t#",
            "#t.#.....#.t#",
            "#t.###.###.t#",
            "#t...#D#...t#",
            "#p..........#",
            "#############",
        ]
    ),

    snakes = [
        Snake(x = 1, y = 8, direction = "left", damage = 2),
        Snake(x = 10, y = 3, direction = "up", damage = 2),
        Snake(x = 2, y = 1, direction = "down", damage = 2),
    ],

    boss = [
        Boss(x = 5, y = 6, direction = "left", damage = 3)
    ]
)

LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, LEVEL_FOUR]

def check_teleporters(game):
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y == t.y:
            game.x = t.target_x
            game.y = t.target_y

def get_next_position(x, y, direction):
    if direction == "right" and x < 11:
        x += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < 11:
        y += 1
    return x, y

def move_fireball(game):
    for f in game.current_level.fireballs:
        new_x, new_y = get_next_position(f.x, f.y, f.direction)
        if (game.current_level.level[new_y][new_x] in ".€kdDdtay"):
            f.x, f.y = new_x, new_y
        elif game.current_level.level[new_y][new_x] == "#" or game.current_level.level[new_y][new_x] == "x":
            if f.direction == "up":
                f.direction = "down"
            elif f.direction == "down":
                f.direction = "up"
            elif f.direction == "left":
                f.direction = "right"
            elif f.direction == "right":
                f.direction = "left"

def check_collision(game):
    for f in game.current_level.fireballs:
        if f.x == game.x and f.y == game.y:
            if game.armor > 0:
                game.armor -= 1
            else:
                game.health -= f.damage

    for s in game.current_level.skeletons:
        if s.x == game.x and s.y == game.y:
            if game.armor > 0:
                game.armor -= 1
            else:
                game.health -= s.damage

    for i in game.current_level.snakes:
        if i.x == game.x and i.y == game.y:
            if game.armor > 0:
                game.armor -= 1
            else:
                game.health -= i.damage

    for b in game.current_level.boss:
        if b.x == game.x and b.y == game.y:
            if game.armor > 0:
                game.armor -= 2
            else:
                game.health -= b.damage

def move_skeleton(game):
    for s in game.current_level.skeletons:
        s.direction = random.choice(["up", "down", "left", "right"])
        new_x, new_y = get_next_position(s.x, s.y, s.direction)
        if game.current_level.level[new_y][new_x] in ".€ktp":  # moves over coins, keys, traps, potion
            s.x, s.y = new_x, new_y
        elif game.current_level.level[new_y][new_x] == "#":
            if s.direction == "up":
                s.direction = "down"
            elif s.direction == "down":
                s.direction = "up"
            elif s.direction == "left":
                s.direction = "right"
            elif s.direction == "right":
                s.direction = "left"

def move_snake(game):
    for s in game.current_level.snakes:
        s.direction = random.choice(["up", "down", "left", "right"])
        new_x, new_y = get_next_position(s.x, s.y, s.direction)
        if game.current_level.level[new_y][new_x] in ".€kt":
            s.x, s.y = new_x, new_y
        elif game.current_level.level[new_y][new_x] == "#":
            if s.direction == "up":
                s.direction = "down"
            elif s.direction == "down":
                s.direction = "up"
            elif s.direction == "left":
                s.direction = "right"
            elif s.direction == "right":
                s.direction = "left"

def move_boss(game):
    for b in game.current_level.boss:
        b.direction = random.choice(["up", "down", "left", "right"])
        new_x, new_y = get_next_position(b.x, b.y, b.direction)
        if game.current_level.level[new_y][new_x] in ".€ktp":
            b.x, b.y = new_x, new_y
        elif game.current_level.level[new_y][new_x] == "#":
            if b.direction == "up":
                b.direction = "down"
            elif b.direction == "down":
                b.direction = "up"
            elif b.direction == "left":
                b.direction = "right"
            elif b.direction == "right":
                b.direction = "left"

def update(game):
    if game.health <= 0:  # health check
        game.status = "game over"

def player_attack(game):
    soundObj = pygame.mixer.Sound("sword.wav")
    soundObj.play()

    for direction in ["up", "down", "left", "right"]:
        new_x, new_y = get_next_position(game.x, game.y, direction)
        for s in game.current_level.skeletons:
            if new_x == s.x and new_y == s.y:
                s.health -= 1

        for i in game.current_level.snakes:
            if new_x == i.x and new_y == i.y:
                i.health -= 1

        for b in game.current_level.boss:
            if new_x == b.x and new_y == b.y:
                b.health -= 0.25

    new_boss = []
    new_skeleton = []
    new_snakes = []

    for s in game.current_level.skeletons:
        if s.health > 0:
            new_skeleton.append(s)
        else:
            soundObj = pygame.mixer.Sound("skeleton.mp3")
            soundObj.play()
    game.current_level.skeletons = new_skeleton

    for i in game.current_level.snakes:
        if i.health > 0:
            new_snakes.append(i)
        else:
            soundObj = pygame.mixer.Sound("snake.mp3")
            soundObj.play()
    game.current_level.snakes = new_snakes

    for b in game.current_level.boss:
        if b.health > 0:
            new_boss.append(b)
        else:
            soundObj = pygame.mixer.Sound("knife.flac")
            soundObj.play()
    game.current_level.boss = new_boss

def start_game():
    return DungeonGame(x = 11, y = 1, current_level = LEVEL_ONE)
