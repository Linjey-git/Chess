import chess
import promotion

from constants import SQUARE_SIZE, BOARD_COLORS
from tkinter import messagebox


class ChessEvents:
    def __init__(self, chess_board, chess_app):
        self.chess_app = chess_app
        self.board = chess_board
        self.selected_square = None  # зберігаємо вибрану клітинку для ходу
        self.selected_piece = None  # зберігаємо вибрану фігуру для ходу

    def on_square_click(self, event):
        """Обробка кліку по клітинці на шахівниці."""
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        print("Перевірку пройдено 0")

        # Інвертуємо координату рядка для коректного відображення на перевернутій шахівниці
        row = 7 - row  # Це інвертує рядки шахівниці (для перевернутого відображення)

        square = 8 * row + col  # Обчислюємо клітинку з урахуванням інвертованих рядків

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.get_legal_moves():  # Перевірка на допустимість ходу
                if self.selected_piece and self.selected_piece.piece_type == chess.PAWN:
                    print("Перевірку пройдено 1")
                    if (self.selected_piece.color == chess.WHITE and row == 7) or (
                            self.selected_piece.color == chess.BLACK and row == 0):
                        print("Перевірку пройдено 2")
                        print(move)
                        # Виклик функції перетворення пішака
                        promotion_move = promotion.get_promotion_choice(self.selected_square, square)
                        if promotion_move:
                            print("Перевірку пройдено 3")
                            move = promotion_move  # Заміна стандартного ходу на хід із перетворенням
                            print(move)

                self.board.make_move(move)
                self.chess_app.update_board()

                if self.board.is_game_over():
                    messagebox.showinfo("Гра завершена", "Гра завершена!")
                    self.board.reset()
                    self.chess_app.update_board()

                self.selected_square = None  # Скидаємо вибір фігури після ходу
            else:
                self.selected_square = None  # Скидаємо вибір, якщо хід недійсний
                self.chess_app.update_board()  # Оновлюємо шахівницю для видалення підсвічених ходів

        else:
            print("Просто клітина")
            piece = self.board.get_board().piece_at(square)
            if piece:  # Якщо клітинка містить фігуру
                print("Є фігура")
                self.selected_square = square  # Вибираємо фігуру
                self.selected_piece = piece
                print(self.selected_piece)
                self.chess_app.update_board()  # Оновлюємо шахівницю для відображення можливих ходів

    def get_board_state(self):
        return {square: str(piece) for square, piece in self.board.board.piece_map().items()}
