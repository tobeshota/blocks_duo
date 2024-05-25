import numpy as np

class ArrayManipulator:
    def __init__(self, array):
        self.original_array = np.array(array)
        self.array = np.array(array)
        self.base = [7, 7]

    def rotate_flip(self, angle, flip):
        result = self.original_array

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

    def __getitem__(self, index):
        angle = (index % 4) * 90
        flip = (index // 4) % 2 == 1
        self.rotate_flip(angle, flip)
        return {"array": self.array, "base": self.base}

# 使用例
some_array = [[1, 2], [3, 4]]
x = ArrayManipulator(some_array)

print("回転なし、反転なし:", x[0])
print("回転なし、反転あり:", x[1])
print("90度回転、反転なし:", x[2])
print("90度回転、反転あり:", x[3])
print("180度回転、反転なし:", x[4])
print("180度回転、反転あり:", x[5])
print("270度回転、反転なし:", x[6])
print("270度回転、反転あり:", x[7])
