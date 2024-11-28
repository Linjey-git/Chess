class ChessBotDFS:
    def __init__(self, depth, evaluator):
        self.depth = depth  # Глубина поиска
        self.evaluator = evaluator  # Функция оценки позиции
        self.nodes_explored = 0  # Счетчик просмотренных узлов
        self.transposition_table = {}  # Таблица переходов для запоминания ранее вычисленных позиций

    def get_best_move(self, board):
        """
        Определение лучшего хода для текущей позиции с использованием минимакса
        
        :param board: Объект chess.Board, представляющий текущую шахматную позицию
        :return: Лучший ход для текущей позиции
        """
        best_move = None  # Лучший найденный ход
        best_value = float('-inf')  # Изначально задаем наихудшую оценку
        alpha, beta = float('-inf'), float('inf')  # Инициализация значений для альфа-бета отсечения

        # Проходим по всем возможным ходам
        for move in self.get_ordered_moves(board):
            board.push(move)  # Выполняем ход
            value = self.minimax(board, self.depth - 1, alpha, beta, False)  # Вычисляем оценку с минимаксом
            board.pop()  # Возвращаем позицию назад

            # Если найденный ход лучше предыдущего, обновляем лучший
            if value > best_value:
                best_value = value
                best_move = move

            # Обновляем значение альфа для отсечения
            alpha = max(alpha, value)

        print(f"Nodes explored: {self.nodes_explored}")  # Вывод количества просмотренных узлов для отладки
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):

        # Реализация алгоритма Минимакс с альфа-бета отсечением и хешированием
        # Генерируем ключ для хэш-таблицы, чтобы учитывать текущую доску, глубину и альфа-бета параметры
        board_key = (board.board_fen(), depth, alpha, beta, maximizing_player)

        # Проверяем, если позиция уже вычислена ранее
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        self.nodes_explored += 1  # Увеличиваем счетчик просмотренных узлов

        # Если достигли максимальной глубины или игра завершена, оцениваем позицию
        if depth == 0 or board.is_game_over():
            evaluation = self.evaluator.evaluate(board)
            self.transposition_table[board_key] = evaluation  # Сохраняем оценку в хэш-таблице
            return evaluation

        if maximizing_player:
            # Максимизирующий игрок (бот)
            max_eval = float('-inf')
            for move in self.get_ordered_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)  # Обновляем альфа
                if beta <= alpha:  # Отсечение
                    break
            self.transposition_table[board_key] = max_eval  # Сохраняем результат в таблице переходов
            return max_eval
        else:
            # Минимизирующий игрок (противник)
            min_eval = float('inf')
            for move in self.get_ordered_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # Обновляем бета
                if beta <= alpha:  # Отсечение
                    break
            self.transposition_table[board_key] = min_eval  # Сохраняем результат в таблице переходов
            return min_eval

    def get_ordered_moves(self, board):
        """
        Возвращает список ходов, упорядоченных по приоритету (например, взятия выше обычных ходов).
        
        :param board: Текущая шахматная доска.
        :return: Список упорядоченных ходов.
        """
        def move_score(move):
            """
            Присваивает ходам вес на основе их приоритета.
            Взятие фигур имеет больший приоритет.
            
            :param move: Ход для оценки.
            :return: Оценка хода.
            """
            if board.is_capture(move):  # Если ход - взятие фигуры
                return 10
            if board.gives_check(move):  # Если ход ставит шах
                return 5
            return 0  # Остальные ходы имеют минимальный приоритет

        moves = list(board.legal_moves)  # Получаем все легальные ходы
        moves.sort(key=move_score, reverse=True)  # Сортируем по оценке (в порядке убывания)
        return moves