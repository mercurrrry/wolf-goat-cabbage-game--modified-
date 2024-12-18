from collections import deque
from typing import Dict, List, Tuple, Optional
from analyze import Statistic
from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, make_move

def bidirectional_search(
    initial_state: Situation, goal_state: Situation
) -> Optional[tuple[List[int], Statistic]]:
    """
    Алгоритм двунаправленного поиска в игре "Волк, коза, капуста, заяц, лиса, человек".
    
    :param initial_state: начальная ситуация
    :param goal_state: целевая ситуация (финиш)
    :return: список действий, ведущих к цели, или None, если решение не найдено
    """
    # Очереди для двух направлений поиска
    front_queue = deque([(initial_state, [], 0)])  # Поиск от начальной ситуации
    back_queue = deque([(goal_state, [], 0)])  # Поиск от целевой ситуации

    # Множества для посещённых ситуаций с каждой стороны
    front_visited = {
        initial_state: []
    }  # Карта: ситуация -> путь от начальной ситуации
    back_visited = {goal_state: []}  # Карта: ситуация -> путь от целевой ситуации

    max_depth = [0, 0]  # Максимальная глубина поиска на фронте
    all_generated = 0  # Общее число порождённых вершин

    while front_queue and back_queue:
        # Расширяем фронт от начальной ситуации
        result, depth_increase, max_depth_in_front = expand_front(
            front_queue, front_visited, back_visited, False
        )

        max_depth[0] = max(max_depth[0], max_depth_in_front)

        all_generated += depth_increase

        if result:
            return result, Statistic(
                len(result), max_depth_in_front + max_depth[1], all_generated
            )  # Путь найден

        # Расширяем фронт от целевой ситуации
        result, depth_increase, max_depth_in_front = expand_front(
            back_queue, back_visited, front_visited, True
        )

        max_depth[1] = max(max_depth[1], max_depth_in_front)

        all_generated += depth_increase

        if result:
            return result, Statistic(
                len(result), max_depth_in_front + max_depth[0], all_generated
            )

    return None  # Решение не найдено


def expand_front(
    queue: deque[Tuple[Situation, List, int]],
    visited_from_this_side: Dict[Situation, List],
    visited_from_other_side: Dict[Situation, List],
    reverse_path: bool,
):
    """
    Расширяет один фронт поиска и проверяет пересечение с другим фронтом.

    :param queue: очередь для текущего фронта поиска
    :param visited_from_this_side: ситуации, посещённые с этой стороны
    :param visited_from_other_side: ситуации, посещённые с противоположной стороны
    :param reverse_path: если True, разворачиваем путь от целевой ситуации
    :return: список действий, если путь найден, или None
    """
    current_state, path, current_depth = queue.popleft()
    nodes_generated = 0  # Счётчик для порождённых вершин
    max_depth_in_front = current_depth  # Максимальная глубина в текущем фронте

    # Проверяем, пересекается ли текущая ситуация с другим фронтом
    if current_state in visited_from_other_side:
        # Получаем путь от другого фронта
        other_path = visited_from_other_side[current_state]

        # Если мы расширяем путь от целевой ситуации, разворачиваем его
        if reverse_path:
            return (
                path + [(3 - x) for x in other_path[::-1]],
                nodes_generated,
                max_depth_in_front,
            )
        else:
            return other_path[::-1] + path, nodes_generated, max_depth_in_front

    # Генерируем возможные действия (0-3)
    for action in range(13):
        next_state = make_move(current_state, action)

        # Если следующая ситация валидна и не посещена с этой стороны
        if next_state and next_state.is_valid and next_state not in visited_from_this_side:
            visited_from_this_side[next_state] = path + [action]  # Обновляем путь
            queue.append((next_state, path + [action], current_depth + 1))
            nodes_generated += 1  # Увеличиваем число порождённых вершин
            max_depth_in_front = max(max_depth_in_front, current_depth + 1)

    return None, nodes_generated, max_depth_in_front