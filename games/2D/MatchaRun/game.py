import pygame
import random
import time
import sys
import math
import os

# Pygame initialisieren
pygame.init()

# Fenster
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 635
UI_HEIGHT = 90
TOTAL_HEIGHT = WINDOW_HEIGHT + UI_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("Ilayda flieht vor Elif")
clock = pygame.time.Clock()

# Farben
BLACK = (0, 0, 0)
WHITE = (240, 240, 245)
GREEN = (0, 210, 80)
PINK = (255, 40, 170)
RED = (255, 40, 40)
YELLOW = (255, 210, 0)
DARK_GRAY = (25, 25, 30)

# Schriftarten
FONT = pygame.font.Font(None, 26)
BIG_FONT = pygame.font.Font(None, 48)
SMALL_FONT = pygame.font.Font(None, 18)
SPRACHE_FONT = pygame.font.Font(None, 20)
STORY_FONT = pygame.font.Font(None, 26)

# Spielfeld-Grenzen
STORY_OFFSET = 55
MARGIN = 30
PLAY_LEFT = MARGIN
PLAY_TOP = MARGIN + STORY_OFFSET
PLAY_RIGHT = WINDOW_WIDTH - MARGIN
PLAY_BOTTOM = WINDOW_HEIGHT - MARGIN
PLAY_WIDTH = PLAY_RIGHT - PLAY_LEFT
PLAY_HEIGHT = PLAY_BOTTOM - PLAY_TOP

# ============== BILD LADEN ==============
energie_path = "energie.png"
HAS_IMAGE = False
if os.path.exists(energie_path):
    try:
        redbull_img = pygame.image.load(energie_path)
        redbull_img = pygame.transform.scale(redbull_img, (32, 32))
        HAS_IMAGE = True
        print("✅ energie.png geladen!")
    except:
        print("❌ energie.png konnte nicht geladen werden")
else:
    print("❌ energie.png nicht gefunden")

# ============== SPRÜCHE ==============
ILAYDA_SAYS = [
    "Hilfe! Elif!", "Mein Matcha!", "Schnell weg!",
    "Nicht erwischen!", "Redbull gibt Kraft!", "Ich muss schneller!",
    "Elif ist zu schnell!", "Wo ist Redbull?", "Ich schaff das!", "Nicht aufgeben!"
]

ELIF_SAYS = [
    "Komm her, Ilayda!", "Gib mein Matcha zuruck!", "Du bist dran!",
    "Halt stand!", "Ich krieg dich!", "Matcha-Diebin!",
    "Du bist zu langsam!", "Ilaydaaaaa!", "Jetzt hab ich dich!", "Dein Ende!"
]

# ============== FUNKTIONEN ==============
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return float(f.read().strip())
    except:
        return None

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def draw_stickman(surface, x, y, color, size=38, name="", spruch=""):
    center_x = int(x)
    center_y = int(y)
    radius = size // 6
    
    pygame.draw.circle(surface, color, (center_x, center_y - radius * 2), radius, 2)
    pygame.draw.line(surface, color, (center_x, center_y - radius), (center_x, center_y + radius), 2)
    pygame.draw.line(surface, color, (center_x - radius, center_y), (center_x + radius, center_y), 2)
    pygame.draw.line(surface, color, (center_x, center_y + radius), (center_x - radius, center_y + radius * 2), 2)
    pygame.draw.line(surface, color, (center_x, center_y + radius), (center_x + radius, center_y + radius * 2), 2)
    
    eye_offset = radius // 2
    pygame.draw.circle(surface, color, (center_x - eye_offset, center_y - radius * 2 - 1), 2)
    pygame.draw.circle(surface, color, (center_x + eye_offset, center_y - radius * 2 - 1), 2)
    pygame.draw.arc(surface, color, (center_x - 4, center_y - radius * 2 - 1, 8, 5), 0, 3.14, 1)
    
    if name:
        name_surface = SMALL_FONT.render(name, True, color)
        name_rect = name_surface.get_rect(center=(center_x, center_y - radius * 2 - 20))
        bg_rect = name_rect.inflate(8, 4)
        pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
        surface.blit(name_surface, name_rect)
    
    if spruch:
        spruch_surface = SPRACHE_FONT.render(spruch, True, WHITE)
        spruch_rect = spruch_surface.get_rect(center=(center_x, center_y + radius * 2 + 25))
        bg_rect = spruch_rect.inflate(10, 4)
        pygame.draw.rect(surface, (0, 0, 0, 220), bg_rect)
        surface.blit(spruch_surface, spruch_rect)

