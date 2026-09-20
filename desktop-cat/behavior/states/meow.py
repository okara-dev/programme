from behavior.state import State
from core.config import MEOW_DURATION


class MeowState(State):
    name = "meow"

    def enter(self):
        self.cat.sprite.play("meow")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= MEOW_DURATION:
            return "walk"
        return None