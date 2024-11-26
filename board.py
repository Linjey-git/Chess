import chess

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def get_board(self):
        """Повертає поточний стан шахівниці."""
        return self.board

    def make_move(self, move):
        """Здійснює хід, якщо він допустимий."""
        if self.board.is_legal(move):
            self.board.push(move)
            return True
        return False

    def get_legal_moves(self):
        """Повертає список допустимих ходів."""
        legal_moves = self.board.legal_moves
        moves_without_promotion = set()  # Множина для зберігання унікальних ходів

        for move in legal_moves:
            if move.promotion:
                # Створюємо новий хід без промоції
                move_without_promotion = chess.Move(move.from_square, move.to_square)
            else:
                move_without_promotion = move

            # Додаємо хід у множину (множина автоматично видаляє дублікати)
            moves_without_promotion.add(move_without_promotion)

        # Повертаємо список унікальних ходів
        return list(moves_without_promotion)

    def is_game_over(self):
        """Перевіряє, чи гра завершена (шах і мат, пат тощо)."""
        return self.board.is_game_over()

    def reset(self):
        """Скидає дошку до початкового стану."""
        self.board = chess.Board()