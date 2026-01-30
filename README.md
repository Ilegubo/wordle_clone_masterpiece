# Word Guessing Game

A modern, interactive word guessing game built with Flet, featuring beautiful themes and a Wordle-like interface.

## Features

- 🎨 **Multiple Themes**: Solarized Dark, Solarized Light, Cursor Dark, and Light Modern themes
- ⌨️ **Interactive Keyboard**: On-screen keyboard with toggle option
- 📏 **Variable Word Length**: Support for 3-8 letter words
- 🎯 **Wordle-like Gameplay**: Individual letter input with color-coded feedback
- 🔄 **Play Again**: Easy restart after winning or losing
- 📱 **Responsive Design**: Dynamic and resizable window
- 📚 **Large Word Database**: Downloads comprehensive English word list

## Installation

1. **Create and activate virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python word_game.py
   ```

## How to Play

1. **Choose Settings**:
   - Select your preferred theme from the dropdown
   - Choose word length (3-8 letters)
   - Toggle keyboard display on/off

2. **Gameplay**:
   - Click letters on the keyboard or type on your physical keyboard
   - Use the backspace button (⌫) to delete letters
   - Press Enter to submit your guess
   - You have 6 attempts to guess the word

3. **Color Feedback**:
   - 🟢 **Green**: Letter is correct and in the right position
   - 🟡 **Yellow**: Letter is correct but in the wrong position
   - ⚫ **Gray**: Letter is not in the word

4. **After Game**:
   - Click "Play Again" to start a new game
   - Change settings anytime during gameplay

## Themes

- **Solarized Dark**: Classic dark theme with blue accents
- **Solarized Light**: Clean light theme with high contrast
- **Cursor Dark**: VS Code-inspired dark theme
- **Light Modern**: Modern light theme with subtle colors

## Technical Details

- **Framework**: Flet (Flutter for Python)
- **Word List**: Automatically downloads from GitHub repository
- **Fallback**: Built-in word list if download fails
- **Cross-platform**: Works on Windows, macOS, and Linux

## File Structure

```
word guessing game/
├── word_game.py          # Main game application
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── byu_secret_word.py   # Original console version
└── words.txt            # Downloaded word list (created automatically)
```

## Troubleshooting

- **Word list download fails**: The game will use a built-in fallback word list
- **Window not resizing**: Make sure you're using the latest version of Flet
- **Performance issues**: Try reducing the word length or disabling the keyboard

## Future Enhancements

- Statistics tracking
- Daily word challenges
- Sound effects
- Share results
- Custom word lists
- Hard mode (use revealed hints)

Enjoy playing! 🎮 