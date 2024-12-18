from wolf_goat_cabbage_fox_rabbit_human.enviroment import Situation, Beach, Object, make_move
from solvers import dfs_with_prioritize, depth, bfs, ucs, bnb, bidirectional_search, bfs_with_cmp
from analyze import Statistic


def print_header():
    print("##############################################")
    print("# Author: Nikonorov F.S. RGRTU group 343")
    print("# Program: WOLF_GOAT_CABBAGE_FOX_RABBIT_HUMAN")
    print(
        "# The game uses algorithms such as Branch and Bound, Depth-First Search (with and without heuristic), Breadth-first search(with and without heuristic), Uniform Cost Search, Bidirectional Search"
    )
    print("# Version: 18.12.2024")
    print("# Loading...")
    print("##############################################")

if __name__ == "__main__":
    print_header()

    Situation_start= Situation(
        left=Object.Wolf | Object.Goat | Object.Cabbage | Object.Fox | Object.Rabbit | Object.Human,
        right=Object(0),
        boat=Object(0),
        Beach=Beach.LEFT,
    )

    Situation_goal = Situation(
        left=Object(0),
        right=Object.Wolf | Object.Goat | Object.Cabbage | Object.Fox | Object.Rabbit | Object.Human,
        boat=Object(0),
        Beach=Beach.RIGHT,
    )

    solvers = [
        bfs,
        depth,
        dfs_with_prioritize,
        ucs,
        bnb,
        bidirectional_search,
        bfs_with_cmp,
    ]

    solver_names = [
        "Breadth-first search",
        "Depth-first search",
        "DFS with prioritize",
        "Uniform Cost Search",
        "Branch and Bound",
        "Bidirectional search",
        "Breadth-first search with prioritize"
    ]


    statistics = []

    for solver in solvers:
        
        if solver == bidirectional_search:
            _, statistic = solver(Situation_start, Situation_goal)
            statistics.append(statistic)
            continue
        
        _, statistic = solver(Situation_start)
        statistics.append(statistic)

    Statistic.print_statistics(statistics, solver_names)


""" Вывод каждого решателя по отдельности"""

    # # Начальная ситуация: сущности на левом берегу, лодка пуста
    # basic_situation = Situation(
    #     left=Object.Wolf | Object.Goat | Object.Cabbage | Object.Fox | Object.Rabbit | Object.Human,
    #     right=Object(0),
    #     boat=Object(0),
    #     Beach=Beach.LEFT,
    # )
    
    # # Проверка пораждающей процедуры

    # # basic_situation.display()
    # # situation = make_move(basic_situation, 1)
    # # situation.display()
    # # situation = make_move(situation, 13)
    # # situation.display()
        
    # solution = bnb(basic_situation)

    # if solution is None:
    #     print("Решения нет.")
    # else:
    #     print(f"Для решения потребовалось {len(solution)} шагов:")
    #     current_Situation = basic_situation
    #     for idx, action in enumerate(solution, 1):
    #         print(f"Ход {idx}:")
    #         # Вывод когда возвращается масстив ситуаций
    #         # action.display()
    #         # Вывод когда возвращается пусть
    #         current_Situation = make_move(current_Situation, action)
    #         current_Situation.display()
