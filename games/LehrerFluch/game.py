import pygame
import random
import math
import time
import os
import json

# Initialisierung
pygame.init()

# Fenster-Einstellungen
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lehrers Fluch")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
PINK = (255, 105, 180)
DARK_PINK = (255, 20, 147)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 150, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (181, 101, 29)
DARK_RED = (139, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
TURQUOISE = (64, 224, 208)
DARK_TURQUOISE = (0, 206, 209)
CRIMSON = (220, 20, 60)
GOLD = (255, 215, 0)
HOT_PINK = (255, 105, 180)
DARK_HOT_PINK = (199, 21, 133)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
SILVER = (192, 192, 192)
DARK_SILVER = (128, 128, 128)
NEON_GREEN = (57, 255, 20)
DARK_NEON_GREEN = (0, 200, 0)

# Rekord-Datei
RECORD_FILE = "lehrers_rekord.json"

# Hintergrundbild laden
try:
    background = pygame.image.load("wald.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    has_background = True
    print("✓ Hintergrundbild geladen!")
except:
    has_background = False
    print("✗ Kein 'wald.jpg' gefunden. Verwende Standard-Hintergrund.")

def save_record(time_record):
    records = {}
    
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, 'r') as f:
                records = json.load(f)
        except:
            records = {}
    
    records["prime"] = time_record
    
    with open(RECORD_FILE, 'w') as f:
        json.dump(records, f)

def load_record():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, 'r') as f:
                records = json.load(f)
                return records.get("prime", None)
        except:
            return None
    return None

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
medium_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

class Stickman:
    def __init__(self, x, y, color=BLUE):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 12
        self.drunk_speed_multiplier = 1.0
        self.slow_multiplier = 1.0
        self.shield_active = False
        self.shield_end_time = 0
        self.invincible = False
        self.invincible_end_time = 0
        self.drunk_end_time = 0
        self.slow_end_time = 0
        self.magnet_active = False
        self.magnet_end_time = 0
        self.heal_boost_active = False
        self.heal_boost_end_time = 0
        self.freeze_active = False
        self.freeze_end_time = 0
        self.teleport_active = False
        self.teleport_end_time = 0
        self.shield_break_active = False
        self.shield_break_end_time = 0
        
    def draw(self):
        # Magnet-Effekt (Julian)
        if self.magnet_active and pygame.time.get_ticks() < self.magnet_end_time:
            pygame.draw.circle(screen, HOT_PINK, (int(self.x), int(self.y)), 30, 2)
            pygame.draw.circle(screen, HOT_PINK, (int(self.x), int(self.y)), 35, 1)
        
        # Heal-Boost-Effekt (Arda)
        if self.heal_boost_active and pygame.time.get_ticks() < self.heal_boost_end_time:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 25, 3)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 30, 2)
            for i in range(3):
                angle = i * 2 * math.pi / 3 + pygame.time.get_ticks() / 1000
                heart_x = int(self.x + 20 * math.cos(angle))
                heart_y = int(self.y + 20 * math.sin(angle))
                pygame.draw.circle(screen, RED, (heart_x, heart_y), 4)
                pygame.draw.circle(screen, RED, (heart_x - 2, heart_y - 2), 2)
                pygame.draw.circle(screen, RED, (heart_x + 2, heart_y - 2), 2)
        
        # Schild-Effekt (Samuel)
        if self.shield_active and pygame.time.get_ticks() < self.shield_end_time:
            pygame.draw.circle(screen, SILVER, (int(self.x), int(self.y)), 20, 3)
            pygame.draw.circle(screen, DARK_SILVER, (int(self.x), int(self.y)), 25, 1)
        
        # Unverwundbarkeits-Effekt (Ege)
        if self.invincible and pygame.time.get_ticks() < self.invincible_end_time:
            if pygame.time.get_ticks() % 200 < 100:
                return
        
        # Freeze-Effekt (Jannis)
        if self.freeze_active and pygame.time.get_ticks() < self.freeze_end_time:
            pygame.draw.circle(screen, (0, 150, 255), (int(self.x), int(self.y)), 28, 3)
            pygame.draw.circle(screen, (0, 200, 255), (int(self.x), int(self.y)), 33, 2)
        
        # Teleport-Effekt (Felix)
        if self.teleport_active and pygame.time.get_ticks() < self.teleport_end_time:
            pygame.draw.circle(screen, PURPLE, (int(self.x), int(self.y)), 30, 3)
            pygame.draw.circle(screen, HOT_PINK, (int(self.x), int(self.y)), 35, 2)
        
        # Shield-Break-Effekt (Onur)
        if self.shield_break_active and pygame.time.get_ticks() < self.shield_break_end_time:
            pygame.draw.circle(screen, NEON_GREEN, (int(self.x), int(self.y)), 28, 3)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 33, 2)
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y) + 8), 
                        (int(self.x), int(self.y) + 25), 2)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y) + 13), 
                        (int(self.x) - 8, int(self.y) + 20), 2)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y) + 13), 
                        (int(self.x) + 8, int(self.y) + 20), 2)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y) + 25), 
                        (int(self.x) - 8, int(self.y) + 38), 2)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y) + 25), 
                        (int(self.x) + 8, int(self.y) + 38), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x) - 3, int(self.y) - 2), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x) + 3, int(self.y) - 2), 2)
        
    def get_rect(self):
        return pygame.Rect(self.x - 12, self.y - 12, 24, 50)

