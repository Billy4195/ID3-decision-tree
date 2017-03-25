from tools import *
from tree import Node
import numpy as np
import sys

def ID3(K):
    data = read_csv_file('iris.data')
    data = np.array(data,dtype=[('sepal_len',float),('sepal_wid',float),('petal_len',float),('petal_wid',float),('class','S32')])
    np.random.shuffle(data)
    arraylist = np.split(data,K)
    for idx in range(K):
        training_data = arraylist[0]
        testing_data = arraylist[idx]
        for i in range(1,K):
            if K != 1 and not i == idx:
                training_data = np.append(training_data,arraylist[i])
        node_count = 1
        root = Node(training_data,node_count)
        root.num = node_count
        cur_node = find_node_to_split(root)
        while cur_node != None:
            (best_rem,best_thre,best_index) = find_mini_rem_feature(cur_node)
            left,right = split(cur_node.data,best_index,best_thre)
            cur_node.set_threshold(best_thre)
            cur_node.set_threshold_index(best_index)
            node_count += 1
            cur_node.left = Node(left,node_count)
            node_count += 1
            cur_node.right = Node(right,node_count)
            cur_node.leaf = False
            cur_node = find_node_to_split(root)
        draw_graph(root)

        validate_tree(root,testing_data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        K = int(sys.argv[1])
        ID3(K)
    else:
        ID3(1)

