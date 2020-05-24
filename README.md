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
    - data is element of `graphDf` collection. Format: `Graph_Analysis_mm-dd-YYYY.

### Dependencies
All dependencies are defined in `Dockerfile` file.

This repository is connected with docker image: `tonibous/track-simulator`

To see more detail of code modules. See documentation in `doc` folder or check code documentation:
`open code-doc/_build/html/index.html`