class Enemy:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 170  
        self.direction = 1
        self.speed = 3
        self.last_shot = 0
        self.last_saying = 0
        self.current_saying = ""
        self.saying_end_time = 0
        self.shield_active = True
        self.teacher_sayings = [
            "Hausaufgaben abgeben!",
            "Setz dich hin!",
            "Ruhe im Klassenzimmer!",
            "Das gibt eine 6!",
            "Nachsitzen!",
            "Wo ist deine Hausaufgabe?",
            "Schau mich an wenn ich mit dir rede!",
            "Das war nicht sehr klug!"
        ]
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 70 or self.x >= WIDTH - 70:
            self.direction *= -1
            
    def draw(self):
        scale = 1.0
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        # Lehrer-Schutzschild anzeigen
        if self.shield_active:
            pygame.draw.circle(screen, (0, 150, 255), (x_pos, y_pos), 25, 2)
            pygame.draw.circle(screen, (0, 200, 255), (x_pos, y_pos), 30, 1)
        
        pygame.draw.line(screen, DARK_BLUE, (x_pos, y_pos + 10 * scale), 
                        (x_pos, y_pos + 28 * scale), int(4 * scale))
        
        pygame.draw.line(screen, DARK_BLUE, (x_pos, y_pos + 16 * scale), 
                        (x_pos - 10 * scale, y_pos + 22 * scale), int(3 * scale))
        pygame.draw.line(screen, DARK_BLUE, (x_pos, y_pos + 16 * scale), 
                        (x_pos + 10 * scale, y_pos + 22 * scale), int(3 * scale))
        
        pygame.draw.line(screen, DARK_GRAY, (x_pos, y_pos + 28 * scale), 
                        (x_pos - 8 * scale, y_pos + 40 * scale), int(3 * scale))
        pygame.draw.line(screen, DARK_GRAY, (x_pos, y_pos + 28 * scale), 
                        (x_pos + 8 * scale, y_pos + 40 * scale), int(3 * scale))
        
        pygame.draw.circle(screen, (255, 200, 150), (x_pos, y_pos), int(10 * scale))
        pygame.draw.circle(screen, DARK_BLUE, (x_pos, y_pos), int(10 * scale), 2)
        
        pygame.draw.circle(screen, BLACK, (x_pos - 5, y_pos - 2), 3, 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 5, y_pos - 2), 3, 1)
        pygame.draw.line(screen, BLACK, (x_pos - 2, y_pos - 2), (x_pos + 2, y_pos - 2), 1)
        
        pygame.draw.circle(screen, BLACK, (x_pos - 5, y_pos - 2), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 5, y_pos - 2), 1)
        
        pygame.draw.line(screen, BLACK, (x_pos - 4, y_pos + 4), (x_pos + 4, y_pos + 4), 2)
        
        pygame.draw.polygon(screen, RED, [(x_pos - 2, y_pos + 10), 
                                         (x_pos + 2, y_pos + 10), 
                                         (x_pos, y_pos + 18)])
        
        # Gegner Name: "Hr. Seng"
        name_text = small_font.render("Hr. Seng", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 35))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, DARK_BLUE, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
        
        if self.current_saying and pygame.time.get_ticks() < self.saying_end_time:
            text = small_font.render(self.current_saying, True, BLACK)
            text_rect = text.get_rect(center=(x_pos, y_pos - 65))
            
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10))
            pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 10), 2)
            points = [(x_pos - 8, y_pos - 48),
                     (x_pos, y_pos - 40),
                     (x_pos + 8, y_pos - 48)]
            pygame.draw.polygon(screen, WHITE, points)
            pygame.draw.polygon(screen, BLACK, points, 2)
            
            screen.blit(text, text_rect)
        
    def shoot(self, target_x, target_y):
        now = pygame.time.get_ticks()
        if not self.shield_active:
            return None
            
        cooldown = 500
        if now - self.last_shot > cooldown:
            self.last_shot = now
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist != 0:
                dx /= dist
                dy /= dist
            
            if random.random() < 0.05:
                self.current_saying = random.choice(self.teacher_sayings)
                self.saying_end_time = now + 2000
            
            return Projectile(self.x, self.y + 15, dx * 6, dy * 6, is_chalk=True)
        return None

class Projectile:
    def __init__(self, x, y, vx, vy, is_chalk=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 6
        self.is_chalk = is_chalk
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self):
        if self.is_chalk:
            pygame.draw.rect(screen, WHITE, (int(self.x) - 4, int(self.y) - 2, 8, 4))
            pygame.draw.rect(screen, LIGHT_GRAY, (int(self.x) - 4, int(self.y) - 2, 8, 4), 1)
        else:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
            pygame.draw.circle(screen, BLACK, (int(self.x) - 2, int(self.y) - 2), 2)
            pygame.draw.arc(screen, BLACK, (int(self.x) - 4, int(self.y) - 1, 8, 6), 0, math.pi, 1)
        
    def get_rect(self):
        return pygame.Rect(self.x - 6, self.y - 6, 12, 12)

