import pygame
import pygame.freetype
import improved_algorithm as improved
import naive_algorithm as naive
from pygame.sprite import Sprite
from enum import Enum
from multiprocessing import Pool

# ================ GUI Constants ================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
KEEP_SELECT = False
LAST_NUMBER_SELECT = 2
LAST_POP_SELECT = 1
CANVAS = 0

# ================ Stat Constants ================
FLOOR_NUM = 0
LIFE_STEPS = 0
TOTAL_WAIT = 0
TOTAL_IN_LIFT = 0
POPULATION = 0
AVG_WAIT = 0
AVG_IN_LIFT = 0


def create_text_surface(string: str, size, font_col, bg_col):
    """ Creates text of a certain font onto a surface. """
    font = pygame.freetype.SysFont("comicsansms", size)
    surface, _ = font.render(text=string, fgcolor=font_col, bgcolor=bg_col)
    return surface.convert_alpha()


class ButtonElement(Sprite):
    """ A button sprite that returns a game state enum when clicked. """
    def __init__(self, centre_pos, string: str, size, font_col, bg_col, action=None):
        """ ButtonElement Constructor. A button sprite that can be drawn onto a canvas
        with specific size, colour, position and action."""
        super().__init__()

        self.mouse_over = False

        default_button = create_text_surface(string, size, font_col, bg_col)
        highlighted_button = create_text_surface(string, (size * 1.2), font_col, bg_col)
        self.buttons = [default_button, highlighted_button]
        self.rects = [default_button.get_rect(center=centre_pos), highlighted_button.get_rect(center=centre_pos)]

        self.action = action

    @property
    def button(self):
        """ Button property, there are two sizes of button. """
        if self.mouse_over:
            return self.buttons[1]
        else:
            return self.buttons[0]

    @property
    def rect(self):
        """ Rectangle property, there are two sizes of rectangle. """
        if self.mouse_over:
            return self.rects[1]
        else:
            return self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """
        Checks mouse position and whether button has been clicked.

        :param tuple mouse_pos: Where the mouse is on the canvas.
        :param bool mouse_up: Whether the mouse has been clicked and
        released.
        :return: The action of the button in the form of a state enum.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, canvas):
        canvas.blit(self.button, self.rect)


class NumElement(Sprite):
    """ A button sprite that returns a number when clicked. """
    def __init__(self, centre_pos, string: str, size, font_col, bg_col, num: int = None):
        """ NumElement Constructor. A number button sprite that can be drawn onto a canvas
        with specific size, colour, position and numerical value."""
        super().__init__()

        default_button = create_text_surface(string, size, font_col, bg_col)
        highlighted_button = create_text_surface(string, (size * 1.2), font_col, bg_col)
        self.buttons = [default_button, highlighted_button]
        self.rects = [default_button.get_rect(center=centre_pos), highlighted_button.get_rect(center=centre_pos)]

        self.number = num
        self.mouse_over = False

    @property
    def button(self):
        """
        The button properties of the button;
        there are two different size buttons.
        """
        if self.mouse_over:
            return self.buttons[1]
        else:
            return self.buttons[0]

    @property
    def rect(self):
        """
        The rectangle properties of the button;
        there are two different size rectangles.
        """
        if self.mouse_over:
            return self.rects[1]
        else:
            return self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """
        Updates the button constantly, checking if
        mouse is over it or has clicked on it.

        :param tuple mouse_pos: Where the mouse is on
        the canvas.
        :param bool mouse_up: Whether the mouse 1 button
        has been pressed and released.

        :return: The number assigned to this button.
        :rtype: int
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return int(self.number)
        else:
            self.mouse_over = False

    def draw(self, canvas):
        """ Blits the button and rectangle onto canvas. """
        canvas.blit(self.button, self.rect)


class LabelElement(Sprite):
    """ A Label sprite. """
    def __init__(self, centre_pos, string, size, font_col, bg_col):
        """ LabelElement Constructor. A label sprite that can be drawn onto a canvas
        with specific size, colour and position.
        """
        super().__init__()

        default_label = create_text_surface(string, size, font_col, bg_col)
        default_rect = default_label.get_rect(center=centre_pos)

        self.def_label = default_label
        self.def_rect = default_rect

    @property
    def label(self):
        """
        The main label of this class.
        :return: The label
        """
        return self.def_label

    @property
    def rect(self):
        """
        The main rectangle for drawing.
        :return: The rectangle
        """
        return self.def_rect

    def draw(self, canvas):
        """
        Blits the label and rectangle.
        :param Canvas canvas: Canvas onto which label
        and rect are blitted.
        """
        canvas.blit(self.label, self.rect)


