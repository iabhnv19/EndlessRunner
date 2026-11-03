import math
import os
import random
import sys
import pygame
pygame.init()

WIDTH, HEIGHT = 1000, 400
GROUND_Y = 320
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
START_SPEED = 8
MAX_SPEED = 18
BG_SPEED = 0.3

MINI_GAME_EVERY = 300                      # a mini game every 300 points
MINI_GAME_REWARDS = {"win": 50, "draw": 10, "lose": 0, "skip": 0}   # bonus points
STAR_POINTS = 10                           # points for each star
MAX_SCORES = 5                             # leaderboard length

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_PATH = os.path.join(BASE_DIR, "dinorunner_highscore.txt")   # one score per line

BG = (247, 247, 247)
TEXT = (83, 83, 83)
DARK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (200, 50, 40)
BLUE = (40, 90, 200)
GREEN = (40, 140, 60)
GOLD = (196, 140, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22, bold=True)
small_font = pygame.font.SysFont("consolas", 18, bold=True)
big_font = pygame.font.SysFont("consolas", 40, bold=True)
ASSET_DIR = os.path.join(BASE_DIR, "assets")

def load(name):
    return pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()

dino_run = [load("run1.svg"), load("run2.svg")]
dino_duck = load("dino_duck.svg")
book_img = load("book.svg")
bird_imgs = [load("bird1.svg"), load("bird2.svg")]
cloud_img = load("cloud.svg")
ground_img = load("ground.svg")
background_img = load("background.svg")
star_img = load("star.svg")
star_small_img = load("star_small.svg")
spark_imgs = {"gold": load("spark_gold.svg"), "green": load("spark_green.svg")}
menu_logo_img = load("menu_logo.svg")
button_img = load("button.svg")
button_hover_img = load("button_hover.svg")
leaderboard_panel_img = load("leaderboard_panel.svg")
gameover_panel_img = load("gameover_panel.svg")
banner_img = load("banner.svg")
mini_panel_img = load("mini_panel.svg")
dim_img = load("dim.svg")
ttt_board_img = load("ttt_board.svg")
ttt_x_img = load("ttt_x.svg")
ttt_o_img = load("ttt_o.svg")
ttt_hover_img = load("ttt_hover.svg")
ttt_win_img = load("ttt_win.svg")
input_box_img = load("input_box.svg")
heart_full_img = load("heart_full.svg")
heart_empty_img = load("heart_empty.svg")
card_back_img = load("card_back.svg")
card_face_img = load("card_face.svg")
card_matched_img = load("card_matched.svg")
card_hover_img = load("card_hover.svg")
card_icons = [load(n) for n in ("icon_heart.svg", "icon_star.svg", "icon_laptop.svg","icon_book.svg", "icon_mug.svg", "icon_bulb.svg")]

def quit_game():
    pygame.quit()
    sys.exit()

def draw_text(text, fnt, color, pos, align="center"):
    """Draw text. align is a pygame Rect attribute: center, midleft, topleft..."""
    img = fnt.render(text, True, color)
    rect = img.get_rect()
    setattr(rect, align, pos)
    screen.blit(img, rect)

def draw_scenery(bg_x, ground_x, clouds=()):
    """Background, clouds and ground (menu, leaderboard and the game)."""
    screen.fill(BG)
    bw = background_img.get_width()
    screen.blit(background_img, (-bg_x, 0))
    screen.blit(background_img, (bw - bg_x, 0))
    for c in clouds:
        c.draw()
    gw = ground_img.get_width()
    screen.blit(ground_img, (-ground_x, GROUND_Y))
    screen.blit(ground_img, (gw - ground_x, GROUND_Y))

def load_scores():
    scores = []
    try:
        with open(SCORE_PATH) as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    scores.append(int(line))
    except OSError:
        pass
    return sorted(scores, reverse=True)[:MAX_SCORES]

def add_score(score):
    if score <= 0:
        return
    scores = sorted(load_scores() + [score], reverse=True)[:MAX_SCORES]
    try:
        with open(SCORE_PATH, "w") as f:
            f.write("\n".join(str(s) for s in scores))
    except OSError:
        pass

def best_score():
    scores = load_scores()
    return scores[0] if scores else 0

particles = []

