from behavior.state import State
from core.config import SLEEP_DURATION


class SleepState(State):
    name = "sleep"

    def enter(self):
        self.cat.sprite.play("sleep")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        if self.time_in_state >= SLEEP_DURATION:
            return "walk"
        return None