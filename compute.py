import math
from matplotlib import pyplot as plt

def compute_entropy(data: dict):
    cnt = 0
    total_num = sum(list(data.values()))
    print(f'total word num: {total_num}')
    for k, v in data.items():
        p = v / total_num
        cnt += -p * math.log(p)
    print(f'entropy: {cnt}')

def zip_law(data: dict):
    cnt_list = data.values()
    sorted_cnt = sorted(enumerate(cnt_list), reverse=True, key=lambda x: x[1])
    plot_y = [item[1] for item in sorted_cnt[:1000]]
    plot_log_y = [math.log(item) for item in plot_y]
    print(plot_y)
    x = range(len(plot_y))
    plot_x = [item + 1 for item in x]
    plot_log_x = [math.log(item) for item in plot_x]
    plt.plot(plot_x, plot_y)
    plt.ylabel('Count')
    plt.xlabel('Order')

    # plt.plot(plot_log_x, plot_log_y)
    # plt.ylabel('Log Count')
    # plt.xlabel('Log Order')
    plt.title('Zipf\'s Law')
    plt.show()

