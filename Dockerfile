FROM python:3.6-slim
ENV PATH "$PATH:/opt/bin"
ENV PYTHONPATH "/app"
ENV RUNPATH "$PYTHONPATH/track_analyzer/main"
ENV MONGO_HOST "db"
ENV MONGO_PORT 27017
ENV MONGO_DATABASE "tracksimulatordbbatchsimulate"
ENV MONGO_GRAPH_INFORMATION_COLLECTION "graphDataframeSimulated"
ENV MONGO_TRACK_INFORMATION_COLLECTION "trackDataframe"
ENV MONGO_TRACK_STATISTICS_COLLECTION "trackStatistics"
ENV LAST_VERSION_GRAPH "Graph_Analysis_05-02-2020"

# Files directories
ENV ROOT_DIRECTORY "/app"
ENV FILE_DIRECTORY ""
ENV EXPORT_ANALYSIS_IMAGES_FOLDER "/data/simulation/gpx/gpx_to_analyze"
ENV EXPORT_SIMULATIONS_GPX_FOLDER "/data/simulation/gpx"
ENV EXPORT_SIMULATIONS_IMAGES_FOLDER "/data/simulation/images"

COPY src /app
COPY bin /opt/bin
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran libspatialindex-dev

ADD requirements.txt .
RUN pip3 install -r requirements.txt
ARG command