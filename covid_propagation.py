import pygame
import sys
import random
import math
import numpy as np

# --------------------------
# Pygame Setup
# --------------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COVID-19 Propagation Simulation (SEIR Model)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# --------------------------
# Simulation Parameters
# --------------------------
N = 1000                        # Number of individuals
infection_radius = 15          # Distance (pixels) for transmission
# Transmission probabilities:
p_transmission_uncontrolled = 0.3  # Before control measures (e.g., day 20)
p_transmission_controlled = 0.1    # After control measures start
control_time = 200.0                # Time (days) when control measures start

dt = 0.1                       # Time step (days)
# Movement parameters
max_speed = 4.0                # Maximum speed (pixels per day)

# Incubation period parameters (in days)
incubation_mean = 60
incubation_std = 20
# Infectious period parameters (in days)
infectious_mean = 80.0
infectious_std = 15

# --------------------------
# Colors for States
# --------------------------
COLOR_S = (0, 0, 255)   # Susceptible: blue
COLOR_E = (255, 165, 0) # Exposed: orange
COLOR_I = (255, 0, 0)   # Infected: red
COLOR_R = (0, 255, 0)   # Recovered: green

# --------------------------
# Person Class (SEIR Model)
# --------------------------
class Person:
    def __init__(self):
        # Place each person at a random position on the screen.
        self.pos = np.array([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)])
        # Assign a random velocity (direction and speed up to max_speed).
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(0, max_speed)
        self.vel = np.array([speed * math.cos(angle), speed * math.sin(angle)])
        # Initial state: Susceptible ("S")
        self.state = "S"
        # Timer for state transitions:
        self.timer = 0.0  # Used for E and I states.
        self.size = 6     # Drawn as circles.
        # New vaccination attributes:
        self.vaccinated = False   # Default: not vaccinated
        self.dose = 0             # 0 = unvaccinated, 1 = first dose, 2 = second dose
    
    def update(self, dt):
        # Random movement: update position based on velocity.
        self.pos += self.vel * dt
        
        # Apply wrap-around boundaries.
        if self.pos[0] < 0:
            self.pos[0] += WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] -= WIDTH
        if self.pos[1] < 0:
            self.pos[1] += HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] -= HEIGHT
        
        # Update state timers and transition between states.
        if self.state == "E":
            self.timer += dt
            # Once incubation period is over, become infectious.
            if self.timer >= max(0, random.gauss(incubation_mean, incubation_std)):
                self.state = "I"
                self.timer = 0.0
        elif self.state == "I":
            self.timer += dt
            # After infectious period, recover.
            if self.timer >= max(0, random.gauss(infectious_mean, infectious_std)):
                self.state = "R"
    
    def draw(self, surface):
        # If vaccinated, override the state color with purple.
        if self.vaccinated:
            draw_color = (128, 0, 128)  # Purple
        else:
            if self.state == "S":
                draw_color = COLOR_S
            elif self.state == "E":
                draw_color = COLOR_E
            elif self.state == "I":
                draw_color = COLOR_I
            else:
                draw_color = COLOR_R

        # Draw the individual.
        pygame.draw.circle(surface, draw_color, (int(self.pos[0]), int(self.pos[1])), self.size)

        # Optionally, if the individual is infectious, draw a red outline for infection perimeter.
        if self.state == "I":
            pygame.draw.circle(surface, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), infection_radius, 1)

# --------------------------
# Create Population
# --------------------------
population = [Person() for _ in range(N)]
# Infect one random individual at t=0 (set as Exposed, so incubation begins).
initial_patient = random.choice(population)
initial_patient.state = "E"
initial_patient.timer = 0.0

# Assign vaccination status to each person.
for person in population:
    if random.random() < 0.3:  # 30% chance to be vaccinated
        person.vaccinated = True
        # Among vaccinated, 80% receive two doses:
        person.dose = 2 if random.random() < 0.8 else 1

# --------------------------
# Main Simulation Loop
# --------------------------
current_time = 0.0  # in days
running = True
while running:
    clock.tick(60)  # Limit to 60 FPS.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    current_time += dt
    # Determine current transmission probability based on control measures.
    if current_time < control_time:
        p_transmission = p_transmission_uncontrolled
    else:
        p_transmission = p_transmission_controlled
    
    # Update each person.
    for person in population:
        person.update(dt)
    
    # Check for transmissions.
    # For each infectious person, infect susceptible individuals within infection_radius.
    for i in range(N):
        if population[i].state != "I":
            continue
        for j in range(N):
            if population[j].state != "S":
                continue
            # Compute distance (e.g., Euclidean distance)
            dx = abs(population[i].pos[0] - population[j].pos[0])
            dy = abs(population[i].pos[1] - population[j].pos[1])
            distance = math.hypot(dx, dy)
            if distance < infection_radius:
                # Determine effective transmission probability:
                if population[j].vaccinated:
                    if population[j].dose == 1:
                        effective_prob = 0.005  # 0.5% chance for one dose
                    elif population[j].dose == 2:
                        effective_prob = 0.002  # 0.2% chance for two doses
                    else:
                        effective_prob = p_transmission  # fallback
                else:
                    effective_prob = p_transmission
                if random.random() < effective_prob:
                    population[j].state = "E"
                    population[j].timer = 0.0
    
    # Drawing.
    screen.fill((0, 0, 0))
    for person in population:
        person.draw(screen)
    
    # Display simulation time and counts.
    count_S = sum(1 for p in population if p.state == "S")
    count_E = sum(1 for p in population if p.state == "E")
    count_I = sum(1 for p in population if p.state == "I")
    count_R = sum(1 for p in population if p.state == "R")
    info_text = f"Time: {current_time:.1f} d    S: {count_S}   E: {count_E}   I: {count_I}   R: {count_R}"
    info_label = font.render(info_text, True, (255,255,255))
    screen.blit(info_label, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()