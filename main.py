import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 400, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Takeoff Simulation")

# Clock for controlling frame rate
clock = pygame.time.Clock()


class Rocket:
    """Class to represent the rocket."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 70
        self.velocity = 0
        self.thrust = -0.2  # Upward acceleration
        self.gravity = 0.05  # Downward acceleration

    def move(self):
        """Update the rocket's position based on thrust and gravity."""
        self.velocity += self.thrust + self.gravity
        self.y += self.velocity

    def draw(self):
        """Draw the rocket on the screen."""
        # Rocket body
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        # Rocket nose
        pygame.draw.polygon(screen, GRAY, [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width // 2, self.y - 20)
        ])


class Particle:
    """Class to represent a single exhaust particle."""
    def __init__(self, x, y, color, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(2, 5)  # Downward motion

    def move(self):
        """Update the particle's position and decrease lifetime."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        """Draw the particle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)


class ParticleSystem:
    """Class to manage multiple particles."""
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        """Emit new particles from a given position."""
        for _ in range(5):  # Number of particles per frame
            color = random.choice([RED, ORANGE, YELLOW])  # Random flame color
            lifetime = random.randint(20, 40)
            self.particles.append(Particle(x, y, color, lifetime))

    def update(self):
        """Update all particles, removing expired ones."""
        for particle in self.particles[:]:
            particle.move()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self):
        """Draw all particles on the screen."""
        for particle in self.particles:
            particle.draw()


# Initialize Rocket and Particle System
rocket = Rocket(WIDTH // 2 - 15, HEIGHT - 100)  # Centered at the bottom
particles = ParticleSystem()

# Starry Background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen

    # Draw stars in the background
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rocket and particles
    rocket.move()
    particles.emit(rocket.x + rocket.width // 2, rocket.y + rocket.height)
    particles.update()

    # Draw rocket and particles
    rocket.draw()
    particles.draw()

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
