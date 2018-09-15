import visualize
import csv
import matplotlib.pyplot as plt

def draw_compare_curve(small, large):
    small_precision = []
    small_recall = []
    large_precision = []
    large_recall = []
    topN = []
    with open(small) as small_data:
        reader1 = csv.DictReader(small_data)
        for row in reader1:
            small_precision.append(float(row['precision']))
            small_recall.append(float(row['recall']))
            topN.append(int(row['TopN']))

    with open(large) as large_data:
        reader2 = csv.DictReader(large_data)
        for row in reader2:
            large_precision.append(float(row['precision']))
            large_recall.append(float(row['recall']))

    range_x = topN
    plt.plot(range_x, small_recall, label='10k 100users', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=8)
    plt.plot(range_x, large_recall, label='100k 100users', linewidth=3, color='g', marker='o',
             markerfacecolor='yellow', markersize=8)

    plt.xlabel('TopN Recommendation List')
    plt.ylabel('Recall Percentage')
    plt.title('Recall Percentage Comparison under 10k/100k movies\n')
    plt.legend()
    plt.show()

    plt.plot(range_x, small_precision, label='100 Users', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=8)
    plt.plot(range_x, large_precision, label='500 Users', linewidth=3, color='g', marker='o',
             markerfacecolor='yellow', markersize=8)
    plt.xlabel('TopN Recommendation List')
    plt.ylabel('Precision Percentage')
    plt.title('Precision Percentage Comparison under 10k/100k movies\n')
    plt.legend()
    plt.show()

def draw_TwoBlocks(small, large):
    small_recall = []
    small_precision = []
    large_recall = []
    large_precision = []
    topN = []
    with open(small) as small_data:
        reader1 = csv.DictReader(small_data)
        for row in reader1:
            small_precision.append(float(row['precision']))
            small_recall.append(float(row['recall']))
            topN.append(int(row['TopN']))

    with open(large) as large_data:
        reader2 = csv.DictReader(large_data)
        for row in reader2:
            large_precision.append(float(row['precision']))
            large_recall.append(float(row['recall']))

    plt.title('Recall Percentage Comparison under 10k movies\nwith different users')
    plt.xlabel('TopN Recommendation List')
    plt.ylabel('Recall Percentage')
    x = topN
    total_width, n = 8, 2
    width = total_width / n
    plt.bar(x, small_recall, width=width, label='100 Users', fc='b')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, large_recall, width=width, label='500 Users', fc='r')
    plt.legend()
    plt.show()

    plt.title('Precision Percentage Comparison under 10k movies\nwith different users')
    plt.xlabel('TopN Recommendation List')
    plt.ylabel('Precision Percentage')
    x = topN
    total_width, n = 8, 2
    width = total_width / n
    plt.bar(x, small_precision, width=width, label='100 Users', fc='b')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, large_precision, width=width, label='500 Users', fc='r')
    plt.legend()
    plt.show()

# draw_compare_curve('./10000_small.csv','./100000_100users.csv')
draw_TwoBlocks('./10000_small.csv','./10000.csv')