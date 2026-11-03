<p align="center">
  <img width="800" height="320" alt="endlessrunner-demo" src="https://github.com/user-attachments/assets/80cd7be4-880c-443c-b884-a604c9a130fd" />
</p>

<div align="center">
  <h1>EndlessRunner</h1>
</div>

<p align="center">
  <strong>A little running. A lot of dodging. An endless chase for the high score.</strong>
</p>

<p align="center">
  A 2D endless runner built with Python and Pygame, inspired by the classic Chrome Dinosaur Game.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-2D%20Game-00A86B?style=flat-square" alt="Pygame">
  <img src="https://img.shields.io/badge/Status-Playable-brightgreen?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License">
</p>

---

## Overview

EndlessRunner is a 2D arcade-style running game where players control a character navigating through an endless environment filled with obstacles, collectible stars, and interactive mini-games.

Jump over obstacles, slide under flying enemies, collect stars, complete mini-games, and push your score as high as possible. The game gradually increases in speed, making every run progressively more challenging than the last.

---

## Game Screenshots

<p align="center">
  <img width="1001" height="403" alt="Image" src="https://github.com/user-attachments/assets/48f48677-40aa-40ab-90f8-0b63376f13f2" />
</p>

<p align="center">
  <img width="1001" height="404" alt="Image" src="https://github.com/user-attachments/assets/5fbfa899-79af-44fa-91c6-0709b9259ff7" />
</p>

---

## Key Features

- **Endless Gameplay** – Continuously generated obstacles with dynamic speed scaling.
- **Player Animations** – Fluid animated running, jumping, and ducking mechanics.
- **Dynamic Obstacles** – Avoid ground obstacles like books and airborne birds with unique trajectories.
- **Star Collection System** – Collect stars during your run for extra bonus points.
- **Interactive Mini-Games** – Triggered every 300 points for extra reward opportunities.
- **Local Leaderboard** – Tracks top 5 scores across playthroughs via local storage.
- **Interactive Game Menu** – Clean navigation for Start Game, Leaderboard, and Quit options.
- **Visual FX** – Animated backgrounds, dynamic clouds, star particles, and score notifications.

---

## Controls

| Action | Primary Key | Alternative Key |
| :--- | :--- | :--- |
| **Jump** | `SPACE` | `UP ARROW` |
| **Slide / Duck** | `DOWN ARROW` | — |
| **Pause / Return to Menu** | `ESC` | — |
| **Navigate Menu** | `UP ARROW` | `DOWN ARROW` |
| **Select Option** | `ENTER` | `SPACE` |
| **Continue Mini-Game** | `SPACE` / `ENTER` | Mouse Click |

---

## Architecture & Workflow Chart

<div align="center">

