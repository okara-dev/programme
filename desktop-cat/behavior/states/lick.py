from behavior.state import State
from core.config import LICK_DURATION


class LickState(State):
    name = "lick"

    def enter(self):
        self.cat.sprite.play("lick")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= LICK_DURATION:
            return "walk"
        return None