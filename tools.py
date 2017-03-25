import csv
import math
import pygraphviz as GP

def read_csv_file(filename):
    data = []
    with open(filename) as csvfile:
        content = csv.reader(csvfile,delimiter=',')
        for row in content:
            if len(row) > 0:
                row[0] = float(row[0])
                row[1] = float(row[1])
                row[2] = float(row[2])
                row[3] = float(row[3])
                data.append(tuple(row))

    return data

def find_node_to_split(node):
    if node is None:
        return None

    if not node.pure and node.leaf:
        return node

    left = find_node_to_split(node.left)
    if not(left is None) and len(left.data) > 10:
        return left

    right = find_node_to_split(node.right)
    if not(right is None) and len(right.data) > 10:
        return right

    return None

def find_mini_rem_feature(node):
    best_rem = float('inf')
    best_thre = float('inf')
    best_index = -1
    for i in range(4):
        cur_rem,cur_thre = find_mini_entrophy_threshold(node,i)
        if cur_rem < best_rem:
            best_rem = cur_rem
            best_thre = cur_thre
            best_index = i

    return (best_rem,best_thre,best_index)

def find_mini_entrophy_threshold(node,feature_index):
    sorted_data = sorted(node.data,key=lambda inst:inst[feature_index])
    best_entrophy = float('inf')
    best_thre = float('inf')
    cur_entrophy = float('inf')
    cur_thre = float('inf')
    for idx in range(len(sorted_data)):
        if cur_thre == sorted_data[idx][feature_index]:
            continue
        cur_thre = sorted_data[idx][feature_index]
        (left,right) = split(sorted_data,feature_index,cur_thre)
        cur_entrophy = calc_entrophy(left) * (len(left)/len(sorted_data)) + calc_entrophy(right) * (len(right)/len(sorted_data))
        if cur_entrophy < best_entrophy:
            best_thre = cur_thre
            best_entrophy = cur_entrophy

    return (best_entrophy,best_thre)

def split(dataset,feature_index,threshold):
    left = []
    right = []
    for instance in dataset:
        if instance[feature_index] < threshold:
            left.append(instance)
        else:
            right.append(instance)

    return left,right

def calc_entrophy(dataset):
    count = {}
    total_count = 0
    for instance in dataset:
        if not instance[4] in count:
            count[instance[4]] = 1
            total_count += 1
        else:
            count[instance[4]] += 1
            total_count += 1
    entrophy = 0
    for key in count:
        prob = count[key]/total_count
        entrophy += -prob * math.log2(prob)

    return entrophy

def index_to_feature_name(index):
    if index == 0:
        return "sepal_length"
    elif index == 1:
        return "sepal_width"
    elif index == 2:
        return "petal_length"
    elif index == 3:
        return "petal_width"
    else:
        return "unknown feature"

def get_node_label(node):
    if node.leaf:
        return '"%d\\n%s"' % (node.num,node.label.decode('utf-8'))
    else:
        return '"%d\\n%s"' % (node.num,index_to_feature_name(node.threshold_index))

def find_next_node(node):
    if node == None:
        return None
    if node.left:
        return node.left
    if node.right:
        return node.right
    return None

def draw_graph(root):
    node_list = []
    node_count = 1
    Graph = GP.AGraph()
    if root.leaf:
        Graph.add_node(get_node_label(root),shape='circle')
    else:
        Graph.add_node(get_node_label(root),shape='box')
        node_list.append(root)
    fp = open('tree.dot','w')
    print("digraph {",file=fp)
    while len(node_list):
        cur_node = node_list.pop(0)
        par_label = get_node_label(cur_node)
        if cur_node.leaf:
            print('\t%s\t [shape=oval];' % par_label,file=fp)
        else:
            print('\t%s\t [shape=box];' % par_label,file=fp)
        if cur_node.left:
            left_label = get_node_label(cur_node.left)
            Graph.add_node(left_label)
            edge_label = '"%s < %f"' % (index_to_feature_name(cur_node.threshold_index),cur_node.threshold)
            Graph.add_edge(par_label,left_label,label=edge_label)
            print('\t%s -> %s \t [label=%s];' % (par_label,left_label,edge_label),file=fp)
            node_list.append(cur_node.left)
        if cur_node.right:
            right_label = get_node_label(cur_node.right)
            Graph.add_node(right_label)
            edge_label = '"%s >= %f"' % (index_to_feature_name(cur_node.threshold_index),cur_node.threshold)
            Graph.add_edge(par_label,right_label,label=edge_label)
            print('\t%s -> %s \t [label=%s];' % (par_label,right_label,edge_label),file=fp)
            node_list.append(cur_node.right)

    print("}",file=fp)

def instance_classify(node,instance):
    if node.leaf:
        return node.label
    if instance[node.threshold_index] < node.threshold:
        return instance_classify(node.left,instance)
    else:
        return instance_classify(node.right,instance)

def validate_tree(root,test_data):
    success_count = 0
    fail_count = 0
    for instance in test_data:
        label = instance_classify(root,instance)
        if label == instance[4]:
            success_count += 1
        else:
            fail_count += 1

    print(success_count/(success_count+fail_count))
