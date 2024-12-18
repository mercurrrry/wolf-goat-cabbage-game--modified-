from copy import deepcopy
from enum import Enum, Flag, auto
from typing import List, Optional
from collections import deque
from functools import cmp_to_key

# Определения классов для типизации
# Создание класса для левого и правого берега
class Beach(Enum):
    LEFT = "Левый"
    RIGHT = "Правый"

# Создание класса для определения сущностей
class Object(Flag):
    Wolf = auto()
    Goat = auto()
    Cabbage = auto()
    Rabbit = auto()
    Fox = auto()
    Human = auto()

# Создаю класс для описания ситуаций
class Situation:
    def __init__(self, left: Object, right: Object, boat: Object, Beach: Beach):
        self.left = left  # Задание левого берега - внутри объекты которые на левом берегу
        self.right = (
            right  # Задание правого берега - внутри объекты которые на правом берегу
        )
        self.boat = boat  # Кто находится в лодке
        self.Beach = Beach  # Текущий берег на котором находится лодка

    # Проверка валидности текущей ситуации
    def is_valid(self):
        # Проверка для каждого берега отдельно
        def check_danger(side, boat_side):
            if (Object.Wolf in side and Object.Goat in side) \
                and (Object.Goat not in boat_side) \
                    and (Object.Human not in side):
                return False
            
            if (Object.Goat in side and Object.Cabbage in side) \
                and (Object.Goat not in boat_side) \
                    and (Object.Human not in side):
                return False
            
            if (Object.Rabbit in side and Object.Fox in side) \
                and (Object.Rabbit not in boat_side) \
                    and (Object.Human not in side):
                return False

            return True


        if self.Beach == Beach.LEFT:
            boat_side = self.left
        else:
            boat_side = self.right

        # Проверяем левый берег
        if not check_danger(self.left, boat_side):
            return False
        # Проверяем правый берег
        if not check_danger(self.right, boat_side):
            return False

        return True

    # Функция для отображения игры
    def display(self):
        # Левый берег
        print(f"Сущности на левом берегу: {self.describe(self.left)}")
        # Правый берег
        print(f"Сущности на правом берегу: {self.describe(self.right)}")
        # Лодка и текущий берег
        print(f"Сущности в лодке: {self.describe(self.boat)}")
        print(f"Берег на котором находится лодка: {self.Beach.value}")
        print("_" * 50)

    # Вспомогательная функция для описания сущностей на берегах и в лодке
    def describe(self, entities):
        description = []
        if Object.Wolf in entities:
            description.append("Волк")
        if Object.Goat in entities:
            description.append("Коза")
        if Object.Cabbage in entities:
            description.append("Капуста")
        if Object.Rabbit in entities:
            description.append("Кролик")
        if Object.Fox in entities:
            description.append("Лиса")
        if Object.Human in entities:
            description.append("Человек")
        return ", ".join(description) if description else "Пусто"

    # Проверка на победу (все перевезены на правый берег)
    def is_goal_Situation(self):
        # Если все сущности находятся на правом берегу и лодка тоже на правом
        return (
            self.left == Object(0)
            and self.boat == Object(0)
            and self.Beach == Beach.RIGHT
        )

    # Генерация уникального ключа состояния для отслеживания посещённых состояний
    def create_key(self):
        return (self.left, self.right, self.boat, self.Beach)

    def __eq__(self, other):
        if not isinstance(other, Situation):
            return False
        return self.create_key() == other.create_key()
    
    
    def __lt__(self, other):
        return self.left.value < other.right.value

    def __hash__(self):
        return hash(self.create_key())


# Сущности
entities = [Object.Wolf, Object.Goat, Object.Cabbage, Object.Fox, Object.Rabbit, Object.Human]

# Пораждающая процедура
def make_move(situation: Situation, action: int):
    situation = deepcopy(situation)

    if action < 6:
        if (
            situation.Beach == Beach.LEFT
            and entities[action] in situation.left
            and situation.boat == Object(0)
        ):
            situation.left &= ~entities[action]
            situation.boat = entities[action]
        else:
            return None
    elif action < 12:
        move_index = action % 6
        if (
        situation.Beach == Beach.RIGHT
        and entities[move_index] in situation.right
        and situation.boat == Object(0)
        ):
            situation.right &= ~entities[move_index]
            situation.boat = entities[move_index]
        else:
            return None
    elif action == 12:
        if situation.Beach == Beach.LEFT:
            situation.Beach = Beach.RIGHT
            situation.right |= situation.boat
        else:
            situation.Beach = Beach.LEFT
            situation.left |= situation.boat
        situation.boat = Object(0)
    else:
        return None
    
    return situation

