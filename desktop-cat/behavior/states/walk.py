from behavior.state import State
from core.config import WALK_DURATION, CAT_WALK_SPEED


class WalkState(State):
    name = "walk"

    def enter(self):
        self.cat.sprite.play("walk")
        if self.cat.facing == 0:
            self.cat.facing = 1
        self.cat.body.velocity.x = self.cat.facing * CAT_WALK_SPEED

    def update(self, dt):
        super().update(dt)

        if self.cat.position.x <= 0:
            self.cat.position.x = 0
            self.cat.facing = 1
            self.cat.body.velocity.x = self.cat.facing * CAT_WALK_SPEED
        screen_w = self.cat.provider.screen_width()
        if self.cat.position.x + self.cat.body.width >= screen_w:
            self.cat.position.x = screen_w - self.cat.body.width
            self.cat.facing = -1
            self.cat.body.velocity.x = self.cat.facing * CAT_WALK_SPEED

    def exit(self):
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= WALK_DURATION:
            return "sit"
        return None