from behavior.state import State
from core.config import RUN_DURATION, CAT_RUN_SPEED
import random


class RunState(State):
    name = "run"

    # Zufällige Aktion nach dem Rennen
    ACTIONS = ["lick", "sleep", "stretch", "itch", "meow"]

    def enter(self):
        self.cat.sprite.play("run")
        self.cat.body.velocity.x = self.cat.facing * CAT_RUN_SPEED

    def update(self, dt):
        super().update(dt)

        if self.cat.position.x <= 0:
            self.cat.position.x = 0
            self.cat.facing = 1
            self.cat.body.velocity.x = self.cat.facing * CAT_RUN_SPEED
        screen_w = self.cat.provider.screen_width()
        if self.cat.position.x + self.cat.body.width >= screen_w:
            self.cat.position.x = screen_w - self.cat.body.width
            self.cat.facing = -1
            self.cat.body.velocity.x = self.cat.facing * CAT_RUN_SPEED

    def exit(self):
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= RUN_DURATION:
            return random.choice(self.ACTIONS)
        return None