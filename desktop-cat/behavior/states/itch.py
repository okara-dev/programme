from behavior.state import State
from core.config import ITCH_DURATION


class ItchState(State):
    name = "itch"

    def enter(self):
        self.cat.sprite.play("itch")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= ITCH_DURATION:
            return "walk"
        return None