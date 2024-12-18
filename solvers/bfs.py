from collections import deque
from typing import Optional, List
from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, make_move
from analyze.statistic import Statistic

# Функция поиска в ширину
def bfs(initial_Situation: Situation) -> Optional[List[int]]:
    """
    Поиск в ширину (Breadth-First Search) в игре "Волк, коза, капуста, заяц, лиса, человек".
    
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
            return path, Statistic(len(path), max_depth, all_generated)

        # Пропускаем, если это состояние уже было посещено
        if current_Situation.create_key() in visited:
            continue

        # Добавляем текущее состояние в посещённые
        visited.add(current_Situation.create_key())
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        # Генерируем все возможные действия (0-13)
        for action in range(13):
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