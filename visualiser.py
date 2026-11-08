import pygame
import random
import time

# ------------------------------
# CONFIG
# ------------------------------
WIDTH = 1000
HEIGHT = 600
ARRAY_SIZE = 150
BAR_COLOR = (100, 149, 237)
HIGHLIGHT_COLOR = (255, 69, 0)
BACKGROUND = (30, 30, 30)
FPS = 60

# ------------------------------
# PyGame Setup
# ------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualiser (PyGame)")
clock = pygame.time.Clock()

# ------------------------------
# Generate Array
# ------------------------------
def generate_array(size):
    return [random.randint(10, HEIGHT - 10) for _ in range(size)]

array = generate_array(ARRAY_SIZE)
bar_width = WIDTH // ARRAY_SIZE

# ------------------------------
# Drawing
# ------------------------------
def draw_array(arr, highlight=None):
    screen.fill(BACKGROUND)
    for i, val in enumerate(arr):
        color = BAR_COLOR
        if highlight and i in highlight:
            color = HIGHLIGHT_COLOR
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - val, bar_width, val))
    pygame.display.update()

# ------------------------------
# Sorting Algorithms (Generators)
# ------------------------------
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            yield (j, j+1)
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield (j, j+1)
    yield None

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            yield (min_idx, j)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield (i, min_idx)
    yield None

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            yield (j, j+1)
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
        yield (j+1, i)
    yield None

def quick_sort(arr):
    def _quick_sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            yield from _quick_sort(low, pivot_index - 1)
            yield from _quick_sort(pivot_index + 1, high)

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            yield (j, high)
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield (i, j)
        arr[i+1], arr[high] = arr[high], arr[i+1]
        yield (i+1, high)
        return i + 1

    yield from _quick_sort(0, len(arr) - 1)
    yield None

# ------------------------------
# Main Loop
# ------------------------------
def run_sort(algorithm):
    global array
    gen = algorithm(array)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        try:
            highlight = next(gen)
            if highlight is None:
                draw_array(array)
                return
            draw_array(array, highlight)
        except StopIteration:
            return

# ------------------------------
# Choose Algorithm Here
# ------------------------------
if __name__ == "__main__":
    run_sort(quick_sort)   # change to bubble_sort, selection_sort, insertion_sort
    pygame.quit()
