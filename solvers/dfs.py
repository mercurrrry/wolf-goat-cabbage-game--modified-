from wolf_goat_cabbage_fox_rabbit_human.enviroment import make_move
from analyze import Statistic


all_generated = 0
max_depth = 0

def depth(current_situation, stack = []):
    """
    Функция поиска решения в игре волк коза капуста с использованием алгоритма поиска в глубину (DFS) в игре "Волк, коза, капуста, заяц, лиса, человек".

    :param initial_situation: начальная ситуация
    :return: массив ситуаций, приводящих к цели, или None, если решение не найдено
    """

    global all_generated, max_depth

    if not stack:
        all_generated = 0
        max_depth = 0

    max_depth = max(max_depth, len(stack))

    if not stack:
        stack = [current_situation]

    # print(len(stack))

    # Проверяем, достигнута ли целевая ситуация
    if current_situation.is_goal_Situation():
        return stack, Statistic(len(stack), max_depth, all_generated)

    # Генерируем все возможные действия (0-13)
    for action in range(13):
        next_situation = make_move(current_situation, action)

        # print(next_situation, action)

        if next_situation in stack:
            continue

        all_generated += 1

        # Если новая ситуация валидна
        if next_situation and next_situation.is_valid():
            result = depth(next_situation, stack + [next_situation])    
            if result:
                return result

    return None  # Решение не найдено