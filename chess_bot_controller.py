from chess_bot_dfs import ChessBotDFS
from chess_bot_bfs import ChessBotBFS
from chess_bot_ucs import ChessBotUCS
from position_evaluator import PositionEvaluator

class ChessBotController:
    def __init__(self, dfs_depth, bfs_depth, ucs_depth):
        # Создаем один экземпляр PositionEvaluator
        self.position_evaluator = PositionEvaluator()  
        
        # Передаем его в каждый бот
        self.dfs_bot = ChessBotDFS(dfs_depth, self.position_evaluator)
        self.bfs_bot = ChessBotBFS(bfs_depth, self.position_evaluator)
        self.ucs_bot = ChessBotUCS(ucs_depth, self.position_evaluator)

    def choose_bot(self, board):
        """
        Выбор бота в зависимости от стадии игры.
        """
        piece_count = sum(1 for square in board.piece_map().values())
        moves_count = sum(1 for _ in board.legal_moves)

        if piece_count > 24 and moves_count < 30:  # Первые 30 ходов
            print("Используем DFS для начала игры.")
            return self.dfs_bot
        elif 10 <= piece_count <= 24 and moves_count <50:  # Средние ходы
            print("Используем BFS для средней стадии игры.")
            return self.bfs_bot
        else:  
            print("Используем UCS для сложных ситуаций.") # Эндшпиль
            return self.ucs_bot

    def get_best_move(self, board):
        """
        Получение лучшего хода от выбранного бота.
        """
        chosen_bot = self.choose_bot(board)
        return chosen_bot.get_best_move(board)