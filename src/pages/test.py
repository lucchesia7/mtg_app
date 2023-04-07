import numpy as np


def solution(a: np.array) -> int:
    ind = 0
    result = 0
    while ind < len(a):
        for i in a:
            result += int(str(a[ind]) + str(i))
        ind += 1
    return result
if __name__ == '__main__':
    print(solution([0,2,4,7]))