import pygame
import drawutils
import random
import constants


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, atk, df, x, y, path):
        super().__init__()
        self.x = x
        self.y = y

        # Velocity - random unique values from -5 to 5
        self.velocity = random.sample(range(-5, 5), 2)

        self.name = name
        self.hp = 100
        self.atk = atk
        self.df = df

        # Creating the image of the pokemon
        self.path = path
        self.picture = pygame.image.load(self.path).convert_alpha()
        self.size = self.picture.get_size()
        self.picture = pygame.transform.scale(self.picture, (self.size[0], self.size[1]))
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.image.fill((255, 255, 255, 0))
        self.image.blit(self.picture, (0, 0))
        drawutils.drawText(self.image, f"HP:{self.hp} ATK:{self.atk} DEF:{self.df}", (0, 100), "Arial", 10)

        # If pokemon collides with the boundaries of the screen, turn vector by 180 degrees
        if self.rect.left < 400 or self.rect.right >= constants.WIDTH:
            self.velocity[0] *= -1
        if self.rect.top < 5 or self.rect.bottom >= constants.HEIGHT:
            self.velocity[1] *= -1
        self.rect.move_ip(self.velocity)

    def attack(self, other):
        if self.hp == 0:
            return

        damage = self.atk - other.df
        if damage > 0:
            other.hp -= damage
        else:
            other.hp -= 1

        if other.hp < 0:
            other.hp = 0

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_def(self):
        return self.df


class FirePokemon(Pokemon):
    def __init__(self, name, atk, df, x, y,
                 path="pokemons_pics/fire/fire_"):
        # Choosing random image of pokemon of a specific type
        random_number = random.randint(1, 10)
        path += f"{str(random_number)}.png"
        super().__init__(name, atk, df, x, y, path)


class WaterPokemon(Pokemon):
    def __init__(self, name, atk, df, x, y,
                 path="pokemons_pics/water/water_"):
        random_number = random.randint(1, 10)
        path += f"{str(random_number)}.png"
        super().__init__(name, atk, df, x, y, path)

    def attack(self, other):
        # Water pokemon's special attack attribute
        if isinstance(other, FirePokemon):
            atk_before_buff = self.atk
            self.atk *= 3
            super().attack(other)
            self.atk = atk_before_buff
        else:
            super().attack(other)


class GrassPokemon(Pokemon):
    def __init__(self, name, atk, df, x, y,
                 path="pokemons_pics/grass/grass_"):
        random_number = random.randint(1, 10)
        path += f"{str(random_number)}.png"
        super().__init__(name, atk, df, x, y, path)

    def attack(self, other):
        # Grass pokemon's special attack attribute
        if isinstance(other, FirePokemon):
            df_before_debuff = other.df
            other.df //= 2
            super().attack(other)
            other.df = df_before_debuff
        else:
            super().attack(other)


class ElectricPokemon(Pokemon):
    def __init__(self, name, atk, df, x, y,
                 path="pokemons_pics/electric/electric_"):
        random_number = random.randint(1, 10)
        path += f"{str(random_number)}.png"
        super().__init__(name, atk, df, x, y, path)

    def attack(self, other):
        # Electric pokemon's special attack attribute
        if isinstance(other, WaterPokemon):
            df_before_debuff = other.df
            other.df = 0
            super().attack(other)
            other.df = df_before_debuff
        else:
            super().attack(other)
