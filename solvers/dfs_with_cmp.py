from functools import cmp_to_key
from wolf_goat_cabbage_fox_rabbit_human.enviroment import make_move
from analyze import Statistic

all_generated = 0
max_depth = 0

def dfs_with_prioritize(current_situation, stack = []):
    """
    Функция поиска решения в игре волк коза капуста с использованием алгоритма поиска в глубину (DFS)
    с приоритетом действий в игре "Волк, коза, капуста, заяц, лиса, человек".

    :param initial_situation: начальная ситуация
    :return: список действий, приводящих к цели, или None, если решение не найдено
    """

    global all_generated, max_depth

    if not stack:
        all_generated = 0
        max_depth = 0

    max_depth = max(max_depth, len(stack))

    if not stack:
        stack = [current_situation]

    # Проверяем, достигнута ли целевая ситуация
    if current_situation.is_goal_Situation():
        return stack, Statistic(len(stack), max_depth, all_generated)
    
    # Оценочная функция реализованная при помощи компаратора
    def evaluation(a, b):
            a_situation = make_move(current_situation, a)
            b_situation = make_move(current_situation, b)

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

    for action in next_actions:
        next_situation = make_move(current_situation, action)

        if next_situation in stack:
            continue

        all_generated += 1

        # Если новая ситуация валидна
        if next_situation and next_situation.is_valid():
            result = dfs_with_prioritize(next_situation, stack + [next_situation])    
            if result:
                return result

    return None  # Решение не найдено