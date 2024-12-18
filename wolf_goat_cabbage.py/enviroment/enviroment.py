from copy import deepcopy
from enum import Enum, Flag, auto

# Определения классов для типизации
# Создание класса для левого и правого берега
class Beach(Enum):
    LEFT = "Левый"
    RIGHT = "Правый"

# Создание класса для определения сущностей
class Object(Flag):
    Wolf = auto()
    Goat = auto()
    Gabbage = auto()

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
            # Волк и коза на одном берегу без лодки - недопустимо
            if (Object.Wolf in side and Object.Goat in side) and (
                Object.Goat not in boat_side
            ):
                return False
            # Коза и капуста на одном берегу без лодки - недопустимо
            if (Object.Goat in side and Object.Gabbage in side) and (
                Object.Goat not in boat_side
            ):
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
        if Object.Gabbage in entities:
            description.append("Капуста")
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
        return self.right.value < other.right.value

    def __hash__(self):
        return hash(self.create_key())


# Сущности
entities = [Object.Wolf, Object.Goat, Object.Gabbage]

# Пораждающая процедура
def make_move(Situation: Situation, action: int):
    Situation = deepcopy(Situation)

    if action < 3:
        # Перевозим с левого берега
        if (
            Situation.Beach == Beach.LEFT
            and entities[action] in Situation.left
            and Situation.boat == Object(0)
        ):

            Situation.left &= ~entities[action]
            Situation.boat = entities[action]
        else:
            return None
    elif action < 6:
        # Перевозим с правого берега
        move_index = action % 3
        if (
            Situation.Beach == Beach.RIGHT
            and entities[move_index] in Situation.right
            and Situation.boat == Object(0)
        ):

            Situation.right &= ~entities[move_index]
            Situation.boat = entities[move_index]
        else:
            return None
    elif action == 6:
        # Перемещаем лодку на противоположный берег
        if Situation.Beach == Beach.LEFT:
            Situation.Beach = Beach.RIGHT
            Situation.right |= Situation.boat
        else:
            Situation.Beach = Beach.LEFT
            Situation.left |= Situation.boat

        # После перемещения лодка пустая
        Situation.boat = Object(0)
    else:
        return None  # Неверный номер действия
    
    return Situation