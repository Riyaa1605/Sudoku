import tkinter as tk
from tkinter import messagebox, font
import random
import time
import copy

# ─── COLOR PALETTE ───────────────────────────────────────────────────────────
BG          = "#1A1A2E"   # deep navy
PANEL       = "#16213E"   # slightly lighter navy
BOARD_BG    = "#0F3460"   # rich blue
CELL_BG     = "#E8F4FD"   # near-white ice
CELL_HOVER  = "#D0E8F8"   # hover tint
CELL_SEL    = "#4FC3F7"   # sky-blue selection
CELL_GROUP  = "#C5DFF0"   # soft grouping tint
PRE_FG      = "#1A1A2E"   # dark navy for clue numbers
USER_FG     = "#0F3460"   # ocean blue for user input
ERROR_BG    = "#FF6B6B"   # coral error
ERROR_FG    = "#FFFFFF"
ACCENT      = "#4FC3F7"   # sky-blue accent
ACCENT2     = "#F7B731"   # gold accent
BORDER      = "#0F3460"   # grid border
THICK_LINE  = "#0A2540"   # 3×3 box border
BTN_BG      = "#4FC3F7"
BTN_FG      = "#1A1A2E"
BTN_HOVER   = "#81D4FA"
NOTE_FG     = "#607D8B"
SUCCESS     = "#26DE81"


