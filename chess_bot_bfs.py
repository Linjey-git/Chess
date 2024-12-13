import chess
from queue import PriorityQueue


class ChessBotBFS:
    def __init__(self, max_depth, evaluator):
        # Maximum depth to explore moves
        self.max_depth = max_depth
        # Evaluation function to score board positions
        self.evaluator = evaluator
        # Counter for the number of positions evaluated
        self.nodes_explored = 0

    def get_best_move(self, board):

        best_move = None
        best_score = float('-inf')  # Initialize with a very low score

        max_depth = self.max_depth

        if (board.turn == chess.WHITE):
            current_player = chess.WHITE
        elif (board.turn == chess.BLACK):
            current_player = chess.BLACK

        # Iterate over all legal moves
        for move in board.legal_moves:
            # First, get the short-term (current board) score for this move
            current_score = self.evaluator.evaluate(board)  # Short-term score

            # Then, get the long-term score for this move by using greedy_best_move_score
            long_term_score = self.greedy_best_move_score(board, move, max_depth, current_player)  # Long-term score

            # Combine both short-term and long-term scores (simple addition for now)
            combined_score = current_score + long_term_score

            # Check if this move has the highest combined score
            if combined_score > best_score:
                best_score = combined_score
                best_move = move

        return best_move

    def greedy_best_move_score(self, board, move, max_depth, current_player):

        # Apply the move to the board
        board.push(move)
        self.nodes_explored += 1

        # Handle edge cases: game over or max depth is 1
        if board.is_game_over() or max_depth == 1:
            score = self.evaluator.evaluate(board)
            board.pop()  # Undo the move
            return score

        # Initialize best score (min or max depending on the player)
        is_maximizing_player = board.turn == current_player
        best_score = float('-inf') if is_maximizing_player else float('inf')

        # Greedy evaluation: Evaluate moves only at the immediate next depth
        for next_move in board.legal_moves:
            board.push(next_move)
            self.nodes_explored += 1

            # Evaluate the board state after the move
            score = self.evaluator.evaluate(board)

            # Update the best score based on whether it's maximizing or minimizing
            if is_maximizing_player:
                best_score = max(best_score, score)  # Maximizing player
            else:
                best_score = min(best_score, score)  # Minimizing player

            board.pop()  # Undo the move to explore the next one

        # Undo the original move
        board.pop()
        return best_score