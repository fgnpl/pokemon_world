import pygame
from pokemons import *
import constants
from pygame.locals import *
from trainers import *


class Battle:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
        self.turn = 1
        self.state = constants.NOT_STARTED

    def draw(self, surface):
        if self.state == constants.NOT_STARTED:
            return
        self.team1.draw(surface)
        self.team2.draw(surface)

        # Creating a line containing the enemies
        if len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
            pygame.draw.line(surface, (255, 0, 0), self.team1.sprites()[0].rect.midright,
                             self.team2.sprites()[0].rect.midleft, 3)
            # Creating a circle that indicates damage done to a pokemon
            hit_circle = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(hit_circle, (255, 0, 0, 100), hit_circle.get_rect().center,
                               hit_circle.get_rect().width // 2 - 5, 0)
            if self.turn == 1:
                surface.blit(hit_circle, self.team2.sprites()[0].rect.topleft)
            else:
                surface.blit(hit_circle, self.team1.sprites()[0].rect.topleft)

    def start(self, trainer1, trainer2):
        if self.state == constants.NOT_STARTED:
            # Music for battle
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music/battle.ogg')
            pygame.mixer.music.play()

            # Initializing trainers and creating teams
            self.trainer1 = trainer1
            self.trainer2 = trainer2
            self.team1 = pygame.sprite.Group()
            self.team1.add(trainer1.best_team(self.n))
            self.team2 = pygame.sprite.Group()

            # Checking for None
            try:
                self.team2.add(trainer2.best_team(self.n))
            except:
                return

            if len(self.team1) < self.n or len(self.team2) < self.n:  # Stopping battle if not enough pokemons
                return

            # Moving pokemons across the battlefield
            y = self.y
            for pokemon in self.team1:
                pokemon.rect.topleft = (self.x + 20, y + 55)
                y += pokemon.rect.height + 5
                pokemon.velocity = [0, 0]
            y = self.y
            for pokemon in self.team2:
                pokemon.rect.topleft = (self.x + 290, y + 55)
                y += pokemon.rect.height + 5
                pokemon.velocity = [0, 0]
            self.state = constants.STARTED
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.state == constants.STARTED:
            nowTime = pygame.time.get_ticks()
            if nowTime - self.last_update > constants.HIT_DELAY:
                self.last_update = nowTime
            else:
                return

            # If it's the turn of a pokemon from the first team
            if self.turn == 1 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team1.sprites()[0].attack(self.team2.sprites()[0])  # Attack
                if self.team2.sprites()[0].hp <= 0:  # Checking opponent's HP
                    self.team2.remove(self.team2.sprites()[0])
                if len(self.team2.sprites()) == 0:  # Battle end
                    return self.finish(1)
            # If it's the turn of a pokemon from the second team
            elif self.turn == 2 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team2.sprites()[0].attack(self.team1.sprites()[0])
                if self.team1.sprites()[0].hp <= 0:
                    self.team1.remove(self.team1.sprites()[0])
                if len(self.team1.sprites()) == 0:
                    return self.finish(2)

            # Changing attacking team
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.team1.update()
            self.team2.update()

    def finish(self, result):
        self.state = constants.NOT_STARTED
        # Regenerating HP for surviving pokemon
        for p in self.team1:
            p.hp = 100
            self.trainer1.add(p)
        for p in self.team2:
            p.hp = 100
            self.trainer2.add(p)

        # Increasing the score of the winning trainer
        if result == 1:
            self.trainer1.wins += 1
        else:
            self.trainer2.wins += 1

    # Check for battle start
    def started(self):
        return True if self.state == constants.STARTED else False
