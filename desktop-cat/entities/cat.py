from core.config import CAT_WIDTH, CAT_HEIGHT, SPRITE_FPS, DEBUG
from core.vector import Vector2
from physics.collision import Physics
from render.sprite import Sprite
from behavior.machine import StateMachine
from behavior.states.walk import WalkState
from behavior.states.sit import SitState
from behavior.states.run import RunState
from behavior.states.sleep import SleepState
from behavior.states.lick import LickState
from behavior.states.stretch import StretchState
from behavior.states.itch import ItchState
from behavior.states.meow import MeowState


class Body:
    def __init__(self, x, y, width, height):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.width = width
        self.height = height


class Cat:
    def __init__(self, provider):
        self.provider = provider
        self.physics = Physics(provider)

        start_x = provider.screen_width() // 2
        start_y = 0
        self.body = Body(start_x, start_y, CAT_WIDTH, CAT_HEIGHT)

        sheets = {
            "walk":    "assets/sprites/cat_walk.png",
            "sit":     "assets/sprites/cat_sit.png",
            "run":     "assets/sprites/cat_run.png",
            "sleep":   "assets/sprites/cat_sleep.png",
            "lick":    "assets/sprites/cat_lick.png",
            "stretch": "assets/sprites/cat_stretch.png",
            "itch":    "assets/sprites/cat_itch.png",
            "meow":    "assets/sprites/cat_meow.png",
        }
        self.sprite = Sprite(sheets, CAT_WIDTH, CAT_HEIGHT, fps=SPRITE_FPS)

        self.facing = 1

        self.machine = StateMachine(
            self,
            {
                "walk":    WalkState(self),
                "sit":     SitState(self),
                "run":     RunState(self),
                "sleep":   SleepState(self),
                "lick":    LickState(self),
                "stretch": StretchState(self),
                "itch":    ItchState(self),
                "meow":    MeowState(self),
            },
            initial="walk",
        )

        self._debug_timer = 0.0

    @property
    def position(self):
        return self.body.position

    @property
    def velocity(self):
        return self.body.velocity

    def update(self, dt):
        self.physics.apply_gravity(self.body, dt)
        self.physics.integrate(self.body, dt)
        self.physics.resolve_ground(self.body)

        self.machine.update(dt)
        self.sprite.update(dt)

        if DEBUG:
            self._debug_timer += dt
            if self._debug_timer >= 0.5:
                self._debug_timer = 0.0
                print(
                    f"[{self.machine.current.name:7s}] "
                    f"pos=({self.position.x:7.0f},{self.position.y:7.0f})"
                )