def depth(current_situation, stack = []):
    
    """
    Функция поиска решения в игре волк коза капуста с использованием алгоритма поиска в глубину (DFS).

    :param initial_situation: начальная ситуация
    :return: массив ситуаций, приводящих к цели, или None, если решение не найдено
    """

    if not stack:
        stack = [current_situation]

    # print(len(stack))

    # Проверяем, достигнута ли целевая ситуация
    if current_situation.is_goal_Situation():
        return stack

    # Генерируем все возможные действия (0-13)
    for action in range(13):
        next_situation = make_move(current_situation, action)

        # print(next_situation, action)

        if next_situation in stack:
            continue

        # Если новая ситуация валидна
        if next_situation and next_situation.is_valid():
            result = depth(next_situation, stack + [next_situation])    
            if result:
                return result

    return None  # Решение не найдено

def dfs_with_prioritize(current_situation, stack = []):
    """
    Функция поиска решения в игре волк коза капуста с использованием алгоритма поиска в глубину (DFS)
    с приоритетом действий.

    :param initial_situation: начальная ситуация
    :return: список действий, приводящих к цели, или None, если решение не найдено
    """
    if not stack:
        stack = [current_situation]

    # Проверяем, достигнута ли целевая ситуация
    if current_situation.is_goal_Situation():
        return stack
    
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

        # Если новая ситуация валидна
        if next_situation and next_situation.is_valid():
            result = dfs_with_prioritize(next_situation, stack + [next_situation])    
            if result:
                return result

    return None  # Решение не найдено


# Функция поиска в ширину
def bfs(initial_Situation: Situation) -> Optional[List[int]]:
    """
    Поиск в ширину (Breadth-First Search) в игре "Волк, коза и капуста".
    
    :param initial_situation: начальное ситуация 
    :return: список действий, приводящий к целевой ситуации, или None, если решение не найдено
    """
    visited = set()  # Храним все посещённые состояния
    queue = deque([(initial_Situation, [])])  # Каждый элемент: (текущее состояние, путь действий)
    
    while queue:
        current_Situation, path = queue.popleft()

        # Проверяем, достигнуто ли целевое состояние
        if current_Situation.is_goal_Situation():
            return path

        # Пропускаем, если это состояние уже было посещено
        if current_Situation.create_key() in visited:
            continue

        # Добавляем текущее состояние в посещённые
        visited.add(current_Situation.create_key())

        # Генерируем все возможные действия (0-13)
        for action in range(13):
            next_Situation = make_move(current_Situation, action)

            # Если новое состояние валидно и не посещено ранее
            if (
                next_Situation
                and next_Situation.is_valid()
                and next_Situation.create_key() not in visited
            ):
                # Добавляем новое состояние в очередь с обновлённым путём
                queue.append((next_Situation, path + [action]))

    return None

if __name__ == "__main__":
    # Начальная ситуация: сущности на левом берегу, лодка пуста
    basic_situation = Situation(
        left=Object.Wolf | Object.Goat | Object.Cabbage | Object.Fox | Object.Rabbit | Object.Human,
        right=Object(0),
        boat=Object(0),
        Beach=Beach.LEFT,
    )
    
    # Проверка пораждающей процедуры
    # basic_situation.display()
    # situation = make_move(basic_situation, 1)
    # situation.display()
    # situation = make_move(situation, 13)
    # situation.display()
        
    solution = dfs_with_prioritize(basic_situation)

    if solution is None:
        print("Решения нет.")
    else:
        print(f"Для решения потребовалось {len(solution)} шагов:")
        current_Situation = basic_situation
        for idx, action in enumerate(solution, 1):
            print(f"Ход {idx}:")
            action.display()
            # current_Situation = make_move(current_Situation, action)
            # current_Situation.display()
