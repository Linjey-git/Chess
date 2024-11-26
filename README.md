# Chess Game

A simple chess application built with Python and Tkinter. This project provides a GUI-based chess game where users can play against each other with all the standard chess rules, including pawn promotion.

## Features

- Interactive chessboard built with Tkinter.
- Supports all standard chess rules:
  - Legal moves validation.
  - Pawn promotion with a selection dialog.
  - Game over detection.
- Lightweight and easy to run locally.

## Prerequisites

Ensure you have Python installed on your system. If not, download and install Python from the [official website](https://www.python.org/).

## Installation

Follow these steps to set up and run the project:

1. **Upgrade `pip`:**
   ```bash
   python.exe -m pip install --upgrade pip
   ```

2. **Install dependencies:**
   - Install Pillow for image handling:
     ```bash
     pip install pillow
     ```
   - Install chess for chess logic:
     ```bash
     pip install chess
     ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/Linjey-git/Chess.git
   cd Chess
   ```
## Usage

- The chessboard will appear in a graphical window.
- Click on a piece to view its legal moves.
- Make a move by selecting a target square.
- If a pawn reaches the opposite end of the board, a promotion dialog will appear for selecting the desired piece.

## Project Structure

- **main.py**: Main entry point of the application.
- **board.py**: Handles the chessboard logic using the chess library.
- **gui.py**: Manages the graphical interface with Tkinter.
- **images/**: Contains the chess piece images used in the application.

## Example

1. Select a piece to highlight its legal moves.
2. Move the piece to a desired square.
3. Enjoy playing chess!

## License

This project is open-source and licensed under the MIT License.
