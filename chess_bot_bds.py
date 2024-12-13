import heapq
from collections import deque

import chess


class ChessBotBDS:
    def __init__(self, evaluator, max_depth):
        """
        Initialize the bot using bidirectional search.
        :param evaluator: PositionEvaluator object for evaluating positions.
        :param max_depth: Maximum search depth.
        """
        self.evaluator = evaluator
        self.max_depth = max_depth

    def bidirectional_search(self, board, target_condition):
        """
        Perform a bidirectional search to find the best move.
        :param board: Current state of the chessboard.
        :param target_condition: Function to check if the target state is reached.
        :return: The best move or None if no solution is found.
        """
        forward_queue = deque([(board.copy(), None, 0)])  # (board state, move leading here, depth)
        backward_queue = deque([(board.copy(), None, 0)])  # Simulated backward search
        visited_forward = {}
        visited_backward = {}

        # Initial conditions
        visited_forward[board.fen()] = None
        visited_backward[board.fen()] = None

        while forward_queue and backward_queue:
            # Expand the forward search
            if forward_queue:
                current_board, move, depth = forward_queue.popleft()

                if depth < self.max_depth:
                    for legal_move in current_board.legal_moves:
                        current_board.push(legal_move)
                        current_fen = current_board.fen()

                        if current_fen in visited_backward:
                            # Intersection found
                            return legal_move

                        if current_fen not in visited_forward:
                            forward_queue.append((current_board.copy(), legal_move, depth + 1))
                            visited_forward[current_fen] = legal_move

                        current_board.pop()

            # Expand the backward search
            if backward_queue:
                current_board, move, depth = backward_queue.popleft()

                if depth < self.max_depth:
                    for legal_move in current_board.legal_moves:
                        current_board.push(legal_move)
                        current_fen = current_board.fen()

                        if current_fen in visited_forward:
                            # Intersection found
                            return visited_forward[current_fen]  # Move from forward search

                        if current_fen not in visited_backward:
                            backward_queue.append((current_board.copy(), legal_move, depth + 1))
                            visited_backward[current_fen] = legal_move

                        current_board.pop()

        return None  # Solution not found

    def get_best_move(self, board):
        """
        Finds the best move using bidirectional search.
        :param board: Current state of the chessboard.
        :return: The best move.
        """
        def target_condition(b):
            # Target condition: for example, checkmate
            return b.is_checkmate()

        best_move = self.bidirectional_search(board, target_condition)
        if best_move is None:
            # If no solution is found, return the best move evaluated by the evaluator
            return max(
                board.legal_moves,
                key=lambda move: self._evaluate_move(board, move),
                default=None
            )
        return best_move

    def _evaluate_move(self, board, move):
        """
        Evaluates a single move on the chessboard.
        :param board: Current state of the chessboard.
        :param move: The move to be evaluated.
        :return: Numerical evaluation score of the move.
        """
        board.push(move)
        score = self.evaluator.evaluate(board)
        board.pop()
        return score
