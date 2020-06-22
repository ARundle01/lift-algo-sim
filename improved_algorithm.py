"""
This module simulates an improved algorithm for a single car
lift system. Each lift has a capacity of 6 people, with the
simulation animating any scenario up to 20 floors. Any higher
and the information will be relayed textually.

Created by 690037391
01/2020 - 04/2020
"""

# ====================
# Imports found below
# ====================

import random
from copy import deepcopy
from typing import Union
import pygame
import animation as animate


# ========================
# Class definitions below
# ========================

class Person:
    """
    The Person class models a real life passenger of a lift.

    :param int current_floor: The current floor of the person.
    :param str direction_to_move: The direction in which the person is to move.
    :param int target_floor: The floor which the person is to get off on.

    """

    def __init__(self, current_floor: int, direction_to_move: str,
                 target_floor: int):
        """ Person Constructor. """
        self.start_floor = current_floor
        self.direction_to_move = direction_to_move
        self.target_floor = target_floor

        self.wait_time = 0
        self.time_in_lift = 0
        self.current_state = "waiting"
        self.all_states = ["waiting", "in lift", "arrived"]

    def get_target_floor(self) -> int:
        """
        Returns the target floor.

        :return: The floor on which the person will get off.
        :rtype: int
        """
        return self.target_floor

    def get_wait_time(self) -> int:
        """
        Returns the wait_time of person.

        :return: The amount of time spent waiting for lift.
        :rtype: int
        """
        return self.wait_time

    def get_time_in_lift(self) -> int:
        """
        Returns the time_in_lift of person.

        :return: The amount of time spent in the lift
        :rtype: int
        """
        return self.time_in_lift

    def increase_wait_time(self):
        """ Increments the wait time by one. """
        self.wait_time += 1

    def increase_time_in_lift(self):
        """ Increments time in lift by one. """
        self.time_in_lift += 1

    def change_state(self, new_state: str):
        """
        Changes the current state of a person.

        :param str new_state: The new state that the person will change to.
        """
        if new_state in self.all_states:
            self.current_state = new_state

    def get_in_lift(self):
        """ Sets state to in lift. """
        self.change_state("in lift")
        print("Got in lift at", self.start_floor)

    def get_out_of_lift(self):
        """ Sets state to arrived. """
        self.change_state("arrived")
        print("Arrived at floor", self.target_floor, "from floor", self.start_floor)


class Lift:
    """
    Represents the lift.

    :param int number_of_floors: The total number of floors in the building.
    """

    def __init__(self, number_of_floors: int):
        """ Lift Constructor. """
        self.current_floor = 1
        self.total_floors = number_of_floors
        self.minimum_floor = 1
        self.top_floor = self.total_floors
        self.bottom_floor = 1
        self.all_states = ["up", "down"]
        self.current_state = "up"
        self.capacity = 6
        self.people_in_lift = []
        self.lifetime_steps = 0
        self.time_switched = 0

    def set_current_state(self, new_state: str):
        """
        Sets the current state (either up or down).

        :param str new_state: The new state that the lift will change to.
        """
        if new_state in self.all_states:
            self.current_state = new_state

    def move_by_one_floor(self, direction: str):
        """
        Moves the lift by one floor in a given direction.

        :param str direction: The direction in which the lift will move.
        """
        if direction == "up":
            self.current_state = direction
            self.current_floor += 1
        elif direction == "down":
            self.current_state = direction
            self.current_floor -= 1

    def check_if_at_top(self) -> bool:
        """
        Checks if the lift is at the top floor.

        :return: Whether the lift as at the top.
        :rtype: bool
        """
        if self.current_floor == self.total_floors:
            return True
        else:
            return False

    def check_if_at_bottom(self) -> bool:
        """
        Checks if the lift is at the bottom floor.

        :return: Whether the lift is at the bottom.
        :rtype: bool
        """
        if self.current_floor == self.bottom_floor:
            return True
        else:
            return False

    def move_lift_up(self):
        """ Moves the lift one floor up. """
        self.set_current_state("up")
        self.move_by_one_floor("up")

    def move_lift_down(self):
        """ Moves the lift one floor down. """
        self.set_current_state("down")
        self.move_by_one_floor("down")

    def add_person_to_lift(self, person: Person):
        """
        Adds a given person to the lift.

        :param Person person: The person that will be added to the lift.
        """
        self.people_in_lift.append(person)
        self.capacity -= 1

    def remove_person_from_lift(self, person: Person):
        """
        Removes a given person from the lift.

        :param Person person: The person that will be removed from the lift.
        """
        for people in self.people_in_lift:
            if people == person:
                self.people_in_lift.remove(people)
                self.capacity += 1

    def get_current_capacity(self) -> int:
        """
        Returns the current capacity of the lift.

        :return: The current capacity of the lift.
        :rtype: int
        """
        return self.capacity

    def switch_direction(self):
        """ Changes the lift direction to the opposite. """
        if self.current_state == "up":
            self.current_state = "down"
        elif self.current_state == "down":
            self.current_state = "up"

    def check_if_empty(self) -> bool:
        """
        Checks if the lift is empty.

        :return: Whether the lift is empty.
        :rtype: bool
        """
        if self.capacity == 6:
            return True
        else:
            return False

    def increment_lifetime_steps(self):
        """ Increments the lifetime steps of the lift. """
        self.lifetime_steps += 1


