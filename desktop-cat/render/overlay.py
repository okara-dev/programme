from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtWidgets import QWidget, QApplication
from core.config import SPRITE_SCALE, CAT_WIDTH, CAT_HEIGHT


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.cat = None

        # Rahmenlos, immer im Vordergrund, kein Taskleisten-Eintrag
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Primären Bildschirm verwenden
        screen = QApplication.primaryScreen()
        geo = screen.geometry()
        self.setGeometry(geo)

        print(f"[overlay] logisch: {geo.width()}x{geo.height()}")
        print(f"[overlay] devicePixelRatio: {screen.devicePixelRatio()}")

    def attach_cat(self, cat):
        self.cat = cat

    def render(self):
        self.update()

    def paintEvent(self, event):
        if self.cat is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        pixmap = self.cat.sprite.current_pixmap()
        if pixmap is None or pixmap.isNull():
            return

        x = int(self.cat.position.x)
        y = int(self.cat.position.y)

        # Skalierung kompensieren: gerenderte Katze ist SCALE-mal größer,
        # aber body.position beschreibt die Original-Kollisionsbox.
        if SPRITE_SCALE != 1:
            offset_x = (CAT_WIDTH * SPRITE_SCALE - CAT_WIDTH) // 2
            offset_y = (CAT_HEIGHT * SPRITE_SCALE - CAT_HEIGHT)
            x -= offset_x
            y -= offset_y

        # Horizontal spiegeln, wenn die Katze nach links schaut
        if self.cat.facing == -1:
            transform = QTransform().scale(-1, 1)
            pixmap = pixmap.transformed(transform)
            x -= pixmap.width() - (CAT_WIDTH * SPRITE_SCALE)

        painter.drawPixmap(QPoint(x, y), pixmap)