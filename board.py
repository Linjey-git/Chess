import chess

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def get_board(self):
        """Повертає поточний стан шахівниці / Returns the current state of the chessboard."""
        return self.board

    def make_move(self, move):
        """Здійснює хід, якщо він допустимий / Executes a move if it is legal."""
        if self.board.is_legal(move):
            self.board.push(move)
            return True
        return False

    def get_legal_moves(self):
        """Повертає список допустимих ходів / Returns a list of legal moves."""
        legal_moves = self.board.legal_moves
        moves_without_promotion = set()  # Множина для зберігання унікальних ходів / Set to store unique moves

        for move in legal_moves:
            if move.promotion:
                # Створюємо новий хід без промоції / Create a new move without promotion
                move_without_promotion = chess.Move(move.from_square, move.to_square)
            else:
                move_without_promotion = move

            # Додаємо хід у множину (множина автоматично видаляє дублікати) /
            # Add the move to the set (the set automatically removes duplicates)
            moves_without_promotion.add(move_without_promotion)

        # Повертаємо список унікальних ходів / Return the list of unique moves
        return list(moves_without_promotion)

    def is_game_over(self):
        """Перевіряє, чи гра завершена (шах і мат, пат тощо) / Checks if the game is over (checkmate, stalemate, etc.)."""
        return self.board.is_game_over()

    def reset(self):
        """Скидає дошку до початкового стану / Resets the board to the initial state."""
        self.board = chess.Board()