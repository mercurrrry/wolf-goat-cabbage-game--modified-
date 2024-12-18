from copy import deepcopy
from enum import Enum, Flag, auto
from typing import List, Optional
from collections import deque

# Определения перечислений и классов
class Coast(Enum):
    LEFT = "Левый"
    RIGHT = "Правый"


class Entity(Flag):
    WOLF = auto()
    GOAT = auto()
    CABBAGE = auto()


class State:
    def __init__(self, left: Entity, right: Entity, boat: Entity, coast: Coast):
        self.left = left  # Левый берег (содержит сущности, находящиеся на левом берегу)
        self.right = (
            right  # Правый берег (содержит сущности, находящиеся на правом берегу)
        )
        self.boat = boat  # Кто находится в лодке
        self.coast = coast  # Текущий берег лодки

    # Функция проверки валидности текущей ситуации
    def is_valid(self):
        # Проверка для каждого берега отдельно
        def check_danger(side, boat_side):
            # Если волк и коза на одном берегу без лодки - опасно
            if (Entity.WOLF in side and Entity.GOAT in side) and (
                Entity.GOAT not in boat_side
            ):
                return False
            # Если коза и капуста на одном берегу без лодки - опасно
            if (Entity.GOAT in side and Entity.CABBAGE in side) and (
                Entity.GOAT not in boat_side
            ):
                return False
            return True

        if self.coast == Coast.LEFT:
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

    # Функция для отображения текущего состояния игры
    def display(self):
        # Левый берег
        print(f"Левый берег: {self.describe(self.left)}")
        # Правый берег
        print(f"Правый берег: {self.describe(self.right)}")
        # Лодка и текущий берег
        print(f"Лодка: {self.describe(self.boat)}")
        print(f"Берег лодки: {self.coast.value}")
        print("-" * 50)

    # Вспомогательная функция для описания сущностей на берегах и в лодке
    def describe(self, entities):
        description = []
        if Entity.WOLF in entities:
            description.append("Волк")
        if Entity.GOAT in entities:
            description.append("Коза")
        if Entity.CABBAGE in entities:
            description.append("Капуста")
        return ", ".join(description) if description else "Пусто"

    # Проверка на победу (все перевезены на правый берег)
    def is_goal_state(self):
        # Если все сущности находятся на правом берегу и лодка тоже на правом
        return (
            self.left == Entity(0)
            and self.boat == Entity(0)
            and self.coast == Coast.RIGHT
        )

    # Генерация уникального ключа состояния для отслеживания посещённых состояний
    def get_key(self):
        return (self.left, self.right, self.boat, self.coast)

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash(self.get_key())


# Сущности
entities = [Entity.WOLF, Entity.GOAT, Entity.CABBAGE]

# Пораждающая процедура
def make_move(state: State, action: int) -> Optional[State]:
    state = deepcopy(state)

    if action < 3:
        # Перевозим с левого берега
        if (
            state.coast == Coast.LEFT
            and entities[action] in state.left
            and state.boat == Entity(0)
        ):

            state.left &= ~entities[action]
            state.boat = entities[action]
        else:
            return None
    elif action < 6:
        # Перевозим с правого берега
        move_index = action % 3
        if (
            state.coast == Coast.RIGHT
            and entities[move_index] in state.right
            and state.boat == Entity(0)
        ):

            state.right &= ~entities[move_index]
            state.boat = entities[move_index]
        else:
            return None
    elif action == 6:
        # Перемещаем лодку на противоположный берег
        if state.coast == Coast.LEFT:
            state.coast = Coast.RIGHT
            state.right |= state.boat
        else:
            state.coast = Coast.LEFT
            state.left |= state.boat

        # После перемещения лодка пустая
        state.boat = Entity(0)
    else:
        return None  # Неверный номер действия

    return state


def dfs(initial_state: State) -> Optional[List[int]]:
    visited = set() # Храним все посещённые состояния
    stack = [(initial_state, [])]  # Каждый элемент: (текущее состояние, путь действий)

    while stack:
        current_state, path = stack.pop()

        # Проверяем, достигнуто ли целевое состояние
        if current_state.is_goal_state():
            return path

        # Добавляем текущее состояние в посещённые
        visited.add(current_state.get_key())

        # Генерируем все возможные действия (0-6)
        for action in range(7):
            next_state = make_move(current_state, action)

            # Если новое состояние валидно и не посещено ранее
            if (
                next_state
                and next_state.is_valid()
                and next_state.get_key() not in visited
            ):
                # Добавляем новое состояние в стек с обновлённым путём
                stack.append((next_state, path + [action]))

    return None  # Решение не найдено


if __name__ == "__main__":
    # Начальное состояние: все на левом берегу, лодка на левом берегу, лодка пуста
    initial_state = State(
        left=Entity.WOLF | Entity.GOAT | Entity.CABBAGE,
        right=Entity(0),
        boat=Entity(0),
        coast=Coast.LEFT,
    )

    print("Начальное состояние:")
    initial_state.display()

    solution = dfs(initial_state)

    if solution is None:
        print("Решение не найдено.")
    else:
        print(f"Найдено решение за {len(solution)} шагов:")
        current_state = initial_state
        for idx, action in enumerate(solution, 1):
            print(f"Ход {idx}:")
            current_state = make_move(current_state, action)
            current_state.display()
        print("Целевое состояние достигнуто!")