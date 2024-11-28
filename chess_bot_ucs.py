import heapq
import chess

class ChessBotUCS:
    def __init__(self, depth, evaluator):
        self.max_depth = depth
        self.evaluator = evaluator
        self.nodes_explored = 0

    def get_best_move(self, board):
        priority_queue = []
        # Начальный элемент: (стоимость, FEN строки, первый ход, глубина)
        heapq.heappush(priority_queue, (0, board.fen(), None, 0))
        best_move = None

        while priority_queue:
            current_cost, current_fen, first_move, depth = heapq.heappop(priority_queue)

            current_board = chess.Board(current_fen)  # Восстанавливаем доску из FEN

            if depth >= self.max_depth or current_board.is_game_over():
                return first_move

            for move in current_board.legal_moves:
                current_board.push(move)
                move_cost = self.evaluator.evaluate(current_board)
                # Преобразуем ход в строку перед добавлением в очередь
                heapq.heappush(priority_queue, (current_cost + move_cost, current_board.fen(), first_move if depth > 0 else move, depth + 1))
                current_board.pop()

        return best_move