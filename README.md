How to Run:
Save all files in the same directory structure as shown above.

Run the game:

bash
python main.py
Features Implemented:
✅ Single Player Mode (vs Computer AI with 3 difficulty levels)
✅ Multiplayer Mode (2 players on same device)
✅ Score Tracking with win/loss/draw counts
✅ Game History log
✅ Visual Feedback with color-coded results
✅ Theme Support (Light/Dark mode)
✅ Statistics Tracking with file saving
✅ Reset Game functionality
✅ Player Customization (name changing)
✅ Clean GUI with intuitive controls

Future Extensions (Easy to Add):
Online Multiplayer: Add socket programming

Sound Effects: Use pygame or playsound

Advanced Animations: Use canvas for smoother animations

Player Avatars: Add image support with PIL

Tournament Mode: Best of 3/5/7 games

Additional Gestures: Rock-Paper-Scissors-Lizard-Spock

Database Storage: Use SQLite for persistent stats

Key Design Patterns Used:
MVC Pattern: GUI (View), GameLogic (Model), Main (Controller)

Callback Pattern: For UI events

Strategy Pattern: For AI difficulty levels

Observer Pattern: For UI updates

The code is modular, well-documented, and easy to extend. Each module has a single responsibility, making maintenance and debugging straightforward.
