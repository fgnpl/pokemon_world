import pygame
import random
import constants
from pokemons import *


class Border(pygame.sprite.Sprite):
    # Strictly vertical or horizontal segment
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # Vertical wall
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # Horizontal wall
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill(constants.BLACK)


class World:
    MAX_POKEMON_ATK = 5
    MAX_POKEMON_DF = 5

    def __init__(self, n_pok, x1, y1, x2, y2):
        self.n_poc = n_pok
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.horBorders = pygame.sprite.Group()
        self.vertBorders = pygame.sprite.Group()
        self.vertBorders.add(Border(x1, y1, x1, y2))
        self.vertBorders.add(Border(x2, y1, x2, y2))
        self.horBorders.add(Border(x1, y1, x2, y1))
        self.horBorders.add(Border(x1, y2, x2, y2))
        self.rect = pygame.Rect(x1, y1, x2-x1, y2-y1)
        self.pokemons = pygame.sprite.Group()
        self.generate_pokemons()

    def generate_pokemons(self):
        # Normal music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/bg_music.ogg')
        pygame.mixer.music.play()

        # Generating pokemon
        for _ in range(self.n_poc):
            t = random.randint(1, 4)
            if t == 1:
                self.pokemons.add(WaterPokemon("wp",
                                               random.randint(1, World.MAX_POKEMON_ATK),
                                               random.randint(1, World.MAX_POKEMON_DF),
                                               random.randint(490, 910), random.randint(150, 700)))
            elif t == 2:
                self.pokemons.add(FirePokemon("fp",
                                              random.randint(1, World.MAX_POKEMON_ATK),
                                              random.randint(1, World.MAX_POKEMON_DF),
                                              random.randint(490, 910), random.randint(150, 700)))
            elif t == 3:
                self.pokemons.add(GrassPokemon("gp",
                                               random.randint(1, World.MAX_POKEMON_ATK),
                                               random.randint(1, World.MAX_POKEMON_DF),
                                               random.randint(490, 910), random.randint(150, 700)))
            else:
                self.pokemons.add(ElectricPokemon("ep",
                                                  random.randint(1, World.MAX_POKEMON_ATK),
                                                  random.randint(1, World.MAX_POKEMON_DF),
                                                  random.randint(490, 910), random.randint(150, 700)))

    # Drawing the field's boundaries and the pokemon
    def draw(self, surface):
        self.horBorders.draw(surface)
        self.vertBorders.draw(surface)
        surface.set_clip(self.rect)
        self.pokemons.draw(surface)
        surface.set_clip(None)

    def update(self):
        self.pokemons.update()

    def catch_pokemon(self, pos):
        for pokemon in self.pokemons:
            if pokemon.rect.collidepoint(pos[0], pos[1]):  # If the user clicked on a pokemon
                self.pokemons.remove(pokemon)  # Removing it from field
                return pokemon  # Returning its value to add the pokemon to the team
        if len(self.pokemons.sprites()) > 0:
            pokemon = self.pokemons.sprites()[0]
            self.pokemons.remove(pokemon)
            return pokemon
        return None
