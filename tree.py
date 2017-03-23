import numpy as np

class Node():
    def __init__(self,data,num=None):
        self.data = np.sort(data,order=['class'])
        self.right = None
        self.left = None
        self.threshold = -1
        self.threshold_index = -1
        self.leaf = True
        self.pure = True
        self.num = num
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
    def set_threshold(self,threshold):
        self.threshold = threshold

    def set_threshold_index(self,index):
        self.threshold_index = index