class GameState(Enum):
    """
    A class of enums that denote the
    states of the gui.
    """
    QUIT = -1
    MENU = 0
    FLOOR_ENTER = 1
    PEOPLE_ENTER = 2
    IMPROVED = 3
    NAIVE = 4
    ALGORITHM_ENTER = 5
    STATS = 6


def menu_screen(canvas):
    """
    The main menu for the system. Redirects to first page of
    selections or quits system. Quitting can only be done from
    here.

    :param Canvas canvas: Canvas onto which drawing is done.
    :return: Gamestate enums.
    """
    start_button = ButtonElement(
        centre_pos=(400, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Start Simulation",
        action=GameState.FLOOR_ENTER
    )

    quit_button = ButtonElement(
        centre_pos=(400, 550),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Quit",
        action=GameState.QUIT
    )

    title_label = LabelElement(
        centre_pos=(400, 200),
        size=40,
        bg_col=WHITE,
        font_col=BLACK,
        string="Lift Simulation System"
    )

    author_label = LabelElement(
        centre_pos=(400, 250),
        size=25,
        bg_col=WHITE,
        font_col=BLACK,
        string="By 690037391"
    )

    buttons = [start_button, quit_button]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        canvas.fill(WHITE)

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            if action is not None:
                return action

            button.draw(canvas)

        title_label.draw(canvas)
        author_label.draw(canvas)

        pygame.display.flip()


def floor_select(canvas):
    """
    Main screen for selecting number of floors.

    :param Canvas canvas: Canvas onto which floor number is drawn.
    :return: Game state enums
    """
    global KEEP_SELECT
    global LAST_NUMBER_SELECT
    global LAST_POP_SELECT
    return_button = ButtonElement(
        centre_pos=(140, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Return to Menu",
        action=GameState.MENU
    )

    people_button = ButtonElement(
        centre_pos=(660, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Choose Population",
        action=GameState.PEOPLE_ENTER
    )

    select_label = LabelElement(
        centre_pos=(400, 100),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Select the number of floors."
    )

    one_button = NumElement(
        centre_pos=(460, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 1",
        num=1
    )

    five_button = NumElement(
        centre_pos=(520, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 5",
        num=5
    )

    ten_button = NumElement(
        centre_pos=(580, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 10",
        num=10
    )

    minus_one_button = NumElement(
        centre_pos=(340, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 1",
        num=1
    )

    minus_five_button = NumElement(
        centre_pos=(280, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 5",
        num=5
    )

    minus_ten_button = NumElement(
        centre_pos=(220, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 10",
        num=10
    )

    if KEEP_SELECT:
        number_select = LAST_NUMBER_SELECT
    else:
        number_select = 2

    while True:
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        canvas.fill(WHITE)

        plus_one = one_button.update(pygame.mouse.get_pos(), mouse_up)
        plus_five = five_button.update(pygame.mouse.get_pos(), mouse_up)
        plus_ten = ten_button.update(pygame.mouse.get_pos(), mouse_up)

        minus_one = minus_one_button.update(pygame.mouse.get_pos(), mouse_up)
        minus_five = minus_five_button.update(pygame.mouse.get_pos(), mouse_up)
        minus_ten = minus_ten_button.update(pygame.mouse.get_pos(), mouse_up)

        if plus_one is not None:
            if number_select < 1000:
                number_select += plus_one

        if minus_one is not None:
            if number_select > 2:
                if number_select - minus_one < 2:
                    number_select = 2
                else:
                    number_select -= minus_one

        if plus_five is not None:
            if number_select < 1000:
                number_select += plus_five

        if minus_five is not None:
            if number_select > 2:
                if number_select - minus_five < 2:
                    number_select = 2
                else:
                    number_select -= minus_five

        if plus_ten is not None:
            if number_select < 1000:
                number_select += plus_ten

        if minus_ten is not None:
            if number_select > 2:
                if number_select - minus_ten < 2:
                    number_select = 2
                else:
                    number_select -= minus_ten

        return_action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if return_action is not None:
            KEEP_SELECT = False
            LAST_POP_SELECT = 1
            return return_action

        population = people_button.update(pygame.mouse.get_pos(), mouse_up)
        if population is not None:
            LAST_NUMBER_SELECT = number_select
            KEEP_SELECT = False
            return population

        return_button.draw(canvas)
        people_button.draw(canvas)

        one_button.draw(canvas)
        five_button.draw(canvas)
        ten_button.draw(canvas)
        minus_one_button.draw(canvas)
        minus_five_button.draw(canvas)
        minus_ten_button.draw(canvas)

        select_label.draw(canvas)

        number_select_label = LabelElement(
            centre_pos=(400, 300),
            size=40,
            bg_col=WHITE,
            font_col=BLACK,
            string=str(number_select),
        )

        number_select_label.draw(canvas)

        pygame.display.flip()


def people_select(canvas):
    """
    The main screen for selecting the
    population of the building.

    :param Canvas canvas: Canvas onto which drawing is done.
    :return: Game state enums
    """
    global KEEP_SELECT
    global LAST_POP_SELECT
    global CANVAS
    return_button = ButtonElement(
        centre_pos=(140, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Return to Menu",
        action=GameState.MENU
    )

    back_button = ButtonElement(
        centre_pos=(400, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Go Back",
        action=GameState.FLOOR_ENTER
    )

    algorithm_button = ButtonElement(
        centre_pos=(660, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Choose an algorithm",
        action=GameState.ALGORITHM_ENTER
    )

    select_label = LabelElement(
        centre_pos=(400, 100),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Select the number of people."
    )

    one_button = NumElement(
        centre_pos=(460, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 1",
        num=1
    )

    five_button = NumElement(
        centre_pos=(520, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 5",
        num=5
    )

    ten_button = NumElement(
        centre_pos=(580, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="+ 10",
        num=10
    )

    minus_one_button = NumElement(
        centre_pos=(340, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 1",
        num=1
    )

    minus_five_button = NumElement(
        centre_pos=(280, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 5",
        num=5
    )

    minus_ten_button = NumElement(
        centre_pos=(220, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="- 10",
        num=10
    )

    pop_select = LAST_POP_SELECT

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        canvas.fill(WHITE)

        plus_one = one_button.update(pygame.mouse.get_pos(), mouse_up)
        plus_five = five_button.update(pygame.mouse.get_pos(), mouse_up)
        plus_ten = ten_button.update(pygame.mouse.get_pos(), mouse_up)

        minus_one = minus_one_button.update(pygame.mouse.get_pos(), mouse_up)
        minus_five = minus_five_button.update(pygame.mouse.get_pos(), mouse_up)
        minus_ten = minus_ten_button.update(pygame.mouse.get_pos(), mouse_up)

        if plus_one is not None:
            if pop_select < 1000:
                pop_select += plus_one

        if minus_one is not None:
            if pop_select > 1:
                if pop_select - minus_one < 1:
                    pop_select = 1
                else:
                    pop_select -= minus_one

        if plus_five is not None:
            if pop_select < 1000:
                pop_select += plus_five

        if minus_five is not None:
            if pop_select > 1:
                if pop_select - minus_five < 1:
                    pop_select = 1
                else:
                    pop_select -= minus_five

        if plus_ten is not None:
            if pop_select < 1000:
                pop_select += plus_ten

        if minus_ten is not None:
            if pop_select > 1:
                if pop_select - minus_ten < 1:
                    pop_select = 1
                else:
                    pop_select -= minus_ten

        action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if action is not None:
            KEEP_SELECT = False
            return action

        algorithm = algorithm_button.update(pygame.mouse.get_pos(), mouse_up)
        if algorithm is not None:
            LAST_POP_SELECT = pop_select
            KEEP_SELECT = False
            CANVAS = canvas
            return algorithm

        action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if action is not None:
            return action

        back = back_button.update(pygame.mouse.get_pos(), mouse_up)
        if back is not None:
            KEEP_SELECT = True
            LAST_POP_SELECT = pop_select
            return back

        one_button.draw(canvas)
        five_button.draw(canvas)
        ten_button.draw(canvas)
        minus_one_button.draw(canvas)
        minus_five_button.draw(canvas)
        minus_ten_button.draw(canvas)

        return_button.draw(canvas)
        back_button.draw(canvas)
        select_label.draw(canvas)
        algorithm_button.draw(canvas)

        pop_select_label = LabelElement(
            centre_pos=(400, 300),
            size=40,
            bg_col=WHITE,
            font_col=BLACK,
            string=str(pop_select),
        )

        pop_select_label.draw(canvas)

        pygame.display.flip()


def run_improved():
    """
        Runs the improved algorithm in a separate process pool,
        and returns any variables in a 3D array.

        :return: An enum for the Stats screen state.
        :rtype: enum
    """
    global LAST_POP_SELECT
    global LAST_NUMBER_SELECT
    global KEEP_SELECT
    global FLOOR_NUM
    global LIFE_STEPS
    global TOTAL_WAIT
    global TOTAL_IN_LIFT
    global POPULATION
    global AVG_WAIT
    global AVG_IN_LIFT

    people_list = improved.generate_people(LAST_NUMBER_SELECT, LAST_POP_SELECT)
    lift_job = Pool(processes=1)

    result = lift_job.starmap(
        improved.better_lift_algorithm, [(LAST_NUMBER_SELECT, LAST_POP_SELECT, people_list)]
    )
    lift_job.close()

    FLOOR_NUM = result[0][0]
    LIFE_STEPS = result[0][1]
    TOTAL_WAIT = result[0][2]
    TOTAL_IN_LIFT = result[0][3]
    POPULATION = result[0][4]
    AVG_WAIT = result[0][5]
    AVG_IN_LIFT = result[0][6]

    LAST_NUMBER_SELECT = 2
    LAST_POP_SELECT = 1
    KEEP_SELECT = False
    return GameState.STATS


def run_naive():
    """
    Runs the Naïve algorithm in a separate process pool,
    and returns any variables in a 3D array.

    :return: An enum for the Stats screen state.
    :rtype: enum
    """
    global LAST_POP_SELECT
    global LAST_NUMBER_SELECT
    global KEEP_SELECT
    global FLOOR_NUM
    global LIFE_STEPS
    global TOTAL_WAIT
    global TOTAL_IN_LIFT
    global POPULATION
    global AVG_WAIT
    global AVG_IN_LIFT

    people_list = improved.generate_people(LAST_NUMBER_SELECT, LAST_POP_SELECT)
    lift_job = Pool(processes=1)

    result = lift_job.starmap(
        naive.naive_lift_algorithm, [(LAST_NUMBER_SELECT, people_list, True)]
    )
    lift_job.close()

    FLOOR_NUM = result[0][0]
    LIFE_STEPS = result[0][1]
    TOTAL_WAIT = result[0][2]
    TOTAL_IN_LIFT = result[0][3]
    POPULATION = result[0][4]
    AVG_WAIT = result[0][5]
    AVG_IN_LIFT = result[0][6]

    LAST_NUMBER_SELECT = 2
    LAST_POP_SELECT = 1
    KEEP_SELECT = False
    return GameState.STATS


def show_stats(canvas):
    """
    Creates the stats display screen.

    :param Canvas canvas: Canvas onto which stats are drawn.
    :return: A state enum
    :rtype: Enum
    """
    global LAST_POP_SELECT
    global LAST_NUMBER_SELECT
    global KEEP_SELECT
    global FLOOR_NUM
    global LIFE_STEPS
    global TOTAL_WAIT
    global TOTAL_IN_LIFT
    global POPULATION
    global AVG_WAIT
    global AVG_IN_LIFT

    canvas.fill(WHITE)

    return_button = ButtonElement(
        centre_pos=(140, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Return to Menu",
        action=GameState.MENU
    )

    title_label = LabelElement(
        centre_pos=(400, 100),
        size=40,
        bg_col=WHITE,
        font_col=BLACK,
        string="Statistics"
    )

    floor_num_label = LabelElement(
        centre_pos=(300, 200),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Number of Floors"
    )
    floor_num_result = LabelElement(
        centre_pos=(600, 200),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(FLOOR_NUM)
    )

    life_steps_label = LabelElement(
        centre_pos=(300, 250),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Lifetime steps"
    )
    life_steps_result = LabelElement(
        centre_pos=(600, 250),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(LIFE_STEPS)
    )

    total_wait_label = LabelElement(
        centre_pos=(300, 300),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Total time waiting for lift"
    )
    total_wait_result = LabelElement(
        centre_pos=(600, 300),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(TOTAL_WAIT)
    )

    total_in_lift_label = LabelElement(
        centre_pos=(300, 350),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Total time spent in lift"
    )
    total_in_lift_result = LabelElement(
        centre_pos=(600, 350),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(TOTAL_IN_LIFT)
    )

    population_label = LabelElement(
        centre_pos=(300, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Population"
    )
    population_result = LabelElement(
        centre_pos=(600, 400),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(POPULATION)
    )

    average_wait_label = LabelElement(
        centre_pos=(300, 450),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Average Waiting time"
    )
    average_wait_result = LabelElement(
        centre_pos=(600, 450),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(AVG_WAIT)
    )

    average_in_lift_label = LabelElement(
        centre_pos=(300, 500),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Average Time spent in Lift"
    )
    average_in_lift_result = LabelElement(
        centre_pos=(600, 500),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string=str(AVG_IN_LIFT)
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        canvas.fill(WHITE)

        return_action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if return_action is not None:
            LAST_POP_SELECT = 1
            LAST_NUMBER_SELECT = 2
            KEEP_SELECT = False
            FLOOR_NUM = 0
            LIFE_STEPS = 0
            TOTAL_WAIT = 0
            TOTAL_IN_LIFT = 0
            POPULATION = 0
            AVG_WAIT = 0
            AVG_IN_LIFT = 0

            return return_action

        return_button.draw(canvas)
        title_label.draw(canvas)

        life_steps_label.draw(canvas)
        life_steps_result.draw(canvas)

        total_in_lift_label.draw(canvas)
        total_in_lift_result.draw(canvas)

        total_wait_label.draw(canvas)
        total_wait_result.draw(canvas)

        population_label.draw(canvas)
        population_result.draw(canvas)

        floor_num_label.draw(canvas)
        floor_num_result.draw(canvas)

        average_in_lift_label.draw(canvas)
        average_in_lift_result.draw(canvas)

        average_wait_label.draw(canvas)
        average_wait_result.draw(canvas)

        pygame.display.flip()


def algorithm_select(canvas):
    """
    Is the main algorithm selection screen.

    :param Canvas canvas: The pygame canvas onto which drawing is done.
    :return: An Enum corresponding to the state to move to.
    :rtype: Enum
    """
    global KEEP_SELECT
    global LAST_POP_SELECT
    global LAST_NUMBER_SELECT

    return_button = ButtonElement(
        centre_pos=(140, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Return to Menu",
        action=GameState.MENU
    )

    back_button = ButtonElement(
        centre_pos=(400, 570),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Go Back",
        action=GameState.PEOPLE_ENTER
    )

    improved_button = ButtonElement(
        centre_pos=(500, 300),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Improved",
        action=GameState.IMPROVED
    )

    naive_button = ButtonElement(
        centre_pos=(300, 300),
        size=20,
        bg_col=WHITE,
        font_col=BLACK,
        string="Naive",
        action=GameState.NAIVE
    )

    title_label = LabelElement(
        centre_pos=(400, 200),
        size=30,
        bg_col=WHITE,
        font_col=BLACK,
        string="Choose an algorithm"
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        canvas.fill(WHITE)

        return_action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if return_action is not None:
            return return_action

        back = back_button.update(pygame.mouse.get_pos(), mouse_up)
        if back is not None:
            KEEP_SELECT = True
            return back

        improved_action = improved_button.update(pygame.mouse.get_pos(), mouse_up)
        if improved_action is not None:
            return improved_action

        naive_action = naive_button.update(pygame.mouse.get_pos(), mouse_up)
        if naive_action is not None:
            return naive_action

        return_button.draw(canvas)
        back_button.draw(canvas)
        improved_button.draw(canvas)
        naive_button.draw(canvas)
        title_label.draw(canvas)

        pygame.display.flip()


def main():
    """
    Controls which state the GUI is in and what to
    do when changing states.
    """
    pygame.init()
    is_done = False

    canvas = pygame.display.set_mode((800, 600))

    game_state = GameState.MENU

    while not is_done:
        if game_state == GameState.MENU:
            game_state = menu_screen(canvas)

        if game_state == GameState.ALGORITHM_ENTER:
            game_state = algorithm_select(canvas)

        if game_state == GameState.FLOOR_ENTER:
            game_state = floor_select(canvas)

        if game_state == GameState.PEOPLE_ENTER:
            game_state = people_select(canvas)

        if game_state == GameState.IMPROVED:
            game_state = run_improved()

        if game_state == GameState.NAIVE:
            game_state = run_naive()

        if game_state == GameState.STATS:
            canvas = pygame.display.set_mode((800, 600))
            game_state = show_stats(canvas)

        if game_state == GameState.QUIT:
            pygame.quit()
            is_done = True


if __name__ == '__main__':
    main()

