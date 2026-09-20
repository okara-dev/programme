import time
from PyQt5.QtCore import QTimer


class GameLoop:
    def __init__(self, cat, overlay, fps=60):
        self.cat = cat
        self.overlay = overlay
        self.dt = 1.0 / fps
        self._last_time = time.perf_counter()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(1000 / fps))

    def tick(self):
        now = time.perf_counter()
        dt = now - self._last_time
        self._last_time = now

        # Clamp, damit nach Pausen kein riesiger Sprung entsteht
        dt = min(dt, 0.1)

        self.cat.update(dt)
        self.overlay.render()