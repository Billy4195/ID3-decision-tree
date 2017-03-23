from tools import *
from tree import Node
import numpy as np

data = read_csv_file('iris.data')
data = np.array(data,dtype=[('sepal_len',float),('sepal_wid',float),('petal_len',float),('petal_wid',float),('class','S32')])
node_count = 0
node_count += 1
root = Node(data,node_count)
root.num = node_count
print(calc_entrophy(data))
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

    cur_node = find_node_to_split(cur_node)
draw_graph(root)
