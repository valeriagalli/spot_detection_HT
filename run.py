"""Script to run spot detection using parameters from a config file."""

import json
from pathlib import Path
from src.spot_detect.io import load_image, save_mask
from src.spot_detect.detection import remove_bg, smooth_image,detect_spots, calculate_channel_statistics, calculate_overlap
from src.spot_detect.plots import plot_channel, plot_overlay


def main():
    # Load settings
    with open("config.json", "r") as f:
        config = json.load(f)
    input_dir = Path(config["input_dir"])
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

   # Load sample image     
    img_name = "sample_image.tif"
    print(f"Loading image: {img_name} from {input_dir}")
    img = load_image((input_dir / img_name).resolve())

    # Initialize empty dictionaries to store results
    masks = {}
    counts = {}
    stats = {}

    # Loop through channels and detect spots
    for i, (name, params) in enumerate(config["channels"].items()):
        print(f"Processing {name} channel...")
        # Print channel statistics (raw values)
        stat = calculate_channel_statistics(img[i], name)
        # Background removal
        bg_method = params["bg_method"]
        bg_sigma = params["bg_sigma"]
        img_no_bg = remove_bg(img[i], bg_method, bg_sigma)
        # Smoothing
        smooth_method = params["smooth_method"]
        smooth_sigma = params["smooth_sigma"]
        img_smoothed = smooth_image(img_no_bg, smooth_method, smooth_sigma)
        # Thresholding to detect spots
        det_method = params["det_method"]
        manual_tresh = None
        otsu_nbins = None
        if det_method == "manual":
            manual_tresh = params["manual_threshold"]
        elif det_method == "otsu":
            otsu_nbins = params["otsu_nbins"]
        n_spots, spots_mask = detect_spots(img_smoothed, det_method, manual_tresh, otsu_nbins)
        # Visualization
        fig = plot_channel(img[i], img_smoothed, spots_mask, name)
        fig.savefig(output_dir / f"{name}_channel.png")
        # Results export
        masks[name] = spots_mask
        counts[name] = n_spots
        stats[name] = stat
    
    # Calculate cross-channel metrics
    n_overlap, overlap_pct = calculate_overlap(masks["DAPI"], masks["GFP"])
    print(f"Overlap pixels: {n_overlap}  ({overlap_pct:.1f}% of union)")
    # Visualization 
    fig = plot_overlay(masks["DAPI"], masks["GFP"])
    fig.savefig(output_dir / "overlay.png")
    
    # Export segmented masks
    out_dir = Path(config["output_dir"])
    out_dir.mkdir(exist_ok=True)
    for name, mask in masks.items():
        mask_path = out_dir / f"{name}_mask.tif"
        save_mask(mask, mask_path)

    # Combine statistics to export in single result file
    results = {
        "spot_counts": counts,
        "channel_statistics": stats,
        "mask_overlap": {
            "pixels": n_overlap,
            "percentage": round(overlap_pct, 1)
        }
    }
    
    # Save results
    results_path = output_dir / "results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    main()