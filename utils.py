import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;sns.set()


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


def plot_accumultaive_distribution(data, ser_data):
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
