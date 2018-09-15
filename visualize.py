import pickle
import matplotlib.pyplot as plt

def plot_draw_block(userList, recall):
    name_list = userList
    num_list = recall
    plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    plt.show()


def plot_draw_scatter(recall):
    x = range(0, len(recall))
    plt.scatter(x, recall,label='User',edgecolors=None)
    # help(plt.scatter)
    plt.xlabel('UserId')
    plt.ylabel('Precision')
    plt.title('Precision Percentage Graph')
    plt.legend()
    plt.show()


def plot_draw_TwoBlocks(userList, recall, precision):
    name_list = userList
    recall_list = recall
    precision_list = precision
    x = list(range(len(recall_list)))
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(x, recall_list, width=width, label='coverage percentage', fc='y')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, precision_list, width=width, label='precision percentage', tick_label=name_list, fc='r')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    path = './presentation/'
    with open(path+'top30_large_1wcoverage_500') as f1:
        w_recall = pickle.load(f1)
    with open(path+'top30_large_1wprecision_500') as f2:
        w_precision = pickle.load(f2)
    with open(path+'top30_large_1wuser_500') as f3:
        w_user = pickle.load(f3)
    mean_recall = 0
    mean_precision = 0
    for i in w_recall:
        mean_recall += i
    mean_recall /= len(w_recall)

    for m in w_precision:
        mean_precision += m
    mean_precision /= len(w_precision)

    # plot_draw_TwoBlocks(w_user,w_recall,w_precision)
    plot_draw_scatter(w_precision)
    # plot_draw_scatter(w_recall)
    # print(mean_recall)
    print(mean_precision)
