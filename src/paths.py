
import pathlib

# Get the project directory as the parent of this module location
BASE = pathlib.Path(__file__).parents[1]

# Get the paths to the corpus
RAW_CORPUS = BASE / 'data' / 'raw'
RAW_CORPUS.mkdir(parents=True, exist_ok=True)

INTERIM_CORPUS = BASE / 'data' / 'interim'
INTERIM_CORPUS.mkdir(parents=True, exist_ok=True)

# Get paths to test data
TEST_DATA_DIRECTORY = BASE / 'src' / 'tests' / 'data'
TEST_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
