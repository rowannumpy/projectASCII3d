import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
import numpy as np
import random

speed_val = 0.05
arr_data = []
sorting_in_progress = False
sort_state = {'i': 0, 'j': 0}
timer = None

def generate_random_array(size=100):
    return random.sample(range(1, size + 1), size)

def get_sorted_array(size=100):
    return list(range(1, size + 1))

def update_2d_bar_chart(ax, arr, n, grid_size):
    ax.clear()

    Z = np.zeros((grid_size, grid_size))

    x_coords = []
    y_coords = []
    values = []

    for idx in range(n):
        diag = idx // grid_size
        pos = idx % grid_size
        row = diag
        col = grid_size - 1 - pos

        if row < grid_size and col < grid_size:
            x_coords.append(row)
            y_coords.append(col)
            values.append(arr[idx])

    hist = ax.hist2d(x_coords, y_coords, bins=grid_size, weights=values, cmap='viridis')

    ax.set_title(f'Bubble Sort Visualization')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.pause(0.001)

def update_speed(val):
    global speed_val
    speed_val = val

def randomize_array(event):
    global arr_data, sorting_in_progress
    if sorting_in_progress:
        return
    arr_data = generate_random_array(100)
    n = len(arr_data)
    grid_size = int(np.ceil(np.sqrt(n)))
    update_2d_bar_chart(ax_main, arr_data, n, grid_size)
    plt.draw()

def reset_array(event):
    global arr_data, sorting_in_progress, sort_state, timer
    if sorting_in_progress:
        return
    if timer:
        timer.stop()
    sort_state = {'i': 0, 'j': 0}
    arr_data = get_sorted_array(100)
    n = len(arr_data)
    grid_size = int(np.ceil(np.sqrt(n)))
    update_2d_bar_chart(ax_main, arr_data, n, grid_size)
    plt.draw()

def animation_step(*args):
    global arr_data, sorting_in_progress, sort_state, timer

    if not sorting_in_progress:
        return True

    n = len(arr_data)
    grid_size = int(np.ceil(np.sqrt(n)))
    i = sort_state['i']
    j = sort_state['j']

    update_2d_bar_chart(ax_main, arr_data, n, grid_size)
    plt.draw()

    if j < n - i - 1:
        if arr_data[j] > arr_data[j + 1]:
            arr_data[j], arr_data[j + 1] = arr_data[j + 1], arr_data[j]

        sort_state['j'] = j + 1
    else:
        sort_state['j'] = 0
        sort_state['i'] = i + 1
        if sort_state['i'] >= n - 1:
            sorting_in_progress = False
            print("Sorting complete!")
            return False

    return True

def start_sorting(event):
    global sorting_in_progress, sort_state, timer
    if sorting_in_progress:
        return
    sorting_in_progress = True
    sort_state = {'i': 0, 'j': 0}
    timer = fig.canvas.new_timer(interval=int(speed_val * 1000))
    timer.add_callback(animation_step)
    timer.start()

def stop_sorting(event):
    global sorting_in_progress, sort_state, timer
    sorting_in_progress = False
    if timer:
        timer.stop()

fig = None
ax_main = None

def main():
    global speed_val, arr_data, ax_main, fig

    print("Bubble Sort Visualiser")
    print("Generating sorted array of 100 unique values...")

    arr = get_sorted_array(100)
    print(f"Starting array (first 10): {arr[:10]}...")

    arr_data = arr.copy()
    n = len(arr_data)
    grid_size = int(np.ceil(np.sqrt(n)))

    fig = plt.figure(figsize=(14, 8))
    ax_main = fig.add_subplot(111)

    ax_speed = plt.axes([0.2, 0.02, 0.4, 0.03])
    slider = Slider(ax_speed, 'Speed', 0.001, 0.1, valinit=0.05)
    slider.on_changed(update_speed)

    ax_shuffle = plt.axes([0.02, 0.90, 0.15, 0.04])
    btn_shuffle = Button(ax_shuffle, 'Shuffle')
    btn_shuffle.on_clicked(randomize_array)

    ax_reset = plt.axes([0.22, 0.90, 0.15, 0.04])
    btn_reset = Button(ax_reset, 'Reset')
    btn_reset.on_clicked(reset_array)

    ax_start = plt.axes([0.48, 0.90, 0.15, 0.04])
    btn_start = Button(ax_start, 'Start')
    btn_start.on_clicked(start_sorting)

    ax_stop = plt.axes([0.76, 0.90, 0.15, 0.04])
    btn_stop = Button(ax_stop, 'Stop')
    btn_stop.on_clicked(stop_sorting)

    update_2d_bar_chart(ax_main, arr_data, n, grid_size)

    print("Showing sorted array.")
    print("Click 'Shuffle' to randomize, 'Reset' to return to sorted.")
    print("Click 'Start' to begin bubble sort, 'Stop' to halt.")
    print("Close the window to exit.")

    plt.show()

if __name__ == "__main__":
    main()