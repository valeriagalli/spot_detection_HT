"""Module for visualization."""

import matplotlib.pyplot as plt
import numpy as np


def plot_channel(raw, smooth, mask, title):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(raw, cmap="gray")
    axes[0].set_title("raw channel")
    axes[1].imshow(smooth, cmap="gray")
    axes[1].set_title("smoothed channel")
    axes[2].imshow(mask, cmap="gray")
    axes[2].set_title("spots detected")
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    return fig


def plot_overlay(mask0, mask1):
    """Builds an RGB composite overlay and either shows it or saves it."""
    # Build RGB composite: DAPI=red, GFP=green
    rgb = np.zeros((mask0.shape[0], mask0.shape[1], 3), dtype=np.uint8)
    mask0 = mask0.astype(bool)
    mask1 = mask1.astype(bool)
    rgb[mask0, 0] = 255  # red channel
    rgb[mask1, 1] = 255  # green channel
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    axes[0].imshow(mask0, cmap="Reds")
    axes[0].set_title("DAPI mask")
    axes[1].imshow(mask1, cmap="Greens")
    axes[1].set_title("GFP mask")
    axes[2].imshow(rgb)
    axes[2].set_title("Overlay (red=DAPI, green=GFP)")
    plt.tight_layout()
    return fig