class Namet:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.0
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        self.animation_offset = 0
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        self.animation_offset = (self.animation_offset + 0.1) % (2 * math.pi)
        float_y = self.y + math.sin(self.animation_offset) * 3
        x_pos = int(self.x)
        y_pos = int(float_y)
        
        pygame.draw.circle(screen, GOLD, (x_pos, y_pos), 12)
        pygame.draw.circle(screen, SILVER, (x_pos, y_pos), 12, 2)
        
        pygame.draw.line(screen, WHITE, (x_pos - 8, y_pos), (x_pos + 8, y_pos), 3)
        pygame.draw.line(screen, WHITE, (x_pos, y_pos - 8), (x_pos, y_pos + 8), 3)
        
        pygame.draw.line(screen, GOLD, (x_pos, y_pos + 12), 
                        (x_pos, y_pos + 30), 3)
        
        pygame.draw.line(screen, GOLD, (x_pos, y_pos + 17), 
                        (x_pos - 12, y_pos + 24), 3)
        pygame.draw.line(screen, GOLD, (x_pos, y_pos + 17), 
                        (x_pos + 12, y_pos + 24), 3)
        
        pygame.draw.line(screen, GOLD, (x_pos, y_pos + 30), 
                        (x_pos - 10, y_pos + 44), 3)
        pygame.draw.line(screen, GOLD, (x_pos, y_pos + 30), 
                        (x_pos + 10, y_pos + 44), 3)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 2), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 2), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 2), 1)
        
        pygame.draw.arc(screen, SILVER, (x_pos - 5, y_pos + 2, 10, 6), 0, math.pi, 2)
        
        # NUR Name, keine Beschreibung
        name_text = small_font.render("Namet", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, GOLD, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Jannis:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.0
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, (0, 150, 255), (x_pos, y_pos), 10)
        pygame.draw.circle(screen, (0, 200, 255), (x_pos, y_pos), 10, 2)
        
        for i in range(4):
            angle = i * math.pi / 2
            pygame.draw.line(screen, (0, 200, 255), 
                           (x_pos + 6 * math.cos(angle), y_pos + 6 * math.sin(angle)),
                           (x_pos + 12 * math.cos(angle), y_pos + 12 * math.sin(angle)), 2)
        
        pygame.draw.line(screen, (0, 150, 255), (x_pos, y_pos + 10), 
                        (x_pos, y_pos + 28), 2)
        
        pygame.draw.line(screen, (0, 150, 255), (x_pos, y_pos + 15), 
                        (x_pos - 10, y_pos + 22), 2)
        pygame.draw.line(screen, (0, 150, 255), (x_pos, y_pos + 15), 
                        (x_pos + 10, y_pos + 22), 2)
        
        pygame.draw.line(screen, (0, 150, 255), (x_pos, y_pos + 28), 
                        (x_pos - 10, y_pos + 40), 2)
        pygame.draw.line(screen, (0, 150, 255), (x_pos, y_pos + 28), 
                        (x_pos + 10, y_pos + 40), 2)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 2), 2)
        pygame.draw.circle(screen, (0, 100, 255), (x_pos - 4, y_pos - 2), 1)
        pygame.draw.circle(screen, (0, 100, 255), (x_pos + 4, y_pos - 2), 1)
        
        pygame.draw.arc(screen, (0, 200, 255), (x_pos - 5, y_pos + 2, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Jannis", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, (0, 150, 255), name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Leon:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 1.5
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        self.drunk_sway = 0
        
    def update(self):
        self.drunk_sway += 0.05
        sway_offset = math.sin(self.drunk_sway) * 0.5
        
        self.x += (self.speed * self.direction) + sway_offset
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        sway = math.sin(self.drunk_sway) * 2
        x_pos = int(self.x + sway)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, BROWN, (x_pos, y_pos), 10)
        pygame.draw.circle(screen, LIGHT_BROWN, (x_pos, y_pos), 10, 2)
        
        pygame.draw.line(screen, BROWN, (x_pos, y_pos + 10), 
                        (x_pos, y_pos + 28), 2)
        
        pygame.draw.line(screen, BROWN, (x_pos, y_pos + 15), 
                        (x_pos - 12, y_pos + 20 + int(sway)), 2)
        pygame.draw.line(screen, BROWN, (x_pos, y_pos + 15), 
                        (x_pos + 12, y_pos + 20 - int(sway)), 2)
        
        pygame.draw.line(screen, BROWN, (x_pos, y_pos + 28), 
                        (x_pos - 10 + int(sway), y_pos + 40), 2)
        pygame.draw.line(screen, BROWN, (x_pos, y_pos + 28), 
                        (x_pos + 10 + int(sway), y_pos + 40), 2)
        
        pygame.draw.circle(screen, RED, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, RED, (x_pos + 4, y_pos - 2), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 2), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 2), 1)
        
        pygame.draw.arc(screen, DARK_RED, (x_pos - 6, y_pos + 4, 12, 8), 0, math.pi, 2)
        
        pygame.draw.rect(screen, (139, 69, 19), (x_pos - 15, y_pos + 5, 4, 10))
        pygame.draw.circle(screen, (139, 69, 19), (x_pos - 15, y_pos + 5), 3)
        
        # NUR Name
        name_text = small_font.render("Leon", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 25))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, BROWN, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
        
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 55)

