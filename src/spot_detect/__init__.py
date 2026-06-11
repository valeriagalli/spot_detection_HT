"""A modular pipeline for fluorescent spot detection and counting."""

from .detection import remove_bg, smooth_image, detect_spots
from .io import load_image, save_mask, print_image_info
from .plots import plot_channel, plot_overlay