# ─── SUDOKU LOGIC ────────────────────────────────────────────────────────────
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    br, bc = 3 * (row // 3), 3 * (col // 3)
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == num:
                return False
    return True


def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_full_board():
    board = [[0] * 9 for _ in range(9)]
    solve(board)
    return board


def make_puzzle(full_board, difficulty):
    clues = {"Easy": 36, "Medium": 28, "Hard": 22, "Expert": 17}
    num_clues = clues.get(difficulty, 30)
    puzzle = copy.deepcopy(full_board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    to_remove = 81 - num_clues
    for r, c in cells[:to_remove]:
        puzzle[r][c] = 0
    return puzzle


# ─── MAIN APP ────────────────────────────────────────────────────────────────
class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.difficulty = tk.StringVar(value="Medium")
        self._show_menu()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_menu(self):
        self._clear()
        MenuScreen(self)

    def _start_game(self, difficulty):
        self._clear()
        GameScreen(self, difficulty)


# ─── MENU SCREEN ─────────────────────────────────────────────────────────────
class MenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True, padx=40, pady=40)
        self._build()

    def _build(self):
        # Title
        tk.Label(self, text="SUDOKU", bg=BG, fg=ACCENT,
                 font=("Helvetica", 52, "bold")).pack(pady=(20, 4))
        tk.Label(self, text="Think. Solve. Win.", bg=BG, fg=NOTE_FG,
                 font=("Helvetica", 14)).pack(pady=(0, 40))

        # Difficulty cards
        tk.Label(self, text="SELECT DIFFICULTY", bg=BG, fg=NOTE_FG,
                 font=("Helvetica", 11, "bold")).pack(pady=(0, 12))

        diff_frame = tk.Frame(self, bg=BG)
        diff_frame.pack()

        difficulties = [
            ("Easy",   "#26DE81", "Great for beginners"),
            ("Medium", "#4FC3F7", "Balanced challenge"),
            ("Hard",   "#F7B731", "For sharp minds"),
            ("Expert", "#FF6B6B", "Maximum challenge"),
        ]

        self._selected_diff = tk.StringVar(value="Medium")

        for diff, color, desc in difficulties:
            self._make_diff_card(diff_frame, diff, color, desc)

        # Play button
        play_btn = tk.Button(
            self, text="▶  PLAY", bg=ACCENT, fg=BTN_FG,
            font=("Helvetica", 16, "bold"),
            relief="flat", cursor="hand2", bd=0,
            padx=40, pady=14,
            command=self._play
        )
        play_btn.pack(pady=30)
        play_btn.bind("<Enter>", lambda e: play_btn.config(bg=BTN_HOVER))
        play_btn.bind("<Leave>", lambda e: play_btn.config(bg=ACCENT))

    def _make_diff_card(self, parent, diff, color, desc):
        var = self._selected_diff
        frame = tk.Frame(parent, bg=PANEL, cursor="hand2",
                         padx=18, pady=12)
        frame.pack(side="left", padx=8, pady=4)

        dot = tk.Label(frame, text="●", bg=PANEL, fg=color,
                       font=("Helvetica", 14))
        dot.pack()
        tk.Label(frame, text=diff, bg=PANEL, fg="white",
                 font=("Helvetica", 12, "bold")).pack()
        tk.Label(frame, text=desc, bg=PANEL, fg=NOTE_FG,
                 font=("Helvetica", 9)).pack()

        def select(e=None):
            var.set(diff)
            for child in parent.winfo_children():
                child.config(relief="flat", bg=PANEL)
                for sub in child.winfo_children():
                    sub.config(bg=PANEL)
            frame.config(relief="solid", bg=BOARD_BG)
            for sub in frame.winfo_children():
                sub.config(bg=BOARD_BG)

        frame.bind("<Button-1>", select)
        for child in frame.winfo_children():
            child.bind("<Button-1>", select)

        if diff == "Medium":
            frame.config(relief="solid", bg=BOARD_BG)
            for sub in frame.winfo_children():
                sub.config(bg=BOARD_BG)

    def _play(self):
        self.master._start_game(self._selected_diff.get())


# ─── GAME SCREEN ─────────────────────────────────────────────────────────────
class GameScreen(tk.Frame):
    def __init__(self, master, difficulty):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)
        self.difficulty = difficulty
        self.selected = None          # (row, col)
        self.errors = 0
        self.MAX_ERRORS = 3
        self.start_time = time.time()
        self.running = True
        self.notes_mode = False
        self.notes = [[set() for _ in range(9)] for _ in range(9)]

        # Generate puzzle
        full = generate_full_board()
        self.solution = copy.deepcopy(full)
        self.puzzle   = make_puzzle(full, difficulty)
        self.board    = copy.deepcopy(self.puzzle)

        self._build_ui()
        self._draw_board()
        self._tick()

        self.bind_all("<Key>", self._on_key)

    # ── UI BUILD ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top bar
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(16, 0))

        back_btn = tk.Label(top, text="← Menu", bg=BG, fg=ACCENT,
                            font=("Helvetica", 12), cursor="hand2")
        back_btn.pack(side="left")
        back_btn.bind("<Button-1>", lambda e: self.master._show_menu())

        tk.Label(top, text=f"★  {self.difficulty}", bg=BG, fg=ACCENT2,
                 font=("Helvetica", 12, "bold")).pack(side="left", padx=20)

        self.timer_label = tk.Label(top, text="00:00", bg=BG, fg="white",
                                    font=("Helvetica", 14, "bold"))
        self.timer_label.pack(side="right")
        tk.Label(top, text="⏱ ", bg=BG, fg=NOTE_FG,
                 font=("Helvetica", 12)).pack(side="right")

        # Error display
        err_frame = tk.Frame(self, bg=BG)
        err_frame.pack(pady=(6, 0))
        tk.Label(err_frame, text="Mistakes:", bg=BG, fg=NOTE_FG,
                 font=("Helvetica", 11)).pack(side="left")
        self.err_dots = []
        for i in range(self.MAX_ERRORS):
            d = tk.Label(err_frame, text="●", bg=BG, fg="#444466",
                         font=("Helvetica", 14))
            d.pack(side="left", padx=3)
            self.err_dots.append(d)

        # Board canvas
        self.CELL = 58
        self.PADDING = 4
        size = self.CELL * 9 + self.PADDING * 2 + 6  # extra for thick lines
        self.canvas = tk.Canvas(self, width=size, height=size,
                                bg=THICK_LINE, highlightthickness=0)
        self.canvas.pack(padx=24, pady=14)
        self.canvas.bind("<Button-1>", self._on_click)

        # Number pad
        pad_frame = tk.Frame(self, bg=BG)
        pad_frame.pack(pady=(0, 10))
        self.num_buttons = []
        for n in range(1, 10):
            btn = tk.Label(pad_frame, text=str(n), bg=PANEL, fg="white",
                           font=("Helvetica", 18, "bold"),
                           width=3, pady=10, cursor="hand2", relief="flat")
            btn.pack(side="left", padx=4)
            btn.bind("<Button-1>", lambda e, num=n: self._input_number(num))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BOARD_BG))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=PANEL))
            self.num_buttons.append(btn)

        # Action buttons row
        act_frame = tk.Frame(self, bg=BG)
        act_frame.pack(pady=(6, 16))

        actions = [
            ("✏ Notes", self._toggle_notes),
            ("⌫ Erase", self._erase),
            ("💡 Hint",  self._hint),
            ("🔄 New",   self._new_game),
        ]
        self.notes_btn = None
        for i, (label, cmd) in enumerate(actions):
            b = tk.Label(act_frame, text=label, bg=PANEL, fg="white",
                         font=("Helvetica", 11), padx=14, pady=8,
                         cursor="hand2", relief="flat")
            b.pack(side="left", padx=5)
            b.bind("<Button-1>", lambda e, c=cmd: c())
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=BOARD_BG))
            b.bind("<Leave>", lambda e, btn=b: btn.config(
                bg=ACCENT if btn == self.notes_btn and self.notes_mode else PANEL))
            if label.startswith("✏"):
                self.notes_btn = b

    # ── BOARD DRAWING ─────────────────────────────────────────────────────────
    def _cell_xy(self, row, col):
        P = self.PADDING
        C = self.CELL
        # extra thick-line pixels: 2 between boxes
        extra_x = (col // 3) * 2
        extra_y = (row // 3) * 2
        x = P + col * C + extra_x
        y = P + row * C + extra_y
        return x, y

    def _draw_board(self):
        self.canvas.delete("all")
        C = self.CELL

        for row in range(9):
            for col in range(9):
                x, y = self._cell_xy(row, col)

                # Cell background
                if self.selected == (row, col):
                    fill = CELL_SEL
                elif self.selected and self._same_group(row, col):
                    fill = CELL_GROUP
                else:
                    fill = CELL_BG

                val = self.board[row][col]
                is_error = (val != 0 and val != self.solution[row][col]
                            and self.puzzle[row][col] == 0)
                if is_error:
                    fill = ERROR_BG

                self.canvas.create_rectangle(
                    x + 1, y + 1, x + C - 1, y + C - 1,
                    fill=fill, outline="", tags=f"cell_{row}_{col}"
                )

                # Number or notes
                if val != 0:
                    color = PRE_FG if self.puzzle[row][col] != 0 else (
                        ERROR_FG if is_error else USER_FG)
                    weight = "bold" if self.puzzle[row][col] != 0 else "normal"
                    self.canvas.create_text(
                        x + C // 2, y + C // 2,
                        text=str(val),
                        font=("Helvetica", 22, weight),
                        fill=color
                    )
                else:
                    # Draw notes
                    ns = self.notes[row][col]
                    if ns:
                        for n in range(1, 10):
                            if n in ns:
                                nr, nc = (n - 1) // 3, (n - 1) % 3
                                nx = x + nc * (C // 3) + C // 6
                                ny = y + nr * (C // 3) + C // 6
                                self.canvas.create_text(
                                    nx, ny, text=str(n),
                                    font=("Helvetica", 8),
                                    fill=NOTE_FG
                                )

        # Thin grid lines
        for row in range(9):
            for col in range(9):
                x, y = self._cell_xy(row, col)
                self.canvas.create_rectangle(
                    x, y, x + C, y + C,
                    fill="", outline=BORDER, width=1
                )

        # Thick box borders
        for br in range(3):
            for bc in range(3):
                r0, c0 = br * 3, bc * 3
                x0, y0 = self._cell_xy(r0, c0)
                x1, y1 = self._cell_xy(r0 + 2, c0 + 2)
                self.canvas.create_rectangle(
                    x0, y0, x1 + self.CELL, y1 + self.CELL,
                    fill="", outline=THICK_LINE, width=3
                )

        self._update_num_buttons()

    def _same_group(self, row, col):
        sr, sc = self.selected
        return (row == sr or col == sc or
                (row // 3 == sr // 3 and col // 3 == sc // 3))

    # ── INTERACTION ──────────────────────────────────────────────────────────
    def _on_click(self, event):
        C = self.CELL
        for row in range(9):
            for col in range(9):
                x, y = self._cell_xy(row, col)
                if x <= event.x <= x + C and y <= event.y <= y + C:
                    self.selected = (row, col)
                    self._draw_board()
                    return

    def _on_key(self, event):
        if event.char in "123456789":
            self._input_number(int(event.char))
        elif event.keysym in ("BackSpace", "Delete", "0"):
            self._erase()
        elif event.keysym == "Up"    and self.selected:
            self.selected = (max(0, self.selected[0] - 1), self.selected[1])
            self._draw_board()
        elif event.keysym == "Down"  and self.selected:
            self.selected = (min(8, self.selected[0] + 1), self.selected[1])
            self._draw_board()
        elif event.keysym == "Left"  and self.selected:
            self.selected = (self.selected[0], max(0, self.selected[1] - 1))
            self._draw_board()
        elif event.keysym == "Right" and self.selected:
            self.selected = (self.selected[0], min(8, self.selected[1] + 1))
            self._draw_board()
        elif event.keysym.lower() == "n":
            self._toggle_notes()

    def _input_number(self, num):
        if not self.selected or not self.running:
            return
        row, col = self.selected
        if self.puzzle[row][col] != 0:
            return  # clue cell

        if self.notes_mode:
            if num in self.notes[row][col]:
                self.notes[row][col].remove(num)
            else:
                self.notes[row][col].add(num)
            self._draw_board()
            return

        self.notes[row][col].clear()
        self.board[row][col] = num

        if num != self.solution[row][col]:
            self.errors += 1
            self._update_errors()
            if self.errors >= self.MAX_ERRORS:
                self._game_over()
        else:
            # Remove notes for peers
            self._remove_peer_notes(row, col, num)

        self._draw_board()

        if all(self.board[r][c] != 0 for r in range(9) for c in range(9)):
            if all(self.board[r][c] == self.solution[r][c]
                   for r in range(9) for c in range(9)):
                self._win()

    def _erase(self):
        if not self.selected:
            return
        row, col = self.selected
        if self.puzzle[row][col] != 0:
            return
        self.board[row][col] = 0
        self.notes[row][col].clear()
        self._draw_board()

    def _toggle_notes(self):
        self.notes_mode = not self.notes_mode
        if self.notes_btn:
            self.notes_btn.config(bg=ACCENT if self.notes_mode else PANEL,
                                  fg=BTN_FG if self.notes_mode else "white")

    def _hint(self):
        if not self.selected:
            # pick random empty cell
            empty = [(r, c) for r in range(9) for c in range(9)
                     if self.board[r][c] == 0 and self.puzzle[r][c] == 0]
            if not empty:
                return
            row, col = random.choice(empty)
            self.selected = (row, col)

        row, col = self.selected
        if self.puzzle[row][col] != 0:
            return
        self.board[row][col] = self.solution[row][col]
        self.notes[row][col].clear()
        self._remove_peer_notes(row, col, self.solution[row][col])
        self._draw_board()

    def _remove_peer_notes(self, row, col, num):
        peers = set()
        for c in range(9): peers.add((row, c))
        for r in range(9): peers.add((r, col))
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                peers.add((r, c))
        for r, c in peers:
            self.notes[r][c].discard(num)

    def _new_game(self):
        self.master._start_game(self.difficulty)

    # ── HUD UPDATES ──────────────────────────────────────────────────────────
    def _update_errors(self):
        for i, dot in enumerate(self.err_dots):
            dot.config(fg=ERROR_BG if i < self.errors else "#444466")

    def _update_num_buttons(self):
        counts = [0] * 10
        for r in range(9):
            for c in range(9):
                v = self.board[r][c]
                if v:
                    counts[v] += 1
        for i, btn in enumerate(self.num_buttons, start=1):
            if counts[i] >= 9:
                btn.config(fg=NOTE_FG)
            else:
                btn.config(fg="white")

    def _tick(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            m, s = divmod(elapsed, 60)
            self.timer_label.config(text=f"{m:02d}:{s:02d}")
            self.after(1000, self._tick)

    # ── WIN / LOSE ────────────────────────────────────────────────────────────
    def _win(self):
        self.running = False
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        self._show_overlay(
            "🎉 Solved!",
            f"You completed {self.difficulty} in {m:02d}:{s:02d}\n"
            f"Mistakes: {self.errors}/{self.MAX_ERRORS}",
            SUCCESS
        )

    def _game_over(self):
        self.running = False
        self._show_overlay(
            "Game Over",
            "Too many mistakes!\nBetter luck next time.",
            ERROR_BG
        )

    def _show_overlay(self, title, msg, color):
        overlay = tk.Toplevel(self)
        overlay.title("")
        overlay.configure(bg=PANEL)
        overlay.resizable(False, False)
        overlay.grab_set()
        overlay.transient(self)

        tk.Label(overlay, text=title, bg=PANEL, fg=color,
                 font=("Helvetica", 28, "bold")).pack(padx=40, pady=(30, 8))
        tk.Label(overlay, text=msg, bg=PANEL, fg="white",
                 font=("Helvetica", 13), justify="center").pack(padx=40)

        btn_frame = tk.Frame(overlay, bg=PANEL)
        btn_frame.pack(pady=24)

        for text, cmd in [("🔄 Play Again", lambda: [overlay.destroy(), self._new_game()]),
                          ("← Menu",       lambda: [overlay.destroy(), self.master._show_menu()])]:
            b = tk.Button(btn_frame, text=text, bg=ACCENT, fg=BTN_FG,
                          font=("Helvetica", 12, "bold"), relief="flat",
                          padx=20, pady=10, cursor="hand2",
                          command=cmd)
            b.pack(side="left", padx=8)
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=ACCENT))

        # center overlay
        self.update_idletasks()
        x = self.winfo_rootx() + self.winfo_width()  // 2 - 160
        y = self.winfo_rooty() + self.winfo_height() // 2 - 100
        overlay.geometry(f"+{x}+{y}")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()