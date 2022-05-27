import pygame_functions
import pygame
import random

import pygame.display

pygame.init()


class Information:
    # setting up colors in R,G,B color modal
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128,128,128
    ORANGE = 255, 215, 0

    BACKGROUND_COLOR = BLACK # Cause Dark mode Rocks!!

    # Describing the color  of the bars
    GRADIENTS = [
        (128, 128, 128),
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('comicsans',30)
    LARGE_FONT = pygame.font.SysFont('comicsans',40)
    SIDE_PAD = 80
    TOP_PAD = 280


    def __init__(self, width, height, lst):
        # lst is a starting list that we want to sort
        # taking in width and height of the window
        self.width = width
        self.height = height

        # Drawing window to display stuff
        self.window = pygame.display.set_mode((width, height))
        # Setting up the window name
        pygame.display.set_caption("Sorting Algo Visualizer")

        # taking in a list and set some info
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) # minimum value of the list to be drawn
        self.max_val = max(lst) # maximum value of the list to be drawn

        # Determining width of blocks
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # Determining the length of blocks
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        # Starting point for generation of blocks
        self.start_x = self.SIDE_PAD // 2

# Function for filling in background color
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.FONT.render(f"{algo_name} -> {'Ascending' if ascending else 'Descending'}", 1,
                                     draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render(' R -> Reset || SPACE -> Start Sorting || A -> Ascending || D -> Descending', 1, draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,40))

    sorting = draw_info.FONT.render('I -> Insertion Sort || B -> Bubble Sort', 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,75))

    draw_list(draw_info)
    pygame.display.update()

# function to draw the list on the screen
def draw_list(draw_info,color_positions = {}, clear_bg = False):
    lst =draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i,val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val-draw_info.min_val)*draw_info.block_height

        color = draw_info.GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))

    if clear_bg:
        pygame.display.update()
# Function for generating list
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                # using generators with yield keyword
                # it is used to store each value and then run some function on it.
                # Telsuko on generators
                yield True
                '''
                If we don't use yield then the function will have full control of the program for it's running time and
                the program will not respond to any other button or function till the completion of this part.
          '''

    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i>0 and lst[i-1] > current and ascending
            descending_sort = i>0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i-1:draw_info.GREEN, i:draw_info.RED}, True)
            yield True
    return lst

def main():
    run = True
    clock = pygame.time.Clock() # regulates how quickly this while will run

    n = 100
    min_val = 0
    max_val = 200

    lst = generate_starting_list(n,min_val,max_val)
    draw_info = Information(1280,720,lst)
    speed = 50

    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None
    while run:
        clock.tick(speed)

        if sorting :
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # Checking if user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False

            if event.key == pygame.K_RIGHT:
                speed += 50

            elif event.key == pygame.K_LEFT:
                if speed > 60:
                    speed -= 50
                else:
                    speed = 2

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info,ascending)

            elif event.key == pygame.K_SPACE and sorting == True:
                sorting = False

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = 'Insertion Sort'

            elif event.key == pygame.K_b and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = 'Bubble Sort'

    pygame.quit()


if __name__ == "__main__":
    main()
