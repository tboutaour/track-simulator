import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns;

sns.set()
from datetime import datetime
import os
import math
import track_simulator.entities.track_point as Point


def get_random_value(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))


def generate_accumulative_distribution(data):
    # Generación distribucion acumulada
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    return ser_dx


# plot
def plot_accumultaive_distribution(data):
    fig, ax = plt.subplots()

    ax = data.plot(drawstyle='steps', legend="True")
    ax.set_xlabel("Meters", fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.legend().set_visible(False)
    ax.grid(True)
    fig.canvas.draw()


# plt.savefig('distDist.eps', format='eps', dpi=600)

def generate_value_from_distribution(data):
    rnd = np.random.random()
    return np.argmax(data > rnd)


def add_dataframe_id(data, track_id):
    data['id'] = track_id
    aux_cols = data.columns.tolist()
    aux_cols = aux_cols[-1:] + aux_cols[:-1]
    return data[aux_cols]


def join_track_projection_data(track, projection, track_id):
    point_df = pd.DataFrame(track, columns=['Point'])
    projected_df = pd.DataFrame(projection, columns=['Projection', 'Origin', 'Target'])
    main_df = pd.concat([point_df, projected_df], axis=1)
    main_df['id_track'] = 200
    return add_dataframe_id(main_df, track_id)


def plot_accumultaive_distribution(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_data = pd.Series(cd_dx, index=data)
    fig, ax = plt.subplots()
    ax = pd.Series(ser_data, index=np.array(data)).plot(drawstyle='steps', legend="True")
    ax.set_xlabel("Meters", fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.legend().set_visible(False)
    ax.grid(True)
    fig.canvas.draw()


def plot_histogram(data, axis):
    sns.distplot(data, color="blue", ax=axis)


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
    today = datetime.utcnow()
    str_day = today.strftime('%Y%m%d_%H%M') + "00"
    folder_path = path + "/" + str_day
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        print("Directory already exists, adding information.")
    return folder_path
