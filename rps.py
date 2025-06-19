import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def store_result(player_choice, computer_choice, result):
    if not supabase:
        print("[Warning] Supabase not configured. Skipping result storage.")
        return
    data = {
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "result": result
    }
    try:
        supabase.table("rps_results").insert(data).execute()
    except Exception as e:
        print(f"[Error] Failed to store result in Supabase: {e}")

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(player, computer):
    if player == computer:
        return "draw"
    elif (
        (player == "rock" and computer == "scissors") or
        (player == "scissors" and computer == "paper") or
        (player == "paper" and computer == "rock")
    ):
        return "win"
    else:
        return "lose"

def main():
    print("Welcome to Rock-Paper-Scissors!")
    score = {"win": 0, "lose": 0, "draw": 0}
    options = ["rock", "paper", "scissors"]
    while True:
        print("\nChoose one (rock/paper/scissors) or 'quit' to exit:")
        player_choice = input().strip().lower()
        if player_choice == 'quit':
            break
        if player_choice not in options:
            print("Invalid choice. Try again.")
            continue
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        result = determine_winner(player_choice, computer_choice)
        print(f"You {result}!")
        score[result] += 1
        store_result(player_choice, computer_choice, result)
        print(f"Score: Wins={score['win']} Losses={score['lose']} Draws={score['draw']}")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
