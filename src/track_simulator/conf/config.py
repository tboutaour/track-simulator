import os

# MongoDB
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_DATABASE = os.environ.get('MONGO_DATABASE')
MONGO_GRAPH_INFORMATION_COLLECTION = 'graphDataframe'
MONGO_TRACK_INFORMATION_COLLECTION = 'trackDataframe'
MONGO_TRACK_STATISTICS_COLLECTION = os.environ.get('MONGO_TRACK_STATISTICS_COLLECTION')
LAST_VERSION_GRAPH = os.environ.get('LAST_VERSION_GRAPH')

# Files directories
ROOT_DIRECTORY = os.environ.get('ROOT_DIRECTORY')
FILE_DIRECTORY = os.environ.get('FILE_DIRECTORY')
EXPORT_ANALYSIS_IMAGES_FOLDER = os.environ.get('EXPORT_ANALYSIS_IMAGES_FOLDER')
EXPORT_SIMULATIONS_GPX_FOLDER = os.environ.get('EXPORT_SIMULATIONS_GPX_FOLDER')
EXPORT_SIMULATIONS_IMAGES_FOLDER = os.environ.get('EXPORT_SIMULATIONS_IMAGES_FOLDER')