import tkinter as tk
import chess


def get_promotion_choice(square_from, square_to):
    """Показує вікно для вибору фігури, на яку перетворити пішака, і повертає хід."""
    promotion_result = None

    def on_choice(choice):
        nonlocal promotion_result
        promotion_result = choice
        promotion_window.destroy()

    promotion_window = tk.Toplevel()
    promotion_window.title("Promote Pawn")

    for piece, label in [(chess.QUEEN, "Queen"), (chess.ROOK, "Rook"),
                         (chess.BISHOP, "Bishop"), (chess.KNIGHT, "Knight")]:
        tk.Button(promotion_window, text=label, command=lambda c=piece: on_choice(c)).pack()

    promotion_window.wait_window()
    if promotion_result is not None:
        # Повертаємо хід із вказаним перетворенням
        return chess.Move(square_from, square_to, promotion=promotion_result)
    return None
