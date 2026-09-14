from ursina import *
from random import randint
import math

app = Ursina()

# ============================================================
#  KONFIGURATION
# ============================================================
window.title = '✨ Mini Quest'
window.borderless = False
window.fullscreen = False
window.size = (1024, 768)
window.fps_counter.enabled = True
mouse.visible = False

# ============================================================
#  FARBDESIGN
# ============================================================
class Palette:
    # Sanftes, modernes Farbschema
    background = color.rgb(20, 25, 35)
    ground = color.rgb(45, 55, 65)
    ground_dark = color.rgb(35, 42, 50)
    player = color.rgb(100, 200, 255)
    player_accent = color.rgb(255, 215, 100)
    coin = color.rgb(255, 215, 0)
    coin_glow = color.rgb(255, 230, 100)
    enemy = color.rgb(255, 80, 80)
    enemy_dark = color.rgb(180, 40, 40)
    platform = color.rgb(120, 100, 80)
    platform_top = color.rgb(160, 140, 120)
    powerup = color.rgb(0, 255, 180)
    ui_text = color.rgb(220, 220, 240)
    ui_accent = color.rgb(255, 215, 100)

# ============================================================
#  SPIELER
# ============================================================
class Player(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            color=Palette.player,
            scale=0.4,
            position=(0, 0.5, 0),
            collider='sphere'
        )
        # Akzent-Ring
        self.accent = Entity(
            parent=self,
            model='torus',
            color=Palette.player_accent,
            scale=0.6,
            rotation=(90, 0, 0),
            opacity=0.6
        )
        # Schatten (Pseudo)
        self.shadow = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, 80),
            scale=(0.6, 0.6),
            position=(0, -0.5, 0),
            rotation=(90, 0, 0)
        )
        
        self.speed = 4
        self.jump_power = 6
        self.gravity = 18
        self.velocity_y = 0
        self.is_grounded = False
        self.collected = 0

    def update(self):
        # === BEWEGUNG ===
        move = Vec3(0, 0, 0)
        if held_keys['w']: move.z -= 1
        if held_keys['s']: move.z += 1
        if held_keys['a']: move.x -= 1
        if held_keys['d']: move.x += 1
        
        if move.length() > 0:
            move.normalize()
            self.position += move * self.speed * time.dt
            # Drehung sanft zur Laufrichtung
            target_angle = -math.degrees(math.atan2(move.x, move.z))
            self.rotation_y = self.rotation_y + (target_angle - self.rotation_y) * 0.15
            # Bobbing
            self.y += math.sin(time.time() * 12) * 0.002
        
        # === SPRINGEN ===
        if held_keys['space'] and self.is_grounded:
            self.velocity_y = self.jump_power
            self.is_grounded = False
        
        # === SCHWERKRAFT ===
        self.velocity_y -= self.gravity * time.dt
        self.y += self.velocity_y * time.dt
        
        if self.y <= 0.5:
            self.y = 0.5
            self.velocity_y = 0
            self.is_grounded = True
        
        # === KAMERA ===
        camera.position = self.position + (0, 4, -6)
        camera.look_at(self.position + (0, 0.5, 0))

# ============================================================
#  MÜNZE
# ============================================================
class Coin(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=Palette.coin,
            scale=0.2,
            position=position,
            collider='sphere'
        )
        # Glow
        self.glow = Entity(
            parent=self,
            model='sphere',
            color=Palette.coin_glow,
            scale=0.4,
            blend_transparency=True,
            opacity=0.2
        )
        # Rotation
        self.rotation_speed = (0, 2, 0)
        # Schweb-Animation
        self.start_y = position.y
        self.float_offset = 0

    def update(self):
        self.rotation += self.rotation_speed * time.dt
        self.float_offset += time.dt * 2
        self.y = self.start_y + math.sin(self.float_offset) * 0.15
        self.glow.scale = 0.4 + math.sin(self.float_offset) * 0.1

