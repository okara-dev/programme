class StateMachine:
    def __init__(self, cat, states: dict, initial: str):
        self.cat = cat
        self.states = states
        self.current = states[initial]
        self.current.enter()

    def update(self, dt):
        self.current.update(dt)
        if self.current.can_exit():
            next_name = self.current.next_state()
            if next_name and next_name in self.states:
                self.transition(next_name)

    def transition(self, name):
        self.current.exit()
        self.current = self.states[name]
        self.current.time_in_state = 0.0
        self.current.enter()