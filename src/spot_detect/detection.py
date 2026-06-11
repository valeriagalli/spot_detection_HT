"""Module to implement spot detection."""

from skimage.filters import gaussian, threshold_otsu, threshold_yen
from skimage.measure import label, regionprops
import numpy as np


def remove_bg(image: np.ndarray, method: str, bg_sigma: float) -> np.ndarray:
    """
    Clean background noise and smooth the image channel.
    
    Parameters
    ----------
    image : np.ndarray
        The input channel image.
    method : str
        Method to remove background (e.g., Gaussian).
    bg_sigma: float
        
    
    Returns
    -------
    np.ndarray
        The cleaned image.
    
    Raises
    ------
    ValueError
        If method is not 'gaussian', i.e. parameters not (yet) configured.
    """
    if method == "gaussian":
        background = gaussian(image, sigma=bg_sigma, preserve_range=True)
        no_bg = image - background
        no_bg = np.clip(no_bg, 0, None) 
        return no_bg
    else:
        raise ValueError(f"Unknown background method: '{method}'."
                         "\nChoose 'gaussian' or add another method and corresponding parameters to the config.") # test


def smooth_image(image: np.ndarray, method: str, smooth_sigma: float) -> np.ndarray:
    """
    Smooth the image channel.
    
    Parameters
    ----------
    image : np.ndarray
        The input channel image.
    method : str
        Method to smooth the image (e.g., Gaussian).
    smooth_sigma: float
    
    Returns
    -------
    np.ndarray
        The smoothed image.
    
    Raises
    ------
    ValueError
        If method is not 'gaussian', i.e. parameters not (yet) configured.
    """
    if method == "gaussian":
        return gaussian(image, sigma=smooth_sigma, preserve_range=True)
    else:
        raise ValueError(f"Unknown background method: '{method}'."
                         "\nChoose 'gaussian' or add another method and corresponding parameters to the config.") # test


def detect_spots(smoothed_image: np.ndarray, method: str, manual_thresh: float, otsu_nbins: int) -> np.ndarray:
    """
    Apply thresholding to segment spots in the image.
    
    Parameters
    ----------
    smoothed_image : np.ndarray, The pre-processed image.
    method: str, 'manual', 'otsu', or 'yen'.
    manual_thresh: float, user-defined cut-off used if method='manual'.
    otsu_nbins: int, bins used for Otsu if method='otsu'. 

    Returns
    -------
    np.ndarray
        Boolean mask where True indicates detected spots.
    
    """
    if method == "manual":
        spots_mask = smoothed_image > manual_thresh
    elif method == "otsu":
        spots_mask = smoothed_image > threshold_otsu(smoothed_image, nbins=otsu_nbins)
    elif method == "yen":
        spots_mask = smoothed_image > threshold_yen(smoothed_image)
    else:
        raise ValueError(f"Invalid parameter for threshold method: '{method}'. Choose 'manual', 'otsu', or 'yen'.")
    # Labeling and counting
    labeled_mask = label(spots_mask) 
    n_spots = int(labeled_mask.max())
    labeled_mask_bool = labeled_mask.astype(bool)
    return n_spots, labeled_mask_bool   


def calculate_channel_statistics(channel_data: np.ndarray, channel_name: str) -> dict:
    """
    Calculate basic pixel statistics for each image channel.
    
    Parameters
    ----------
    img : np.ndarray
        Image channel from multichannel image.
    channel_name : str
        Name of the image channel.
    
    Returns
    -------
    statistics: dict
        Dictionary with basic statistics
    """
    stats = {}
    stats["channel"] = channel_name
    stats["mean"] = np.mean(channel_data)
    stats["std"] = np.std(channel_data)
    stats["min"] = np.min(channel_data)
    stats["max"] = np.max(channel_data)
    stats_rounded = {k: (round(v, 2) if isinstance(v, (int, float, np.number)) else v) for k, v in stats.items()}
    return stats_rounded


def calculate_overlap(mask_a: np.ndarray, mask_b: np.ndarray) -> tuple[int, float]:
    """Computes the total overlapping pixels and the percentage relative to the union.
    
    Parameters
    ----------
    mask_a : np.ndarray
        The first binary mask.
    mask_b : np.ndarray
        The second binary mask.
        
    Returns
    -------
    tuple[int, float]
        A tuple containing: number of overlap pixels, percentage of overlap.
    """
    union_mask = mask_a | mask_b
    union_sum = int(np.sum(union_mask))
    # Edge case: if both masks are completely empty to avoid dividing by zero
    if union_sum == 0:
        return 0, 0.0
    overlap_mask = mask_a & mask_b
    n_overlap = int(np.sum(overlap_mask))
    overlap_pct = 100.0 * n_overlap / union_sum
    return n_overlap, overlap_pct