# ================
# Functions below
# ================

def initialize_animation(number_of_floors: int):
    """
    Initializes the animation of the lift.

    :param int number_of_floors: The total number of floors in the building.

    :return: Variables used in animation of lift.
    :rtype: Union[int, Canvas, Clock, tuple]
    """
    canvas_x, canvas_y = animate.calc_canvas_size(number_of_floors)
    lift_width, lift_height = animate.calc_elevator_size(number_of_floors)
    canvas = animate.canvas_init(canvas_x, canvas_y)
    clock = pygame.time.Clock()
    lift_x_coord = (canvas_x - lift_width) // 2
    lift_y_coord = canvas_y - (lift_height + 10)
    lift_colour = (60, 69, 82)

    return \
        canvas_x, canvas_y, lift_width, lift_height, canvas, \
        clock, lift_x_coord, lift_y_coord, lift_colour


def generate_people(number_of_floors: int, number_of_people: int) -> list:
    """
    Creates a set number of people on random floors, with random
    target floors.

    :param int number_of_floors: The total number of floors.
    :param int number_of_people: The total number of people.
    :return: An array containing Person objects.
    :rtype: list
    """
    list_of_people = []

    for person in range(number_of_people):
        random_floor = random.randint(1, number_of_floors)

        if random_floor == number_of_floors:
            random_direction = "down"
        elif random_floor == 1:
            random_direction = "up"
        else:
            random_direction = random.choice(["up", "down"])

        if random_direction == "up":
            random_target = random.randint(random_floor + 1, number_of_floors)
        elif random_direction == "down":
            random_target = random.randint(1, random_floor - 1)

        list_of_people.append(
            Person(random_floor, random_direction, random_target))

    return list_of_people


def create_people_occurrence_list(people_list: list) -> list:
    """
    Creates an array containing dictionaries. Dictionaries contain floor number
    and how many people at that floor.

    :param list people_list: Array of all people in building.

    :return: An array of dictionaries that contains floor number and people on floor.
    :rtype: list
    """

    # Init empty lists and dicts.
    list_of_floors = []
    floor_occurrence_list = []
    floor_occurrence = {}

    # For every person in the list, add their start floor to the list.
    for person in people_list:
        list_of_floors.append(person.start_floor)

    # For every floor in the list of floors, count how many times that
    # floor occurs.
    # Create a dictionary mapping floor number to number of occurrences.
    # Finally, some floors are double counted. Iterate through, adding dicts
    # not in the final list to it, erasing double counts.
    for floor in list_of_floors:
        no_of_floor = list_of_floors.count(floor)
        floor_occurrence["floor_number"] = floor
        floor_occurrence["occurrences"] = no_of_floor

        floor_occurrence_list.append(deepcopy(floor_occurrence))

    final_list_occurrences = []
    for occurrence in floor_occurrence_list:
        if occurrence not in final_list_occurrences:
            final_list_occurrences.append(occurrence)

    return final_list_occurrences


def update_occurrence_list(occurrence_list: list, floor_number: int):
    """
    Updates the occurrence array with the current number of
    people on each floor.

    :param list occurrence_list: Number of people on each floor as an array of dictionaries.
    :param int floor_number: The floor which is being updated.
    """
    for floor in occurrence_list:
        if floor["floor_number"] == floor_number:
            floor["occurrences"] = floor["occurrences"] - 1

        if floor["occurrences"] == 0:
            occurrence_list.remove(floor)

    return occurrence_list


