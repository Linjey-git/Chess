from chess_bot_dfs import ChessBotDFS
from chess_bot_bfs import ChessBotBFS
from chess_bot_bds import ChessBotBDS
from position_evaluator import PositionEvaluator

class ChessBotController:
    def __init__(self, dfs_depth, bfs_depth, bds_depth):
        # Create a single instance of PositionEvaluator
        self.position_evaluator = PositionEvaluator()
        
        # Pass it to each bot
        self.dfs_bot = ChessBotDFS(dfs_depth, self.position_evaluator)
        self.bfs_bot = ChessBotBFS(bfs_depth, self.position_evaluator)
        self.bds_bot = ChessBotBDS(bds_depth, self.position_evaluator)

    def choose_bot(self, board):
        """
        Bot selection based on the stage of the game.
        """
        piece_count = sum(1 for square in board.piece_map().values())
        moves_count = sum(1 for _ in board.legal_moves)

        if piece_count > 24 and moves_count < 1000000:  # First 30 moves (temporarily replaced with a debug value)
            print("Use BFS for the initial stage of the game")
            return self.bfs_bot
        elif 20 <= piece_count <= 24 and moves_count <50:  # Middle moves
            print("Use DFS for the middle stage of the game")
            return self.dfs_bot
        else:
            print("Use BFS for complex situations") # Endgame
            # return self.ucs_bot
            return self.bds_bot

    def get_best_move(self, board):
        """
        Getting the best move from the selected bot
        """
        chosen_bot = self.choose_bot(board)
        return chosen_bot.get_best_move(board)