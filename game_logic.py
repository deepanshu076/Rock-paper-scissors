# game_logic.py
import random
from typing import Dict, Tuple, Optional
from config import GAME_CHOICES, CHOICE_BEATS

class GameLogic:
    def __init__(self):
        self.history = []
        self.round_number = 0
        
    def determine_winner(self, choice1: str, choice2: str) -> Dict:
        """Determine the winner between two choices"""
        if choice1 == choice2:
            return {"result": "draw", "winner": None, "message": "It's a draw!"}
        
        if CHOICE_BEATS[choice1] == choice2:
            return {"result": "win", "winner": "player1", "message": f"{choice1.capitalize()} beats {choice2}!"}
        else:
            return {"result": "win", "winner": "player2", "message": f"{choice2.capitalize()} beats {choice1}!"}
    
    def play_round(self, player1_choice: str, player2_choice: str) -> Dict:
        """Play a single round and return results"""
        self.round_number += 1
        result = self.determine_winner(player1_choice, player2_choice)
        
        round_data = {
            "round": self.round_number,
            "player1_choice": player1_choice,
            "player2_choice": player2_choice,
            "result": result["result"],
            "winner": result["winner"],
            "message": result["message"],
            "timestamp": self._get_timestamp()
        }
        
        self.history.append(round_data)
        return round_data
    
    def calculate_stats(self, player_name: str = "player1") -> Dict:
        """Calculate statistics for a player"""
        if not self.history:
            return {"wins": 0, "losses": 0, "draws": 0, "win_rate": 0}
        
        wins = sum(1 for r in self.history if r["winner"] == player_name)
        draws = sum(1 for r in self.history if r["result"] == "draw")
        losses = len(self.history) - wins - draws
        
        win_rate = (wins / len(self.history)) * 100 if self.history else 0
        
        return {
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": round(win_rate, 2)
        }
    
    def reset_game(self):
        """Reset game state"""
        self.history = []
        self.round_number = 0
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def get_choice_emoji(self, choice: str) -> str:
        """Get emoji for choice"""
        from config import CHOICE_EMOJIS
        return CHOICE_EMOJIS.get(choice, "❓")