import matplotlib.cm as cm
import numpy as np
import seaborn as sns;

sns.set()
from datetime import datetime
import os


def get_color_list(n, color_map='plasma', start=0, end=1):
    return [cm.get_cmap(color_map)(x) for x in np.linspace(start, end, n)]


def get_node_colors_by_stat(data, criteria, start=0, end=1):
    df = data.sort_values(criteria)
    df['colors'] = get_color_list(len(df), start=start, end=end)
    return df['colors']


def plot_points(ax, t, color):
    for a in t:
        lat = a[1]
        lon = a[0]
        ax.scatter(lon, lat, c=color, s=20)


def plot_example_emission_prob():
    """
    Function to plot emission probability given values of SIGMA
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import math
    import matplotlib.cm as cm
    fig = plt.figure()
    SIGMA = np.array(range(10))
    # Create the vectors X and Y
    x = np.array(range(40))
    colors = cm.rainbow(np.linspace(0, 1, len(SIGMA)))
    for sigma in SIGMA:
        c = (1 / (sigma * math.sqrt(2 * math.pi)))
        y = c * math.e ** (-0.5 * ((x / sigma) ** 2))

        # Create the plot
        plt.plot(x, y, color=colors[sigma], label="SIGMA=" + str(sigma))
        plt.legend()
    # Show the plot
    fig.suptitle('Emission probability given ditance point-projection', fontsize=10)
    plt.xlabel('distance point-projection in meters', fontsize=9)
    plt.ylabel('emission probabilitiy', fontsize=9)
    plt.show()


def plot_example_transition_prob():
    """
    Function to plot transition probability given values of BETA
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import math
    import matplotlib.cm as cm
    fig = plt.figure()
    BETA = np.around(np.linspace(0, 1, 11), 2)
    # Create the vectors X and Y
    x = np.array(range(12))
    colors = cm.rainbow(np.linspace(0, 1, len(BETA)))
    for idx, beta in np.ndenumerate(BETA):
        y = (1 / beta) * math.e ** (-(abs(x)))

        # Create the plot
        plt.plot(x, y, color=colors[idx], label="BETA=" + str(beta))
        plt.legend()
    # Show the plot
    fig.suptitle('Transition probability given track distance', fontsize=10)
    plt.xlabel('track distance in nodes', fontsize=9)
    plt.ylabel('transition probabilitiy', fontsize=9)
    plt.show()


def create_folder(path):
    """
    Function to create folder with timestamp
    :param path: Destination folder path to add directory
    :return:
    """
    today = datetime.utcnow()
    str_day = today.strftime('%Y%m%d_%H%M') + "00"
    folder_path = path + "/" + str_day
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        print("Directory already exists, adding information.")
    return folder_path
