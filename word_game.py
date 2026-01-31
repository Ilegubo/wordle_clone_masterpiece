import flet as ft
import random
import requests
import os
from typing import List, Dict, Optional
try:
    from english_words import english_words_lower_alpha_set as all_words
except ImportError:
    all_words = set()

class WordGuessingGame:
    def __init__(self):
        self.words_by_length = {}
        self.current_word = ""
        self.current_guess = ""
        self.attempts = []
        self.max_attempts = 6
        self.game_won = False
        self.game_over = False
        self.word_length = 5
        self.show_keyboard = True
        
        # Theme definitions
        self.themes = {
            "cursor_dark": {
                "bg": "#1e1e1e",
                "fg": "#d4d4d4",
                "primary": "#007acc",
                "secondary": "#4ec9b0",
                "accent": "#c586c0",
                "success": "#4ec9b0",
                "warning": "#dcdcaa",
                "error": "#f44747",
                "card_bg": "#252526",
                "border": "#3c3c3c"
            },
            "light_modern": {
                "bg": "#ffffff",
                "fg": "#1e1e1e",
                "primary": "#0078d4",
                "secondary": "#107c10",
                "accent": "#b4009e",
                "success": "#107c10",
                "warning": "#b58900",
                "error": "#d13438",
                "card_bg": "#f3f2f1",
                "border": "#e1dfdd"
            }
        }
        self.current_theme = "cursor_dark"
        
        # Game flow state
        self.game_started = False
        self.game_paused = False
        
    def download_words(self):
        """Generate a list of common English words (5-8 letters) using wordfreq, fallback to built-ins."""
        try:
            from wordfreq import top_n_list
            # Get top common English words
            top_words = top_n_list("en", 50000)
            common_filtered = []
            for w in top_words:
                w = w.lower()
                if w.isalpha() and 5 <= len(w) <= 8:
                    common_filtered.append(w)
            # Deduplicate while preserving order
            seen = set()
            deduped = []
            for w in common_filtered:
                if w not in seen:
                    seen.add(w)
                    deduped.append(w)
            if not deduped:
                raise RuntimeError("No words produced from wordfreq")
            with open("words.txt", "w", encoding="utf-8") as f:
                f.write("# source: wordfreq top common words 5-8 letters\n")
                f.write("\n".join(deduped))
            # print(f"Generated common word list: {len(deduped)} words")
        except Exception as e:
            # print(f"Falling back to built-in common words due to: {e}")
            self.create_fallback_words()
    
    def create_fallback_words(self):
        """Create a fallback list of common 5-8 letter words if generation fails"""
        fallback_words = [
            # 5 letters
            "about", "after", "again", "below", "bring", "cause", "could", "every", "first", "found",
            "great", "group", "house", "large", "learn", "never", "other", "place", "right", "small",
            "sound", "still", "study", "their", "there", "these", "thing", "think", "those", "under",
            "water", "where", "which", "world", "young",
            # 6 letters
            "little", "people", "public", "number", "school", "family", "system", "change", "should", "during",
            "better", "always", "second", "before", "father", "mother", "others", "street", "market", "friend",
            # 7 letters
            "another", "because", "between", "country", "example", "history", "interest", "morning", "nothing", "picture",
            "program", "service", "through", "without", "womanly", "working", "writing", "student", "teacher", "company",
            # 8 letters
            "anything", "building", "children", "decision", "distance", "everyone", "football", "language", "learning", "meeting",
            "research", "security", "solution", "strength", "training", "treasure", "universe", "whatever", "yourself", "business",
        ]
        with open("words.txt", "w", encoding="utf-8") as f:
            f.write("# source: built-in common words 5-8 letters\n")
            f.write("\n".join(fallback_words))
    
    def load_words(self):
        """Load and organize words (only 5-letter words)"""
        try:
            with open("words.txt", "r") as f:
                words = f.read().splitlines()
            
            # Filter words: only 5-letter words
            for word in words:
                word = word.strip().lower()
                if word and not word.startswith('#') and word.isalpha() and len(word) == 5:
                    if 5 not in self.words_by_length:
                        self.words_by_length[5] = []
                    self.words_by_length[5].append(word)
            
            # print(f"Loaded {sum(len(words) for words in self.words_by_length.values())} words")
        except Exception as e:
            # print(f"Error loading words: {e}")
            self.create_fallback_words()
            self.load_words()
    
    def get_random_word(self, length: int = 5) -> str:
        """Get a random 5-letter word"""
        # Always use length 5
        if 5 in self.words_by_length and self.words_by_length[5]:
            return random.choice(self.words_by_length[5])
        
        # Fallback: use english_words library to find 5-letter words
        if all_words:
            candidates = [w for w in all_words if len(w) == 5 and w.isalpha()]
            if candidates:
                return random.choice(candidates)
        
        # Last resort: common 5-letter word
        return "hello"
    
    def start_new_game(self):
        """Start a new game"""
        self.current_word = self.get_random_word(self.word_length)
        self.current_guess = ""
        self.attempts = []
        self.game_won = False
        self.game_over = False
        # print(f"New word: {self.current_word}")  # For debugging
    
    def add_letter(self, letter: str):
        """Add a letter to current guess"""
        if (
            len(self.current_guess) < self.word_length
            and not self.game_over
            and self.game_started
            and not self.game_paused
        ):
            self.current_guess += letter.lower()
            self.update_ui()
    
    def remove_letter(self):
        """Remove last letter from current guess"""
        if self.current_guess and not self.game_over and self.game_started and not self.game_paused:
            self.current_guess = self.current_guess[:-1]
            self.update_ui()
    
    def submit_guess(self):
        """Submit current guess"""
        if (
            len(self.current_guess) == self.word_length
            and not self.game_over
            and self.game_started
            and not self.game_paused
        ):
            # Accept the guess regardless of dictionary membership
            self.attempts.append(self.current_guess)
            self.current_guess = ""

            # Check game state
            if self.attempts[-1] == self.current_word:
                self.game_won = True
                self.game_over = True
            elif len(self.attempts) >= self.max_attempts:
                self.game_over = True

            self.update_ui()
    
    def get_letter_color(self, letter: str, position: int, attempt: str) -> str:
        """Get color for a letter based on game rules"""
        # Deprecated single-letter check; prefer compute_attempt_colors for correct handling
        if letter == self.current_word[position]:
            return self.themes[self.current_theme]["success"]
        elif letter in self.current_word:
            return self.themes[self.current_theme]["warning"]
        else:
            return self.themes[self.current_theme]["error"]

    def compute_attempt_colors(self, attempt: str) -> List[str]:
        """Compute colors for an entire attempt using Wordle rules handling repeated letters.

        - First mark exact matches (green)
        - Count remaining letters in target (excluding greens)
        - For non-green positions, mark yellow only up to remaining counts, otherwise gray
        """
        target = self.current_word
        n = len(target)
        colors: List[Optional[str]] = [None] * n
        
        try:
            theme = self.themes.get(self.current_theme, self.themes["cursor_dark"])
        except (KeyError, IndexError):
            theme = {"success": "#00ff00", "warning": "#ffff00", "error": "#ff0000"}

        # Step 1: mark greens and build counts for remaining target letters
        remaining: Dict[str, int] = {}
        for i in range(n):
            if i < len(attempt) and attempt[i] == target[i]:
                colors[i] = theme.get("success", "#00ff00")
            else:
                remaining[target[i]] = remaining.get(target[i], 0) + 1

        # Step 2: mark yellows/greys for non-green positions
        for i in range(n):
            if colors[i] is not None:
                continue
            ch = attempt[i] if i < len(attempt) else ""
            if ch and remaining.get(ch, 0) > 0:
                colors[i] = theme.get("warning", "#ffff00")
                remaining[ch] -= 1
            else:
                colors[i] = theme.get("error", "#ff0000")

        return colors
    
    def create_ui(self, page: ft.Page):
        """Create the main UI"""
        self.page = page
        page.title = "Word Guessing Game"
        page.theme_mode = ft.ThemeMode.DARK
        page.window_width = 650
        page.window_height = 550
        page.window_resizable = True
        page.padding = 20
        
        # Theme selector (only Light and Dark)
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            value=self.current_theme,
            options=[
                ft.dropdown.Option("light_modern", "Light Theme"),
                ft.dropdown.Option("cursor_dark", "Dark Theme"),
            ],
            on_select=self.change_theme
        )
        
        # Word length selector - removed (only 5-letter words supported)
        # self.length_dropdown is no longer used
        
        # Keyboard toggle
        self.keyboard_toggle = ft.Switch(
            label="Keyboard",
            value=self.show_keyboard,
            on_change=self.toggle_keyboard
        )
        
        # Game board
        self.game_board = ft.Column(spacing=5)
        
        # Current guess display
        self.current_guess_display = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )
        
        # Keyboard
        self.keyboard = ft.Column(spacing=5)
        
        # Status text
        self.status_text = ft.Text(
            "Welcome to Word Guessing Game!",
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Game controls: Begin / Pause / End
        self.begin_btn = ft.Button("Begin", on_click=lambda e: self.begin_game())
        self.pause_btn = ft.Button("Pause", on_click=lambda e: self.pause_game())
        self.end_btn = ft.Button("End", on_click=lambda e: self.end_game())
        self.controls_row = ft.Row([
            self.begin_btn,
            self.pause_btn,
            self.end_btn
        ], alignment=ft.MainAxisAlignment.START, spacing=10)
        
        # Play again button
        self.play_again_btn = ft.Button(
            "Play Again",
            on_click=self.play_again,
            visible=False
        )
        
        # Layout
        # Left: Keyboard container (will be toggled visible/invisible)
        self.keyboard_container = ft.Container(
            content=ft.Column([
                self.keyboard
            ], alignment=ft.MainAxisAlignment.START, spacing=0),
            width=480,
            alignment=ft.Alignment(-1, -1),
            visible=self.show_keyboard  # Start visible based on show_keyboard
        )
        
        page.add(
            ft.Row([
                self.keyboard_container,
                # Right: Game board, guess display, status, controls (vertical)
                ft.Column([
                    ft.Row([
                        ft.Container(self.theme_dropdown, bgcolor=None),
                        ft.Container(self.keyboard_toggle, bgcolor=None),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            self.status_text,
                    ft.Container(height=10),
                    self.controls_row,
            ft.Container(height=20),
            self.game_board,
            ft.Container(height=20),
            self.current_guess_display,
            ft.Container(height=20),
            ft.Row([self.play_again_btn], alignment=ft.MainAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.START, spacing=0, expand=True)
            ], alignment=ft.MainAxisAlignment.START, spacing=40)
        )
        
        # Initialize game
        self.download_words()
        self.load_words()
        self.start_new_game()
        self._setup_theme()
        self.update_ui()
        # Set up physical keyboard event handlers
        page.on_keyboard_event = self.handle_keyboard_event
        page.on_key_down = self.handle_keyboard_event
    
    def change_theme(self, e):
        """Change the current theme"""
        self.current_theme = e.control.value
        # Smooth theme switch: update all UI pieces with new theme
        self.apply_theme()
        self.update_ui()
    
    def toggle_keyboard(self, e):
        """Toggle keyboard visibility"""
        self.show_keyboard = e.control.value
        self.keyboard_container.visible = self.show_keyboard
        self.update_ui()
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def apply_theme(self):
        """Apply current theme to the page and UI"""
        self._setup_theme()
        # Proactively refresh controls that depend on theme colors
        self.update_ui()
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def _setup_theme(self):
        """Setup theme colors without triggering UI updates (safe for init)"""
        theme = self.themes[self.current_theme]
        # Update page base color
        if hasattr(self, 'page') and self.page:
            self.page.bgcolor = theme["bg"]
            # Set page theme mode for better default control contrast
            self.page.theme_mode = ft.ThemeMode.DARK if self.current_theme == "cursor_dark" else ft.ThemeMode.LIGHT

        # Apply label and field styles for readability
        fg = theme["fg"]
        # Dropdowns
        if hasattr(self, 'theme_dropdown') and self.theme_dropdown:
            self.theme_dropdown.label = "Theme"
            self.theme_dropdown.text_style = ft.TextStyle(color=fg)
            self.theme_dropdown.label_style = ft.TextStyle(color=fg)
        if hasattr(self, 'length_dropdown') and self.length_dropdown:
            self.length_dropdown.text_style = ft.TextStyle(color=fg)
            self.length_dropdown.label_style = ft.TextStyle(color=fg)
        # Switch label
        if hasattr(self, 'keyboard_toggle') and self.keyboard_toggle:
            self.keyboard_toggle.label = "Keyboard"
            self.keyboard_toggle.label_style = ft.TextStyle(color=fg)
    
    def create_letter_box(self, letter: str = "", color: str = None, is_current: bool = False) -> ft.Container:
        """Create a letter box for the game board"""
        theme = self.themes[self.current_theme]
        
        if color is None:
            color = theme["border"]
        
        return ft.Container(
            width=50,
            height=50,
            border=ft.Border(left=ft.BorderSide(2, color), right=ft.BorderSide(2, color), top=ft.BorderSide(2, color), bottom=ft.BorderSide(2, color)),
            border_radius=8,
            alignment=ft.Alignment(0, 0),
            bgcolor=theme["card_bg"] if not is_current else theme["primary"],
            content=ft.Text(
                letter.upper() if letter else "",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme["fg"]
            )
        )
    
    def create_keyboard_row(self, letters: List[str]) -> ft.Row:
        """Create a row of keyboard buttons"""
        theme = self.themes[self.current_theme]
        keyboard_disabled = (not self.game_started) or self.game_paused or self.game_over
        
        buttons = []
        for letter in letters:
            btn = ft.Button(
                letter.upper(),
                width=55,
                height=50,
                on_click=lambda e, l=letter: self.add_letter(l),
                disabled=keyboard_disabled,
                style=ft.ButtonStyle(
                    bgcolor=theme["card_bg"],
                    color=theme["fg"],
                    alignment=ft.Alignment(0, 0)
                )
            )
            buttons.append(btn)
        
        return ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=5)
    
    def update_ui(self):
        """Update the entire UI"""
        theme = self.themes[self.current_theme]
        
        # Clear existing content
        self.game_board.controls.clear()
        self.current_guess_display.controls.clear()
        self.keyboard.controls.clear()
        
        # Update game board
        for attempt in self.attempts:
            row = ft.Row(spacing=5, alignment=ft.MainAxisAlignment.CENTER)
            colors = self.compute_attempt_colors(attempt)
            for i, letter in enumerate(attempt):
                color = colors[i]
                row.controls.append(self.create_letter_box(letter, color))
            self.game_board.controls.append(row)
        
        # Add empty rows for remaining attempts
        for _ in range(self.max_attempts - len(self.attempts)):
            row = ft.Row(spacing=5, alignment=ft.MainAxisAlignment.CENTER)
            for _ in range(self.word_length):
                row.controls.append(self.create_letter_box())
            self.game_board.controls.append(row)
        
        # Update current guess display
        for i in range(self.word_length):
            letter = self.current_guess[i] if i < len(self.current_guess) else ""
            self.current_guess_display.controls.append(
                self.create_letter_box(letter, is_current=True)
            )
        
        # Update keyboard
        if self.show_keyboard:
            keyboard_layout = [
                "qwertyuiop",
                "asdfghjkl",
                "zxcvbnm"
            ]
            
            for row_letters in keyboard_layout:
                self.keyboard.controls.append(
                    self.create_keyboard_row(list(row_letters))
                )
            
            # Add control buttons
            control_row = ft.Row(
                [
                    ft.Button(
                        "⌫",
                        width=60,
                        height=50,
                        on_click=lambda e: self.remove_letter(),
                        disabled=(not self.game_started) or self.game_paused or self.game_over,
                        style=ft.ButtonStyle(
                            bgcolor=theme["card_bg"],
                            color=theme["fg"],
                            alignment=ft.Alignment(0, 0)
                        )
                    ),
                    ft.Button(
                        "Enter",
                        width=85,
                        height=50,
                        on_click=lambda e: self.submit_guess(),
                        disabled=(not self.game_started) or self.game_paused or self.game_over,
                        style=ft.ButtonStyle(
                            bgcolor=theme["primary"],
                            color=theme["fg"],
                            alignment=ft.Alignment(0, 0)
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
            self.keyboard.controls.append(control_row)
        
        # Update control buttons and status
        self.begin_btn.disabled = self.game_started and not self.game_over
        self.pause_btn.text = "Resume" if self.game_paused and self.game_started and not self.game_over else "Pause"
        self.pause_btn.disabled = (not self.game_started) or self.game_over
        self.end_btn.disabled = (not self.game_started) or self.game_over

        if not self.game_started and not self.game_over:
            self.status_text.value = "Click Begin to start the game."
            self.status_text.color = theme["fg"]
            self.play_again_btn.visible = False
        elif self.game_paused and not self.game_over:
            self.status_text.value = "Game paused. Click Resume to continue."
            self.status_text.color = theme["warning"]
            self.play_again_btn.visible = False
        elif self.game_won:
            self.status_text.value = f"Congratulations! You won in {len(self.attempts)} attempts!"
            self.status_text.color = theme["success"]
            self.play_again_btn.visible = True
        elif self.game_over:
            self.status_text.value = f"Game Over! The word was: {self.current_word.upper()}"
            self.status_text.color = theme["error"]
            self.play_again_btn.visible = True
        else:
            self.status_text.value = f"Attempts: {len(self.attempts)}/{self.max_attempts}"
            self.status_text.color = theme["fg"]
            self.play_again_btn.visible = False
        
        self.page.update()
    
    def play_again(self, e):
        """Start a new game"""
        self.start_new_game()
        self.game_started = True
        self.game_paused = False
        self.update_ui()

    def handle_keyboard_event(self, e: ft.KeyboardEvent):
        # Accept inputs even if not started: first key press begins the game (letters/backspace) or submit (enter)
        if e.key is None:
            return
        key_raw = e.key
        key = key_raw.lower()

        # Normalize Enter keys across platforms (Enter, NumpadEnter, Return)
        is_enter = key in {"enter", "numpadenter", "return"}
        is_backspace = key == "backspace"
        is_letter = len(key) == 1 and key.isalpha()

        # If game paused or over, ignore
        if self.game_over or self.game_paused:
            return

        # Auto-begin on first interaction if not started yet
        if not self.game_started and (is_letter or is_backspace or is_enter):
            self.begin_game()

        # After ensuring started, route actions
        if is_letter:
            self.add_letter(key)
        elif is_enter:
            self.submit_guess()
        elif is_backspace:
            self.remove_letter()

    def begin_game(self):
        # Start or restart the game and enable inputs
        if not self.game_started or self.game_over:
            self.start_new_game()
        self.game_started = True
        self.game_paused = False
        self.update_ui()

    def pause_game(self):
        # Toggle pause state if game is started and not over
        if not self.game_started or self.game_over:
            return
        self.game_paused = not self.game_paused
        self.update_ui()

    def end_game(self):
        # End the game immediately
        if not self.game_started or self.game_over:
            return
        self.game_over = True
        self.update_ui()

def main(page: ft.Page):
    game = WordGuessingGame()
    game.create_ui(page)

if __name__ == "__main__":
    ft.app(target=main) 