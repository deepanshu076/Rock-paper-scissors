# config.py
import tkinter as tk
from typing import Dict, Tuple, List

# Color Schemes
COLORS = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#333333",
        "button_bg": "#e0e0e0",
        "button_fg": "#333333",
        "highlight": "#4a90e2",
        "win": "#4CAF50",
        "loss": "#F44336",
        "draw": "#FF9800",
        "text": "#000000"
    },
    "dark": {
        "bg": "#2c3e50",
        "fg": "#ecf0f1",
        "button_bg": "#34495e",
        "button_fg": "#ecf0f1",
        "highlight": "#3498db",
        "win": "#27ae60",
        "loss": "#e74c3c",
        "draw": "#f39c12",
        "text": "#ffffff"
    }
}

# Game Constants
GAME_CHOICES = ["rock", "paper", "scissors"]
CHOICE_EMOJIS = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
CHOICE_BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

# Difficulty Levels
DIFFICULTY = {
    "easy": {"name": "Easy", "description": "Random moves"},
    "medium": {"name": "Medium", "description": "Basic pattern detection"},
    "hard": {"name": "Hard", "description": "Adaptive strategy"}
}

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Rock Paper Scissors Game"

# Player Settings
DEFAULT_PLAYERS = {
    "player1": {"name": "Player 1", "score": 0, "wins": 0, "losses": 0, "draws": 0},
    "player2": {"name": "Player 2", "score": 0, "wins": 0, "losses": 0, "draws": 0},
    "computer": {"name": "Computer", "score": 0, "wins": 0, "losses": 0, "draws": 0}
}