
import pathlib

# Get the project directory as the parent of this module location
BASE = pathlib.Path(__file__).parents[1]

# Get the paths to the corpus
RAW_CORPUS = BASE / 'data' / 'raw' / 'corpus'
INTERIM_CORPUS = BASE / 'data' / 'interim' / 'corpus'
