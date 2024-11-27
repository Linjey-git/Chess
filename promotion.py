import tkinter as tk
import chess


def get_promotion_choice(square_from, square_to):
    """Показує вікно для вибору фігури, на яку перетворити пішака, і повертає хід. /
    Displays a window for selecting the piece to promote a pawn to, and returns the move."""
    promotion_result = None

    def on_choice(choice):
        """Обробник вибору фігури для перетворення / Handles the selection of a promotion piece."""
        nonlocal promotion_result
        promotion_result = choice
        promotion_window.destroy()  # Закриває вікно / Closes the window

    # Створюємо нове вікно для вибору перетворення пішака /
    # Create a new window for selecting pawn promotion
    promotion_window = tk.Toplevel()
    promotion_window.title("Promote Pawn")

    # Додаємо кнопки для кожного варіанту перетворення /
    # Add buttons for each promotion option
    for piece, label in [(chess.QUEEN, "Queen"), (chess.ROOK, "Rook"),
                         (chess.BISHOP, "Bishop"), (chess.KNIGHT, "Knight")]:
        tk.Button(promotion_window, text=label, command=lambda c=piece: on_choice(c)).pack()

    # Очікуємо закриття вікна перед поверненням результату /
    # Wait for the window to close before returning the result
    promotion_window.wait_window()
    if promotion_result is not None:
        # Повертаємо хід із вказаним перетворенням /
        # Return the move with the specified promotion
        return chess.Move(square_from, square_to, promotion=promotion_result)
    return None