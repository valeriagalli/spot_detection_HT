# Spot Detection
Simple Python package for detecting fluorescent spots in a 2-channel microscopy image and computing the overlap (co-localization).
- **Channel 0**: DAPI (nuclear stain)
- **Channel 1**: GFP (protein of interest)


## Requirements
This project can be installed using either conda or pip.

- Python 3.10
- numpy
- scipy
- scikit-image
- matplotlib
- tifffile
- pytest
- jupyter


## Installation
**Navigate to the project directory:**
```bash
cd spot_detect
```
**With conda:**
```bash
cd spot_detect
conda env create -f environment.yml
conda activate spot-detect
```

**With pip:**
```bash
pip install -e .
```


## Usage

### Command line execution
You can run the detection pipeline entirely from the command line. 
To tweak parameters (like thresholds or background subtraction methods), update the values inside `config.json`.
Note: ch0 corresponds to DAPI, ch1 corresponds to GFP.

To run:
```bash
python run.py --config config.json
```

### Interactive exploration 
Alternatively, you can explore the step-by-step visualizations and analysis workflows interactively by opening the Jupyter notebook.
The parameter definitions inside the notebook cells are intentionally explicit to let you tune and test parameters visually before saving them to the main configuration file.

To open the notebook:
```bash
jupyter notebook notebooks/demo.ipynb
```

## Running tests
This project uses pytest to verify pipeline functions against synthetic test images. To execute the test suite, run:
```bash
pytest
```


## Project structure
```
│   .gitignore
│   config.json
│   environment.yml
│   LICENSE
│   README.md
│   run.py
│   setup.py
│
├───data
│   ├───output
│   └───raw_images
│           sample_image.tif
│
├───notebooks
│       demo_task.ipynb
│
├───src
│   └───spot_detect
│           detection.py
│           io.py
│           plots.py
│           __init__.py
│
└───tests
        test_detection.py
```

## Contribute 
If you would like to add new image processing algorithms:

1. **Background Removal:** Add your function to `src/spot_detect/detection.py` and update the `if/else` logic inside `remove_background`.
2. **Spot Detection:** Add your function to `src/spot_detect/detection.py` and update the options inside `count_spots`.
3. **Tests:** Add a new test function to `tests/test_detection.py` to verify your code works.


## License 
This project is licensed under the BSD 3-Clause License.


## TODO
- Switch to pip if the library is fully implemented in Python to avoid the need for conda.
- Improve robustness with error handling (e.g., add an `if` safety clause to handle a missing or corrupted `config.json` file.)
- Add missing tests for the other modules to ensure coverage (`io.py` and `plots.py`).
- Additional channels can be added by extending the channels section of `config.json`.
- Test compatibility with different Python versions and operating systems (CI).
