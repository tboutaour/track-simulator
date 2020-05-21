FROM python:3.6-slim
ENV PATH "$PATH:/opt/bin"
ENV PYTHONPATH "/app"
ENV RUNPATH "/app/track_simulator/main"
ENV MONGO_HOST "db"
ENV MONGO_PORT 27017
ENV MONGO_DATABASE "trackdb"
ENV MONGO_GRAPH_INFORMATION_COLLECTION "graphDf"
ENV MONGO_TRACK_INFORMATION_COLLECTION "trackDf"
ENV MONGO_TRACK_STATISTICS_COLLECTION "statisticsDf"
ENV LAST_VERSION_GRAPH "Graph_Analysis_05-16-2020"
ENV ROOT_DIRECTORY "/app"
ENV FILE_DIRECTORY "/analysis"
ENV EXPORT_ANALYSIS_IMAGES_FOLDER "/data/analysis/statistics"
ENV EXPORT_SIMULATIONS_GPX_FOLDER "/data/simulation/gpx"
ENV EXPORT_SIMULATIONS_IMAGES_FOLDER "/data/simulation/images"
ENV NORTH_COMPONENT 39.5713
ENV SOUTH_COMPONENT 39.5573
ENV EAST_COMPONENT 2.6257
ENV WEST_COMPONENT 2.6023

COPY src /app
COPY bin /opt/bin
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran libspatialindex-dev

ADD requirements.txt .
RUN pip3 install -r requirements.txt
ARG command