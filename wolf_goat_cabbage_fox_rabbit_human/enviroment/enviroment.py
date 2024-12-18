from copy import deepcopy
from enum import Enum, Flag, auto
from typing import List, Optional

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

def make_move_for_ucs(situation: Situation, action: int):
    return make_move(situation, action), action