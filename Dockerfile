FROM python:3.6-slim
COPY src /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran libspatialindex-dev

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash"]