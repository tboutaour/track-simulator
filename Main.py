from entities.Graph_impl import Graph
from entities.HMMMapMatching_impl import MapMatching
from entities.HiddenMarkovModel_impl import HMM
from entities.GPXLoaderSaver_impl import GPXLoaderSaver as LoaderSaver
from entities.TrackAnalyzerStatistics_impl import TrackAnalyzerStatistics as Statistics
import entities.TrackAnalyzerStatistics_impl as TrackAnalizerStatistics
import matplotlib.pyplot as plt
import pandas as pd
import osmnx
import numpy as np
import seaborn as sns; sns.set()


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


def plot_histogram(data, axis):
    sns.distplot(data, color="blue", ax=axis)


def generate_value_from_distribution(data):
    rnd = np.random.random()
    return np.argmax(data > rnd)


test_file = LoaderSaver("tracks/Ficheros/rutasMFlores/activity_3689734814.gpx")
bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
hidden_markov_model = HMM(graph=bellver_graph)
fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
points = list(list(zip(*test_file.parseFile()))[2])
hmm = MapMatching(points, hidden_markov_model)
points.pop()
mapped_points = hmm.match()
point_df = pd.DataFrame(points, columns=['Point'])
projected_df = pd.DataFrame(mapped_points, columns=['Projection', 'Origin', 'Target'])
main_df = pd.concat([point_df, projected_df], axis=1)
print(main_df)
statistics = Statistics(bellver_graph, main_df)
statistics.get_distance_point_projection()
distance_point_projection = list(statistics.dataset['Point_projection_distance'])
# distance_point_projection.pop()
distance_between_points = statistics.get_distance_between_points()
for r in mapped_points:
    plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
    print(r)
plt.show()

_, ax1 = plt.subplots()
plot_histogram(distance_point_projection, ax1)

_, ax2 = plt.subplots()
plot_histogram(distance_between_points, ax2)

plot_accumultaive_distribution(TrackAnalizerStatistics.generate_accumulative_distribution(distance_point_projection))

plot_accumultaive_distribution(TrackAnalizerStatistics.generate_accumulative_distribution(distance_between_points))