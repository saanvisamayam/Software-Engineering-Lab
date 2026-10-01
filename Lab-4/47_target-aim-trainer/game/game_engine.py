import pygame
import random
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60

        self.difficulties = {
            "Easy": (45, 14, 120),
            "Medium": (40, 12, 90),
            "Hard": (35, 10, 60)
        }

        self.difficulty = "Medium"

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over = False

        pygame.mixer.init()

        self.hit_sound = pygame.mixer.Sound(
            "game/sounds/hit.wav"
        )
        self.miss_sound = pygame.mixer.Sound(
            "game/sounds/miss.wav"
        )
        self.game_over_sound = pygame.mixer.Sound(
            "game/sounds/game_over.wav"
        )

        self.target = self._spawn_target()

    def _spawn_target(self):
        x = random.randint(
            self.margin,
            self.width - self.margin
        )

        y = random.randint(
            self.margin + self.hud_height,
            self.height - self.margin
        )

        base_radius, min_radius, lifespan_frames = (
            self.difficulties[self.difficulty]
        )

        return Target(
            x,
            y,
            base_radius,
            min_radius,
            lifespan_frames
        )

    def reset_game(self):
        self.time_left_frames = self.round_seconds * 60
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game_over = False
        self.target = self._spawn_target()

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.difficulty = "Easy"
                    self.reset_game()

                elif event.key == pygame.K_m:
                    self.difficulty = "Medium"
                    self.reset_game()

                elif event.key == pygame.K_h:
                    self.difficulty = "Hard"
                    self.reset_game()

                elif event.key == pygame.K_x:
                    pygame.quit()
                    raise SystemExit

            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos

        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.hit_sound.play()
            self.target = self._spawn_target()

        else:
            self.misses += 1
            self.miss_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input.
        # This game is mouse-driven.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.game_over = True
            self.game_over_sound.play()
            return

        self.target.update()

        if self.target.expired():
            self.misses += 1
            self.miss_sound.play()
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses

        if total == 0:
            return 0.0

        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if self.game_over:
            game_over_text = self.font.render(
                "GAME OVER",
                True,
                WHITE
            )

            score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            acc_text = self.font.render(
                f"Accuracy: {self.accuracy()}%",
                True,
                WHITE
            )

            instruction_text = self.font.render(
                "[E] Easy   [M] Medium   [H] Hard",
                True,
                WHITE
            )

            exit_text = self.font.render(
                "[X] Exit",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                (
                    self.width // 2
                    - game_over_text.get_width() // 2,
                    150
                )
            )

            screen.blit(
                score_text,
                (
                    self.width // 2
                    - score_text.get_width() // 2,
                    210
                )
            )

            screen.blit(
                acc_text,
                (
                    self.width // 2
                    - acc_text.get_width() // 2,
                    250
                )
            )

            screen.blit(
                instruction_text,
                (
                    self.width // 2
                    - instruction_text.get_width() // 2,
                    320
                )
            )

            screen.blit(
                exit_text,
                (
                    self.width // 2
                    - exit_text.get_width() // 2,
                    360
                )
            )

            return

        r = int(self.target.visual_radius())

        pygame.draw.circle(
            screen,
            RED,
            (self.target.x, self.target.y),
            r
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.target.x, self.target.y),
            r,
            2
        )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        seconds_left = max(
            0,
            self.time_left_frames // 60
        )

        timer_text = self.font.render(
            f"Time: {seconds_left}s",
            True,
            WHITE
        )

        screen.blit(
            timer_text,
            (self.width - 140, 10)
        )

        acc_text = self.font.render(
            f"Accuracy: {self.accuracy()}%",
            True,
            WHITE
        )

        screen.blit(
            acc_text,
            (self.width // 2 - 90, 10)
        )