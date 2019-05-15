 Brexit in Transnational Social Media
==============================

This repo is my work for the *Brexit in Transnational Social Media* theme in the [Helsinki Digital Humanities Hackathon #DHH19](https://www.helsinki.fi/en/helsinki-centre-for-digital-humanities/helsinki-digital-humanities-hackathon). 

It is currently in early development. 

## Getting Started

Two `make` commands allow you to recreate the environment used in this analysis. Use

- `make create_environment` for the initial creation of the environment
    + when prompted, enter `conda activate brexit_in_transnational_social_media` (if you are using conda as your package manager)
- `make requirements` to get the required packages.

You can test whether your environment is set up correctly with `make test_environment`.

To see which other `make` rules are available as well a description of what they do, simply use `make help`. 


## Data
The assumption here is that the raw data exists in a `data/raw` directory in the form of line-delineated JSON. (You can specify the path in `src/paths.py`). Should you wish to transform the data to `.csv` files, run `make transform`. The output will appear in `data/interim` directory (an alternative directory can again be specified in `src/paths.py`). 


## Tests
After installing the required packages, you can run the tests by entering `pytest` in the terminal. 
