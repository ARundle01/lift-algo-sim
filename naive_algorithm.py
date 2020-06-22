import random
from copy import deepcopy
import pygame
import animation as animate
from typing import Union

total_time_naive = 0
total_time_better = 0


class Person:
    """
    Represents a passenger in the lift.

    :param int current_floor: The current floor that the person is on.
    :param str direction_to_move: The direction in which the person will move.
    :param int target_floor: The floor on which the person will exit the lift.
    """

    def __init__(self, current_floor: int, direction_to_move: str, target_floor: int):
        """ Person constructor. """
        self.start_floor = current_floor
        self.direction_to_move = direction_to_move
        self.target_floor = target_floor

        self.wait_time = 0
        self.time_in_lift = 0
        self.current_state = "waiting"
        self.all_states = ["waiting", "in lift", "arrived"]

    def get_target_floor(self) -> int:
        """
        Returns the target floor of a person.

        :return: The floor on which the person will get off the lift.
        :rtype: int
        """

        return self.target_floor

    def get_wait_time(self) -> int:
        """
        Returns the wait time of person.

        :return: The time spent waiting for the lift.
        :rtype: int
        """

        return self.wait_time

    def get_time_in_lift(self) -> int:
        """
        Returns the time_in_lift of person.

        :return: The time spent in the lift.
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
        Change the current_state to a given state.

        :param str new_state: The new state that is to be changed to.
        """

        if new_state in self.all_states:
            self.current_state = new_state

    def get_in_lift(self):
        """ Changes the current state to in lift. """

        self.change_state("in lift")
        print("Got in lift at", self.start_floor)

    def get_out_of_lift(self):
        """ Changes the current state to arrived. """

        self.change_state("arrived")
        print("Arrived at floor", self.target_floor, "from floor", self.start_floor)


class NaiveLift:
    """
    Defines the lift used in the Naive Lift Algorithm.

    :param int number_of_floors: The total number of floors in the building.
    :param list all_people: All people in the building.
    :param int current_floor: The current floor the lift is on.
    :param str current_direction: The current direction the lift is moving in.
    """

    def __init__(self, number_of_floors: int, all_people: list, current_floor: int = 1, current_direction: str = "up"):
        self.current_floor: int = current_floor
        self.current_direction: str = current_direction
        self.bottom_floor: int = 1
        self.top_floor: int = number_of_floors
        self.lifetime_steps: int = 0
        self.people_in_lift: list = []
        self.all_people: list = all_people
        self.capacity = 6

    def add_people_to_lift(self, person):
        """
        Adds a given person to the lift.

        :param Person person: The person that is to be added to the lift.
        """

        self.people_in_lift.append(person)
        self.decrease_capacity()

    def remove_people_from_lift(self, person):
        """
        Removes a given person from the lift.

        :param Person person: The person that is to be removed from the lift.
        """

        for index in self.people_in_lift:
            if index == person:
                self.people_in_lift.remove(index)
                self.increase_capacity()

    def change_directions(self):
        """ Changes the direction of travel of the lift. """

        if self.current_floor == self.bottom_floor:
            self.current_direction = "up"
        elif self.current_floor == self.top_floor:
            self.current_direction = "down"

    def move_lift_by_one_floor(self):
        """ Moves the lift in current direction by one floor. """

        if self.current_direction == "up":

            if self.current_floor == self.top_floor:
                self.change_directions()
                self.current_floor -= 1
                self.increment_lifetime_steps()

                if self.top_floor <= 20:
                    print("Currently on floor", self.current_floor, "moving", self.current_direction)

            else:
                self.current_floor += 1
                self.increment_lifetime_steps()

                if self.top_floor <= 20:
                    print("Currently on floor", self.current_floor, "moving", self.current_direction)

        elif self.current_direction == "down":

            if self.current_floor == self.bottom_floor:
                self.change_directions()
                self.current_floor += 1
                self.increment_lifetime_steps()

                if self.top_floor <= 20:
                    print("Currently on floor", self.current_floor, "moving", self.current_direction)

            else:
                self.current_floor -= 1
                self.increment_lifetime_steps()

                if self.top_floor <= 20:
                    print("Currently on floor", self.current_floor, "moving", self.current_direction)

    def increment_lifetime_steps(self):
        """ Increases the lifetime number of steps by one. """
        self.lifetime_steps += 1

    def increase_capacity(self):
        """ Increases the capacity by 1, up to 6."""
        if self.capacity != 6:
            self.capacity += 1

    def decrease_capacity(self):
        """ Decreases the capacity by 1, down to 0. """
        if self.capacity != 0:
            self.capacity -= 1


def increase_all_waiting(list_of_people: list):
    """ Increases the amount of time person has been waiting. """
    for person in list_of_people:
        if person.current_state == "waiting":
            person.increase_wait_time()


def increase_all_in_elevator(list_of_people: list):
    """ Increases the amount of time a person has spent in elevator. """
    for person in list_of_people:
        person: Person
        if person.current_state == "in lift":
            person.increase_time_in_lift()