def spawn_powerup():
    x = random.randint(PLAY_LEFT + 40, PLAY_RIGHT - 40)
    y = random.randint(PLAY_TOP + 40, PLAY_BOTTOM - 40)
    return {'x': x, 'y': y, 'active': True, 'timer': 0}

# ============== SPIELER-KLASSEN ==============
class Player:
    def __init__(self, x, y, color, name, speed=3.5):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.speed = speed
        self.size = 38
        self.spruch = ""
        self.spruch_timer = 0
        self.boost_timer = 0
    
    def move(self, dx, dy):
        current_speed = self.speed
        if self.boost_timer > 0:
            current_speed = self.speed * 1.8
            self.boost_timer -= 1
        
        new_x = self.x + dx * current_speed
        new_y = self.y + dy * current_speed
        
        new_x = max(PLAY_LEFT + self.size//2, min(PLAY_RIGHT - self.size//2, new_x))
        new_y = max(PLAY_TOP + self.size//2, min(PLAY_BOTTOM - self.size//2, new_y))
        
        if new_x != self.x or new_y != self.y:
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def get_pos(self):
        return (self.x, self.y)
    
    def set_spruch(self, spruch):
        self.spruch = spruch
        self.spruch_timer = 90
    
    def apply_boost(self):
        self.boost_timer = 180
        self.set_spruch("REDBULL!!!")

class AIPlayer:
    def __init__(self, x, y, color, name, speed=2.8):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.speed = speed
        self.size = 38
        self.spruch = ""
        self.spruch_timer = 0
        self.direction_change_timer = 0
    
    def move_towards_target(self, target_x, target_y):
        self.direction_change_timer += 1
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            dx = dx / dist
            dy = dy / dist
            
            if random.random() < 0.1:
                angle = random.uniform(-0.3, 0.3)
                new_dx = dx * math.cos(angle) - dy * math.sin(angle)
                new_dy = dx * math.sin(angle) + dy * math.cos(angle)
                dx, dy = new_dx, new_dy
            
            self.try_move(dx, dy)
        
        if self.direction_change_timer > random.randint(30, 70):
            self.direction_change_timer = 0
            if random.random() < 0.15:
                angle = random.uniform(0, 2 * math.pi)
                dx = math.cos(angle)
                dy = math.sin(angle)
                self.try_move(dx, dy)
    
    def try_move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        new_x = max(PLAY_LEFT + self.size//2, min(PLAY_RIGHT - self.size//2, new_x))
        new_y = max(PLAY_TOP + self.size//2, min(PLAY_BOTTOM - self.size//2, new_y))
        
        self.x = new_x
        self.y = new_y
    
    def get_pos(self):
        return (self.x, self.y)
    
    def set_spruch(self, spruch):
        self.spruch = spruch
        self.spruch_timer = 90

# ============== HAUPTSPIEL ==============
def main():
    # Spieler erstellen
    ilayda = Player(WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 + STORY_OFFSET//2 - 10, PINK, "Ilayda", speed=3.5)
    elif_ai = AIPlayer(WINDOW_WIDTH//2 + 180, WINDOW_HEIGHT//2 + STORY_OFFSET//2 - 10, GREEN, "Elif", speed=2.8)
    
    # Spiel-Status
    start_time = time.time()
    time_limit = 120
    highscore = load_highscore()
    current_score = 0
    game_over = False
    game_active = True
    
    # Power-Ups
    powerups = []
    powerup_spawn_timer = 0
    max_powerups = 5
    
    # Sprüche
    spruch_wechsel_timer = 0
    ilayda_spruch_index = 0
    elif_spruch_index = 0
    
    # Highscore-Text
    highscore_text = f"Highscore: {highscore:.1f}s" if highscore is not None else "Highscore: --"
    
    # Initiale Sprüche setzen
    ilayda.set_spruch(ILAYDA_SAYS[0])
    elif_ai.set_spruch(ELIF_SAYS[0])
    
    running = True
    
    while running:
        # ===== EVENTS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and game_over:
                    # NEUSTART
                    ilayda = Player(WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 + STORY_OFFSET//2 - 10, PINK, "Ilayda", speed=3.5)
                    elif_ai = AIPlayer(WINDOW_WIDTH//2 + 180, WINDOW_HEIGHT//2 + STORY_OFFSET//2 - 10, GREEN, "Elif", speed=2.8)
                    start_time = time.time()
                    current_score = 0
                    game_over = False
                    game_active = True
                    powerups = []
                    powerup_spawn_timer = 0
                    spruch_wechsel_timer = 0
                    ilayda_spruch_index = 0
                    elif_spruch_index = 0
                    highscore = load_highscore()
                    highscore_text = f"Highscore: {highscore:.1f}s" if highscore is not None else "Highscore: --"
                    ilayda.set_spruch(ILAYDA_SAYS[0])
                    elif_ai.set_spruch(ELIF_SAYS[0])
                if event.key == pygame.K_z and game_over:
                    running = False
        
        # ===== SPRÜCHE WECHSELN =====
        if game_active and not game_over:
            spruch_wechsel_timer += 1
            if spruch_wechsel_timer >= 300:
                spruch_wechsel_timer = 0
                ilayda_spruch_index = (ilayda_spruch_index + 1) % len(ILAYDA_SAYS)
                elif_spruch_index = (elif_spruch_index + 1) % len(ELIF_SAYS)
                
                if ilayda.spruch_timer == 0:
                    ilayda.set_spruch(ILAYDA_SAYS[ilayda_spruch_index])
                if elif_ai.spruch_timer == 0:
                    elif_ai.set_spruch(ELIF_SAYS[elif_spruch_index])
        
        # ===== BEWEGUNG =====
        if game_active and not game_over:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 and dy != 0:
                dx = dx * 0.707
                dy = dy * 0.707
            
            if dx != 0 or dy != 0:
                ilayda.move(dx, dy)
        
        if game_active and not game_over:
            ilayda_pos = ilayda.get_pos()
            elif_ai.move_towards_target(ilayda_pos[0], ilayda_pos[1])
        
        # ===== POWER-UPS =====
        if game_active and not game_over:
            powerup_spawn_timer += 1
            if powerup_spawn_timer > random.randint(80, 200) and len(powerups) < max_powerups:
                powerups.append(spawn_powerup())
                powerup_spawn_timer = 0
        
        if game_active and not game_over:
            for powerup in powerups[:]:
                if powerup['active']:
                    if distance(ilayda.x, ilayda.y, powerup['x'], powerup['y']) < 32:
                        ilayda.apply_boost()
                        powerup['active'] = False
                        powerups.remove(powerup)
        
        # ===== KOLLISION =====
        if game_active and not game_over:
            dist = distance(ilayda.x, ilayda.y, elif_ai.x, elif_ai.y)
            if dist < 34:
                game_active = False
                game_over = True
                current_score = time.time() - start_time
                
                if highscore is None or current_score > highscore:
                    highscore = current_score
                    save_highscore(highscore)
                    highscore_text = f"Highscore: {highscore:.1f}s"
        
        # ===== ZEIT =====
        if game_active and not game_over:
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                game_active = False
                game_over = True
                current_score = elapsed
                
                if highscore is None or current_score > highscore:
                    highscore = current_score
                    save_highscore(highscore)
                    highscore_text = f"Highscore: {highscore:.1f}s"
        
        # ===== SPRÜCHE-TIMER =====
        if ilayda.spruch_timer > 0:
            ilayda.spruch_timer -= 1
            if ilayda.spruch_timer == 0:
                ilayda.spruch = ""
        
        if elif_ai.spruch_timer > 0:
            elif_ai.spruch_timer -= 1
            if elif_ai.spruch_timer == 0:
                elif_ai.spruch = ""
        
        # ===== POWER-UP TIMER =====
        for powerup in powerups[:]:
            powerup['timer'] += 1
            if powerup['timer'] > 300:
                powerup['active'] = False
                powerups.remove(powerup)
        
        # ===== ZEICHNEN =====
        screen.fill(BLACK)
        
        # Spielfeld-Rand
        pygame.draw.rect(screen, DARK_GRAY, (PLAY_LEFT, PLAY_TOP, PLAY_WIDTH, PLAY_HEIGHT), 1)
        
        # Story-Text
        story_text = STORY_FONT.render("Ohoh, Ilayda hat Elifs Matcha geklaut... RENN!", True, WHITE)
        story_rect = story_text.get_rect(center=(WINDOW_WIDTH//2, 28))
        screen.blit(story_text, story_rect)
        
        # Power-Ups zeichnen
        for powerup in powerups:
            if powerup['active']:
                if HAS_IMAGE:
                    img_rect = redbull_img.get_rect(center=(int(powerup['x']), int(powerup['y'])))
                    screen.blit(redbull_img, img_rect)
                else:
                    pygame.draw.circle(screen, RED, (int(powerup['x']), int(powerup['y'])), 16)
                    pygame.draw.circle(screen, WHITE, (int(powerup['x']), int(powerup['y'])), 16, 2)
                    rb_text = SMALL_FONT.render("RB", True, WHITE)
                    rb_rect = rb_text.get_rect(center=(int(powerup['x']), int(powerup['y'])))
                    screen.blit(rb_text, rb_rect)
        
        # Strichmännchen
        draw_stickman(screen, ilayda.x, ilayda.y, PINK, ilayda.size, "Ilayda", ilayda.spruch)
        draw_stickman(screen, elif_ai.x, elif_ai.y, GREEN, elif_ai.size, "Elif", elif_ai.spruch)
        
        # BOOST-Anzeige
        if ilayda.boost_timer > 0:
            boost_text = BIG_FONT.render("BOOST!", True, YELLOW)
            boost_rect = boost_text.get_rect(center=(ilayda.x, ilayda.y - 55))
            screen.blit(boost_text, boost_rect)
        
        # ===== UI =====
        ui_y = WINDOW_HEIGHT
        pygame.draw.rect(screen, (10, 10, 15), (0, ui_y, WINDOW_WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (0, ui_y), (WINDOW_WIDTH, ui_y), 1)
        
        # Timer / Highscore / Info
        if game_active:
            elapsed = time.time() - start_time
            timer_text = FONT.render(f"Zeit: {elapsed:.1f}s / {time_limit}s", True, WHITE)
            screen.blit(timer_text, (10, ui_y + 8))
        else:
            timer_text = FONT.render(f"Ueberlebt: {current_score:.1f}s", True, WHITE)
            screen.blit(timer_text, (10, ui_y + 8))
        
        highscore_display = FONT.render(highscore_text, True, YELLOW)
        screen.blit(highscore_display, (280, ui_y + 8))
        
        rb_info = FONT.render("Redbull = Speed", True, RED)
        screen.blit(rb_info, (480, ui_y + 8))
        
        controls = FONT.render("Pfeiltasten / WASD", True, WHITE)
        screen.blit(controls, (660, ui_y + 8))
        
        # Status
        if game_over:
            status = FONT.render("GAME OVER! T=Neustart  Z=Beenden", True, RED)
            screen.blit(status, (10, ui_y + 40))
        else:
            status = FONT.render("Flieh vor Elif!", True, WHITE)
            screen.blit(status, (10, ui_y + 40))
        
        # ===== GAME OVER OVERLAY =====
        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            if current_score >= time_limit:
                text = BIG_FONT.render("ILAYDA HAT UEBERLEBT!", True, GREEN)
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 - 40))
                screen.blit(text, text_rect)
                
                sub_text = FONT.render("Der Matcha ist sicher!", True, WHITE)
                sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 + 10))
                screen.blit(sub_text, sub_rect)
            else:
                text = BIG_FONT.render("ERWISCHT VON ELIF!", True, RED)
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 - 60))
                screen.blit(text, text_rect)
                
                sub_text1 = FONT.render("Ilayda wurde gefangen!", True, WHITE)
                sub_rect1 = sub_text1.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 + 10))
                screen.blit(sub_text1, sub_rect1)
                
                sub_text2 = FONT.render(f"Ueberlebt: {current_score:.1f}s", True, WHITE)
                sub_rect2 = sub_text2.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 + 40))
                screen.blit(sub_text2, sub_rect2)
            
            if highscore is not None:
                best_text = FONT.render(f"Highscore: {highscore:.1f}s", True, YELLOW)
                best_rect = best_text.get_rect(center=(WINDOW_WIDTH//2, PLAY_TOP + PLAY_HEIGHT//2 + 70))
                screen.blit(best_text, best_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()