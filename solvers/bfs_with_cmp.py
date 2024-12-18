from collections import deque
from typing import Optional, List
from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, make_move
from analyze.statistic import Statistic
from functools import cmp_to_key

"""
    Функция не является обязательной в рамках текущей учебной программы
"""

def bfs_with_cmp(initial_Situation: Situation) -> Optional[List[int]]:
    """
    Поиск в ширину (Breadth-First Search с оценочной функцией) в игре "Волк, коза, капуста лиса заяц человек".
    
    :param initial_situation: начальное ситуация 
    :return: список действий, приводящий к целевой ситуации, или None, если решение не найдено
    """
    visited = set()  # Храним все посещённые состояния
    queue = deque(
        [(initial_Situation, [], 0)]
    )  # Каждый элемент: (текущая ситуация, путь действий, глубина)

    max_depth = 0  # Максимальная глубина поиска
    all_generated = 0  # Общее число порождённых вершин
    
    while queue:
        current_Situation, path, depth = queue.popleft()


        # Проверяем, достигнуто ли целевое состояние
        if current_Situation.is_goal_Situation():
            return path, Statistic(len(path), max_depth + 1, all_generated)

        # Пропускаем, если это состояние уже было посещено
        if current_Situation.create_key() in visited:
            continue

        # Добавляем текущее состояние в посещённые
        visited.add(current_Situation.create_key())
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        def evaluation(a, b):
            a_situation = make_move(current_Situation, a)
            b_situation = make_move(current_Situation, b)

            if a_situation is None:
                return 1
            elif b_situation is None:
                return -1
            elif a_situation == b_situation:
                return 0
            else:
                return -1 if a_situation < b_situation else 1

        # Генерируем все возможные действия (0-13)
        next_actions = list(range(13))
        
        next_actions.sort(key=cmp_to_key(evaluation))

        # Генерируем все возможные действия (0-13)
        for action in next_actions:
            next_Situation = make_move(current_Situation, action)

            # Если новое состояние валидно и не посещено ранее
            if (
                next_Situation
                and next_Situation.is_valid()
                and next_Situation.create_key() not in visited
            ):
                # Добавляем новую ситуацию в очередь с обновлённым путём
                queue.append((next_Situation, path + [action], depth + 1))

    return None