"""Minimal testing for core functionalities."""
import pytest
import numpy as np
from src.spot_detect.detection import remove_bg, detect_spots


def test_remove_bg_invalid_method():
    """Ensure that invalid background removal method raises error."""
    dummy_img = np.zeros((50, 50))
    invalid_method = "abcd"
    with pytest.raises(ValueError):
        remove_bg(image=dummy_img, method=invalid_method, bg_sigma=1.0)


def test_detect_spots_empty_image():
    """Ensure an image with no signal returns zero detected spots."""
    # Create a 50x50 blank black image
    dummy_img = np.zeros((50, 50))
    # Run pipeline with a manual threshold
    count, _ = detect_spots(dummy_img, method='manual', manual_thresh=100, otsu_nbins=None)
    assert count == 0


def test_detect_spots_single_spot():
    """Ensure a single clear bright spot is counted correctly."""
    # Create a 50x50 black image
    dummy_img = np.zeros((50, 50))
    # Place a single bright square in the middle
    dummy_img[20:30, 20:30] = 255
    # Run pipeline
    count, _ = detect_spots(dummy_img, method='manual', manual_thresh=100, otsu_nbins=None)
    assert count == 1