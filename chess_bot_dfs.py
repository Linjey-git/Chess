class ChessBotDFS:
    def __init__(self, depth, evaluator):
        self.depth = depth  # Search depth
        self.evaluator = evaluator  # Position evaluation function
        self.nodes_explored = 0 # Counter for the number of nodes explored
        self.transposition_table = {}  # Transposition table for storing previously computed positions

    def get_best_move(self, board):
        """
        Determining the best move for the current position using minimax

        :param board: chess.Board object representing the current chess position
        :return: The best move for the current position
        """
        best_move = None  # The best move found
        best_value = float('-inf')  # Initially set the worst evaluation 
        alpha, beta = float('-inf'), float('inf')  # Initialization of values for alpha-beta pruning

        # We go through all possible moves
        for move in self.get_ordered_moves(board):
            board.push(move)  # We make a move
            value = self.minimax(board, self.depth - 1, alpha, beta, False)  # We calculate the evaluation using minimax
            board.pop()  # We revert the position

            # If the found move is better than the previous one, we update the best
            if value > best_value:
                best_value = value
                best_move = move

            # We update the alpha value for pruning
            alpha = max(alpha, value)

        print(f"Nodes explored: {self.nodes_explored}")  # Output the number of nodes evaluated for debugging
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):

        # Generate a key for the hash table to account for the current board, depth, and alpha-beta parameters
        # We generate a key for the hash table to account for the current board, depth, and alpha-beta parameters
        board_key = (board.board_fen(), depth, alpha, beta, maximizing_player)

        # We check if the position has already been evaluated previously
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        self.nodes_explored += 1  # We increase the counter of evaluated nodes

        # If we have reached the maximum depth or the game is over, we evaluate the position
        if depth == 0 or board.is_game_over():
            evaluation = self.evaluator.evaluate(board)
            self.transposition_table[board_key] = evaluation  # We store the evaluation in the hash table
            return evaluation

        if maximizing_player:
            # Maximizing player (bot)
            max_eval = float('-inf')
            for move in self.get_ordered_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)  # We update alpha
                if beta <= alpha:  # Pruning
                    break
            self.transposition_table[board_key] = max_eval  # We store the result in the transposition table
            return max_eval
        else:
            # Minimizing player (opponent)
            min_eval = float('inf')
            for move in self.get_ordered_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # We update beta
                if beta <= alpha:  # Pruning
                    break
            self.transposition_table[board_key] = min_eval  # We store the result in the transposition table
            return min_eval

    def get_ordered_moves(self, board):
        """
        Returns a list of moves ordered by priority (for example, captures above regular moves).
        
        :param board: Current chessboard.
        :return: List of ordered moves.
        """
        def move_score(move):
            """
            Assigns a weight to moves based on their priority.  
            Capturing pieces has a higher priority.
            
            :param move: Move for evaluation.
            :return: Move evaluation.
            """
            if board.is_capture(move):  # If the move is a capture
                return 10
            if board.gives_check(move):  # If the move puts the king in check
                return 5
            return 0  # Other moves have the lowest priority

        moves = list(board.legal_moves)  # Get all legal moves
        moves.sort(key=move_score, reverse=True)  # Sort by evaluation (in descending order)
        return moves