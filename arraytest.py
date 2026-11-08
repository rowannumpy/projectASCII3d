import random as ran
import matplotlib.pyplot as plt


def plotbar(arr):
    # init plotting
    x = 1
    y = 0
    fig, ax = plt.subplots()
    graph = ax.plot(x, y, color='g')[0]
    plt.ylim(0, 100)


def updatebar(arr):


def genarr():
    arr = ran.sample(range(1, 101), 100)
    return arr


def bubblesort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def main():
    arr = genarr()
    print(arr)
    bubblesort(arr)
    print(arr)


main()