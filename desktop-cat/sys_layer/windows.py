import pywinctl
from PyQt5.QtWidgets import QApplication


class WindowRect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height


class WindowsWindowProvider:
    """Fragt Fenstergeometrien und Bildschirmmaße vom OS ab."""

    def __init__(self):
        # Echte (physische) Auflösung holen, nicht die skalierte
        screen = QApplication.primaryScreen()
        self._screen_w = screen.size().width()
        self._screen_h = screen.size().height()
        # Physische Auflösung (ohne Windows-Skalierung)
        self._phys_w = screen.geometry().width()
        self._phys_h = screen.geometry().height()

    def screen_width(self):
        # Physische Breite in "logischen" Pixeln
        screen = QApplication.primaryScreen()
        return screen.geometry().width()

    def screen_height(self):
        # Physische Höhe in "logischen" Pixeln
        screen = QApplication.primaryScreen()
        return screen.geometry().height()

    def get_windows(self):
        rects = []
        try:
            for win in pywinctl.getAllWindows():
                if not win.visible:
                    continue
                if win.width <= 0 or win.height <= 0:
                    continue
                rects.append(WindowRect(win.left, win.top, win.width, win.height))
        except Exception:
            pass
        return rects