```mermaid
flowchart TD
    %% Node Definitions %%
    START([Launch Endless_runner.py])
    INIT[Initialize Pygame Window & Load SVGs]
    LOAD_DATA[(Load Local High Score)]
    MENU_STATE[Display Interactive Main Menu]
    CHOICE{Player Action}
    SHOW_LB[Render Top 5 Scores]
    EXIT([Exit Application])
    GAME_LOOP[Enter Main Gameplay Loop]

    INPUT[Process Keyboard Inputs]
    MOVE[Update Player Jump & Slide State]
    SPAWN[Spawn Dynamic Obstacles & Stars]
    SCROLL[Scroll Background & Increase Speed]
    COLLISION{Collision Check}

    GAMEOVER[Game Over Screen]
    STAR_SCORE[Add +10 Star Score]
    SCORE_CHECK{Score Check}

    MINI_GAME[Trigger Random Mini-Game]
    MG_TYPE{Mini-Game Type}
    TTT[Tic-Tac-Toe Challenge]
    CARD[Memory Card Matching]
    MG_RESULT[Evaluate Outcome]
    MG_BONUS[Award Bonus Points: Win +50 / Draw +10]

    CHECK_HS{New High Score?}
    SAVE_HS[(Save Score to File)]
    RESTART{Player Choice}

    %% Launch Sequence %%
    START --> INIT
    INIT --> LOAD_DATA
    LOAD_DATA --> MENU_STATE

    %% Main Menu Choice %%
    MENU_STATE --> CHOICE
    CHOICE -->|Leaderboard| SHOW_LB
    CHOICE -->|Quit| EXIT
    CHOICE -->|Start Game| GAME_LOOP

    %% Active Game Loop %%
    subgraph Engine [" Core Game Loop (Pygame) "]
        GAME_LOOP --> INPUT
        INPUT --> MOVE
        MOVE --> SPAWN
        SPAWN --> SCROLL
        SCROLL --> COLLISION
    end

    %% Gameplay Outcomes %%
    COLLISION -->|Obstacle Hit| GAMEOVER
    COLLISION -->|Star Pickup| STAR_SCORE
    COLLISION -->|No Hit| SCORE_CHECK

    %% Mini-Game Milestone Trigger %%
    SCORE_CHECK -->|300 Point Milestone| MINI_GAME
    SCORE_CHECK -->|Regular Loop| GAME_LOOP

    %% Mini-Game Sub-System %%
    subgraph MiniGames [" Interactive Mini-Game Engine "]
        MINI_GAME --> MG_TYPE
        MG_TYPE --> TTT
        MG_TYPE --> CARD
        TTT --> MG_RESULT
        CARD --> MG_RESULT
        MG_RESULT --> MG_BONUS
    end

    MG_BONUS --> GAME_LOOP

    %% Game Over & Score Persistence %%
    GAMEOVER --> CHECK_HS
    CHECK_HS -->|Yes| SAVE_HS
    CHECK_HS -->|No| RESTART
    SAVE_HS --> RESTART
    RESTART -->|Play Again| GAME_LOOP
    RESTART -->|Main Menu| MENU_STATE

    %% Styling Palette %%
    classDef startEnd fill:#FF6B6B,stroke:#C0392B,stroke-width:2px,color:#FFF;
    classDef initLoop fill:#4ECDC4,stroke:#16A085,stroke-width:2px,color:#FFF;
    classDef coreEngine fill:#3498DB,stroke:#2980B9,stroke-width:2px,color:#FFF;
    classDef decision fill:#F1C40F,stroke:#D68910,stroke-width:2px,color:#000;
    classDef minigame fill:#9B59B6,stroke:#8E44AD,stroke-width:2px,color:#FFF;
    classDef storage fill:#2ECC71,stroke:#27AE60,stroke-width:2px,color:#FFF;

    class START,EXIT,GAMEOVER startEnd;
    class INIT,MENU_STATE,SHOW_LB initLoop;
    class GAME_LOOP,INPUT,MOVE,SPAWN,SCROLL,STAR_SCORE coreEngine;
    class CHOICE,COLLISION,SCORE_CHECK,MG_TYPE,CHECK_HS,RESTART decision;
    class MINI_GAME,TTT,CARD,MG_RESULT,MG_BONUS minigame;
    class LOAD_DATA,SAVE_HS storage;
```

</div>

## Mini-Game Mechanics

Mini-games trigger automatically every 300 points during a active run.

| Match Outcome | Score Bonus |
| :--- | :--- |
| **Win** | +50 Points |
| **Draw** | +10 Points |
| **Lose** | +0 Points |
| **Skip** | +0 Points |

---

## Tech Stack

| Component | Technology / Library | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.13 | Core game logic and state management |
| **Engine** | Pygame | Graphics rendering, window frame, collision, and inputs |
| **Graphics** | SVG Assets | Scalable vector graphics rendered dynamically |
| **Storage** | File I/O (`txt`) | Persistent local high score storage |

---

## Game Assets & Resources

Below is a breakdown of vector assets used inside the game graphics engine:

| Category | Asset File | Purpose |
| :--- | :--- | :--- |
| **Sprites** | `run1.svg`, `run2.svg`, `dino_duck.svg` | Player movement and state animations |
| **Enemies** | `bird1.svg`, `bird2.svg`, `book.svg` | Flying and ground obstacle entities |
| **Environment** | `background.svg`, `ground.svg`, `cloud.svg` | Dynamic scrolling background layers |
| **Collectibles** | `star.svg`, `star_small.svg`, `spark_gold.svg`, `spark_green.svg` | Score pickups and visual particle effects |
| **UI Components** | `banner.svg`, `menu_logo.svg`, `button.svg`, `button_hover.svg` | Menu headers, titles, and button states |
| **Panels** | `leaderboard_panel.svg`, `gameover_panel.svg`, `mini_panel.svg`, `dim.svg` | Modal popups, overlays, and game screens |
| **Mini-Game** | `ttt_board.svg`, `ttt_x.svg`, `ttt_o.svg`, `ttt_hover.svg`, `ttt_win.svg` | Tic-Tac-Toe mini-game visual assets |
| **Cards & Icons** | `card_back.svg`, `card_face.svg`, `card_hover.svg`, `card_matched.svg`, `icon_*.svg` | Memory card mini-game and status icons |

<div align="center">

### Environment & World