def remove_from_people_list(list_of_people: list):
    """ Removes a person from the list of people. """
    for person in list_of_people:
        if person.current_state == "arrived":
            list_of_people.remove(person)


def check_for_people(list_of_people: list, lift: NaiveLift):
    """ Checks if there are people on the same floor as the lift that are waiting. """
    for person in list_of_people:
        if person.current_state == "waiting":
            if lift.current_floor == person.start_floor:
                return True
        else:
            return False


def return_people_on_floor(list_of_people: list, lift: NaiveLift):
    """ Returns the person that is on the same floor as the lift waiting. """
    people_on_floor = []

    for person in list_of_people:
        if person.current_state == "waiting":
            if lift.current_floor == person.start_floor:
                people_on_floor.append(person)

    return people_on_floor


def add_person_to_lift(person: Person, lift: NaiveLift):
    """ Adds a person to the lift. """
    lift.add_people_to_lift(person)
    person.get_in_lift()


def remove_person_from_lift(person: Person, lift: NaiveLift, list_of_people: list):
    """ Removes a person form the lift. """
    person.get_out_of_lift()
    lift.remove_people_from_lift(person)
    remove_from_people_list(list_of_people)


def check_if_on_target_floor(lift: NaiveLift, list_of_people: list):
    """ Checks if any of the people in the lift are at their target floor. """
    if isinstance(lift, NaiveLift):
        global total_time_naive
        for person in lift.people_in_lift:
            if person.target_floor == lift.current_floor:
                remove_person_from_lift(person, lift, list_of_people)
                total_time_naive += person.time_in_lift


def instance_rand_people(no_floors: int, is_random: bool = True, no_people: int = 30) -> list:
    """
    Creates new instances of people on random floors. Default is 30 people.

    :param int no_floors: The number of floors in the building.
    :param bool is_random: Whether the number of people is random. Default is True.
    :param int no_people: The number of people to generate. Default is 30.
    :return: An array of all people in the building.
    :rtype: list
    """

    people = []
    if is_random:
        for person in range(random.randint(10, 30)):
            rand_current_floor = random.randint(1, no_floors)
            if rand_current_floor == no_floors:
                rand_direction = "down"
            elif rand_current_floor == 1:
                rand_direction = "up"
            else:
                rand_direction = random.choice(["up", "down"])

            if rand_direction == "up":
                rand_target_floor = random.randint(rand_current_floor + 1, no_floors)
            else:
                rand_target_floor = random.randint(1, rand_current_floor - 1)

            people.append(Person(rand_current_floor, rand_direction, rand_target_floor))
    else:
        for person in range(no_people):
            rand_current_floor = random.randint(1, no_floors)
            if rand_current_floor == no_floors:
                rand_direction = "down"
            elif rand_current_floor == 1:
                rand_direction = "up"
            else:
                rand_direction = random.choice(["up", "down"])

            if rand_direction == "up":
                rand_target_floor = random.randint(rand_current_floor + 1, no_floors)
            else:
                rand_target_floor = random.randint(1, rand_current_floor - 1)

            people.append(Person(rand_current_floor, rand_direction, rand_target_floor))

    return people


def initialize_animation(number_of_floors: int) -> Union[int, tuple, any]:
    """
    Initializes the animation variables.

    :param int number_of_floors: The number of floors in the building.
    :return: Variables for use in animation.
    :rtype: Union[int, tuple, any]
    """

    canvas_x, canvas_y = animate.calc_canvas_size(number_of_floors)
    lift_width, lift_height = animate.calc_elevator_size(number_of_floors)
    canvas = animate.canvas_init(canvas_x, canvas_y)
    clock = pygame.time.Clock()
    lift_x_coord = (canvas_x - lift_width) // 2
    lift_y_coord = canvas_y - (lift_height + 10)
    lift_colour = (60, 69, 82)

    return canvas_x, canvas_y, lift_width, lift_height, canvas, clock, lift_x_coord, lift_y_coord, lift_colour


def create_people_occurrence_array(people_array: list) -> list:
    """
    Creates an array containing dictionaries. Dictionaries contain floor number and how many people at that floor.

    :param list people_array: Array of all people in the building.

    :return: Array of dictionaries mapping floor number to the number of people on said floor.
    :rtype: list
    """

    # Init empty arrays and dicts.
    array_of_floors: list = []
    floor_occurrence_array: list = []
    floor_occurrence: dict = {}

    # For every person in the array, add their start floor to the array.
    for person in people_array:
        array_of_floors.append(person.start_floor)

    # For every floor in the array of floors, count how many times that floor occurs.
    # Create a dictionary mapping floor number to number of occurrences.
    # Finally, some floors are double counted. Iterate through, adding dicts
    # Not in the final array to it, erasing double counts.
    for floor in array_of_floors:
        no_of_floor = array_of_floors.count(floor)
        floor_occurrence["floor_number"] = floor
        floor_occurrence["occurrences"] = no_of_floor

        floor_occurrence_array.append(deepcopy(floor_occurrence))

    final_list_occurrences = []
    for occurrence in floor_occurrence_array:
        if occurrence not in final_list_occurrences:
            final_list_occurrences.append(occurrence)

    return final_list_occurrences