# ============================================================
#  GEGNER (einfach)
# ============================================================
class Enemy(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=Palette.enemy,
            scale=(0.5, 0.5, 0.5),
            position=position,
            collider='box'
        )
        # Augen
        self.eye_l = Entity(
            parent=self,
            model='sphere',
            color=color.white,
            scale=0.08,
            position=(-0.15, 0.1, 0.25)
        )
        self.eye_r = Entity(
            parent=self,
            model='sphere',
            color=color.white,
            scale=0.08,
            position=(0.15, 0.1, 0.25)
        )
        self.pupil_l = Entity(
            parent=self.eye_l,
            model='sphere',
            color=color.black,
            scale=0.5,
            position=(0, 0, 0.05)
        )
        self.pupil_r = Entity(
            parent=self.eye_r,
            model='sphere',
            color=color.black,
            scale=0.5,
            position=(0, 0, 0.05)
        )
        
        self.speed = 1.2
        self.range = 6
        self.state = 'idle'  # idle, chase

    def update(self):
        dist = distance(self, player)
        
        if dist < self.range:
            self.state = 'chase'
            direction = (player.position - self.position).normalized()
            self.position += direction * self.speed * time.dt
            self.rotation_y = -math.degrees(math.atan2(direction.x, direction.z))
            
            # Augen folgen Spieler
            look_dir = (player.position - self.position).normalized()
            self.eye_l.rotation_y = -math.degrees(math.atan2(look_dir.x, look_dir.z))
            self.eye_r.rotation_y = -math.degrees(math.atan2(look_dir.x, look_dir.z))
        else:
            self.state = 'idle'
            # Leichte Wackelbewegung
            self.rotation_y += time.dt * 20
        
        # Kollision mit Spieler
        if dist < 0.8:
            game_over()

# ============================================================
#  POWER-UP
# ============================================================
class PowerUp(Entity):
    def __init__(self, position):
        super().__init__(
            model='octahedron',
            color=Palette.powerup,
            scale=0.2,
            position=position,
            collider='sphere'
        )
        self.glow = Entity(
            parent=self,
            model='sphere',
            color=Palette.powerup,
            scale=0.5,
            blend_transparency=True,
            opacity=0.15
        )
        self.rotation_speed = (2, 2, 0)
        self.start_y = position.y
        
    def update(self):
        self.rotation += self.rotation_speed * time.dt
        self.y = self.start_y + math.sin(time.time() * 2) * 0.1
        self.glow.scale = 0.5 + math.sin(time.time() * 3) * 0.1

# ============================================================
#  PLATTFORM (dekorativ)
# ============================================================
class Platform(Entity):
    def __init__(self, position, size=1.5):
        super().__init__(
            model='cube',
            color=Palette.platform,
            scale=(size, 0.2, size),
            position=position,
            collider='box'
        )
        # Oberseite heller
        self.top = Entity(
            parent=self,
            model='quad',
            color=Palette.platform_top,
            scale=(size * 0.9, size * 0.9),
            position=(0, 0.11, 0),
            rotation=(90, 0, 0)
        )

# ============================================================
#  SPIEL-LOGIK
# ============================================================
def spawn_coins(count=8):
    for _ in range(count):
        x = randint(-6, 6)
        z = randint(-6, 6)
        # Nicht zu nah am Start
        if abs(x) < 2 and abs(z) < 2:
            continue
        coins.append(Coin((x, 0.8, z)))

def spawn_enemies(count=3):
    for _ in range(count):
        x = randint(-5, 5)
        z = randint(-5, 5)
        if abs(x) < 3 and abs(z) < 3:
            continue
        enemies.append(Enemy((x, 0.5, z)))

def spawn_powerups(count=2):
    for _ in range(count):
        x = randint(-5, 5)
        z = randint(-5, 5)
        if abs(x) < 2 and abs(z) < 2:
            continue
        powerups.append(PowerUp((x, 1.0, z)))

def collect_coin(coin):
    global score
    coins.remove(coin)
    destroy(coin)
    destroy(coin.glow)
    score += 1
    score_text.text = f'🌟 {score}'

