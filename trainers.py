import pygame
import drawutils
import constants
import random
import pokemons


class Trainer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.wins = 0
        self.box = []

        # Initializing trainer's image
        path = f"trainers_pics/trainer_1.png"
        self.picture = pygame.image.load(path).convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (125, 165))
        self.image = pygame.Surface(self.picture.get_size(), pygame.SRCALPHA, 32)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def add(self, pokemon):
        self.box.append(pokemon)

    # Algorithm of a normal trainer: choosing first n pokemon from the box
    def best_team(self, n):
        team = self.box[:n]
        self.box = self.box[n:]
        return team

    def update(self):
        self.rect.center = (self.x, self.y)
        self.image.fill((255, 255, 255, 0))
        self.image.blit(self.picture, (0, 0))
        drawutils.drawText(self.image, f"Wins:{self.wins} Pokemons:{len(self.box)}", (0, 150))


class SmartTrainer(Trainer):
    # Algorithm of a smart trainer
    def best_team(self, n):
        average = []

        # Sorting by sum of attack and defense
        for index, pokemon in enumerate(self.box):
            average.append((index, (pokemon.atk + pokemon.df)))
        average.sort(key=lambda tup: tup[1], reverse=True)

        # Fire pokemons go to the end
        for index in range(len(average)):
            tup = average[index]
            if type(self.box[tup[0]]) == pokemons.FirePokemon:
                if tup == average[-1]:
                    break
                elif tup[1] - average[index + 1][1] < 2:
                    average.insert(index + 1, average.pop(index))

        # Creating a team of the n sorted pokemon
        print(average)
        print(self.box)
        team = []
        for index in range(n):
            team.append(self.box[average[index][0]])

        # Removing pokemon in the team from the box
        for pokemon in team:
            if pokemon in self.box:
                self.box.remove(pokemon)
        print(team)

        # Returning reversed list of the team, so the strongest pokemon has higher chances of survival
        return team[::-1]
