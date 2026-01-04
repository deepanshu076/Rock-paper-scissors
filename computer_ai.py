# computer_ai.py
import random
from typing import List, Optional, Dict
from config import GAME_CHOICES, CHOICE_BEATS

class ComputerAI:
    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.player_history = []
        self.computer_history = []
        
    def make_move(self, player_last_move: Optional[str] = None) -> str:
        """Make a move based on difficulty level"""
        if self.difficulty == "easy":
            return self._easy_move()
        elif self.difficulty == "medium":
            return self._medium_move(player_last_move)
        elif self.difficulty == "hard":
            return self._hard_move(player_last_move)
        else:
            return self._easy_move()
    
    def _easy_move(self) -> str:
        """Random move"""
        return random.choice(GAME_CHOICES)
    
    def _medium_move(self, player_last_move: Optional[str]) -> str:
        """Basic pattern recognition"""
        if not player_last_move or random.random() < 0.3:
            return self._easy_move()
        
        # Sometimes counter the player's last move
        if random.random() < 0.6:
            return CHOICE_BEATS[player_last_move]
        else:
            return self._easy_move()
    
    def _hard_move(self, player_last_move: Optional[str]) -> str:
        """Adaptive strategy with pattern detection"""
        if len(self.player_history) < 3:
            return self._medium_move(player_last_move)
        
        # Analyze player patterns
        player_pattern = self._detect_pattern()
        
        if player_pattern and random.random() < 0.7:
            # Counter the predicted pattern
            predicted_move = self._predict_next_move()
            if predicted_move:
                return CHOICE_BEATS[predicted_move]
        
        return self._medium_move(player_last_move)
    
    def _detect_pattern(self) -> Optional[str]:
        """Detect simple patterns in player moves"""
        if len(self.player_history) < 3:
            return None
        
        # Check for repeating pattern
        last_three = self.player_history[-3:]
        if len(set(last_three)) == 1:
            return "repeating"
        
        # Check for rotational pattern
        if self._is_rotational_pattern():
            return "rotational"
        
        return None
    
    def _predict_next_move(self) -> Optional[str]:
        """Predict player's next move"""
        if not self.player_history:
            return None
        
        # Simple frequency-based prediction
        freq = {choice: 0 for choice in GAME_CHOICES}
        for move in self.player_history[-5:]:
            if move in freq:
                freq[move] += 1
        
        return max(freq, key=freq.get)
    
    def _is_rotational_pattern(self) -> bool:
        """Check if player is using rotational pattern"""
        if len(self.player_history) < 4:
            return False
        
        # Check for rock->paper->scissors or reverse pattern
        pattern_indices = [GAME_CHOICES.index(move) for move in self.player_history[-4:]]
        
        # Check if indices are consecutive (with wrap-around)
        for i in range(len(pattern_indices) - 1):
            expected_next = (pattern_indices[i] + 1) % 3
            if pattern_indices[i + 1] != expected_next:
                return False
        
        return True
    
    def update_history(self, player_move: str, computer_move: str):
        """Update move history"""
        self.player_history.append(player_move)
        self.computer_history.append(computer_move)
    
    def set_difficulty(self, difficulty: str):
        """Change AI difficulty"""
        self.difficulty = difficulty