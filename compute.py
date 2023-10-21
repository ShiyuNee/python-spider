import math
from matplotlib import pyplot as plt

def compute_entropy(data: dict):
    cnt = 0
    total_num = sum(list(data.values()))
    print(total_num)
    for k, v in data.items():
        p = v / total_num
        cnt += -p * math.log(p)
    print(cnt)

def chef_theory(data: dict):
    cnt_list = data.values()
    sorted_cnt = sorted(enumerate(cnt_list), reverse=True, key=lambda x: x[1])
    
    plot_y = [item[1] for item in sorted_cnt[:500]]
    print(plot_y)
    x = range(len(plot_y))
    plot_x = [item + 1 for item in x]
    plt.plot(plot_x, plot_y)
    plt.show()

