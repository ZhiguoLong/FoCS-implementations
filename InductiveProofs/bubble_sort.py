
def bubble_sort(arr):
    """
    Algorithm 2: Bubble sort algorithm
    Input: arr: a list of numbers
    Output: arr: a (in-place) sorted list of numbers in ascending order
    """
    swap = True
    n = len(arr)
    while swap:
        swap = False
        for i in range(n-1):
                if arr[i] > arr[i+1]:
                    arr[i], arr[i+1] = arr[i+1], arr[i]
                    swap = True

if __name__ == '__main__':
    arr = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort(arr)
    print(arr)