class Samuel:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 1.2
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, SILVER, (x_pos, y_pos), 14)
        pygame.draw.circle(screen, DARK_SILVER, (x_pos, y_pos), 14, 2)
        
        pygame.draw.circle(screen, DARK_SILVER, (x_pos, y_pos), 18, 2)
        pygame.draw.line(screen, DARK_SILVER, (x_pos - 18, y_pos), (x_pos + 18, y_pos), 2)
        pygame.draw.line(screen, DARK_SILVER, (x_pos, y_pos - 18), (x_pos, y_pos + 18), 2)
        
        pygame.draw.line(screen, SILVER, (x_pos, y_pos + 14), 
                        (x_pos, y_pos + 32), 4)
        
        pygame.draw.line(screen, SILVER, (x_pos, y_pos + 18), 
                        (x_pos - 14, y_pos + 26), 4)
        pygame.draw.line(screen, SILVER, (x_pos, y_pos + 18), 
                        (x_pos + 14, y_pos + 26), 4)
        
        pygame.draw.line(screen, SILVER, (x_pos, y_pos + 32), 
                        (x_pos - 12, y_pos + 48), 4)
        pygame.draw.line(screen, SILVER, (x_pos, y_pos + 32), 
                        (x_pos + 12, y_pos + 48), 4)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 3), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 3), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 3), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 3), 1)
        
        pygame.draw.arc(screen, DARK_SILVER, (x_pos - 5, y_pos + 3, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Samuel", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 30))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(20, 8))
        pygame.draw.rect(screen, SILVER, name_rect.inflate(20, 8), 2)
        screen.blit(name_text, name_rect)
        
    def get_rect(self):
        return pygame.Rect(self.x - 18, self.y - 18, 36, 66)

class Arda:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.5
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, GREEN, (x_pos, y_pos), 12)
        pygame.draw.circle(screen, GOLD, (x_pos, y_pos), 12, 2)
        
        for i in range(3):
            angle = i * 2 * math.pi / 3
            heart_x = x_pos + 10 * math.cos(angle)
            heart_y = y_pos + 10 * math.sin(angle)
            pygame.draw.circle(screen, RED, (int(heart_x), int(heart_y)), 4)
            pygame.draw.circle(screen, RED, (int(heart_x) - 2, int(heart_y) - 2), 2)
            pygame.draw.circle(screen, RED, (int(heart_x) + 2, int(heart_y) - 2), 2)
        
        pygame.draw.line(screen, GREEN, (x_pos, y_pos + 12), 
                        (x_pos, y_pos + 30), 3)
        
        pygame.draw.line(screen, GREEN, (x_pos, y_pos + 17), 
                        (x_pos - 12, y_pos + 24), 3)
        pygame.draw.line(screen, GREEN, (x_pos, y_pos + 17), 
                        (x_pos + 12, y_pos + 24), 3)
        
        pygame.draw.line(screen, GREEN, (x_pos, y_pos + 30), 
                        (x_pos - 10, y_pos + 44), 3)
        pygame.draw.line(screen, GREEN, (x_pos, y_pos + 30), 
                        (x_pos + 10, y_pos + 44), 3)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 3), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 3), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 3), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 3), 1)
        
        pygame.draw.arc(screen, GOLD, (x_pos - 5, y_pos + 3, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Arda", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, GREEN, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Ege:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.8
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, TURQUOISE, (x_pos, y_pos), 12)
        pygame.draw.circle(screen, DARK_TURQUOISE, (x_pos, y_pos), 12, 2)
        
        pygame.draw.circle(screen, GOLD, (x_pos - 6, y_pos - 6), 4)
        for i in range(8):
            angle = i * math.pi / 4
            pygame.draw.line(screen, GOLD, 
                           (x_pos - 6 + 4 * math.cos(angle), 
                            y_pos - 6 + 4 * math.sin(angle)),
                           (x_pos - 6 + 7 * math.cos(angle), 
                            y_pos - 6 + 7 * math.sin(angle)), 1)
        
        for i in range(3):
            x_offset = -8 + i * 8
            pygame.draw.arc(screen, DARK_TURQUOISE, 
                          (x_pos + x_offset, y_pos + 8, 8, 4), 
                          0, math.pi, 1)
        
        pygame.draw.line(screen, TURQUOISE, (x_pos, y_pos + 12), 
                        (x_pos, y_pos + 30), 3)
        
        pygame.draw.line(screen, TURQUOISE, (x_pos, y_pos + 17), 
                        (x_pos - 12, y_pos + 24), 3)
        pygame.draw.line(screen, TURQUOISE, (x_pos, y_pos + 17), 
                        (x_pos + 12, y_pos + 24), 3)
        
        pygame.draw.line(screen, TURQUOISE, (x_pos, y_pos + 30), 
                        (x_pos - 10, y_pos + 44), 3)
        pygame.draw.line(screen, TURQUOISE, (x_pos, y_pos + 30), 
                        (x_pos + 10, y_pos + 44), 3)
        
        # NUR Name
        name_text = small_font.render("Ege", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, TURQUOISE, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Julian:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.0
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, HOT_PINK, (x_pos, y_pos), 10)
        pygame.draw.circle(screen, DARK_HOT_PINK, (x_pos, y_pos), 10, 2)
        
        pygame.draw.rect(screen, DARK_HOT_PINK, (x_pos - 12, y_pos - 12, 24, 4))
        pygame.draw.rect(screen, DARK_HOT_PINK, (x_pos - 12, y_pos + 8, 24, 4))
        pygame.draw.rect(screen, DARK_HOT_PINK, (x_pos - 12, y_pos - 4, 4, 8))
        pygame.draw.rect(screen, DARK_HOT_PINK, (x_pos + 8, y_pos - 4, 4, 8))
        
        pygame.draw.line(screen, HOT_PINK, (x_pos, y_pos + 10), 
                        (x_pos, y_pos + 28), 2)
        
        pygame.draw.line(screen, HOT_PINK, (x_pos, y_pos + 15), 
                        (x_pos - 10, y_pos + 22), 2)
        pygame.draw.line(screen, HOT_PINK, (x_pos, y_pos + 15), 
                        (x_pos + 10, y_pos + 22), 2)
        
        pygame.draw.line(screen, HOT_PINK, (x_pos, y_pos + 28), 
                        (x_pos - 10, y_pos + 40), 2)
        pygame.draw.line(screen, HOT_PINK, (x_pos, y_pos + 28), 
                        (x_pos + 10, y_pos + 40), 2)
        
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 2), 2)
        
        pygame.draw.arc(screen, DARK_HOT_PINK, (x_pos - 5, y_pos + 2, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Julian", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, HOT_PINK, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Felix:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 3.0
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, PURPLE, (x_pos, y_pos), 10)
        pygame.draw.circle(screen, HOT_PINK, (x_pos, y_pos), 10, 2)
        
        pygame.draw.circle(screen, HOT_PINK, (x_pos - 10, y_pos - 8), 4, 1)
        pygame.draw.circle(screen, HOT_PINK, (x_pos + 10, y_pos - 8), 4, 1)
        pygame.draw.circle(screen, HOT_PINK, (x_pos - 10, y_pos + 8), 4, 1)
        pygame.draw.circle(screen, HOT_PINK, (x_pos + 10, y_pos + 8), 4, 1)
        
        pygame.draw.line(screen, PURPLE, (x_pos, y_pos + 10), 
                        (x_pos, y_pos + 28), 2)
        
        pygame.draw.line(screen, PURPLE, (x_pos, y_pos + 15), 
                        (x_pos - 10, y_pos + 22), 2)
        pygame.draw.line(screen, PURPLE, (x_pos, y_pos + 15), 
                        (x_pos + 10, y_pos + 22), 2)
        
        pygame.draw.line(screen, PURPLE, (x_pos, y_pos + 28), 
                        (x_pos - 10, y_pos + 40), 2)
        pygame.draw.line(screen, PURPLE, (x_pos, y_pos + 28), 
                        (x_pos + 10, y_pos + 40), 2)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 2), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 2), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 2), 1)
        
        pygame.draw.arc(screen, HOT_PINK, (x_pos - 5, y_pos + 2, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Felix", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, PURPLE, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

class Onur:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        self.speed = 2.2
        self.talking = False
        self.talk_start = 0
        self.lifetime = pygame.time.get_ticks()
        
    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 40 or self.x >= WIDTH - 40:
            self.direction *= -1
            
        if self.talking and pygame.time.get_ticks() - self.talk_start > 3000:
            return False
        return True
        
    def draw(self):
        x_pos = int(self.x)
        y_pos = int(self.y)
        
        pygame.draw.circle(screen, NEON_GREEN, (x_pos, y_pos), 10)
        pygame.draw.circle(screen, DARK_NEON_GREEN, (x_pos, y_pos), 10, 2)
        
        pygame.draw.line(screen, YELLOW, (x_pos - 10, y_pos - 10), (x_pos + 10, y_pos + 10), 2)
        pygame.draw.line(screen, YELLOW, (x_pos - 10, y_pos + 10), (x_pos + 10, y_pos - 10), 2)
        pygame.draw.circle(screen, YELLOW, (x_pos, y_pos), 14, 1)
        
        pygame.draw.line(screen, NEON_GREEN, (x_pos, y_pos + 10), 
                        (x_pos, y_pos + 28), 2)
        
        pygame.draw.line(screen, NEON_GREEN, (x_pos, y_pos + 15), 
                        (x_pos - 10, y_pos + 22), 2)
        pygame.draw.line(screen, NEON_GREEN, (x_pos, y_pos + 15), 
                        (x_pos + 10, y_pos + 22), 2)
        
        pygame.draw.line(screen, NEON_GREEN, (x_pos, y_pos + 28), 
                        (x_pos - 10, y_pos + 40), 2)
        pygame.draw.line(screen, NEON_GREEN, (x_pos, y_pos + 28), 
                        (x_pos + 10, y_pos + 40), 2)
        
        pygame.draw.circle(screen, WHITE, (x_pos - 4, y_pos - 2), 2)
        pygame.draw.circle(screen, WHITE, (x_pos + 4, y_pos - 2), 2)
        pygame.draw.circle(screen, BLACK, (x_pos - 4, y_pos - 2), 1)
        pygame.draw.circle(screen, BLACK, (x_pos + 4, y_pos - 2), 1)
        
        pygame.draw.arc(screen, DARK_NEON_GREEN, (x_pos - 5, y_pos + 2, 10, 6), 0, math.pi, 2)
        
        # NUR Name
        name_text = small_font.render("Onur", True, BLACK)
        name_rect = name_text.get_rect(center=(x_pos, y_pos - 22))
        pygame.draw.rect(screen, WHITE, name_rect.inflate(15, 8))
        pygame.draw.rect(screen, NEON_GREEN, name_rect.inflate(15, 8), 2)
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 60)

def show_start_screen():
    screen.fill(BLACK)
    
    if has_background:
        screen.blit(background, (0, 0))
    else:
        for _ in range(100):
            pygame.draw.circle(screen, WHITE, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    title_shadow = big_font.render("LEHRERS FLUCH", True, (50, 0, 50))
    title = big_font.render("LEHRERS FLUCH", True, DARK_BLUE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4 - 30))
    screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title, title_rect)
    
    subtitle = medium_font.render("Überlebe den Unterricht!", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//4 + 40))
    screen.blit(subtitle, subtitle_rect)
    
    prime_record = load_record()
    if prime_record:
        record_text = font.render(f"🏆 Rekord: {prime_record:.1f} Sekunden", True, YELLOW)
        record_rect = record_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 90))
        screen.blit(record_text, record_rect)
    
    start_text = medium_font.render("DRÜCKE [SPACE] ZUM STARTEN", True, GREEN)
    start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    if pygame.time.get_ticks() % 1000 < 500:
        screen.blit(start_text, start_rect)
    
    quit_text = small_font.render("Drücke [ESC] zum Beenden", True, RED)
    quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(quit_text, quit_rect)
    
    # Charakter-Info - nur Namen
    char_text = small_font.render("👥 Namet | Jannis | Leon | Samuel | Arda | Ege | Julian | Felix | Onur", True, WHITE)
    char_rect = char_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
    screen.blit(char_text, char_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return None
        
        if pygame.time.get_ticks() % 1000 < 500:
            screen.blit(start_text, start_rect)
        else:
            pygame.draw.rect(screen, BLACK, start_rect.inflate(20, 10))
        
        pygame.display.flip()
        clock.tick(30)

def show_game_over(won, is_new_record, time_taken, best_time):
    screen.fill(BLACK)
    
    if has_background:
        screen.blit(background, (0, 0))
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    if is_new_record:
        text = big_font.render("🏆 NEUER REKORD! 🏆", True, GREEN)
        sub_text = font.render(f"Du hast {time_taken:.1f} Sekunden überlebt!", True, WHITE)
        if best_time is not None:
            record_text = font.render(f"🔥 Alter Rekord war {best_time:.1f}s - Unglaublich!", True, YELLOW)
        else:
            record_text = font.render("🔥 Erster Rekord - Unglaublich!", True, YELLOW)
        time_text = font.render(f"⏱️ Überlebenszeit: {time_taken:.1f} Sekunden", True, ORANGE)
    else:
        text = big_font.render("💀 DURCHGEFALLEN! 💀", True, RED)
        sub_text = font.render("Hr. Seng hat dich erwischt!", True, WHITE)
        if best_time:
            record_text = font.render(f"📊 Deine Zeit: {time_taken:.1f}s | Rekord: {best_time:.1f}s", True, WHITE)
        else:
            record_text = font.render(f"📊 Deine Zeit: {time_taken:.1f}s", True, WHITE)
        time_text = font.render(f"⏱️ Überlebenszeit: {time_taken:.1f} Sekunden", True, ORANGE)
    
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//3 - 30))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 20))
    time_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    record_rect = record_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    screen.blit(text, text_rect)
    screen.blit(sub_text, sub_rect)
    screen.blit(time_text, time_rect)
    screen.blit(record_text, record_rect)
    
    restart_text = medium_font.render("DRÜCKE [R] FÜR NEUSTART", True, GREEN)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT - 80))
    
    menu_text = medium_font.render("DRÜCKE [M] FÜR MENÜ", True, RED)
    menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT - 40))
    
    if pygame.time.get_ticks() % 1000 < 500:
        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)
    else:
        pygame.draw.rect(screen, BLACK, restart_rect.inflate(20, 10))
        pygame.draw.rect(screen, BLACK, menu_rect.inflate(20, 10))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    return False
        
        if pygame.time.get_ticks() % 1000 < 500:
            screen.blit(restart_text, restart_rect)
            screen.blit(menu_text, menu_rect)
        else:
            pygame.draw.rect(screen, BLACK, restart_rect.inflate(20, 10))
            pygame.draw.rect(screen, BLACK, menu_rect.inflate(20, 10))
        
        pygame.display.flip()
        clock.tick(30)
    return False

