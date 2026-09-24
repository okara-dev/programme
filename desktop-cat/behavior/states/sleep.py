from behavior.state import State


class SleepState(State):
    name = "sleep"

    def enter(self):
        self.cat.sprite.play("sleep")
        self.cat.body.velocity.x = 0.0

    def next_state(self):
        # Kein Timer — bleibt schlafen bis Maus-Berührung (siehe cat.py)
        return None