# Mini Game Hub

A multi-user game hub built using Bash and Python (Pygame), featuring multiple games, authentication, leaderboard tracking, and statistical visualisation.

## Features
- User authentication using Bash (main.sh) with passwords hashed using SHA-256
- Multiple 2-player games (Tic-Tac-Toe, Connect-4, Othello, Battleship, Pong)
- Pygame-based graphical interface
- Persistent leaderboard using history.csv
- Sorting leaderboard by wins, losses, or win/loss ratio
- Matplotlib visualisations:
  - Top 5 players
  - Most played games

## Project Structure

 
├── main.sh  
├── game.py  
├── leaderboard.sh  
├── games/  
│   ├── tictactoe.py  
│   ├── connect4.py  
│   ├── othello.py  
│   ├── battleship.py  
│   ├── pong.py  
├── assets/  
├── history.csv  
└── users.tsv  

---

## How to Run

1. Make scripts executable:
```bash
chmod +x main.sh leaderboard.sh
```

2. Run the program:
```bash
bash main.sh
```

3. Enter usernames and passwords when prompted.

4. Select a game from the menu and play.

5. Take a look at the leaderboard and other stats.

## Requirements

- Python 3
- pygame
- numpy
- matplotlib

## System Design

* `main.sh` → Handles secure login/registration using SHA and launches the game engine
* `game.py` → Controls the basic game class, the game menu and gameplay
* `leaderboard.sh` → Processes game history and displays leaderboard
* `games/` → Contains implementations of individual games
* `users.tsv` → Stores user credentials
* `history.csv` → Stores game results (winner, loser, game, date)

## Leaderboard

- Reads data from history.csv
- Calculates wins, losses, and win/loss ratio per player
- Supports sorting by:
  - Wins
  - Losses
  - Ratio

## Statistics

After each game:
- Bar chart of top 5 players by wins
- Pie chart of most played games

Charts are generated using matplotlib and displayed in the GUI.

## Notes

- Passwords are hashed using SHA-256
- No absolute paths are used; project runs on any system
- Works on both Linux and Git Bash (Windows)

## Authors

- Samhitha Poladi (25B1088)
- Riddhima Singh (25B1068)


