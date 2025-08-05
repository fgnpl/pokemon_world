import pygame
import constants
from pygame.locals import *
from world import *
from battle import *
from trainers import *
from pokemons import *

# Initializing pygame and creating a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Pokemons")
clock = pygame.time.Clock()

# Creating the game world
# First number - number of pokemon in the world
world = World(20, 400, 5, constants.WIDTH - 5, constants.HEIGHT - 5)

# Both players are smart trainers
trainers = [Trainer(85, 85), SmartTrainer(325, 85)]
trainers_g = pygame.sprite.Group()
trainers_g.add(trainers)

# 5 pokemons in each team per battle
battle = Battle(5, 10, 120)

running = True
ntrainer = 0

# Main cycle 
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if len(world.pokemons) == 0 and not battle.started():
                world.generate_pokemons()
            else:
                pokemon = world.catch_pokemon(e.pos)
                if pokemon is not None:
                    trainers[ntrainer].add(pokemon)
                    ntrainer += 1
                    ntrainer %= len(trainers)
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                pass

    # Rendering
    screen.fill(constants.BEIGE)
    world.draw(screen)
    trainers_g.draw(screen)
    battle.draw(screen)

    # Flipping display after drawing everything
    pygame.display.flip()
    clock.tick(constants.FPS)

    # Updating
    world.update()
    battle.update()
    trainers_g.update()

    # Commencing battle
    if len(world.pokemons) == 0:
        battle.start(trainers[0], trainers[1])
        if not battle.started():
            world.generate_pokemons()

pygame.quit()
