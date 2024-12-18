from typing import List
from prettytable import PrettyTable, ALL

class Statistic:
    def __init__(self, depth: int, max_depth: int, all_generated: int):
        self.depth = depth
        self.max_depth = max_depth
        self.all_generated = all_generated

    @property
    def branching_factor(self) -> float:
        return self.all_generated / self.depth
    
    @property
    def direction(self) -> float:
        return self.all_generated ** (1 / self.depth)
    
    
    def __str__(self) -> str:
        return f"""Statistic:
        Depth: {self.depth}
        Max depth: {self.max_depth}
        All generated: {self.all_generated}
        Branching factor: {self.branching_factor:.2f}
        Direction: {self.direction:.2f}"""
    
    @staticmethod
    def print_statistics(statistics: List["Statistic"], solver_names: List[str]):
        """
        Выводит таблицу статистики для каждого решателя.
        
        :param statistics: Список объектов Statistic, содержащий статистику для каждого решателя.
        :param solver_names: Список имён решателей, соответствующий каждому объекту Statistic.
        """
        table = PrettyTable(border=True,
                    hrules=ALL,
                    vertical_char="│",
                    horizontal_char="─",
                    junction_char="┼",
                    left_junction_char="├",
                    right_junction_char="┤",
                    top_left_junction_char="┌",
                    top_right_junction_char="┐",
                    top_junction_char="┬",
                    bottom_junction_char="┴",
                    bottom_right_junction_char="┘",
                    bottom_left_junction_char="└",
                    start=0,
                    end=7)
        table.field_names = ["Solver", "Depth", "Max Depth", "All Generated", "Branching Factor", "Direction"]
        
        # Добавляем статистику по каждому решателю в таблицу
        for stat, name in zip(statistics, solver_names):
            table.add_row([
                name,
                stat.depth,
                stat.max_depth,
                stat.all_generated,
                f"{stat.branching_factor:.2f}",
                f"{stat.direction:.2f}"
            ])
        
        # Выводим таблицу
        print(table)
    