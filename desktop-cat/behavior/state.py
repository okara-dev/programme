class State:
    name = "base"
    min_duration = 0.0
    max_duration = float("inf")

    def __init__(self, cat):
        self.cat = cat
        self.time_in_state = 0.0

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        self.time_in_state += dt

    def can_exit(self) -> bool:
        return self.time_in_state >= self.min_duration

    def next_state(self):
        return None