def game_over():
    global running
    running = False
    
    # Overlay
    overlay = Entity(
        model='quad',
        scale=(20, 20),
        color=color.rgba(0, 0, 0, 180),
        z=10
    )
    Text(
        text='💫 GAME OVER',
        position=(0, 0.2),
        scale=3,
        color=Palette.ui_accent,
        z=20
    )
    Text(
        text=f'Punkte: {score}',
        position=(0, -0.05),
        scale=1.5,
        color=Palette.ui_text,
        z=20
    )
    Text(
        text='Drücke R für Neustart',
        position=(0, -0.3),
        scale=1,
        color=color.gray,
        z=20
    )

def reset_game():
    global score, coins, enemies, powerups, running
    # Alles löschen
    for e in coins + enemies + powerups:
        destroy(e)
    for e in scene.entities:
        if isinstance(e, Text) and e.text in ['💫 GAME OVER', 'Punkte:', 'Drücke R für Neustart']:
            destroy(e)
        if isinstance(e, Entity) and e.model and e.model.name == 'quad' and e.z == 10:
            destroy(e)
    
    coins.clear()
    enemies.clear()
    powerups.clear()
    score = 0
    score_text.text = '🌟 0'
    player.position = (0, 0.5, 0)
    player.collected = 0
    running = True
    
    spawn_coins(8)
    spawn_enemies(3)
    spawn_powerups(2)

# ============================================================
#  UPDATE-FUNKTION
# ============================================================
def update():
    global running
    
    if not running:
        if held_keys['r']:
            reset_game()
        return
    
    player.update()
    
    # Münzen einsammeln
    for coin in coins[:]:
        if distance(player, coin) < 0.6:
            collect_coin(coin)
    
    # Power-Ups einsammeln
    for powerup in powerups[:]:
        if distance(player, powerup) < 0.6:
            powerups.remove(powerup)
            destroy(powerup)
            destroy(powerup.glow)
            # Speed-Boost für 3 Sekunden
            player.speed = 8
            invoke(setattr, player, 'speed', 4, delay=3)
            # Visueller Effekt
            player.color = Palette.powerup
            invoke(setattr, player, 'color', Palette.player, delay=3)
    
    # Gegner aktualisieren
    for enemy in enemies[:]:
        enemy.update()

# ============================================================
#  SZENE AUFBAUEN
# ============================================================
# Boden
ground = Entity(
    model='plane',
    color=Palette.ground,
    scale=20,
    position=(0, -0.5, 0),
    collider='box'
)

# Dekoratives Gitter auf dem Boden
for i in range(-8, 9, 2):
    for j in range(-8, 9, 2):
        if (i + j) % 4 == 0:
            tile = Entity(
                model='quad',
                color=Palette.ground_dark,
                scale=(0.8, 0.8),
                position=(i, -0.49, j),
                rotation=(90, 0, 0)
            )

# Plattformen dekorativ
platforms = [
    (-3, 0.3, -3), (3, 0.3, 3),
    (-4, 0.3, 4), (4, 0.3, -4),
    (0, 0.3, -4), (0, 0.3, 4)
]
for pos in platforms:
    Platform(pos)

# Spieler
player = Player()

# Spielobjekte
coins = []
enemies = []
powerups = []
score = 0
running = True

spawn_coins(8)
spawn_enemies(3)
spawn_powerups(2)

# ============================================================
#  UI
# ============================================================
score_text = Text(
    text='🌟 0',
    position=(-0.85, 0.45),
    scale=2,
    color=Palette.ui_accent
)

# Subtile Hinweise
controls = Text(
    text='WASD  •  Leerzeichen  •  Sammeln',
    position=(0, -0.45),
    scale=0.8,
    color=color.rgba(255, 255, 255, 60),
    origin=(0, 0)
)

# Dekorative Ränder
border_top = Entity(
    model='quad',
    color=color.rgba(255, 215, 100, 30),
    scale=(2, 0.002),
    position=(0, 0.48),
    parent=camera.ui
)

# ============================================================
#  START
# ============================================================
app.run()