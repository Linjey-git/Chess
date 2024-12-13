import chess

class PositionEvaluator:
    def __init__(self):
        # Piece values
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.5,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0 #The evaluation of the king is meaningless, as the king cannot be captured; checkmate is the only goal, and this is handled by king_safety.
        }

        # Central squares
        self.center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        self.wider_center = [
            chess.C3, chess.D3, chess.E3, chess.F3,
            chess.C4, chess.F4,
            chess.C5, chess.F5,
            chess.C6, chess.D6, chess.E6, chess.F6
        ]

    def evaluate(self, board):
        """
        Overall position evaluation
        """
        if board.turn == chess.BLACK:
            multiplier = 1
        else: 
            multiplier = -1  # We change the sign depending on the color 
        score = 0
        score += self.material_balance(board) * 4
        score += self.center_control(board) * 3
        score += self.pawn_structure(board) * 2
        score += self.king_safety(board) * 5
        score += self.piece_activity(board) * 1
        score += self.threats(board) * 3
        return score * multiplier

    def material_balance(self, board):
        """
        Evaluation of material difference.
        """
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score -= value
                elif piece.color == chess.BLACK:
                    score += value
        return score

    def center_control(self, board):
        """
        Evaluation of central control
        """
        score = 0
        for square in self.center_squares:
            piece = board.piece_at(square)
            if piece:
                score += 0.5 if piece.color == chess.BLACK else -0.5

        for square in self.wider_center:
            piece = board.piece_at(square)
            if piece:
                score += 0.25 if piece.color == chess.BLACK else -0.25

        return score

    def pawn_structure(self, board):
        """
        Evaluation of pawn structure: isolated, doubled
        """
        score = 0
        pawns = list(board.pieces(chess.PAWN, chess.BLACK)) + list(board.pieces(chess.PAWN, chess.WHITE))
        pawn_files = {file: [] for file in range(8)}

        for square in pawns:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            pawn_files[file].append(rank)

        for file, ranks in pawn_files.items():
            if len(ranks) > 1:
                score -= 0.5  # Doubled pawns
            if len(ranks) == 1:
                neighbors = [file - 1, file + 1]
                if not any(neighbor in pawn_files and pawn_files[neighbor] for neighbor in neighbors):
                    score -= 0.5  # Isolated pawns

        return score

    def king_safety(self, board):
        score = 0
        """
        King safety evaluation (LOTS OF POINTS FOR CHECKMATE)
        """

        """
        Simple king safety evaluation (outdated)
        if black_king_square in [chess.G8, chess.C8]:
            score += 1
        if white_king_square in [chess.G1, chess.C1]:
            score -= 1
        if board.is_checkmate() and board.turn == chess.WHITE:
            score += 1000  # Black wins if the white king is in checkmate
        """

        if board.is_checkmate() and board.turn == chess.WHITE:
            score += 10000  #We add points to the bot for a white checkmate.
        elif board.is_checkmate() and board.turn == chess.BLACK:
            score -= 10000 
        return score

    def piece_activity(self, board):
        """
        Piece activity evaluation: number of available moves.
        """
        score = 0
        for move in board.legal_moves:
            if board.color_at(move.from_square) == chess.BLACK:
                score += 0.1
            else:
                score -= 0.1
        return score

    def threats(self, board):
        """
        Threat evaluation: attacked opponent pieces.
        """
        score = 0
        for square in chess.SQUARES:
            attackers = board.attackers(chess.BLACK, square)
            piece = board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                score += len(attackers) * self.piece_values.get(piece.piece_type, 0)

            attackers = board.attackers(chess.WHITE, square)
            piece = board.piece_at(square)
            if piece and piece.color == chess.BLACK:
                score -= len(attackers) * self.piece_values.get(piece.piece_type, 0)

        return score