import naive_algorithm as naive
import improved_algorithm as improved
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from copy import deepcopy


def create_people_list(number_of_floors: int, population: int):
    people_list = improved.generate_people(number_of_floors, population)

    return people_list


def get_stats_for_both(number_of_floors: int, population: int):
    people_list = create_people_list(number_of_floors, population)

    number_of_floors_n, life_steps_n, total_wait_n, total_time_naive_n, max_people_n, avg_wait_n, avg_in_lift_n = \
        naive.naive_lift_algorithm(number_of_floors, deepcopy(people_list), True)

    number_of_floors_i, life_steps_i, total_wait_i, total_time_naive_i, max_people_i, avg_wait_i, avg_in_lift_i = \
        improved.better_lift_algorithm(number_of_floors, population, deepcopy(people_list))

    print(number_of_floors_n, life_steps_n, total_wait_n, total_time_naive_n, max_people_n, avg_wait_n, avg_in_lift_n)
    print(number_of_floors_i, life_steps_i, total_wait_i, total_time_naive_i, max_people_i, avg_wait_i, avg_in_lift_i)


def both_graphs():
    lower_limit = 21
    upper_limit = 50
    avg_wait_array_n = []
    number_floor_array_n = []

    avg_wait_array_i = []
    number_floor_array_i = []

    for simulation in range(lower_limit, upper_limit + 1, 1):
        people_list = create_people_list(simulation, simulation * 3)

        number_of_floors_n, life_steps, total_wait, total_time_naive, max_people, avg_wait_n, avg_in_lift = \
            naive.naive_lift_algorithm(simulation, deepcopy(people_list), True)

        avg_wait_array_n.append(avg_wait_n)
        number_floor_array_n.append(simulation)

        number_of_floors_i, life_steps, total_wait, total_time_naive, max_people, avg_wait_i, avg_in_lift = \
            improved.better_lift_algorithm(simulation, simulation * 3, deepcopy(people_list))

        avg_wait_array_i.append(avg_wait_i)
        number_floor_array_i.append(simulation)

    print(avg_wait_array_n)
    print(avg_wait_array_i)
    print(number_floor_array_n)
    print(number_floor_array_i)

    plt.plot(number_floor_array_i, avg_wait_array_i, "bx")
    plt.xlabel("Number of Floors")
    plt.title("Number of Floors against Average Wait Time for the Better Algorithm")
    plt.ylabel("Average Wait Time")
    plt.axis([21, 50, 0, 1000])
    coefficients = np.polyfit(number_floor_array_i, avg_wait_array_i, 1)
    best_fit = np.poly1d(coefficients)
    plt.plot(number_floor_array_i, best_fit(number_floor_array_i), "r")
    plt.savefig("better_algo_150_people")
    plt.show()

    plt.plot(number_floor_array_n, avg_wait_array_n, "bx")
    plt.xlabel("Number of Floors")
    plt.title("Number of Floors against Average Wait Time for the Naïve Algorithm")
    plt.ylabel("Average Wait Time")
    plt.axis([21, 50, 0, 1000])
    coefficients = np.polyfit(number_floor_array_n, avg_wait_array_n, 1)
    best_fit = np.poly1d(coefficients)
    plt.plot(number_floor_array_n, best_fit(number_floor_array_n), "r")
    plt.savefig("naive_algo_150_people")
    plt.show()


if __name__ == '__main__':
    get_stats_for_both(72, 2160)