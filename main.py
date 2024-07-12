import os
import cv2
import numpy as np
from pygame import mixer
from game import (check_collision, check_teleporters, move_boss, move_fireball,
                  move_player, move_skeleton, move_snake, player_attack,
                  start_game, update)

GAME_TITLE = "2D Dungeon Game"

mixer.init()
mixer.music.load("ave_maria.mp3")
mixer.music.play(loops=-1)

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
}

SYMBOLS = {
    ".": "floor",
    "#": "wall",
    "x": "stairs_down",
    "€": "coin",
    "t": "trap",
    "k": "key",
    "D": "closed_door",
    "d": "open_door",
    "p": "potion",
    "a": "armor",
    "c": "chest",
    "s": "long_sword",
    "u": "undead",          # boss
    "+": "snake",           # boss apprentice 
    "y": "piggy"
}

# constants measured in pixels
SCREEN_SIZE_X, SCREEN_SIZE_Y = 2560, 1600  # 840, 640
TILE_SIZE = 160

def read_image(filename: str) -> np.ndarray:
    img = cv2.imread(filename)  # sometimes returns None
    if img is None:
        raise IOError(f"Image not found: '{filename}'")
    img = np.kron(img, np.ones((5, 5, 1), dtype=img.dtype))  # double image size
    return img

def read_images():
    return {
        filename[:-4]: read_image(os.path.join("tiles", filename))
        for filename in os.listdir("tiles")
        if filename.endswith(".png")
    }

def draw_tile(frame, x, y, image, xbase=0, ybase=0):
    # calculate screen position in pixels
    xpos = xbase + x * TILE_SIZE
    ypos = ybase + y * TILE_SIZE

    # copy the image to the screen
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image

def draw_bar(size, frame, xbase, ybase, icon):
    for i in range(size):
        draw_tile(frame, x=i, y=0, xbase=xbase, ybase=ybase, image=images[icon])

def draw(game, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    # draw dungeon tiles
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])

    elements = [
        [game.current_level.teleporters, "teleporter"],
        [game.current_level.fireballs, "fireball"],
        [game.current_level.skeletons, "skeleton"],
        [game.current_level.snakes, "snake"],
        [game.current_level.boss, "undead"],
    ]

    for monsters, imagename in elements:
        for m in monsters:
            draw_tile(frame, x = m.x, y = m.y, image = images[imagename])

    draw_tile(frame, x = game.x, y = game.y, image = images["player"])

    for dmg in game.damages:
        if dmg.counter > 0:
            # draw_tile(frame, x=dmg.x, y=dmg.y, image=images[dmg.image])
            cv2.putText(
                frame,
                dmg.text,
                org=(TILE_SIZE * dmg.x, TILE_SIZE * dmg.y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.5,
                color=(128, 128, 255),
                thickness=4,
            )
            dmg.counter -= 1

    # coin display
    draw_tile(frame, x=0, y=0, xbase=2300, ybase=250, image=images["coin"])
    cv2.putText(
        frame,
        str(game.coins),
        org=(2080, 375),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=3,
        color=(255, 128, 128),
        thickness=7,
    )

    # health bar
    draw_bar(game.health, frame, 2080, 480, "heart")
    draw_bar(game.armor, frame, 2080, 860, "armor")
    draw_bar(game.sword, frame, 2080, 1060, "long_sword")
    
    if game.current_level.boss:
        draw_bar(int(game.current_level.boss[0].health), frame, 2080, 1260, "prompt_no")

    # inventory of collected items
    for i, item in enumerate(game.items):
        y = i // 2
        x = i % 2
        draw_tile(frame, x=i, y=0, xbase=2080, ybase=660, image=images[item])
    cv2.imshow(GAME_TITLE, frame)

def handle_keyboard(game):
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        game.status = "exited"
    if key == " ":
        player_attack(game)
    if key in MOVES:
        move_player(game, MOVES[key])

img = cv2.imread("title.png")

img[-100:] = 0  # last 100 pixel rows are black
img = cv2.putText(
    img,
    "Willkommen! Dies ist das 2D-Dungeon-Spiel!",
    org = (150, 980),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale = 1,
    color=(255, 255, 255),  # white
    thickness = 2,
)

cv2.imshow("Cutscene", img)
cv2.waitKey(0)

# game start
images = read_images()
game = start_game()

counter = 0
while game.status == "running":
    counter += 1
    draw(game, images)
    handle_keyboard(game)
    check_teleporters(game)

    if counter % 25 == 0:
        update(game)
        move_fireball(game)
        check_collision(game)
        move_skeleton(game)
        move_snake(game)
        move_boss(game)

cv2.destroyAllWindows()
mixer.music.stop()

if game.status == "finished":
    img = cv2.imread("win.png")
    img[-100:] = 0  # last 100 pixel rows are black
    img = cv2.putText(
        img,
        "YOU WIN! GAME OVER!",
        org = (300, 990),  # x/y position of the text
        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
        fontScale = 1,
        color = (255, 255, 255),  # white
        thickness = 2,
    )

    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)
else:
    img = cv2.imread("end.png")
    img[-100:] = 0  # last 100 pixel rows are black
    img = cv2.putText(
        img,
        "YOU DIED! GAME OVER!",
        org = (300, 990),  # x/y position of the text
        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
        fontScale = 1,
        color = (255, 255, 255),  # white
        thickness = 2,
    )

    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)