def update_occurrence_array(occurrence_array: list, floor_number: int) -> list:
    """
    Updates a given floor in the occurrence array.

    :param list occurrence_array: Array of dictionaries mapping floor number and people on floor.
    :param int floor_number: The floor to be updated.
    :return: The updated occurrence array.
    :rtype: list
    """

    for floor in occurrence_array:
        if floor["floor_number"] == floor_number:
            floor["occurrences"] = floor["occurrences"] - 1

        if floor["occurrences"] == 0:
            occurrence_array.remove(floor)

    return occurrence_array


def draw_people_on_floor(canvas, no_floors: int, lift_height: int, lift_x_coord: int, occurrence_array: list):
    """
    Draws the number of people on each floor onto the animation.

    :param Canvas canvas: The canvas onto which the people are drawn.
    :param int no_floors: The number of people in the building.
    :param int lift_height: The pixel height of the lift.
    :param int lift_x_coord: The X coordinate, in pixels, of the upper left corner of the lift.
    :param list occurrence_array: Array of dictionaries mapping floor number and people on floor.
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
            text_rectangle_y = (20 + (no_floors * lift_height) + ((no_floors - 1) * 3)) - (10 + (lift_height // 2))
        else:
            text_rectangle_y = ((12 + lift_height) + ((no_floors - floor_number) * (lift_height + 3))) - 2 - (
                    lift_height // 2)

        text_rectangle.center = (text_rectangle_x, text_rectangle_y)
        canvas.blit(text_surface, text_rectangle)


def naive_lift_algorithm(number_of_floors: int = 20, people_list: list = None, return_stats: bool = False):
    """
    The main decision subroutine for this algorithm.

    This algorithm is modelled on old mechanical pulley style lifts. As with old pulley systems, this lift
    cannot change direction in transit and can only do so at both the top and bottom floors. This lift can
    stop at each floor and has a maximum capacity of 6 people.

    :param int number_of_floors: The number of floors in the building, defaults to 20.
    :param list people_list: All people in the building, defaults to None. A previously formed array can be
    used instead.
    :param bool return_stats: Whether this subroutine should return various stats, defaults to False.
    """

    if number_of_floors <= 20:
        lift_y_coord: int
        canvas_x, canvas_y, lift_width, lift_height, canvas, clock, lift_x_coord, lift_y_coord, lift_colour = \
            initialize_animation(number_of_floors)
    is_done = False

    if not people_list:
        people_list = instance_rand_people(number_of_floors)

    occurrence_array = create_people_occurrence_array(people_list)

    naive_lift = NaiveLift(number_of_floors, people_list)
    max_people = len(people_list)
    total_wait = 0
    global total_time_naive

    while people_list or not is_done:
        if number_of_floors <= 20:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_done = True

        if people_list:
            naive_lift.move_lift_by_one_floor()

            if number_of_floors <= 20:
                if naive_lift.current_direction == "up":
                    lift_y_coord -= (lift_height + 3)
                elif naive_lift.current_direction == "down":
                    lift_y_coord += (lift_height + 3)

            increase_all_waiting(people_list)
            increase_all_in_elevator(people_list)
            check_if_on_target_floor(naive_lift, people_list)

            if check_for_people(people_list, naive_lift):
                people_on_floor = return_people_on_floor(people_list, naive_lift)

                for person in people_on_floor:
                    if 0 < naive_lift.capacity <= 6:
                        add_person_to_lift(person, naive_lift)
                        total_wait += person.wait_time
                        occurrence_array = update_occurrence_array(occurrence_array, naive_lift.current_floor)

        if number_of_floors <= 20:
            animate.draw_white_bg(canvas)
            animate.draw_building_lines(canvas, number_of_floors, lift_width, lift_height, lift_x_coord)
            draw_people_on_floor(canvas, number_of_floors, lift_height, lift_x_coord, occurrence_array)
            pygame.draw.rect(canvas, lift_colour, pygame.Rect(lift_x_coord, lift_y_coord, lift_width, lift_height))
            pygame.display.flip()
            clock.tick(number_of_floors)

            if not people_list:
                print("Naive lift has finished.\n")
                break

        elif number_of_floors > 20:
            if not people_list:
                print("Naive lift has finished.\n")
                break

    avg_wait = total_wait // max_people
    avg_in_lift = total_time_naive // max_people
    life_steps = naive_lift.lifetime_steps
    print("Number of Floors:", number_of_floors, "floors.")
    print("Lifetime steps for lift:", life_steps, "steps.")
    print("Total Time Waiting for Lift:", total_wait, "steps.")
    print("Total Time in Lift:", total_time_naive, "steps.")
    print("Number of People:", max_people, "people.")
    print("Average Wait Time:", avg_wait, "steps per person.")
    print("Average Time in Lift:", avg_in_lift, "steps per person.")

    if return_stats:
        return number_of_floors, life_steps, total_wait, total_time_naive, max_people, avg_wait, avg_in_lift
