# TrackSimulator
TrackSimulator is an application for track analysis and simulation in a 
delimited territory. It uses Viterbi algorithm and Hidden Markov Model
for map-matching. Information is stored in MongoDB.

### User guide
Dependencies
-   You need to have installed docker in your machine.

### Installation
Installation is done by `/bin/install.sh` script.

### Use
It is need to get a folder for all the application work. By default,
a `track-simulator` folder is created in `$HOME` path.

`track-simulator` folder is composed by:
- `config`: stores docker-compose file.
- `data`: stores analysis result files.
- `db`: mongoDB files.
- `analysis`: stores files for analysis input.

Available actions:
- Track analysis: `ts-cli analysis [--file_directory]`
    - file_directory should be a `track-simulator/analyze` subpath.
- Track simulation: `ts-cli simulate [--distance, --origin_node, --data, --quantity]`
    - distance in meters
    - origin node from OSM determination points.
    - data is element of `graphDf` collection. Format: `Graph_Analysis_mm-dd-YYYY`.

### Dependencies
All dependencies are defined in `Dockerfile` file.

This repository is connected with docker image: `tonibous/track-simulator`

To see more detail of code modules. See documentation in `doc` folder or check code documentation:
`open code-doc/_build/html/index.html`


### Available environment variables:

| Tables                                | Description                                       | Required  | Default value                 |
| --------------------------------------|:-------------------------------------------------:|:----------|------------------------------:|
| PATH                                  | Path where the executable will be                 | Yes       | `/opt/bin`                    |
| PYTHONPATH                            | Path where python app will be                     | Yes       | `/app`                        |
| RUNPATH                               | Path where main will be                           | Yes       | `/app/track_simulator/main`   |
| MONGO_HOST                            | Mongo host                                        | Yes       | `db`                          |          
| MONGO_PORT                            | Mongo port                                        | Yes       | `27017`                       |
| MONGO_DATABASE                        | Database for track-simulator                      | Yes       | `trackdb`                     |
| MONGO_GRAPH_INFORMATION_COLLECTION    | Database collection for information               | Yes       | `graphdf`                     |
| MONGO_TRACK_INFORMATION_COLLECTION    | Database collection for track information         | Yes       | `trackdf`                     |
| MONGO_TRACK_STATISTICS_COLLECTION     | Database collection for statistics information    | Yes       | `statisticsDf`                |
| LAST_VERSION_GRAPH                    | Default version of graph in MongoDB               | Yes       | `Graph_Analysis_05-16-2020`   |
| ROOT_DIRECTORY                        | Root directory of app                             | Yes       | `/app`                        |
| FILE_DIRECTORY                        | Directory where analysis tracks are stored        | Yes       | `/analysis`                   |
| EXPORT_ANALYSIS_IMAGES_FOLDER         | Directory where analysis results are stored       | Yes       | `/data/analysis/statistics`   |
| EXPORT_SIMULATIONS_GPX_FOLDER         | Directory where simulation gpx files are stored   | Yes       | `/data/simulation/gpx`        |
| EXPORT_SIMULATIONS_IMAGES_FOLDER      | Directory where simulation images are stored      | Yes       | `/data/simulation/images`     |
| NORTH_COMPONENT                       | North component for analyze-simulate              | Yes       | `39.5713`                     |
| SOUTH_COMPONENT                       | South component for analyze-simulate              | Yes       | `39.5573`                     |
| EAST_COMPONENT                        | East component for analyze-simulate               | Yes       | `2.6257`                      |
| WEST_COMPONENT                        | West component for analyze-simulate               | Yes       | `2.6023`                      |
| GENERATION_DISTANCE                   | Distance if statistics not loaded                 | Yes       | `20`                          |
| DESTINATION_NODE_THRESHOLD            | Maximum distance threshold for simulate segment   | Yes       | `24`                          |