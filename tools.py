import csv
import math

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
    if not(left is None):
        return left

    right = find_node_to_split(node.right)
    if not(right is None):
        return right

    return None

def find_mini_rem_feature(node):
    best_rem = float('inf')
    best_thre = float('inf')
    best_index = -1
    for i in range(4):
        cur_rem,cur_thre = find_mini_entrophy_threshold(node,i)
        print(cur_rem,cur_thre)
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
