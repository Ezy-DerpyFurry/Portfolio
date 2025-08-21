### I wanna try to modularize pygame to add to my library so heres a testing game I made

import pygame
import math
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("suwvivalz yis :3")
font = pygame.font.Font(None, 36)

x, y = WIDTH/2, HEIGHT/2
size = 10
speed = 0.5
max_speed = 1.0

clock = pygame.time.Clock()

wood = 0

grass = []
ponds = []
trees = []

def spawn(amount: int = 15, type: str = "trees"):
    if type == "trees" or type == "grass":
        for _ in range(amount):
            while True:
                px = random.randint(0, WIDTH - 5)
                py = random.randint(0, HEIGHT - 5)
                if type == "grass":
                    pr = random.randint(20, 50)
                else:
                    pr = random.randint(2, 4)

                valid = True
                for pond_x, pond_y, pond_r in ponds:
                    dist = math.dist((px, py), (pond_x, pond_y))
                    if dist < pond_r + pr:
                        valid = False
                        break

                if valid:
                    if type == "grass":
                        grass.append((px, py, pr))
                    else:
                        trees.append((px, py, pr))
                    break
    elif type == "ponds":
        for _ in range(amount):
            px = random.randint(0, WIDTH - 50)
            py = random.randint(0, HEIGHT - 50)
            pr = random.randint(15, 40)
            ponds.append((px, py, pr))

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def player_center():
    return (x + size / 2, y + size / 2)

def inside(px, py, pr, reach):
    cx, cy = player_center()
    dist = math.dist((cx, cy), (px, py))
    return dist - reach < pr

spawn(15, "ponds")
spawn(35, "grass")
spawn(15, "trees")

key_values = {
    pygame.K_RIGHT: 1,
    pygame.K_LEFT: -1,
    pygame.K_UP: -1,
    pygame.K_DOWN: 1
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LSHIFT]:
        speed = speed * 1.2

    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        x += speed * (speed + 0.001) * (key_values[pygame.K_RIGHT] * keys[pygame.K_RIGHT] + key_values[pygame.K_LEFT] * keys[pygame.K_LEFT])
        speed = clamp(speed + 0.001, 0.5, max_speed)
        x = max(0, min(WIDTH-0.5, x))

    if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        y += speed * (speed + 0.001) * (key_values[pygame.K_DOWN] * keys[pygame.K_DOWN] + key_values[pygame.K_UP] * keys[pygame.K_UP])
        speed = clamp(speed + 0.001, 0.5, max_speed)
        y = max(0, min(HEIGHT-0.5, y))

    move_keys = [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]
    if not any(keys[k] for k in move_keys):
        speed = 0.5

    new_trees = []
    for tree in trees:
        if not inside(*tree, 15):
            new_trees.append(tree)
        else:
            wood += 1
            if len(trees) + len(new_trees) == 1:
                spawn(15, "trees")
    trees = new_trees

    for pond in ponds:
        if inside(*pond, 0):
            wood = 0
            speed = 0.25

    window.fill((0, 225, 0))


    for px, py, pr in grass:
        pygame.draw.rect(window, (0,175,0), (px, py, size*10, size*10))
    for px, py, pr in ponds:
        pygame.draw.circle(window, (0, 100, 255), (px, py), pr)
    for px, py, pr in trees:
        pygame.draw.circle(window, (100,40,0), (px, py), pr)
    text_surface = font.render(f"Wood: {wood}", True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()
    text_rect = text_surface.get_rect(center=(text_width - 40, text_height - 5))
    window.blit(text_surface, text_rect)

    pygame.draw.rect(window, (255, 0, 0), (int(x), int(y), size, size))
    pygame.display.flip()
    clock.tick(144)