def spawn_burst(x, y, kind="gold", n=16):
    for _ in range(n):
        angle = random.uniform(0, math.tau)
        spd = random.uniform(2, 7)
        particles.append([x, y, math.cos(angle) * spd, math.sin(angle) * spd,
                          random.randint(25, 50), spark_imgs[kind]])


def draw_particles():
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.18
        p[4] -= 1
        if p[4] <= 0:
            particles.remove(p)
            continue
        p[5].set_alpha(min(255, p[4] * 8))
        screen.blit(p[5], (p[0], p[1]))
        p[5].set_alpha(255)

class Banner:
    def __init__(self, text, frames=90):
        self.text = text
        self.timer = self.frames = frames

    def draw(self):
        self.timer -= 1
        alpha = int(255 * min(1.0, self.timer / 20))
        img = banner_img.copy()
        txt = font.render(self.text, True, DARK)
        img.blit(txt, txt.get_rect(center=(img.get_width() // 2, img.get_height() // 2 - 2)))
        img.set_alpha(alpha)
        screen.blit(img, img.get_rect(center=(WIDTH // 2, 80)))

    def done(self):
        return self.timer <= 0

class Dino:
    def __init__(self):
        self.x = 80
        self.y = GROUND_Y - dino_run[0].get_height()
        self.vel_y = 0
        self.on_ground = True
        self.ducking = False
        self.frame = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False

    def update(self, keys):
        self.ducking = keys[pygame.K_DOWN] and self.on_ground

        self.vel_y += GRAVITY
        self.y += self.vel_y

        height = (dino_duck if self.ducking else dino_run[0]).get_height()
        if self.y + height >= GROUND_Y:
            self.y = GROUND_Y - height
            self.vel_y = 0
            self.on_ground = True

        self.frame += 1

    def image(self):
        if self.ducking:
            return dino_duck
        if not self.on_ground:
            return dino_run[0]
        return dino_run[(self.frame // 6) % 2]

    def rect(self):
        img = self.image()
        return pygame.Rect(self.x, self.y, img.get_width(), img.get_height())

    def hitbox(self):
        return self.rect().inflate(-10, -8)

    def draw(self):
        screen.blit(self.image(), (self.x, self.y))


class Obstacle:
    def __init__(self, speed):
        self.kind = "bird" if (random.random() < 0.3 and speed > 9) else "book"
        self.frame = 0
        if self.kind == "book":
            w, h = book_img.get_size()
            self.rect = pygame.Rect(WIDTH + 20, GROUND_Y - h, w, h)
        else:
            w, h = bird_imgs[0].get_size()
            bottom = GROUND_Y - random.choice([35, 13])   # 35 = slide under, 13 = jump over
            self.rect = pygame.Rect(WIDTH + 20, bottom - h, w, h)

    def update(self, speed):
        self.rect.x -= speed
        self.frame += 1

    def hitbox(self):
        return self.rect.inflate(-8, -8)

    def draw(self):
        if self.kind == "book":
            screen.blit(book_img, self.rect)
        else:
            screen.blit(bird_imgs[(self.frame // 10) % 2], self.rect)

class Star:
    def __init__(self):
        self.x = float(WIDTH + 20)
        self.base_y = GROUND_Y - random.randint(110, 190)
        self.bob = random.uniform(0, math.tau)
        self.alive = True

    def update(self, speed):
        self.x -= speed
        self.bob += 0.1
        if self.x < -60:
            self.alive = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.base_y + math.sin(self.bob) * 6), 48, 48)

    def draw(self):
        screen.blit(star_img, self.rect().topleft)

class Cloud:
    def __init__(self, x=None):
        self.x = x if x is not None else WIDTH + random.randint(0, 300)
        self.y = random.randint(30, 150)

    def update(self, speed):
        self.x -= speed * 0.3
        if self.x < -cloud_img.get_width():
            self.x = WIDTH + random.randint(0, 200)
            self.y = random.randint(30, 150)

    def draw(self):
        screen.blit(cloud_img, (self.x, self.y))

def main_menu():
    """Returns 0 (start game), 1 (leaderboard) or 2 (quit)."""
    labels = ["START GAME", "LEADERBOARD", "QUIT"]
    rects = [button_img.get_rect(center=(WIDTH // 2, 150 + i * 62)) for i in range(3)]
    selected = 0
    bg_x = ground_x = 0
    frame = 0
    runner_x = float(WIDTH + 60)           

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return selected
            if event.type == pygame.MOUSEMOTION:
                for i, r in enumerate(rects):
                    if r.collidepoint(event.pos):
                        selected = i
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, r in enumerate(rects):
                    if r.collidepoint(event.pos):
                        return i

        bg_x = (bg_x + 6 * BG_SPEED) % background_img.get_width()
        ground_x = (ground_x + 6) % ground_img.get_width()
        frame += 1
        if runner_x > 90:
            runner_x -= 4
        draw_scenery(bg_x, ground_x)

        runner = dino_run[(frame // 8) % 2]
        screen.blit(runner, (int(runner_x), GROUND_Y - runner.get_height()))

        screen.blit(menu_logo_img, menu_logo_img.get_rect(center=(WIDTH // 2, 62)))

        for i, r in enumerate(rects):
            screen.blit(button_hover_img if i == selected else button_img, r)
            draw_text(labels[i], font, DARK, (r.centerx, r.centery - 2))

        draw_text(f"BEST: {best_score():05d}", small_font, DARK, (WIDTH // 2, 345))
        draw_text("SPACE jump   DOWN slide   grab the stars!", small_font, TEXT, (WIDTH // 2, 374))

        pygame.display.flip()

def leaderboard_screen():
    panel_rect = leaderboard_panel_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bg_x = ground_x = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

        bg_x = (bg_x + 6 * BG_SPEED) % background_img.get_width()
        ground_x = (ground_x + 6) % ground_img.get_width()
        draw_scenery(bg_x, ground_x)

        screen.blit(leaderboard_panel_img, panel_rect)
        draw_text("LEADERBOARD", font, DARK, (panel_rect.centerx, panel_rect.top + 28))

        scores = load_scores()
        if not scores:
            draw_text("NO SCORES YET", font, TEXT, (panel_rect.centerx, panel_rect.centery - 5))
            draw_text("GO FOR A RUN!", small_font, TEXT, (panel_rect.centerx, panel_rect.centery + 28))
        for i, s in enumerate(scores):
            y = panel_rect.top + 95 + i * 46
            color = GOLD if i == 0 else TEXT
            draw_text(f"{i + 1}.", font, color, (panel_rect.left + 120, y), "midleft")
            draw_text(f"{s:05d}", font, color, (panel_rect.right - 120, y), "midright")

        draw_text("ESC / click to go back", small_font, TEXT, (panel_rect.centerx, panel_rect.bottom - 24))
        pygame.display.flip()

PANEL_POS = ((WIDTH - 620) // 2, 10)
PANEL_CX = WIDTH // 2
SIDE_CX = PANEL_POS[0] + 620 - 150          
WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
BOARD_X, BOARD_Y, CELL = PANEL_POS[0] + 25, 70, 100

def check_winner(board):
    """Returns ('X' / 'O' / 'draw' / None, winning cells)."""
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    if all(board):
        return "draw", ()
    return None, ()

def computer_move(board):
    empty = [i for i in range(9) if not board[i]]
    if random.random() < 0.35:                
        return random.choice(empty)
    for mark in ("O", "X"):                   
        for i in empty:
            board[i] = mark
            winner, _ = check_winner(board)
            board[i] = ""
            if winner == mark:
                return i
    if 4 in empty:
        return 4
    return random.choice(empty)

class TicTacToe:
    title = "TIC TAC TOE"
    bonus_pos = (SIDE_CX, 262)
    footer_pos = (SIDE_CX, 330)

    def __init__(self):
        self.board = [""] * 9
        self.turn = "X"
        self.result = None
        self.win_cells = ()
        self.ai_timer = 0

    def cell_at(self, pos):
        x, y = pos[0] - BOARD_X, pos[1] - BOARD_Y
        if 0 <= x < 3 * CELL and 0 <= y < 3 * CELL:
            return (y // CELL) * 3 + x // CELL
        return None

    def cell_pos(self, i):
        return BOARD_X + (i % 3) * CELL, BOARD_Y + (i // 3) * CELL

    def finish(self):
        winner, self.win_cells = check_winner(self.board)
        if winner:
            self.result = {"X": "win", "O": "lose", "draw": "draw"}[winner]

    def handle_event(self, event):
        picked = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            picked = self.cell_at(event.pos)
        if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_9:
            picked = event.key - pygame.K_1
        if picked is not None and self.turn == "X" and not self.board[picked]:
            self.board[picked] = "X"
            self.turn = "O"
            self.ai_timer = 30
            self.finish()

    def update(self):
        if self.result is None and self.turn == "O":
            self.ai_timer -= 1
            if self.ai_timer <= 0:
                self.board[computer_move(self.board)] = "O"
                self.turn = "X"
                self.finish()

    def draw(self):
        screen.blit(ttt_board_img, (BOARD_X, BOARD_Y))
        for i in self.win_cells:
            screen.blit(ttt_win_img, self.cell_pos(i))
        if self.result is None and self.turn == "X":
            hover = self.cell_at(pygame.mouse.get_pos())
            if hover is not None and not self.board[hover]:
                screen.blit(ttt_hover_img, self.cell_pos(hover))
        for i, mark in enumerate(self.board):
            if mark:
                x, y = self.cell_pos(i)
                screen.blit(ttt_x_img if mark == "X" else ttt_o_img, (x + 10, y + 10))

        draw_text("YOU = X", font, RED, (SIDE_CX, 118))
        draw_text("CPU = O", font, BLUE, (SIDE_CX, 150))
        if self.result is None:
            draw_text("YOUR TURN" if self.turn == "X" else "CPU THINKING...", font, DARK, (SIDE_CX, 215))
            draw_text("click a square or 1-9", small_font, TEXT, (SIDE_CX, 255))
        else:
            draw_result(self.result, (SIDE_CX, 215))

class GuessNumber:
    title = "GUESS THE NUMBER"
    bonus_pos = (PANEL_CX, 312)
    footer_pos = (PANEL_CX, 360)
    MAX_TRIES = 6

    def __init__(self):
        self.secret = random.randint(1, 100)
        self.tries = self.MAX_TRIES
        self.typed = ""
        self.history = []                
        self.feedback = "TYPE YOUR FIRST GUESS"
        self.result = None
        self.frame = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.typed = self.typed[:-1]
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.typed:
            self.check()
        else:
            ch = getattr(event, "unicode", "")
            if ch.isdigit() and len(self.typed) < 3:
                self.typed += ch

    def check(self):
        guess = int(self.typed)
        self.typed = ""
        self.tries -= 1
        if guess == self.secret:
            self.feedback = f"CORRECT! IT WAS {self.secret}"
            self.result = "win"
            return
        self.history.append(f"{guess} {'LOW' if guess < self.secret else 'HIGH'}")
        if self.tries <= 0:
            self.feedback = f"OUT OF TRIES! IT WAS {self.secret}"
            self.result = "lose"
        else:
            self.feedback = ("TOO LOW" if guess < self.secret else "TOO HIGH") + f" - {self.tries} LEFT"

    def update(self):
        self.frame += 1

    def draw(self):
        draw_text("I'M THINKING OF A NUMBER FROM 1 TO 100", small_font, TEXT, (PANEL_CX, 82))

        for i in range(self.MAX_TRIES):             # hearts = tries left
            img = heart_full_img if i < self.tries else heart_empty_img
            screen.blit(img, (PANEL_CX - 92 + i * 32, 100))

        box = input_box_img.get_rect(center=(PANEL_CX, 175))
        screen.blit(input_box_img, box)
        cursor = "|" if (self.frame // 25) % 2 == 0 and self.result is None else ""
        draw_text(self.typed + cursor, big_font, DARK, (box.centerx, box.centery - 2))

        color = GREEN if self.result == "win" else RED if self.result == "lose" else DARK
        draw_text(self.feedback, font, color, (PANEL_CX, 238))
        if self.history:
            draw_text("   ".join(self.history[-4:]), small_font, TEXT, (PANEL_CX, 275))
        if self.result is None:
            draw_text("type a number + ENTER", small_font, TEXT, (PANEL_CX, 315))

CARD = 72
CARD_GAP = 8
GRID_X, GRID_Y = PANEL_POS[0] + 30, 80

class MemoryMatch:
    title = "MEMORY MATCH"
    bonus_pos = (SIDE_CX, 262)
    footer_pos = (PANEL_CX, 360)

    def __init__(self):
        self.icons = list(range(len(card_icons))) * 2
        random.shuffle(self.icons)
        self.revealed = [False] * 12
        self.matched = [False] * 12
        self.picked = []
        self.lock = 0
        self.moves = 0
        self.result = None

    def card_rect(self, i):
        return pygame.Rect(GRID_X + (i % 4) * (CARD + CARD_GAP),
                           GRID_Y + (i // 4) * (CARD + CARD_GAP), CARD, CARD)

    def handle_event(self, event):
        if self.lock > 0 or event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        for i in range(12):
            if self.card_rect(i).collidepoint(event.pos) and not self.revealed[i] and not self.matched[i]:
                self.revealed[i] = True
                self.picked.append(i)
                if len(self.picked) == 2:
                    self.moves += 1
                    a, b = self.picked
                    if self.icons[a] == self.icons[b]:
                        self.matched[a] = self.matched[b] = True
                        self.picked = []
                        spawn_burst(*self.card_rect(a).center, "green", 8)
                        spawn_burst(*self.card_rect(b).center, "green", 8)
                        if all(self.matched):
                            self.result = "win"
                    else:
                        self.lock = 45
                break

    def update(self):
        if self.lock > 0:
            self.lock -= 1
            if self.lock == 0:
                for i in self.picked:
                    self.revealed[i] = False
                self.picked = []

    def draw(self):
        mouse = pygame.mouse.get_pos()
        for i in range(12):
            r = self.card_rect(i)
            if self.matched[i]:
                screen.blit(card_matched_img, r)
            elif self.revealed[i]:
                screen.blit(card_face_img, r)
            else:
                screen.blit(card_back_img, r)
                if self.result is None and self.lock == 0 and r.collidepoint(mouse):
                    screen.blit(card_hover_img, card_hover_img.get_rect(center=r.center))
            if self.matched[i] or self.revealed[i]:
                icon = card_icons[self.icons[i]]
                screen.blit(icon, icon.get_rect(center=r.center))

        draw_text(f"MOVES: {self.moves}", font, DARK, (SIDE_CX, 118))
        draw_text(f"PAIRS: {sum(self.matched) // 2} / 6", font, DARK, (SIDE_CX, 150))
        if self.result is None:
            draw_text("find the matching pairs", small_font, TEXT, (SIDE_CX, 215))
        else:
            draw_result(self.result, (SIDE_CX, 215))


MINI_GAMES = [TicTacToe, GuessNumber, MemoryMatch]      

def draw_result(result, pos):
    title = {"win": "YOU WIN!", "lose": "YOU LOSE", "draw": "DRAW"}[result]
    color = {"win": GREEN, "lose": RED, "draw": TEXT}[result]
    draw_text(title, big_font, color, pos)

def play_mini_game(game, backdrop):
    """Runs one mini game on top of a frozen screenshot. Returns win / lose / draw / skip."""
    ended_at = None
    pygame.event.clear()

    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "skip"
            if game.result:
                press = (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)) or \
                        (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
                if press and ended_at is not None and now - ended_at > 500:
                    return game.result
            else:
                game.handle_event(event)

        game.update()
        if game.result and ended_at is None:
            ended_at = now
            if game.result == "win":
                spawn_burst(WIDTH // 2, 200, "gold", 30)

        screen.blit(backdrop, (0, 0))
        screen.blit(dim_img, (0, 0))
        screen.blit(mini_panel_img, PANEL_POS)
        draw_text(f"MINI GAME: {game.title}", font, WHITE, (WIDTH // 2, PANEL_POS[1] + 28))
        game.draw()

        if game.result:
            bonus = MINI_GAME_REWARDS[game.result]
            draw_text(f"BONUS +{bonus}" if bonus else "NO BONUS", font, DARK, game.bonus_pos)
            draw_text("click / SPACE to go on", small_font, TEXT, game.footer_pos)
        else:
            draw_text(f"WIN +{MINI_GAME_REWARDS['win']}   ESC = skip", small_font, TEXT, game.footer_pos)

        draw_particles()
        pygame.display.flip()

def run_round():
    """Plays until game over. Returns 'restart' or 'menu'."""
    dino = Dino()
    obstacles, stars = [], []
    clouds = [Cloud(random.randint(0, WIDTH)) for _ in range(3)]
    score = 0.0
    speed = START_SPEED
    ground_x = bg_x = 0
    spawn_timer = 60
    star_timer = random.randint(200, 400)
    stars_collected = 0
    next_mini = MINI_GAME_EVERY
    mini_count = 0
    best = best_score()
    new_best = False
    banner = None
    game_over = False
    particles.clear()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game_over:
                        return "restart"
                    dino.jump()

        if not game_over:
            dino.update(pygame.key.get_pressed())
            score += 0.1
            speed = min(MAX_SPEED, START_SPEED + score / 100)
            ground_x = (ground_x + speed) % ground_img.get_width()
            bg_x = (bg_x + speed * BG_SPEED) % background_img.get_width()

            spawn_timer -= 1
            if spawn_timer <= 0:
                obstacles.append(Obstacle(speed))
                spawn_timer = random.randint(55, 110)

            for ob in obstacles:
                ob.update(speed)
                if ob.hitbox().colliderect(dino.hitbox()):
                    game_over = True
                    add_score(int(score))
                    if int(score) > best:
                        best, new_best = int(score), True
                        spawn_burst(dino.x + 24, dino.y + 30, "gold", 30)
            obstacles = [o for o in obstacles if o.rect.right > 0]
            star_timer -= 1
            if star_timer <= 0:
                stars.append(Star())
                star_timer = random.randint(180, 420)
            for st in stars:
                st.update(speed)
                if st.alive and st.rect().colliderect(dino.hitbox()):
                    st.alive = False
                    stars_collected += 1
                    score += STAR_POINTS
                    spawn_burst(*st.rect().center, "gold", 14)
                    banner = Banner(f"STAR!  +{STAR_POINTS}", 45)
            stars = [s for s in stars if s.alive]

            for c in clouds:
                c.update(speed)
            if not game_over and int(score) >= next_mini:
                game = MINI_GAMES[mini_count % len(MINI_GAMES)]()
                result = play_mini_game(game, screen.copy())
                bonus = MINI_GAME_REWARDS[result]
                score += bonus
                mini_count += 1
                next_mini += MINI_GAME_EVERY
                obstacles, stars = [], []     
                spawn_timer = 90
                banner = Banner(f"{game.title}: {result.upper()}" + (f"  +{bonus}" if bonus else ""), 120)
                pygame.event.clear()

        draw_scenery(bg_x, ground_x, clouds)
        dino.draw()
        for ob in obstacles:
            ob.draw()
        for st in stars:
            st.draw()

        hud = font.render(f"HI {best:05d}  {int(score):05d}", True, TEXT)
        screen.blit(hud, (WIDTH - hud.get_width() - 20, 15))
        screen.blit(star_small_img, (16, 12))
        draw_text(f"x {stars_collected}", font, DARK, (46, 24), "midleft")
        draw_text(f"MINI GAME AT {next_mini}", small_font, TEXT, (16, 52), "midleft")

        if banner:
            banner.draw()
            if banner.done():
                banner = None

        if game_over:
            panel = gameover_panel_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(dim_img, (0, 0))
            screen.blit(gameover_panel_img, panel)
            draw_text("GAME OVER", font, WHITE, (panel.centerx, panel.top + 28))
            draw_text(f"SCORE {int(score):05d}     STARS {stars_collected}", font, DARK, (panel.centerx, panel.top + 90))
            draw_text("NEW BEST SCORE!" if new_best else f"BEST {best:05d}", font,
                      GOLD if new_best else TEXT, (panel.centerx, panel.top + 125))
            draw_text("SPACE = restart     ESC = menu", small_font, TEXT, (panel.centerx, panel.top + 170))

        draw_particles()
        pygame.display.flip()

def main():
    while True:
        choice = main_menu()
        if choice == 0:
            while run_round() == "restart":
                pass
        elif choice == 1:
            leaderboard_screen()
        else:
            quit_game()

if __name__ == "__main__":
    main()