def main():
    while True:
        start = show_start_screen()
        if start is None:
            break
        
        best_time = load_record()
        
        player = Stickman(WIDTH//2, HEIGHT//2)
        enemy = Enemy()
        projectiles = []
        namet_list = []
        jannis_list = []
        leon_list = []
        samuel_list = []
        arda_list = []
        ege_list = []
        julian_list = []
        felix_list = []
        onur_list = []
        
        health = 50
        collected_namets = 0
        start_time = time.time()
        last_namet_spawn = pygame.time.get_ticks()
        last_jannis_spawn = pygame.time.get_ticks()
        last_leon_spawn = pygame.time.get_ticks()
        last_samuel_spawn = pygame.time.get_ticks()
        last_arda_spawn = pygame.time.get_ticks()
        last_ege_spawn = pygame.time.get_ticks()
        last_julian_spawn = pygame.time.get_ticks()
        last_felix_spawn = pygame.time.get_ticks()
        last_onur_spawn = pygame.time.get_ticks()
        
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            base_speed = 6
            
            if player.drunk_speed_multiplier > 1.0 and current_time > player.drunk_end_time:
                player.drunk_speed_multiplier = 1.0
            
            if player.slow_multiplier < 1.0 and current_time > player.slow_end_time:
                player.slow_multiplier = 1.0
            
            if player.freeze_active and current_time < player.freeze_end_time:
                enemy.speed = 1.0
            else:
                enemy.speed = 3.0
            
            move_speed = base_speed * player.drunk_speed_multiplier * player.slow_multiplier
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 25:
                player.x -= move_speed
            if keys[pygame.K_RIGHT] and player.x < WIDTH - 25:
                player.x += move_speed
            if keys[pygame.K_UP] and player.y > 100:
                player.y -= move_speed
            if keys[pygame.K_DOWN] and player.y < HEIGHT - 50:
                player.y += move_speed
            
            enemy.update()
            
            if player.shield_break_active and current_time < player.shield_break_end_time:
                enemy.shield_active = False
            else:
                enemy.shield_active = True
            
            projectile = enemy.shoot(player.x, player.y)
            if projectile:
                projectiles.append(projectile)
            
            for proj in projectiles[:]:
                proj.update()
                if proj.y > HEIGHT or proj.y < 0 or proj.x > WIDTH or proj.x < 0:
                    projectiles.remove(proj)
                elif proj.get_rect().colliderect(player.get_rect()):
                    if player.shield_active and current_time < player.shield_end_time:
                        player.shield_active = False
                        projectiles.remove(proj)
                    elif player.invincible and current_time < player.invincible_end_time:
                        projectiles.remove(proj)
                    else:
                        if player.heal_boost_active and current_time < player.heal_boost_end_time:
                            health -= 5
                        else:
                            health -= 10
                        projectiles.remove(proj)
                        if health <= 0:
                            running = False
            
            # Namet spawnen
            if current_time - last_namet_spawn > 20000:
                namet_list.append(Namet())
                last_namet_spawn = current_time
            
            for namet in namet_list[:]:
                if not namet.update():
                    namet_list.remove(namet)
                elif current_time - namet.lifetime > 5000:
                    namet_list.remove(namet)
                elif namet.get_rect().colliderect(player.get_rect()):
                    if player.heal_boost_active and current_time < player.heal_boost_end_time:
                        health += 40
                    else:
                        health += 20
                    if health > 50:
                        health = 50
                    namet_list.remove(namet)
                    collected_namets += 1
            
            # Jannis - Freeze
            if current_time - last_jannis_spawn > 35000:
                jannis_list.append(Jannis())
                last_jannis_spawn = current_time
            
            for jannis in jannis_list[:]:
                if not jannis.update():
                    jannis_list.remove(jannis)
                elif current_time - jannis.lifetime > 5000:
                    jannis_list.remove(jannis)
                elif jannis.get_rect().colliderect(player.get_rect()):
                    player.freeze_active = True
                    player.freeze_end_time = current_time + 10000
                    jannis_list.remove(jannis)
            
            # Leon - Drunk
            if current_time - last_leon_spawn > 30000:
                leon_list.append(Leon())
                last_leon_spawn = current_time
            
            for leon in leon_list[:]:
                if not leon.update():
                    leon_list.remove(leon)
                elif current_time - leon.lifetime > 5000:
                    leon_list.remove(leon)
                elif leon.get_rect().colliderect(player.get_rect()):
                    player.drunk_speed_multiplier = 2.5
                    player.drunk_end_time = current_time + 10000
                    leon_list.remove(leon)
            
            # Samuel - Shield
            if current_time - last_samuel_spawn > 25000:
                samuel_list.append(Samuel())
                last_samuel_spawn = current_time
            
            for samuel in samuel_list[:]:
                if not samuel.update():
                    samuel_list.remove(samuel)
                elif current_time - samuel.lifetime > 5000:
                    samuel_list.remove(samuel)
                elif samuel.get_rect().colliderect(player.get_rect()):
                    player.shield_active = True
                    player.shield_end_time = current_time + 10000
                    samuel_list.remove(samuel)
            
            # Arda - Heal-Boost
            if current_time - last_arda_spawn > 28000:
                arda_list.append(Arda())
                last_arda_spawn = current_time
            
            for arda in arda_list[:]:
                if not arda.update():
                    arda_list.remove(arda)
                elif current_time - arda.lifetime > 5000:
                    arda_list.remove(arda)
                elif arda.get_rect().colliderect(player.get_rect()):
                    player.heal_boost_active = True
                    player.heal_boost_end_time = current_time + 10000
                    arda_list.remove(arda)
            
            # Ege - Invincible
            if current_time - last_ege_spawn > 32000:
                ege_list.append(Ege())
                last_ege_spawn = current_time
            
            for ege in ege_list[:]:
                if not ege.update():
                    ege_list.remove(ege)
                elif current_time - ege.lifetime > 5000:
                    ege_list.remove(ege)
                elif ege.get_rect().colliderect(player.get_rect()):
                    player.invincible = True
                    player.invincible_end_time = current_time + 10000
                    ege_list.remove(ege)
            
            # Julian - Magnet
            if current_time - last_julian_spawn > 30000:
                julian_list.append(Julian())
                last_julian_spawn = current_time
            
            for julian in julian_list[:]:
                if not julian.update():
                    julian_list.remove(julian)
                elif current_time - julian.lifetime > 5000:
                    julian_list.remove(julian)
                elif julian.get_rect().colliderect(player.get_rect()):
                    player.magnet_active = True
                    player.magnet_end_time = current_time + 10000
                    julian_list.remove(julian)
            
            # Felix - Teleport
            if current_time - last_felix_spawn > 28000:
                felix_list.append(Felix())
                last_felix_spawn = current_time
            
            for felix in felix_list[:]:
                if not felix.update():
                    felix_list.remove(felix)
                elif current_time - felix.lifetime > 5000:
                    felix_list.remove(felix)
                elif felix.get_rect().colliderect(player.get_rect()):
                    player.teleport_active = True
                    player.teleport_end_time = current_time + 10000
                    felix_list.remove(felix)
            
            # Onur - Shield-Break
            if current_time - last_onur_spawn > 26000:
                onur_list.append(Onur())
                last_onur_spawn = current_time
            
            for onur in onur_list[:]:
                if not onur.update():
                    onur_list.remove(onur)
                elif current_time - onur.lifetime > 5000:
                    onur_list.remove(onur)
                elif onur.get_rect().colliderect(player.get_rect()):
                    player.shield_break_active = True
                    player.shield_break_end_time = current_time + 10000
                    onur_list.remove(onur)
            
            # Teleport-Effekt
            if player.teleport_active and current_time < player.teleport_end_time:
                if random.random() < 0.02:
                    player.x = random.randint(60, WIDTH - 60)
                    player.y = random.randint(100, HEIGHT - 100)
            
            # Magnet-Effekt
            if player.magnet_active and current_time < player.magnet_end_time:
                for namet in namet_list[:]:
                    dx = player.x - namet.x
                    dy = player.y - namet.y
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist > 0 and dist < 200:
                        namet.x += dx / dist * 3
                        namet.y += dy / dist * 3
            
            # Zeichnen
            if has_background:
                screen.blit(background, (0, 0))
            else:
                screen.fill(BLACK)
                for i in range(HEIGHT):
                    color_value = 20 + (i * 30 // HEIGHT)
                    pygame.draw.line(screen, (0, 0, color_value), (0, i), (WIDTH, i))
            
            player.draw()
            enemy.draw()
            
            for proj in projectiles:
                proj.draw()
            
            for namet in namet_list:
                namet.draw()
                
            for jannis in jannis_list:
                jannis.draw()
            
            for leon in leon_list:
                leon.draw()
            
            for samuel in samuel_list:
                samuel.draw()
            
            for arda in arda_list:
                arda.draw()
            
            for ege in ege_list:
                ege.draw()
            
            for julian in julian_list:
                julian.draw()
            
            for felix in felix_list:
                felix.draw()
            
            for onur in onur_list:
                onur.draw()
            
            # UI
            time_taken = time.time() - start_time
            
            max_hearts = 5
            hearts = health // 10
            
            for i in range(max_hearts):
                x_pos = 35 + i * 30
                if i < hearts:
                    color = RED
                    pygame.draw.circle(screen, color, (x_pos, 30), 10)
                    pygame.draw.circle(screen, color, (x_pos - 6, 26), 4)
                    pygame.draw.circle(screen, color, (x_pos + 6, 26), 4)
                    pygame.draw.polygon(screen, color, [(x_pos, 38), (x_pos - 8, 30), (x_pos + 8, 30)])
                else:
                    pygame.draw.circle(screen, (50, 0, 0), (x_pos, 30), 10, 1)
                    pygame.draw.circle(screen, (50, 0, 0), (x_pos - 6, 26), 3)
                    pygame.draw.circle(screen, (50, 0, 0), (x_pos + 6, 26), 3)
                pygame.draw.circle(screen, WHITE, (x_pos, 30), 10, 1)
            
            namet_text = font.render(f"⭐ Namet gesammelt: {collected_namets} | +2 Leben", True, GOLD)
            screen.blit(namet_text, (10, 60))
            
            timer_text = font.render(f"⏱️ Zeit: {time_taken:.1f}s", True, WHITE)
            screen.blit(timer_text, (WIDTH - 180, 15))
            
            if best_time:
                record_text = font.render(f"🏆 Rekord: {best_time:.1f}s", True, YELLOW)
                screen.blit(record_text, (WIDTH - 180, 55))
            
            diff_text = font.render("💀 LEHRERS FLUCH (UNENDLICH)", DARK_BLUE, True)
            screen.blit(diff_text, (WIDTH//2 - 160, 15))
            
            # Status-Anzeigen - nur Namen der Charaktere
            y_offset = 90
            
            namet_hint = small_font.render("⭐ Namet", True, GOLD)
            screen.blit(namet_hint, (10, y_offset))
            y_offset += 20
            
            jannis_hint = small_font.render("❄️ Jannis", True, (0, 150, 255))
            screen.blit(jannis_hint, (10, y_offset))
            y_offset += 20
            
            leon_hint = small_font.render("🍺 Leon", True, BROWN)
            screen.blit(leon_hint, (10, y_offset))
            y_offset += 20
            
            samuel_hint = small_font.render("🛡️ Samuel", True, SILVER)
            screen.blit(samuel_hint, (10, y_offset))
            y_offset += 20
            
            arda_hint = small_font.render("❤️ Arda", True, GREEN)
            screen.blit(arda_hint, (10, y_offset))
            y_offset += 20
            
            ege_hint = small_font.render("🇹🇷 Ege", True, TURQUOISE)
            screen.blit(ege_hint, (10, y_offset))
            y_offset += 20
            
            julian_hint = small_font.render("🧲 Julian", True, HOT_PINK)
            screen.blit(julian_hint, (10, y_offset))
            y_offset += 20
            
            felix_hint = small_font.render("🌀 Felix", True, PURPLE)
            screen.blit(felix_hint, (10, y_offset))
            y_offset += 20
            
            onur_hint = small_font.render("💥 Onur", True, NEON_GREEN)
            screen.blit(onur_hint, (10, y_offset))
            
            # Aktive Effekte
            if player.drunk_speed_multiplier > 1.0 and current_time < player.drunk_end_time:
                remaining = (player.drunk_end_time - current_time) // 1000
                drunk_text = font.render(f"🍺 BETRUNKEN! 2.5x SCHNELLER! ({remaining}s)", True, ORANGE)
                drunk_rect = drunk_text.get_rect(center=(WIDTH//2, HEIGHT - 80))
                pygame.draw.rect(screen, BLACK, drunk_rect.inflate(20, 10))
                pygame.draw.rect(screen, ORANGE, drunk_rect.inflate(20, 10), 3)
                screen.blit(drunk_text, drunk_rect)
                
                if random.random() < 0.3:
                    player.x += random.uniform(-1, 1) * 0.5
            
            if player.shield_active and current_time < player.shield_end_time:
                remaining = (player.shield_end_time - current_time) // 1000
                shield_text = font.render(f"🛡️ SCHILD AKTIV! ({remaining}s)", True, SILVER)
                shield_rect = shield_text.get_rect(center=(WIDTH//2, HEIGHT - 110))
                pygame.draw.rect(screen, BLACK, shield_rect.inflate(20, 10))
                pygame.draw.rect(screen, SILVER, shield_rect.inflate(20, 10), 3)
                screen.blit(shield_text, shield_rect)
            
            if player.invincible and current_time < player.invincible_end_time:
                remaining = (player.invincible_end_time - current_time) // 1000
                invincible_text = font.render(f"⭐ UNVERWUNDBAR! ({remaining}s)", True, GOLD)
                invincible_rect = invincible_text.get_rect(center=(WIDTH//2, HEIGHT - 140))
                pygame.draw.rect(screen, BLACK, invincible_rect.inflate(20, 10))
                pygame.draw.rect(screen, GOLD, invincible_rect.inflate(20, 10), 2)
                screen.blit(invincible_text, invincible_rect)
            
            if player.magnet_active and current_time < player.magnet_end_time:
                remaining = (player.magnet_end_time - current_time) // 1000
                magnet_text = font.render(f"🧲 MAGNET AKTIV! ({remaining}s)", True, HOT_PINK)
                magnet_rect = magnet_text.get_rect(center=(WIDTH//2, HEIGHT - 170))
                pygame.draw.rect(screen, BLACK, magnet_rect.inflate(20, 10))
                pygame.draw.rect(screen, HOT_PINK, magnet_rect.inflate(20, 10), 2)
                screen.blit(magnet_text, magnet_rect)
            
            if player.heal_boost_active and current_time < player.heal_boost_end_time:
                remaining = (player.heal_boost_end_time - current_time) // 1000
                heal_boost_text = font.render(f"❤️ HEAL-BOOST! Weniger Schaden! ({remaining}s)", True, GREEN)
                heal_boost_rect = heal_boost_text.get_rect(center=(WIDTH//2, HEIGHT - 200))
                pygame.draw.rect(screen, BLACK, heal_boost_rect.inflate(20, 10))
                pygame.draw.rect(screen, GREEN, heal_boost_rect.inflate(20, 10), 2)
                screen.blit(heal_boost_text, heal_boost_rect)
            
            if player.freeze_active and current_time < player.freeze_end_time:
                remaining = (player.freeze_end_time - current_time) // 1000
                freeze_text = font.render(f"❄️ FREEZE! Hr. Seng ist langsamer! ({remaining}s)", True, (0, 200, 255))
                freeze_rect = freeze_text.get_rect(center=(WIDTH//2, HEIGHT - 230))
                pygame.draw.rect(screen, BLACK, freeze_rect.inflate(20, 10))
                pygame.draw.rect(screen, (0, 200, 255), freeze_rect.inflate(20, 10), 2)
                screen.blit(freeze_text, freeze_rect)
            
            if player.teleport_active and current_time < player.teleport_end_time:
                remaining = (player.teleport_end_time - current_time) // 1000
                teleport_text = font.render(f"🌀 TELEPORT AKTIV! ({remaining}s)", True, PURPLE)
                teleport_rect = teleport_text.get_rect(center=(WIDTH//2, HEIGHT - 260))
                pygame.draw.rect(screen, BLACK, teleport_rect.inflate(20, 10))
                pygame.draw.rect(screen, PURPLE, teleport_rect.inflate(20, 10), 2)
                screen.blit(teleport_text, teleport_rect)
            
            if player.shield_break_active and current_time < player.shield_break_end_time:
                remaining = (player.shield_break_end_time - current_time) // 1000
                break_text = font.render(f"💥 SHIELD-BREAK! Hr. Seng schießt nicht! ({remaining}s)", True, NEON_GREEN)
                break_rect = break_text.get_rect(center=(WIDTH//2, HEIGHT - 290))
                pygame.draw.rect(screen, BLACK, break_rect.inflate(20, 10))
                pygame.draw.rect(screen, NEON_GREEN, break_rect.inflate(20, 10), 2)
                screen.blit(break_text, break_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        final_time = time.time() - start_time
        
        is_new_record = False
        if health <= 0:
            if best_time is None or final_time > best_time:
                is_new_record = True
                save_record(final_time)
        
        result = show_game_over(False, is_new_record, final_time, best_time)
        
        if result == "menu":
            continue
        elif not result:
            break

if __name__ == "__main__":
    main()
    pygame.quit()