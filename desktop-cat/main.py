import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from core.config import FPS
from core.loop import GameLoop
from entities.cat import Cat
from render.overlay import Overlay
from sys_layer.windows import WindowsWindowProvider


def main():
    app = QApplication(sys.argv)

    provider = WindowsWindowProvider()
    overlay = Overlay()
    cat = Cat(provider=provider)
    overlay.attach_cat(cat)

    loop = GameLoop(cat=cat, overlay=overlay, fps=FPS)
    overlay.show()

    # Overlay jede Sekunde nach vorne holen (verhindert Verschwinden hinter Desktop)
    def keep_on_top():
        overlay.raise_()

    top_timer = QTimer()
    top_timer.timeout.connect(keep_on_top)
    top_timer.start(1000)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()