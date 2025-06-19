# Rock-Paper-Scissors Python Game

A simple CLI Rock-Paper-Scissors game against the computer. Results are stored in Supabase.

## Features
- Play Rock, Paper, Scissors against the computer
- Tracks wins, losses, and draws per session
- Stores each game result in Supabase

## Setup
1. Clone this repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Supabase URL and Key.
4. Create a table in Supabase called `rps_results` with columns:
   - `id` (int, primary key, auto increment)
   - `player_choice` (text)
   - `computer_choice` (text)
   - `result` (text)

## Running the Game
```
python rps.py
```

Enjoy!
