import numpy as np

class ArrayManipulator:
    def __init__(self, array):
        self.array = np.array(array)
        self.base = [7, 7]

    def rotate_flip(self, angle, flip):
        result = self.array
        
        if angle == 90:
            result = np.rot90(result, k=-1)
            self.base = [8, 7]
        elif angle == 180:
            result = np.rot90(result, k=2)
            self.base = [8, 8]
        elif angle == 270:
            result = np.rot90(result, k=1)
            self.base = [7, 8]
        else:
            self.base = [7, 7]

        if flip:
            result = np.flip(result, axis=1)
            self.base = [self.base[1], self.base[0]]
        self.array = result

x = ArrayManipulator([[1, 0], [0, 0]])
x.rotate_flip(90, True)
print(x.base)
print(x.array)