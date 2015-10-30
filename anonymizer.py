"""
run semi_partition with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from semi_partition import semi_partition
from utils.read_data import read_data
from utils.read_data import read_tree
import sys, copy, random
# sys.setrecursionlimit(500000)

__DEBUG = True


def get_result_one(att_trees, data, k=10):
    "run semi_partition for one time, with k=10"
    print "K=%d" % k
    print "Mondrian"
    data_back = copy.deepcopy(data)
    _, eval_result = semi_partition(att_trees, data, k)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + "seconds"
    print "Missing Pollution = %.2f %%" % eval_result[2]


def get_result_k(att_trees, data):
    """
    change k, whle fixing QD and size of dataset
    """
    data_back = copy.deepcopy(data)
    all_ncp = []
    all_rtime = []
    all_pollution = []
    # for k in range(5, 105, 5):
    for k in [2, 5, 10, 25, 50, 100]:
        _, eval_result = semi_partition(att_trees, data, k)
        data = copy.deepcopy(data_back)
        all_ncp.append(round(eval_result[0], 2))
        all_rtime.append(round(eval_result[1], 2))
        all_pollution.append(round(eval_result[2], 2))
        if __DEBUG:
            print '#' * 30
            print "K=%d" % k
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
            print "Missing Pollution = %.2f %%" % eval_result[2]
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution


def get_result_dataset(att_trees, data, k=10, n=10):
    """
    fix k and QI, while changing size of dataset
    n is the proportion nubmber.
    """
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % k
    joint = 5000
    datasets = []
    check_time = length / joint
    if length % joint == 0:
        check_time -= 1
    for i in range(check_time):
        datasets.append(joint * (i + 1))
    datasets.append(length)
    all_ncp = []
    all_rtime = []
    all_pollution = []
    for pos in datasets:
        ncp = rtime = pollution = 0
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(n):
            temp = random.sample(data, pos)
            result, eval_result = semi_partition(att_trees, temp, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            pollution += eval_result[2]
            data = copy.deepcopy(data_back)
            # save_to_file((att_trees, temp, result, k, L))
        ncp /= n
        rtime /= n
        pollution /= n
        if __DEBUG:
            print "Average NCP %0.2f" % ncp + "%"
            print "Running time %0.2f" % rtime + "seconds"
            print "Missing Pollution = %.2f %%" % pollution + "%"
        all_ncp.append(round(eval_result[0], 2))
        all_rtime.append(round(eval_result[1], 2))
        all_pollution.append(round(eval_result[2], 2))
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution


def get_result_qi(att_trees, data, k=10):
    """
    change nubmber of QI, whle fixing k and size of dataset
    """
    data_back = copy.deepcopy(data)
    ls = len(data[0])
    all_ncp = []
    all_rtime = []
    all_pollution = []
    for i in reversed(range(1, ls)):
        _, eval_result = semi_partition(att_trees, data, k, i)
        data = copy.deepcopy(data_back)
        all_ncp.append(round(eval_result[0], 2))
        all_rtime.append(round(eval_result[1], 2))
        all_pollution.append(round(eval_result[2], 2))
        if __DEBUG:
            print '#' * 30
            print "Number of QI=%d" % i
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
            print "Missing Pollution = %.2f %%" % eval_result[2]
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution


if __name__ == '__main__':
    FLAG = ''
    # redirout = open('log.txt', 'w')
    # sys.stdout = redirout
    LEN_ARGV = len(sys.argv)
    try:
        FLAG = sys.argv[1]
    except:
        pass
    k = 10
    RAW_DATA = read_data()
    ATT_TREES = read_tree()
    print '#' * 30
    if FLAG == 'k':
        get_result_k(ATT_TREES, RAW_DATA)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, RAW_DATA)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, RAW_DATA)
    elif FLAG == 'one':
        if LEN_ARGV > 1:
            k = int(sys.argv[2])
            get_result_one(ATT_TREES, RAW_DATA, k)
        else:
            get_result_one(ATT_TREES, RAW_DATA)
    elif FLAG == '':
        get_result_one(ATT_TREES, RAW_DATA)
    else:
        print "Usage: python anonymizer [k | qi | data | one]"
        print "k: varying k, qi: varying qi numbers, data: varying size of dataset, \
                one: run only once"
    # anonymized dataset is stored in result
    print "Finish Semi_Partition!!"
    # redirout.close()
