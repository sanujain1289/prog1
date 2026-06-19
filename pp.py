import pygame
import random
import math
 
pygame.init()
W, H = 300, 500
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
 
# Bee
bee_x = 60
bee_y = H // 2
bee_vy = 0
GRAVITY = 0.7
BUZZ = -7
 
# Thorns: [x, y, radius, speed_x, drift_y]
thorns = []
# Flowers: [x, y, collected]
flowers = []
 
score = 0
game_over = False
started = False
frames = 0
 
def spawn_thorn():
    r = random.randint(14, 32)
    y = random.randint(r + 40, H - r - 40)
    sx = random.uniform(2.0, 3.5)
    dy = random.uniform(-0.5, 0.5)
    thorns.append([float(W + r), float(y), r, sx, dy])
 
def spawn_flower():
    y = random.randint(50, H - 70)
    flowers.append([float(W), float(y), False])
 
def draw_bg():
    # Sky gradient
    for y in range(H - 60):
        ratio = y / (H - 60)
        r = int(135 + (100 - 135) * ratio)
        g = int(206 + (180 - 206) * ratio)
        b = int(235 + (140 - 235) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (W, y))
    # Ground
    pygame.draw.rect(screen, (90, 160, 60), (0, H - 60, W, 60))
    pygame.draw.rect(screen, (110, 180, 70), (0, H - 62, W, 4))
    # Ground flowers
    for gx in range(20, W, 55):
        pygame.draw.circle(screen, (255, 100, 100), (gx, H - 48), 5)
        pygame.draw.circle(screen, (255, 220, 80), (gx, H - 48), 3)
        pygame.draw.line(screen, (60, 130, 40), (gx, H - 43), (gx, H - 35), 2)
    for gx in range(45, W, 55):
        pygame.draw.circle(screen, (200, 130, 255), (gx, H - 42), 4)
        pygame.draw.circle(screen, (255, 220, 120), (gx, H - 42), 2)
        pygame.draw.line(screen, (60, 130, 40), (gx, H - 38), (gx, H - 32), 2)
 
def draw_bee(y):
    iy = int(y)
    # Wings (animate)
    wing_up = frames % 6 < 3
    wy = iy - 16 if wing_up else iy - 11
    pygame.draw.ellipse(screen, (220, 230, 255),
                        (bee_x - 8, wy, 18, 13))
    pygame.draw.ellipse(screen, (220, 230, 255),
                        (bee_x + 3, wy, 18, 13))
    # Body
    pygame.draw.ellipse(screen, (255, 200, 40),
                        (bee_x - 15, iy - 10, 30, 20))
    # Stripes
    for sx in range(-6, 12, 6):
        pygame.draw.line(screen, (50, 40, 10),
                         (bee_x + sx, iy - 9),
                         (bee_x + sx, iy + 9), 3)
    # Eye
    pygame.draw.circle(screen, (255, 255, 255), (bee_x + 11, iy - 3), 5)
    pygame.draw.circle(screen, (30, 30, 30), (bee_x + 12, iy - 3), 3)
    # Stinger
    pygame.draw.polygon(screen, (80, 60, 30), [
        (bee_x - 15, iy - 3),
        (bee_x - 15, iy + 3),
        (bee_x - 22, iy)])
 
def draw_thorn(x, y, r):
    ix, iy = int(x), int(y)
    # Spiky star shape
    pts = []
    n = 10
    for i in range(n * 2):
        a = math.radians(i * 180 / n - 90)
        cr = r + 7 if i % 2 == 0 else r * 0.55
        pts.append((ix + int(cr * math.cos(a)),
                     iy + int(cr * math.sin(a))))
    pygame.draw.polygon(screen, (45, 100, 35), pts)
    # Center body
    pygame.draw.circle(screen, (65, 140, 50), (ix, iy), int(r * 0.6))
    pygame.draw.circle(screen, (90, 170, 70),
                       (ix - r // 5, iy - r // 5), int(r * 0.3))
 
def draw_flower(x, y):
    ix, iy = int(x), int(y)
    for i in range(5):
        angle = i * 72
        px = ix + int(8 * math.cos(math.radians(angle)))
        py = iy + int(8 * math.sin(math.radians(angle)))
        pygame.draw.circle(screen, (255, 255, 100), (px, py), 5)
    pygame.draw.circle(screen, (255, 180, 50), (ix, iy), 5)
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                bee_y = H // 2
                bee_vy = 0
                thorns.clear()
                flowers.clear()
                score = 0
                frames = 0
                game_over = False
                started = True
            else:
                started = True
                bee_vy = BUZZ
 
    if started and not game_over:
        bee_vy += GRAVITY
        bee_y += bee_vy
        frames += 1
 
        # Score: 1 per second
        if frames % 15 == 0:
            score += 1
 
        # Spawn thorns
        rate = min(0.10, 0.04 + frames * 0.00004)
        if random.random() < rate:
            spawn_thorn()
 
        # Spawn flowers occasionally
        if random.random() < 0.008:
            spawn_flower()
 
        # Move thorns
        for t in thorns:
            t[0] -= t[3]
            t[1] += t[4]
            if t[1] - t[2] < 30 or t[1] + t[2] > H - 70:
                t[4] = -t[4]
 
        thorns[:] = [t for t in thorns if t[0] + t[2] > -10]
 
        # Move flowers
        for f in flowers:
            f[0] -= 2.5
 
        flowers[:] = [f for f in flowers if f[0] > -15 and not f[2]]
 
        # Collision: thorns
        for t in thorns:
            dx = bee_x - t[0]
            dy = bee_y - t[1]
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < t[2] + 13:
                game_over = True
 
        # Collect flowers
        for f in flowers:
            if not f[2]:
                dx = bee_x - f[0]
                dy = bee_y - f[1]
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 18:
                    f[2] = True
                    score += 3
 
        # Bounds
        if bee_y > H - 70 or bee_y < 10:
            game_over = True
 
    # Draw
    draw_bg()
 
    for f in flowers:
        if not f[2]:
            draw_flower(f[0], f[1])
 
    for t in thorns:
        draw_thorn(t[0], t[1], t[2])
 
    draw_bee(bee_y)
 
    # HUD
    font = pygame.font.Font(None, 36)
    screen.blit(font.render(str(score), True, (255, 255, 255)),
                (W // 2 - 10, 12))
 
    if game_over:
        # Solid panel
        panel = pygame.Rect(W // 2 - 100, H // 2 - 50, 200, 100)
        pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=12)
        pygame.draw.rect(screen, (80, 80, 80), panel, 2, border_radius=12)
        bf = pygame.font.Font(None, 40)
        gt = bf.render('Game Over!', True, (255, 80, 80))
        screen.blit(gt, gt.get_rect(center=(W // 2, H // 2 - 22)))
        sf = pygame.font.Font(None, 26)
        st = sf.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(st, st.get_rect(center=(W // 2, H // 2 + 8)))
        hf = pygame.font.Font(None, 20)
        ht = hf.render('Tap to restart', True, (180, 180, 180))
        screen.blit(ht, ht.get_rect(center=(W // 2, H // 2 + 32)))
    elif not started:
        panel = pygame.Rect(W // 2 - 80, H // 2 - 25, 160, 50)
        pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=12)
        pygame.draw.rect(screen, (80, 80, 80), panel, 2, border_radius=12)
        hf = pygame.font.Font(None, 28)
        ht = hf.render('Tap to buzz!', True, (255, 255, 255))
        screen.blit(ht, ht.get_rect(center=(W // 2, H // 2)))
 
    pygame.display.flip()
    clock.tick(15)
 
pygame.quit()