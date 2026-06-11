"""Module to read images."""

import tifffile
import numpy as np


def print_image_info(image):
    """Prints dimensions, data type, and pixel value ranges of an image."""
    print("Image shape:", image.shape)
    print("Image data type:", image.dtype)
    print("Image data ranges:(min, max)", np.min(image), np.max(image))


def load_image(fp: str):
    """Loads a TIFF image from the specified file path."""
    return tifffile.imread(fp)


def save_mask(mask, fp: str):
    """Saves a binary or labeled mask array as a TIFF file."""
    tifffile.imwrite(fp, mask)
    print(f"Saving mask to {fp}")
