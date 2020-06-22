import pygame
from typing import Union

pygame.init()


def canvas_init(canvas_x: int, canvas_y: int):
    """
    Initializes the pygame canvas, onto which animation is done.

    :param int canvas_x: The pixel width of the canvas.
    :param int canvas_y: The pixel height of the canvas.

    :return: The canvas onto which animation is done.
    :rtype: object
    """
    canvas = pygame.display.set_mode((canvas_x, canvas_y))
    return canvas


def calc_canvas_size(no_floors: int) -> [int]:
    """
    Calculates the size of the canvas based on the number of floors.

    :param int no_floors: The number of floors in the building.

    :return: The width and height of the canvas.
    :rtype: Union[int, int]
    """
    canvas_x = 560
    if 2 <= no_floors <= 12:
        canvas_y = ((no_floors * 60) + 20 + ((no_floors - 1) * 3))

        return canvas_x, canvas_y

    elif 12 < no_floors <= 18:
        canvas_y = ((no_floors * 40) + 20 + ((no_floors - 1) * 3))

        return canvas_x, canvas_y

    elif 18 < no_floors <= 20:
        canvas_y = ((no_floors * 30) + 20 + ((no_floors - 1) * 3))

        return canvas_x, canvas_y

    elif 20 < no_floors or no_floors < 2:
        print("Cannot animate an elevator with floors less than 2 or greater than 20.")


def calc_elevator_size(no_floors: int) -> [int]:
    """
    Calculates the size of the lift itself, based on the number of floors.

    :param int no_floors: The number of floors in the building.

    :return: The pixel width and height of the lift itself.
    :rtype: Union[int, int]
    """
    if 2 <= no_floors <= 12:
        lift_width = 60
        lift_height = 60

        return lift_width, lift_height

    elif 12 < no_floors <= 18:
        lift_width = 40
        lift_height = 40

        return lift_width, lift_height

    elif 18 < no_floors <= 20:
        lift_width = 30
        lift_height = 30

        return lift_width, lift_height

    elif 20 < no_floors or no_floors < 2:
        print("Cannot animate an elevator with floors less than 2 or greater than 20.")


def draw_white_bg(canvas: object):
    """
    Draws the white background for the animation.

    :param object canvas: The canvas onto which animation is done.
    """
    canvas.fill((255, 255, 255))


def draw_building_lines(canvas: object, no_floors: int, lift_width: int, lift_height: int, lift_x_coord: int):
    """
    Draws the lines representing the building that the elevator is in.

    :param object canvas: The canvas onto which animation is done.
    :param int no_floors: The total number of floors in the building.
    :param int lift_width: The pixel width of the lift itself.
    :param int lift_height: The pixel height of the lift itself.
    :param int lift_x_coord: The X coordinate of the top left corner of the lift itself.
    """
    # Define line colour.
    line_colour = (0, 0, 0)

    # Define the x-coords of the horizontal line.
    point_1_x = lift_x_coord - (lift_width + 100)
    point_2_x = lift_x_coord + (2 * lift_width + 100)

    # Define the left hand vertical line.
    vert_line_a_point_1 = (point_1_x, 10)
    vert_line_a_point_2 = (point_1_x, (lift_height + 11) + ((no_floors - 1) * (lift_height + 3)))

    # Define the right hand vertical line.
    vert_line_b_point_1 = (point_2_x, 10)
    vert_line_b_point_2 = (point_2_x, (lift_height + 11) + ((no_floors - 1) * (lift_height + 3)))

    # Draw the two vertical lines.
    pygame.draw.line(canvas, line_colour, vert_line_a_point_1, vert_line_a_point_2)
    pygame.draw.line(canvas, line_colour, vert_line_b_point_1, vert_line_b_point_2)

    # Draw each floor.
    for floor in range(0, no_floors + 1):
        if floor == 1:
            point_1_y = point_2_y = 11 + lift_height
            point_1 = (point_1_x, point_1_y)
            point_2 = (point_2_x, point_2_y)

            pygame.draw.line(canvas, line_colour, point_1, point_2)
        else:
            point_1_y = point_2_y = (lift_height + 11) + ((floor - 1) * (lift_height + 3))
            point_1 = (point_1_x, point_1_y)
            point_2 = (point_2_x, point_2_y)

            pygame.draw.line(canvas, line_colour, point_1, point_2)