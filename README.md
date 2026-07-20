
🎯 Sudoku
A clean, fully-featured Sudoku game built with Python and Tkinter — inspired by sudoku.com.

Python Tkinter License

📸 Preview
┌─────────────────────────────┐
│        S U D O K U          │
│      Think. Solve. Win.     │
│                             │
│  [ Easy ] [Medium] [ Hard ] │
│           [Expert]          │
│                             │
│         ▶  PLAY             │
└─────────────────────────────┘
Deep navy UI · Sky-blue highlights · Gold accents · Coral error states

✨ Features
Feature	Details
4 Difficulty Levels	Easy (36 clues), Medium (28), Hard (22), Expert (17)
Smart Highlighting	Selected cell + entire row, column & box highlighted
Notes / Pencil Marks	Toggle note mode to jot candidate digits per cell
Error Detection	Wrong entries highlighted in red immediately
Mistake Tracker	3 lives shown as colored dots — game ends at 3 errors
Hint System	Reveals the correct digit for any empty cell
Live Timer	MM:SS stopwatch running from first move
Keyboard Navigation	Arrow keys, number keys, Backspace, N for notes
Number Pad	On-screen 1–9 pad; digits gray out when fully placed
Win / Game Over	Overlay showing time taken and mistake count
New Game	Instantly restart at the same or different difficulty
🚀 Getting Started
Requirements
Python 3.7 or higher
Tkinter — included with Python on most platforms
Linux users: if Tkinter is missing, install it with:

sudo apt install python3-tk
Run the game
python3 sudoku.py
No pip installs needed. No external dependencies. Just Python.

🎮 How to Play
Selecting a cell
Click any empty cell on the board, or use the arrow keys to move around.

Entering a number
Click a cell, then press 1–9 on your keyboard, or click the on-screen number pad.
Clue cells (the pre-filled numbers) cannot be changed.
Notes mode
Toggle pencil/notes mode by clicking ✏ Notes or pressing N.
In notes mode, clicking a digit adds or removes it as a small candidate mark inside the cell — useful for advanced solving techniques. Notes are auto-cleared for related cells when you correctly place a number.

Erasing
Click ⌫ Erase or press Backspace / Delete to clear the selected cell and its notes.

Hints
Click 💡 Hint to reveal the correct answer for the selected cell (or a random empty cell if none is selected).

Mistakes
You have 3 lives. Each wrong entry costs one life. At 3 mistakes, the game ends.

⌨️ Keyboard Shortcuts
Key	Action
1 – 9	Enter digit in selected cell
Backspace / Delete / 0	Erase selected cell
Arrow keys	Move selection
N	Toggle notes mode
🗂️ Project Structure
sudoku.py          ← entire game, single file
README.md          ← this file
The project is intentionally a single file with no dependencies — easy to share, run anywhere, and read end-to-end.

Code layout inside sudoku.py
COLOR PALETTE       hex values for all UI colors
SUDOKU LOGIC        is_valid(), solve(), generate_full_board(), make_puzzle()
SudokuApp           root Tk window, screen router
MenuScreen          difficulty picker, play button
GameScreen          board canvas, HUD, interaction handlers
  ├── _build_ui()       top bar, error dots, canvas, numpad, action buttons
  ├── _draw_board()     renders all 81 cells, notes, grid lines, box borders
  ├── _on_click()       maps canvas click → (row, col)
  ├── _on_key()         keyboard handler
  ├── _input_number()   validates entry, updates board, checks win/lose
  ├── _hint()           fills correct answer for a cell
  ├── _toggle_notes()   switches pencil-mark mode
  ├── _tick()           1-second timer loop
  ├── _win()            stops timer, shows success overlay
  └── _game_over()      stops timer, shows failure overlay

🧠 How the Puzzle Generation Works
Solve an empty board — a backtracking algorithm fills the grid with shuffled digit order, producing a random valid solution every run.
Remove digits — cells are removed at random until the target clue count for the chosen difficulty is reached.
Store the solution — the full board is kept in memory for instant validation of every entry.
The randomised solve step means no two games are the same.

🎨 Design
Role	Value
Background	#1A1A2E deep navy
Panel	#16213E dark navy
Board blue	#0F3460 rich blue
Cell	#E8F4FD ice white
Selection	#4FC3F7 sky blue
Accent	#F7B731 gold
Error	#FF6B6B coral
Success	#26DE81 mint green
