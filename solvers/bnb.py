from typing import List, Optional
from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, make_move
from analyze import Statistic

# Функция поиска с использованием метода ветвей и границ
def bnb(initial_Situation: Situation) -> Optional[List[int]]:
    """
    Функция поиска с использованием метода ветвей и границ (Branch and Bound, BnB) в игре "Волк, коза, капуста, заяц, лиса, человек".

    Берётся начальное состояние и строится дерево с помощью рекурсивной функции,
    где каждый узел - это ситуация, а каждый ребро - это действие,
    которое привело к этому состоянию.

    Алгоритм работает следующим образом:
    1. Инициализируем лучшее решение как None и лучшую стоимость как бесконечность.
    2. Вспомогательная рекурсивная функция explore исследует все возможные пути,
       начиная с начального состояния.
    3. Если текущая стоимость превышает лучшую найденную, прекращаем исследование.
    4. Если достигнуто целевое состояние, обновляем лучшее решение и минимальную стоимость.
    5. Если текущее состояние уже посещено, выходим из функции.
    6. Генерируем все возможные действия (0-12) и рекурсивно вызываем explore
       для следующего состояния.
    7. Удаляем текущее состояние из посещённых после его исследования.
    8. Возвращаем лучшее найденное решение.

    :param initial_Situation: начальная ситуация
    :return: путь, который привёл к целевому состоянию, или None,
             если решение не найдено
    """
    best_solution = None  # Инициализация лучшего решения как None
    best_cost = float("inf")  # Инициализация лучшей стоимости как бесконечность
    visited = set()  # Множество для хранения посещённых состояний
    max_depth = 0
    all_generated = 0

    # Вспомогательная рекурсивная функция для исследования всех возможных путей
    def explore(Situation: Situation, path, cost, depth):
        nonlocal best_solution, best_cost, max_depth, all_generated

        # Если текущая стоимость превышает лучшую найденную, прекращаем исследование
        if cost >= best_cost:
            return

        # Проверяем, достигнуто ли целевое состояние
        if Situation.is_goal_Situation():
            best_solution = path  # Обновляем лучшее решение
            best_cost = cost  # Обновляем минимальную стоимость
            return

        # Если текущее состояние уже посещено, выходим из функции
        if Situation in visited:
            return

        # Добавляем текущее состояние в посещённые
        visited.add(Situation)
        all_generated += 1
        max_depth = max(max_depth, depth)
        # Генерируем все возможные действия
        for action in range(13):
            next_Situation = make_move(Situation, action)

            # Если следующее состояние валидно, продолжаем его исследовать
            if next_Situation and next_Situation.is_valid():
                # Рекурсивно вызываем explore для следующего состояния
                explore(next_Situation, path + [action], cost + 1, depth + 1)

        # Удаляем текущее состояние из посещённых после его исследования
        visited.remove(Situation)

    # Запускаем исследование с начального состояния
    explore(initial_Situation, [], 0, 0)

    if best_solution is not None:
        return best_solution, Statistic(
            len(best_solution), max_depth + 1, all_generated
        )
    else:
        return None