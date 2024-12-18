from heapq import heappop, heappush
from typing import List, Optional
from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, make_move_for_ucs
from analyze.statistic import Statistic

# Функция поиска с использованием стратегии равных цен
def ucs(initial_Situation: Situation) -> Optional[List[int]]:
    """
    Функция поиска решения в игре в"Волк, коза, капуста, заяц, лиса, человек" с использованием алгоритма поиска по стратегии равных цен (Uniform Cost Search, UCS).

    UCS — это вариант поиска по графу, где для каждой вершины учитывается стоимость пути от начальной точки.
    В данном случае все переходы имеют одинаковую стоимость.

    Алгоритм работает следующим образом:
    1. Инициализируем приоритетную очередь, в которой каждый элемент представляет текущую стоимость, состояние и путь.
    2. Извлекаем состояние с наименьшей стоимостью из очереди.
    3. Проверяем, достигнуто ли целевое состояние — если да, возвращаем путь.
    4. Добавляем текущее состояние в множество посещённых.
    5. Генерируем возможные действия (0-13) и для каждого действия:
       - Если следующее состояние валидно и не посещено ранее, добавляем его в очередь с обновлённой стоимостью и путём.
    6. Если решение не найдено, возвращаем None.

    :param initial_Situation: начальная ситуация
    :return: список действий, ведущих к цели, или None, если решение не найдено
    """
    queue = [
        (0, initial_Situation, [], 0)
    ]  # Очередь с приоритетом (стоимость, ситуация, путь, глубина)
    visited = set()  # Множество для хранения посещённых ситуаций

    max_depth = 0  # Максимальная глубина поиска
    all_generated = 0  # Общее число порождённых вершин

    while queue:
        cost, current_Situation, path, depth = heappop(
            queue
        )  # Извлекаем ситуацию с наименьшей стоимостью

        # Пропускаем, если это состояние уже было посещено
        if current_Situation.create_key() in visited:
            continue

        # Проверяем, достигнута ли целевая ситуация
        if current_Situation.is_goal_Situation():
            return path, Statistic(len(path), max_depth + 1, all_generated)

        # Добавляем текущую ситуацию в посещённые
        visited.add(current_Situation.create_key())
        all_generated += 1

        # Обновляем максимальную глубину
        max_depth = max(max_depth, depth)

        # Генерируем все возможные действия (0-12)
        for action in range(13):
            next_Situation, weight = make_move_for_ucs(current_Situation, action)
            weight = weight%6
            # Если следующая ситуация валидна и не посещена ранее
            if (
                next_Situation
                and next_Situation.is_valid()
                and next_Situation.create_key() not in visited
            ):
                # Добавляем новую ситуацию в очередь с обновлённым путём
                heappush(queue, (cost + weight, next_Situation, path + [action], depth + 1))

    return None  # Решение не найдено