# main.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_logic import GameLogic
from computer_ai import ComputerAI
from gui import GameGUI
from utils import save_game_stats, load_game_stats, format_history_entry

class RockPaperScissorsGame:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = GameGUI(self.root)
        
        # Initialize game components
        self.game_logic = GameLogic()
        self.computer_ai = ComputerAI(difficulty="medium")
        
        # Game state
        self.game_mode = "single"  # "single" or "multi"
        self.scores = {"player1": 0, "player2": 0}
        self.stats = load_game_stats()
        
        # Setup callbacks
        self.gui.set_choice_callback(self.on_player_choice)
        self.gui.set_reset_callback(self.reset_game)
        self.gui.set_mode_callback(self.change_game_mode)
        self.gui.set_theme_callback(self.on_theme_change)
        
        # Initialize GUI
        self.update_player_names()
        
    def update_player_names(self):
        """Update player names based on game mode"""
        if self.game_mode == "single":
            self.gui.player_names["player2"] = "Computer"
        else:
            self.gui.player_names["player2"] = "Player 2"
    
    def on_player_choice(self, player1_choice: str):
        """Handle player's choice"""
        if self.game_mode == "single":
            self.play_single_player(player1_choice)
        else:
            self.play_multi_player(player1_choice)
    
    def play_single_player(self, player1_choice: str):
        """Play single player round"""
        # Disable buttons during animation
        self.gui.enable_choices(False)
        
        # Get computer choice
        player_last_move = None
        if self.game_logic.history:
            player_last_move = self.game_logic.history[-1].get("player1_choice")
        
        computer_choice = self.computer_ai.make_move(player_last_move)
        
        # Update choices display
        self.gui.update_choices(player1_choice, computer_choice)
        
        # Play round
        round_result = self.game_logic.play_round(player1_choice, computer_choice)
        
        # Update scores
        if round_result["winner"] == "player1":
            self.scores["player1"] += 1
        elif round_result["winner"] == "player2":
            self.scores["player2"] += 1
        
        self.gui.update_scores(self.scores["player1"], self.scores["player2"])
        
        # Update result display
        result_color = "draw" if round_result["result"] == "draw" else \
                      "win" if round_result["winner"] == "player1" else "loss"
        self.gui.update_result(round_result["message"], result_color)
        
        # Add to history
        history_entry = format_history_entry(round_result)
        self.gui.add_to_history(history_entry)
        
        # Update AI history
        self.computer_ai.update_history(player1_choice, computer_choice)
        
        # Re-enable buttons
        self.gui.enable_choices(True)
    
    def play_multi_player(self, player1_choice: str):
        """Play multiplayer round"""
        # For multiplayer, we need to get Player 2's choice
        # In this simple implementation, we'll use a dialog
        # For a better implementation, you might want to modify the GUI
        
        self.gui.update_result("Player 2's turn...", "normal")
        self.gui.update_choices(player1_choice, "❓")
        
        # Show player 2 choice dialog
        player2_choice = self.get_player2_choice()
        
        if player2_choice:
            # Play round
            round_result = self.game_logic.play_round(player1_choice, player2_choice)
            
            # Update scores
            if round_result["winner"] == "player1":
                self.scores["player1"] += 1
            elif round_result["winner"] == "player2":
                self.scores["player2"] += 1
            
            self.gui.update_scores(self.scores["player1"], self.scores["player2"])
            
            # Update result display
            result_color = "draw" if round_result["result"] == "draw" else "win"
            self.gui.update_result(round_result["message"], result_color)
            
            # Update choices display
            self.gui.update_choices(player1_choice, player2_choice)
            
            # Add to history
            history_entry = format_history_entry(round_result)
            self.gui.add_to_history(history_entry)
        else:
            self.gui.update_result("Player 2 canceled", "draw")
    
    def get_player2_choice(self):
        """Get Player 2's choice via dialog"""
        from tkinter import simpledialog
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Player 2 Choice")
        dialog.geometry("300x200")
        
        choice_var = tk.StringVar()
        
        tk.Label(dialog, text="Player 2, choose your move:", 
                font=("Arial", 12)).pack(pady=20)
        
        choices = [("Rock", "rock"), ("Paper", "paper"), ("Scissors", "scissors")]
        
        for text, value in choices:
            tk.Radiobutton(dialog, text=text, variable=choice_var, 
                          value=value, font=("Arial", 10)).pack()
        
        def submit():
            dialog.choice_result = choice_var.get()
            dialog.destroy()
        
        tk.Button(dialog, text="Submit", command=submit).pack(pady=20)
        
        dialog.choice_result = None
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return dialog.choice_result
    
    def change_game_mode(self, mode: str):
        """Change game mode"""
        self.game_mode = mode
        self.reset_game()
        self.update_player_names()
        
        if mode == "single":
            self.gui.update_result("Single Player Mode - vs Computer", "normal")
        else:
            self.gui.update_result("Multi Player Mode - 2 Players", "normal")
    
    def reset_game(self):
        """Reset the game"""
        self.scores = {"player1": 0, "player2": 0}
        self.game_logic.reset_game()
        self.computer_ai = ComputerAI(difficulty="medium")
        
        self.gui.update_scores(0, 0)
        self.gui.update_result("Game Reset - Make your move!", "normal")
        self.gui.update_choices("", "")
        self.gui.clear_history()
        
        # Save stats before reset
        self.save_current_stats()
    
    def on_theme_change(self, theme: str):
        """Handle theme change"""
        # Update any theme-specific logic here
        pass
    
    def save_current_stats(self):
        """Save current game statistics"""
        player_stats = self.game_logic.calculate_stats("player1")
        
        stats = {
            "total_games": len(self.game_logic.history),
            "wins": player_stats["wins"],
            "losses": player_stats["losses"],
            "draws": player_stats["draws"],
            "win_rate": player_stats["win_rate"],
            "last_played": self.game_logic._get_timestamp() if self.game_logic.history else "Never",
            "game_mode": self.game_mode,
            "final_scores": self.scores
        }
        
        save_game_stats(stats)
        self.stats = stats
    
    def show_statistics(self):
        """Show game statistics"""
        from utils import create_statistics_summary
        
        stats_text = create_statistics_summary(self.stats)
        messagebox.showinfo("Game Statistics", stats_text)
    
    def run(self):
        """Start the game"""
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Run main loop
        self.root.mainloop()
        
        # Save stats on exit
        self.save_current_stats()

def main():
    """Main entry point"""
    try:
        game = RockPaperScissorsGame()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        messagebox.showerror("Error", f"Failed to start game: {e}")

if __name__ == "__main__":
    main()