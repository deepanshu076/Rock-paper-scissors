# utils.py
import json
import os
from datetime import datetime
from typing import Dict, Any

def save_game_stats(stats: Dict, filename: str = "game_stats.json"):
    """Save game statistics to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving stats: {e}")
        return False

def load_game_stats(filename: str = "game_stats.json") -> Dict:
    """Load game statistics from file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading stats: {e}")
    return {}

def format_history_entry(round_data: Dict) -> str:
    """Format round data for history display"""
    emoji_map = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    
    player1_emoji = emoji_map.get(round_data.get("player1_choice", ""), "❓")
    player2_emoji = emoji_map.get(round_data.get("player2_choice", ""), "❓")
    
    result_text = ""
    if round_data.get("result") == "draw":
        result_text = "Draw"
    elif round_data.get("winner") == "player1":
        result_text = "Player 1 wins"
    else:
        result_text = "Player 2 wins"
    
    return f"Round {round_data.get('round', 0)}: {player1_emoji} vs {player2_emoji} - {result_text}"

def validate_choice(choice: str) -> bool:
    """Validate if choice is valid"""
    valid_choices = ["rock", "paper", "scissors"]
    return choice.lower() in valid_choices

def calculate_win_rate(wins: int, total_games: int) -> float:
    """Calculate win rate percentage"""
    if total_games == 0:
        return 0.0
    return (wins / total_games) * 100

def get_current_time() -> str:
    """Get current time formatted"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_statistics_summary(stats: Dict) -> str:
    """Create a formatted statistics summary"""
    summary = []
    summary.append("=== GAME STATISTICS ===")
    summary.append(f"Total Games: {stats.get('total_games', 0)}")
    summary.append(f"Wins: {stats.get('wins', 0)}")
    summary.append(f"Losses: {stats.get('losses', 0)}")
    summary.append(f"Draws: {stats.get('draws', 0)}")
    summary.append(f"Win Rate: {stats.get('win_rate', 0):.2f}%")
    summary.append(f"Last Played: {stats.get('last_played', 'Never')}")
    return "\n".join(summary)