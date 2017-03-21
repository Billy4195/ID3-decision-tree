import numpy as np

class Node():
    def __init__(self,data):
        self.data = np.sort(data,order=['class'])
        self.right = None
        self.left = None
        self.threshold = -1
        self.leaf = True
        self.pure = True
        cur_label = self.data[0][4]
        cur_count = 1
        max_count = -1
        max_label = self.data[0][4]
        for instance in data:
            if instance[4] != cur_label:
                if cur_count > max_count:
                    max_label = cur_label
                    max_count = cur_count
                self.pure = False
                cur_label = instance[4] 
                cur_count = 1
            else:
                cur_count += 1
        self.label = max_label