def draw_people_on_floor(canvas, no_floors: int, lift_height: int,
                         lift_x_coord: int, occurrence_array: list):
    """
    Counts the number of people on each floor and draws it onto the animation.

    :param Canvas canvas: The canvas onto which animation is done.
    :param int no_floors: The total number of floors.
    :param int lift_height: The height in pixels of the lift.
    :param int lift_x_coord: The X coordinate of the upper left corner of the lift.
    :param list occurrence_array: Number of people on each floor as an array of dictionaries.
    """
    text_font = pygame.font.SysFont('comicsansms', 30)

    for person in occurrence_array:
        floor_number = int(person["floor_number"])
        people_on_floor = str(person["occurrences"])

        text_surface = text_font.render(people_on_floor, True, (0, 0, 0))
        text_rectangle = text_surface.get_rect()
        if lift_height == 60:
            text_rectangle_x = lift_x_coord + 80
        elif lift_height == 40:
            text_rectangle_x = lift_x_coord + 60
        else:
            text_rectangle_x = lift_x_coord + 50

        if floor_number == no_floors:
            text_rectangle_y = 10 + (lift_height // 2)
        elif floor_number == 1:
            text_rectangle_y = \
                (
                        20 + (no_floors * lift_height) + ((no_floors - 1) * 3)
                ) - (10 + (lift_height // 2))
        else:
            text_rectangle_y = \
                (
                        (12 + lift_height) +
                        (
                                (no_floors - floor_number) * (lift_height + 3)
                        )
                ) - 2 - (lift_height // 2)

        text_rectangle.center = (text_rectangle_x, text_rectangle_y)
        canvas.blit(text_surface, text_rectangle)


def check_ahead(occurrence_array: list, lift: Lift) -> bool:
    """
    Checks if there is anyone that needs to be collected in the current direction the lift is travelling.

    :param list occurrence_array: Number of people on each floor as an array of dictionaries.
    :param Lift lift: The Lift object that is being used.

    :return: Whether there are people ahead that need picking up.
    :rtype: bool
    """
    if lift.current_state == "up":
        if lift.check_if_at_top():
            return False
        else:
            for floor in occurrence_array:
                if floor["floor_number"] > lift.current_floor:
                    return True
                elif floor["floor_number"] < lift.current_floor:
                    continue
                else:
                    return False

    elif lift.current_state == "down":
        if lift.check_if_at_bottom():
            return False
        else:
            for floor in occurrence_array:
                if floor["floor_number"] < lift.current_floor:
                    return True
                elif floor["floor_number"] > lift.current_floor:
                    continue
                else:
                    return False


def check_passengers(lift: Lift) -> bool:
    """
    Checks if anyone in the lift needs to continue in the current direction the lift is travelling.

    :param Lift lift: The Lift object that is being used.

    :return: Whether there is anyone in the lift that needs to be delivered in the current direction.
    :rtype: bool
    """
    for people in lift.people_in_lift:
        people: Person
        if lift.current_state == "up":
            if lift.check_if_at_top():
                return False
            elif people.target_floor > lift.current_floor:
                return True
            elif people.target_floor < lift.current_floor:
                continue
            else:
                return False
        elif lift.current_state == "down":
            if lift.check_if_at_bottom():
                return False
            elif people.target_floor < lift.current_floor:
                return True
            elif people.target_floor > lift.current_floor:
                continue
            else:
                return False


def increment_all_waiting(people_list: list):
    """
    Increments the time spent waiting for all people currently waiting.

    :param List people_list: All people in the building.
    """
    for people in people_list:
        if people.current_state == "waiting":
            people.increase_wait_time()


def increment_all_in_lift(people_list: list):
    """
    Increments the time spent in lift for all people in the lift currently.

    :param List people_list: All people in the building.
    """
    for people in people_list:
        if people.current_state == "in lift":
            people.increase_time_in_lift()


def get_all_waiting(people_list: list) -> int:
    """
    Returns the total steps spent waiting.

    :param list people_list: All people in the building.

    :return: The total steps spent by all Person objects waiting.
    :rtype: int
    """
    total_wait = 0
    for people in people_list:
        people: Person
        if people.current_state == "arrived":
            total_wait += people.get_wait_time()

    return total_wait


def get_all_in_lift(people_list: list) -> int:
    """
    Returns the total number of steps spent in the lift.

    :param list people_list: All people in the building.

    :return: The total steps spent by all Person objects in the lift
    :rtype: int
    """
    total_in_lift = 0
    for people in people_list:
        people: Person
        if people.current_state == "arrived":
            total_in_lift += people.get_time_in_lift()

    return total_in_lift


def better_lift_algorithm(number_of_floors: int, number_of_people: int,
                          list_of_people: list = None):
    """
    The main decision algorithm for improved lift.

    :param int number_of_floors: The total number of floors in the building.
    :param int number_of_people: The total number of people in the building.
    :param list list_of_people: The list of all people in the building, defaults to None if no array is present.
    """
    # Initialize animation if number of floors is less than 20.
    if number_of_floors <= 20:
        canvas_x, canvas_y, lift_width, lift_height, canvas, clock, lift_x_coord, lift_y_coord, lift_colour = \
            initialize_animation(number_of_floors)

    # Initialize the lift.
    lift = Lift(number_of_floors)

    # If an array is not present, create one.
    if list_of_people is None:
        list_of_people = generate_people(number_of_floors, number_of_people)
    else:
        list_of_people = list_of_people

    # Create the occurrence array.
    occurrence_list = create_people_occurrence_list(list_of_people)

    is_done = False
    max_people = len(list_of_people)
    people_arrived = []

    # Loop terminates when no people are left or when is_done is True.
    while list_of_people and not is_done:
        # Below condition allows for window to terminate if QUIT event is sent.
        if number_of_floors <= 20:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_done = True

        # For every person in building, iterate.
        for people in list_of_people:
            people: Person
            people.increase_wait_time()

            # If they are waiting, on same floor as lift,
            # going in the same direction and there is space,
            # add them to the lift.
            if people.current_state == "waiting":
                if people.start_floor == lift.current_floor:
                    if people.direction_to_move == lift.current_state:
                        if lift.get_current_capacity() != 0:
                            lift.add_person_to_lift(people)
                            people.get_in_lift()
                            list_of_people.remove(people)
                            occurrence_list = update_occurrence_list(occurrence_list, lift.current_floor)

        # For every person in the lift, iterate.
        for people in lift.people_in_lift:
            people: Person
            people.increase_time_in_lift()

            # If lift is on a person's target floor, they get off the lift.
            if people.target_floor == lift.current_floor:
                people.get_out_of_lift()
                lift.remove_person_from_lift(people)
                people_arrived.append(people)

        # If there are still people in the same direction as the lift.
        if check_ahead(occurrence_list, lift):

            # If lift is going up, move up, animate movement and reset lift switch counter.
            if lift.current_state == "up":
                lift.move_lift_up()
                lift.increment_lifetime_steps()
                if number_of_floors <= 20:
                    lift_y_coord -= (lift_height + 3)
                    lift.time_switched = 0

            # If lift is going down, move down, animate movement and reset lift switch counter.
            elif lift.current_state == "down":
                lift.move_lift_down()
                lift.increment_lifetime_steps()
                if number_of_floors <= 20:
                    lift_y_coord += (lift_height + 3)
                    lift.time_switched = 0

        # If there are no people in same direction.
        else:

            # Check if people in lift need to go in current direction.
            if check_passengers(lift):

                # If lift is going up, move up, animate movement and reset lift switch counter.
                if lift.current_state == "up":
                    lift.move_lift_up()
                    lift.increment_lifetime_steps()
                    if number_of_floors <= 20:
                        lift_y_coord -= (lift_height + 3)
                        lift.time_switched = 0

                # If lift is going down, move down, animate movement and reset lift switch counter.
                elif lift.current_state == "down":
                    lift.move_lift_down()
                    lift.increment_lifetime_steps()
                    if number_of_floors <= 20:
                        lift_y_coord += (lift_height + 3)
                        lift.time_switched = 0

            # Finally, if there is no in or out of lift to go in that direction,
            # turn the other direction and repeat.
            else:
                lift.switch_direction()
                lift.time_switched += 1

        # If the number of floors is 20 or less, animate the lift.
        #
        # This is done to prevent the animation from leaving the
        # physical bounds of the screen.
        if number_of_floors <= 20:
            animate.draw_white_bg(canvas)
            animate.draw_building_lines(canvas, number_of_floors, lift_width, lift_height, lift_x_coord)
            draw_people_on_floor(canvas, number_of_floors, lift_height, lift_x_coord, occurrence_list)
            pygame.draw.rect(canvas, lift_colour, pygame.Rect(lift_x_coord, lift_y_coord, lift_width, lift_height))
            pygame.display.flip()
            clock.tick(number_of_floors)

            # If the number of direction switches is more than 5,
            # terminate the animation.
            #
            # The lift should never switch more than a few times,
            # unless there is no one left in the building to serve.
            if lift.time_switched > 5:
                is_done = True

        if lift.time_switched > 5:
            is_done = True

    # Calculate the stats for simulation and print.
    total_wait = get_all_waiting(people_arrived)
    if total_wait == 0:
        total_wait = 1

    avg_wait = total_wait // max_people
    if avg_wait == 0:
        avg_wait = 1

    life_steps = lift.lifetime_steps

    total_in_lift = get_all_in_lift(people_arrived)
    if total_in_lift == 0:
        total_in_lift = 1

    avg_in_lift = total_in_lift // max_people
    if avg_in_lift == 0:
        avg_in_lift = 1

    print("Number of Floors:", number_of_floors, "floors.")
    print("Lifetime steps for lift:", life_steps, "steps.")
    print("Total Time Waiting for Lift:", total_wait, "steps.")
    print("Total Time in Lift:", total_in_lift, "steps.")
    print("Number of People:", max_people, "people.")
    print("Average Wait Time:", avg_wait, "steps per person.")
    print("Average Time in Lift:", avg_in_lift, "steps per person.")
    pygame.quit()

    return number_of_floors, life_steps, total_wait, total_in_lift, max_people, avg_wait, avg_in_lift
