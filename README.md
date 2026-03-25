# SSL Project 2026 - Mini Game Hub
Samhitha Poladi (25B1088) and Riddhima Singh (25B1068)

Mini Game Hub is a multi-user game platform that combines Bash scripting and Python (Pygame) to create an interactive gaming experience.
The system begins with user authentication in Bash, after which two players can select and play different board games through a graphical interface.
Game results are stored and used to generate a leaderboard and basic analytics.

**Features**

* User authentication with password handling using Bash scripts
* Multiple two-player board games (Tic-Tac-Toe, Connect Four, Othello, Battleship)
* Graphical interface using Pygame
* Use of NumPy for board representation and efficient win checking
* Storage of users and match history
* Leaderboard generation showing wins, losses, and win/loss ratio
* Basic data visualisation using MatPlotLib (e.g., top players, most played games)
* Modular code structure using classes and separate files

**How to Run**

```bash id="r0x5m9"
bash main.sh
```

**Project Structure**

* `main.sh` → Handles login/registration and launches the game engine
* `game.py` → Controls game menu and gameplay
* `leaderboard.sh` → Processes game history and displays leaderboard
* `games/` → Contains implementations of individual games
* `users.tsv` → Stores user credentials
* `history.csv` → Stores game results (winner, loser, date, game)

**Technologies Used**

* Bash (authentication and leaderboard processing)
* Python (core logic and structure)
* Pygame (GUI and rendering)
* NumPy (board operations)
* Matplotlib (data visualisation)




## Weekly Contribution Plan (6 Weeks)

### Week 1

* Samhitha:

  * Set up project structure and repository
  * Begin implementing authentication in `main.sh`
    
* Riddhima:

  * Set up Python environment and dependencies
  * Create base game class and initialize Pygame window

### Week 2

* Samhitha:

  * Complete authentication system (login, registration, user storage in `users.tsv`)
    
* Riddhima:

  * Implement board representation using NumPy
  * Set up reusable rendering framework in Pygame

### Week 3

* Samhitha:

  * Implement Tic-Tac-Toe logic (including win conditions)
    
* Riddhima:

  * Implement Tic-Tac-Toe GUI and interactions

### Week 4

* Samhitha:

  * Implement Connect Four logic (gravity, win checking)
    
* Riddhima:

  * Implement Connect Four GUI and improve visuals

### Week 5

* Samhitha:

  * Implement Othello logic (valid moves, disc flipping, turn handling)
    
* Riddhima:

  * Implement Battleship logic (grid setup, ship placement, hit/miss detection)
  * Integrate all games into a unified menu system

### Week 6

* Samhitha:

  * Implement result recording (winner, loser, date, game)
  * Assist in testing and debugging
    
* Riddhima:

  * Implement leaderboard display using `leaderboard.sh`
  * Add basic visualisations using Matplotlib
  * Final cleanup, documentation, and integration
