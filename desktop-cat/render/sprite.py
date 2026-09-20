from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from core.config import SPRITE_FPS, SPRITE_SCALE


class Sprite:
    """Verwaltet ein Sprite-Sheet: alle Frames horizontal nebeneinander."""

    def __init__(self, sheets: dict, frame_w: int, frame_h: int, fps: int = SPRITE_FPS):
        self.sheets = {name: QPixmap(path) for name, path in sheets.items()}
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.fps = fps

        self.animation = None
        self.current_frame = 0
        self.time = 0.0

    def play(self, name: str):
        if name == self.animation:
            return
        if name not in self.sheets:
            return
        self.animation = name
        self.current_frame = 0
        self.time = 0.0

    def update(self, dt: float):
        if self.animation is None:
            return
        self.time += dt
        if self.time >= 1.0 / self.fps:
            self.time = 0.0
            self.current_frame += 1

    def current_pixmap(self) -> QPixmap:
        if self.animation is None:
            return QPixmap()
        sheet = self.sheets[self.animation]
        frame_count = max(1, sheet.width() // self.frame_w)
        idx = self.current_frame % frame_count
        frame = sheet.copy(idx * self.frame_w, 0, self.frame_w, self.frame_h)

        # Skalieren (Pixel-Art: FastTransformation = scharfe Kanten)
        if SPRITE_SCALE != 1:
            frame = frame.scaled(
                frame.width() * SPRITE_SCALE,
                frame.height() * SPRITE_SCALE,
                Qt.KeepAspectRatio,
                Qt.FastTransformation,
            )
        return frame