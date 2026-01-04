# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Dict, Tuple, Callable, Optional
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, CHOICE_EMOJIS

class GameGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Theme
        self.theme = "light"
        self.colors = COLORS[self.theme]
        
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.score_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14)
        self.normal_font = font.Font(family="Helvetica", size=12)
        
        # Callbacks
        self.choice_callback = None
        self.reset_callback = None
        self.theme_callback = None
        self.mode_callback = None
        
        # Game state
        self.game_mode = "single"
        self.scores = {"player1": 0, "player2": 0}
        self.player_names = {"player1": "Player 1", "player2": "Computer"}
        
        # Setup UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize all UI components"""
        self.root.configure(bg=self.colors["bg"])
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="ROCK PAPER SCISSORS",
            font=self.title_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=(0, 20))
        
        # Score Display Frame
        score_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        score_frame.pack(fill="x", pady=(0, 20))
        
        # Player 1 Score
        self.player1_score_var = tk.StringVar(value="0")
        player1_frame = tk.Frame(score_frame, bg=self.colors["bg"])
        player1_frame.pack(side="left", expand=True)
        
        player1_name = tk.Label(
            player1_frame,
            text=self.player_names["player1"],
            font=self.normal_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        player1_name.pack()
        
        self.player1_score_label = tk.Label(
            player1_frame,
            textvariable=self.player1_score_var,
            font=self.score_font,
            bg=self.colors["bg"],
            fg=self.colors["highlight"]
        )
        self.player1_score_label.pack()
        
        # VS Label
        vs_label = tk.Label(
            score_frame,
            text="VS",
            font=self.score_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        vs_label.pack(side="left", expand=True, padx=20)
        
        # Player 2 Score
        self.player2_score_var = tk.StringVar(value="0")
        player2_frame = tk.Frame(score_frame, bg=self.colors["bg"])
        player2_frame.pack(side="left", expand=True)
        
        player2_name = tk.Label(
            player2_frame,
            text=self.player_names["player2"],
            font=self.normal_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        player2_name.pack()
        
        self.player2_score_label = tk.Label(
            player2_frame,
            textvariable=self.player2_score_var,
            font=self.score_font,
            bg=self.colors["bg"],
            fg=self.colors["highlight"]
        )
        self.player2_score_label.pack()
        
        # Choice Buttons Frame
        choice_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        choice_frame.pack(pady=20)
        
        # Choice buttons
        self.choice_buttons = {}
        choices = ["rock", "paper", "scissors"]
        
        for i, choice in enumerate(choices):
            btn = tk.Button(
                choice_frame,
                text=f"{CHOICE_EMOJIS[choice]}\n{choice.capitalize()}",
                font=self.button_font,
                bg=self.colors["button_bg"],
                fg=self.colors["button_fg"],
                relief="raised",
                width=10,
                height=3,
                command=lambda c=choice: self._on_choice_click(c)
            )
            btn.grid(row=0, column=i, padx=10, pady=5)
            self.choice_buttons[choice] = btn
        
        # Result Display
        self.result_var = tk.StringVar(value="Make your move!")
        self.result_label = tk.Label(
            main_frame,
            textvariable=self.result_var,
            font=self.button_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            height=2
        )
        self.result_label.pack(pady=10)
        
        # Choices Display
        choices_display_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        choices_display_frame.pack(pady=10)
        
        self.player1_choice_var = tk.StringVar(value="❓")
        self.player2_choice_var = tk.StringVar(value="❓")
        
        player1_choice_label = tk.Label(
            choices_display_frame,
            textvariable=self.player1_choice_var,
            font=font.Font(size=48),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        player1_choice_label.pack(side="left", padx=20)
        
        vs_small_label = tk.Label(
            choices_display_frame,
            text="VS",
            font=self.score_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        vs_small_label.pack(side="left", padx=20)
        
        player2_choice_label = tk.Label(
            choices_display_frame,
            textvariable=self.player2_choice_var,
            font=font.Font(size=48),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        player2_choice_label.pack(side="left", padx=20)
        
        # Game History
        history_frame = tk.LabelFrame(
            main_frame,
            text="Game History",
            font=self.normal_font,
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        history_frame.pack(fill="both", expand=True, pady=10)
        
        # History text widget
        self.history_text = tk.Text(
            history_frame,
            height=8,
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["text"],
            state="disabled"
        )
        history_scrollbar = tk.Scrollbar(history_frame, orient="vertical")
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_text.yview)
        
        self.history_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        history_scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        # Control Buttons Frame
        control_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        control_frame.pack(pady=10)
        
        # Game Mode Buttons
        mode_frame = tk.Frame(control_frame, bg=self.colors["bg"])
        mode_frame.pack(pady=5)
        
        single_player_btn = tk.Button(
            mode_frame,
            text="Single Player",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=self._on_single_player
        )
        single_player_btn.pack(side="left", padx=5)
        
        multi_player_btn = tk.Button(
            mode_frame,
            text="Multi Player",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=self._on_multi_player
        )
        multi_player_btn.pack(side="left", padx=5)
        
        # Action Buttons
        action_frame = tk.Frame(control_frame, bg=self.colors["bg"])
        action_frame.pack(pady=5)
        
        reset_btn = tk.Button(
            action_frame,
            text="Reset Game",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=self._on_reset
        )
        reset_btn.pack(side="left", padx=5)
        
        settings_btn = tk.Button(
            action_frame,
            text="Settings",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=self._on_settings
        )
        settings_btn.pack(side="left", padx=5)
        
        exit_btn = tk.Button(
            action_frame,
            text="Exit",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg="#ff4444",
            command=self.root.quit
        )
        exit_btn.pack(side="left", padx=5)
    
    def _on_choice_click(self, choice: str):
        """Handle choice button click"""
        if self.choice_callback:
            self.choice_callback(choice)
    
    def _on_reset(self):
        """Handle reset button click"""
        if self.reset_callback:
            self.reset_callback()
    
    def _on_single_player(self):
        """Switch to single player mode"""
        self.game_mode = "single"
        self.player_names["player2"] = "Computer"
        if self.mode_callback:
            self.mode_callback("single")
    
    def _on_multi_player(self):
        """Switch to multiplayer mode"""
        self.game_mode = "multi"
        self.player_names["player2"] = "Player 2"
        if self.mode_callback:
            self.mode_callback("multi")
    
    def _on_settings(self):
        """Open settings dialog"""
        self._show_settings_dialog()
    
    def update_scores(self, player1_score: int, player2_score: int):
        """Update score display"""
        self.scores["player1"] = player1_score
        self.scores["player2"] = player2_score
        self.player1_score_var.set(str(player1_score))
        self.player2_score_var.set(str(player2_score))
    
    def update_result(self, result_text: str, result_type: str = "normal"):
        """Update result display with color coding"""
        self.result_var.set(result_text)
        
        if result_type == "win":
            self.result_label.config(fg=self.colors["win"])
        elif result_type == "loss":
            self.result_label.config(fg=self.colors["loss"])
        elif result_type == "draw":
            self.result_label.config(fg=self.colors["draw"])
        else:
            self.result_label.config(fg=self.colors["fg"])
    
    def update_choices(self, player1_choice: str, player2_choice: str):
        """Update choice displays"""
        from config import CHOICE_EMOJIS
        self.player1_choice_var.set(CHOICE_EMOJIS.get(player1_choice, "❓"))
        self.player2_choice_var.set(CHOICE_EMOJIS.get(player2_choice, "❓"))
    
    def add_to_history(self, history_entry: str):
        """Add entry to game history"""
        self.history_text.config(state="normal")
        self.history_text.insert("end", history_entry + "\n")
        self.history_text.see("end")
        self.history_text.config(state="disabled")
    
    def clear_history(self):
        """Clear game history"""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        self.history_text.config(state="disabled")
    
    def set_choice_callback(self, callback: Callable):
        """Set callback for choice selection"""
        self.choice_callback = callback
    
    def set_reset_callback(self, callback: Callable):
        """Set callback for reset"""
        self.reset_callback = callback
    
    def set_mode_callback(self, callback: Callable):
        """Set callback for mode change"""
        self.mode_callback = callback
    
    def set_theme_callback(self, callback: Callable):
        """Set callback for theme change"""
        self.theme_callback = callback
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.theme = "dark" if self.theme == "light" else "light"
        self.colors = COLORS[self.theme]
        
        # Update all widget colors
        self._update_widget_colors()
        
        if self.theme_callback:
            self.theme_callback(self.theme)
    
    def _update_widget_colors(self):
        """Update colors for all widgets"""
        # This is a simplified version - in practice you'd need to update each widget
        self.root.configure(bg=self.colors["bg"])
        
        # Update specific widgets
        for widget in self.root.winfo_children():
            if hasattr(widget, 'configure'):
                try:
                    if isinstance(widget, (tk.Label, tk.Button, tk.Frame)):
                        widget.configure(bg=self.colors["bg"])
                except:
                    pass
    
    def _show_settings_dialog(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.colors["bg"])
        
        # Theme toggle
        theme_btn = tk.Button(
            settings_window,
            text=f"Switch to {'Dark' if self.theme == 'light' else 'Light'} Theme",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=self.toggle_theme
        )
        theme_btn.pack(pady=20)
        
        # Player name entry
        name_frame = tk.Frame(settings_window, bg=self.colors["bg"])
        name_frame.pack(pady=20)
        
        tk.Label(
            name_frame,
            text="Player 1 Name:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).pack(side="left", padx=5)
        
        player1_name_entry = tk.Entry(name_frame, font=self.normal_font)
        player1_name_entry.insert(0, self.player_names["player1"])
        player1_name_entry.pack(side="left", padx=5)
        
        # Apply button
        apply_btn = tk.Button(
            settings_window,
            text="Apply Changes",
            font=self.normal_font,
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            command=lambda: self._apply_settings(
                player1_name_entry.get(),
                settings_window
            )
        )
        apply_btn.pack(pady=20)
    
    def _apply_settings(self, player1_name: str, window: tk.Toplevel):
        """Apply settings changes"""
        if player1_name.strip():
            self.player_names["player1"] = player1_name.strip()
        window.destroy()
    
    def enable_choices(self, enable: bool = True):
        """Enable or disable choice buttons"""
        state = "normal" if enable else "disabled"
        for btn in self.choice_buttons.values():
            btn.config(state=state)