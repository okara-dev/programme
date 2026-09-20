from behavior.state import State
from core.config import SIT_DURATION


class SitState(State):
    name = "sit"

    def enter(self):
        self.cat.sprite.play("sit")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= SIT_DURATION:
            return "run"
        return None