<img width="3520" height="400" alt="Image" src="https://github.com/user-attachments/assets/29050f58-4434-4b7f-86ef-000909b934fe" /><br>
<sub><b>background.svg</b></sub>

### Player Animations

| Running (Frame 1) | Running (Frame 2) | Ducking / Sliding |
| :---: | :---: | :---: |
| <img src="assets/run1.svg" width="90" alt="Run 1"> | <img src="assets/run2.svg" width="90" alt="Run 2"> | <img src="assets/dino_duck.svg" width="120" alt="Duck"> |
| `run1.svg` | `run2.svg` | `dino_duck.svg` |

### Obstacles & Collectibles

| Ground Obstacle | Flying Enemy (Frame 1) | Flying Enemy (Frame 2) | Pickup Star | Small Star |
| :---: | :---: | :---: | :---: | :---: |
| <img src="assets/book.svg" width="60" alt="Book"> | <img src="assets/bird1.svg" width="60" alt="Bird 1"> | <img src="assets/bird2.svg" width="60" alt="Bird 2"> | <img src="assets/star.svg" width="50" alt="Star"> | <img src="assets/star_small.svg" width="40" alt="Star Small"> |
| `book.svg` | `bird1.svg` | `bird2.svg` | `star.svg` | `star_small.svg` |

</div>

---

## Getting Started

### Prerequisites

Ensure you have Python 3 and `pip` installed on your system.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iabhnv19/EndlessRunner.git
   ```

2. **Navigate to project folder**
   ```bash
   cd EndlessRunner
   ```

3. **Install dependencies**
   ```bash
   pip install pygame
   ```

4. **Launch the game**
   ```bash
   python Endless_runner.py
   ```

---

## Project Structure

```text
EndlessRunner/
│
├── assets/
│   ├── background.svg
│   ├── banner.svg
│   ├── bird1.svg / bird2.svg
│   ├── book.svg
│   ├── run1.svg / run2.svg / dino_duck.svg
│   ├── star.svg / spark_*.svg
│   ├── ttt_*.svg
│   └── ... (all SVG game graphics)
│
├── Endless_runner.py
├── dinorunner_highscore.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Limitations

- The game is a local single-player application and does not feature online multiplayer or remote leaderboards.
- High scores are saved in a local plain-text file (`dinorunner_highscore.txt`) without encryption or database backend.
- Frame rate and rendering speed are dependent on the host machine's hardware capabilities.
- Pygame must be installed locally to execute the application script directly.
- The application is designed for academic learning and demonstration, not commercial production use.

---

## Troubleshooting

<details>
<summary><b><code>python</code> or <code>pip</code> is not recognized</b></summary>

<br>

Python is either not installed or its installation folder is not available in your system's PATH.

- Download and install Python 3.x from [python.org](https://www.python.org/).
- Ensure **"Add Python to PATH"** is checked during installation.
- Open a new terminal and verify installation:

```bash
python --version
```

</details>

<details>
<summary><b>ModuleNotFoundError: No module named 'pygame'</b></summary>

<br>

Pygame package is missing in your active Python environment. Install it using `pip`:

```bash
pip install pygame
```

If using Python 3 explicitly on Linux or macOS:

```bash
pip3 install pygame
```

</details>

<details>
<summary><b>Asset loading errors / Missing file paths</b></summary>

<br>

Ensure you are launching the script from the root `EndlessRunner` repository directory where the `assets/` folder is located.

```bash
cd EndlessRunner
python Endless_runner.py
```

</details>

<details>
<summary><b>Game runs too fast or stutters</b></summary>

<br>

Check that your display driver is updated and no external frame rate limiters are locking Pygame window refresh rates.

</details>

---

## Future Improvements

- Add sound effects and dynamic background music.
- Introduce customizable character skins and unlockable visual themes.
- Implement online leaderboards powered by a cloud backend database.
- Add gamepad / controller support alongside keyboard inputs.
- Create cross-platform executable bundles (`.exe` / `.app`) for easier distribution.
- Add additional obstacle types and boss stage events.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

<br>

## Developer

Developed By 
<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/iabhnv19">
        <img src="https://github.com/iabhnv19.png" width="80" height="80" alt="Abhinav's GitHub profile picture" />
        <br />
        <strong>Abhinav</strong>
        <br />
        @iabhnv19
      </a>
    </td>
  </tr>
</table>
</div>
<div align="center">
Made with ❤️ by [Abhinav](https://github.com/iabhnv19)<br>
 If this Project seems cool, consider starring the repo!
</div>
</div>
