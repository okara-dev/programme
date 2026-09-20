from behavior.state import State
from core.config import STRETCH_DURATION


class StretchState(State):
    name = "stretch"

    def enter(self):
        self.cat.sprite.play("stretch")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= STRETCH_DURATION:
            return "walk"
        return None