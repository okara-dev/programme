import random
import sys
import os
import pygame

# Spieleinstellungen
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20  

# Prüfen, ob Fenstergrößen durch Zellgröße teilbar sind
assert WINDOW_WIDTH % CELL_SIZE == 0, "Fensterbreite muss durch Zellgröße teilbar sein."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Fensterhöhe muss durch Zellgröße teilbar sein."

# Farben 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CROCODILE_GREEN = (0, 150, 0)
STRAWBERRY_RED = (220, 30, 30)
STRAWBERRY_LEAF = (34, 139, 34)

# Datei für Highscore
HIGHSCORE_FILE = "highscore.txt"

# Hilfsfunktionen für Highscore

def load_highscore():
    """Lädt den Highscore aus der Datei. Falls keine Datei existiert, wird 0 zurückgegeben."""
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return int(f.read())
        except:
            return 0

def save_highscore(score):
    """Speichert den Highscore in die Datei."""
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Zeichenfunktionen

def draw_grid(surface):
    """Zeichnet das Raster auf dem Spielfeld."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

def draw_strawberry(surface, pos):
    """Zeichnet eine einfache Erdbeere auf einem Zell-Koordinatenpunkt."""
    x, y = pos
    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
    radius = CELL_SIZE // 2 - 2

    # Körper der Erdbeere
    pygame.draw.circle(surface, STRAWBERRY_RED, center, radius)

    # Blatt der Erdbeere (einfaches Dreieck)
    leaf_points = [
        (x + CELL_SIZE // 2, y + 4),
        (x + 4, y + 10),
        (x + CELL_SIZE - 4, y + 10),
    ]
    pygame.draw.polygon(surface, STRAWBERRY_LEAF, leaf_points)

def get_random_location():
    """Gibt eine zufällige Zellposition zurück."""
    x = random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE
    y = random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE
    return x, y

# Hauptspiel-Runde

def play_round(screen, clock, font, highscore):
    """
    Spielrunde starten.
    - screen: Pygame-Fenster
    - clock: Pygame-Uhr für FPS
    - font: Schriftart
    - highscore: aktueller Highscore
    Rückgabe: (True/False ob Neustart, Highscore)
    """

    # Krokodil initialisieren (3 Segmente)
    croc = [(CELL_SIZE * 5, CELL_SIZE * 5),
            (CELL_SIZE * 4, CELL_SIZE * 5),
            (CELL_SIZE * 3, CELL_SIZE * 5)]
    direction = (CELL_SIZE, 0)  # Startet nach rechts

    strawberry = get_random_location()
    score = 0
    running = True

    while running:
        # -------------------------------
        # Ereignisverarbeitung (Tastatur, Quit)
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, highscore
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, highscore
                elif event.key == pygame.K_r:
                    return True, highscore
                elif event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        # Krokodil bewegen
        new_head = (croc[0][0] + direction[0], croc[0][1] + direction[1])

        # Bildschirm-Rand Wrap-around
        new_head = (
            new_head[0] % WINDOW_WIDTH,
            new_head[1] % WINDOW_HEIGHT,
        )

        # Kollision mit sich selbst prüfen
        if new_head in croc:
            running = False

        croc.insert(0, new_head)

        # Erdbeere fressen
        if new_head == strawberry:
            score += 1
            # neue Erdbeere auf zufälliger Position, nicht auf Krokodil
            while strawberry in croc:
                strawberry = get_random_location()
        else:
            croc.pop()  # Schwanz bewegen

        # Bildschirm zeichnen
        screen.fill(BLACK)
        draw_grid(screen)

        # Krokodil zeichnen
        for segment in croc:
            pygame.draw.rect(screen, CROCODILE_GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Erdbeere zeichnen
        draw_strawberry(screen, strawberry)

        # Score anzeigen
        score_surf = font.render(f"Punkte: {score}", True, WHITE)
        highscore_surf = font.render(f"Rekord: {highscore}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        screen.blit(highscore_surf, (10, 40))

        pygame.display.flip()
        clock.tick(10)  # Geschwindigkeit: 10 FPS

    # Highscore aktualisieren
    if score > highscore:
        highscore = score
        save_highscore(highscore)

    # Game Over Bildschirm
    game_over_surf = font.render("Game Over", True, WHITE)
    score_surf = font.render(f"Punkte: {score}", True, WHITE)
    highscore_surf = font.render(f"Rekord: {highscore}", True, WHITE)
    hint_surf = font.render("R = Neustart | Esc = Beenden", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_surf, (WINDOW_WIDTH // 2 - game_over_surf.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
    screen.blit(score_surf, (WINDOW_WIDTH // 2 - score_surf.get_width() // 2, WINDOW_HEIGHT // 2 - 10))
    screen.blit(highscore_surf, (WINDOW_WIDTH // 2 - highscore_surf.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
    screen.blit(hint_surf, (WINDOW_WIDTH // 2 - hint_surf.get_width() // 2, WINDOW_HEIGHT // 2 + 60))
    pygame.display.flip()

    # Warten auf Benutzeraktion
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, highscore
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, highscore
                if event.key == pygame.K_ESCAPE:
                    return False, highscore
        clock.tick(10)

# Hauptfunktion
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Crocodile")

    font = pygame.font.SysFont(None, 36)

    # Highscore laden
    highscore = load_highscore()

    while True:
        running, highscore = play_round(screen, clock, font, highscore)
        if not running:
            break

    pygame.quit()
    sys.exit(0)

# Start des Spiels
# -------------------------------
if __name__ == "__main__":
    main()