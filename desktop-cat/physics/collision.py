from core.config import GRAVITY, MAX_FALL_SPEED


class Physics:
    """Gravitation + Kollision mit dem Bildschirmboden.

    Fenster-Erkennung ist deaktiviert, damit die Katze zuverlässig
    sichtbar auf dem unteren Bildschirmrand läuft.
    """

    def __init__(self, provider):
        self.provider = provider

    def apply_gravity(self, body, dt):
        body.velocity.y += GRAVITY * dt
        if body.velocity.y > MAX_FALL_SPEED:
            body.velocity.y = MAX_FALL_SPEED

    def integrate(self, body, dt):
        body.position.x += body.velocity.x * dt
        body.position.y += body.velocity.y * dt

    def has_ground_below(self, body) -> bool:
        """Prüft, ob direkt unter der Katze der Bildschirmboden ist."""
        feet_y = body.position.y + body.height
        return feet_y + 4 >= self.provider.screen_height()

    def ground_y(self, body):
        """Der Boden ist immer der untere Bildschirmrand."""
        return self.provider.screen_height()

    def resolve_ground(self, body):
        """Wenn die Katze unter den Boden fällt, korrigiere Position."""
        ground = self.ground_y(body)
        feet_y = body.position.y + body.height
        if feet_y >= ground:
            body.position.y = ground - body.height
            body.velocity.y = 0.0
            return True
        return False