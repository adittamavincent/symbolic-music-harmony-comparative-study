"""
Visualization script for Strube Harmonic Evaluation Framework.
Loads outputs/SUMMARY_TABLE.csv and generates a premium, publication-quality bar chart

comparing DeepBach, Coconet, and NotaGen across four experimental conditions.
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set premium styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Roboto', 'Helvetica Neue', 'Arial']
plt.rcParams['text.color'] = '#222222'
plt.rcParams['axes.labelcolor'] = '#222222'
plt.rcParams['xtick.color'] = '#444444'
plt.rcParams['ytick.color'] = '#444444'

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SUMMARY_PATH = PROJECT_ROOT / "outputs" / "SUMMARY_TABLE.csv"
OUTPUT_IMG_PATH = PROJECT_ROOT / "outputs" / "strube_evaluation_results.png"

def main():
    print("Generating results visualization...")
    if not SUMMARY_PATH.exists():
        print(f"Error: {SUMMARY_PATH} does not exist. Run evaluation first!")
        return

    df = pd.read_csv(SUMMARY_PATH)

    # Pivot table to get Model as columns and Condition as index
    pivot_df = df.pivot(index='Condition', columns='Model', values='Avg Strube Score')

    # Reorder index to follow standard flow: A -> B -> C -> D
    conditions_order = ['A_neutral', 'B_key', 'C_satb', 'D_full']
    pivot_df = pivot_df.reindex(conditions_order)

    # Reorder columns chronologically: Deepbach -> Coconet -> Notagen
    models_order = ['Deepbach', 'Coconet', 'Notagen']
    # Filter columns to only those present
    columns_present = [col for col in models_order if col in pivot_df.columns]
    pivot_df = pivot_df[columns_present]

    # Define harmonious premium color palette
    # Deepbach = Sleek Blue-Gray, Coconet = Classic Slate Green, Notagen = Vibrant Purple
    colors = ['#4A6B82', '#628D75', '#8C52FF']

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Plot grouped bars
    x = np.arange(len(pivot_df.index))
    width = 0.25

    for idx, model_name in enumerate(pivot_df.columns):
        offset = (idx - len(pivot_df.columns) / 2) * width + width / 2
        rects = ax.bar(x + offset, pivot_df[model_name], width, label=model_name,
                       color=colors[idx], edgecolor='white', linewidth=1, alpha=0.9)

        # Add values on top of bars
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold', color='#444444')

    # Set elegant labels and titles
    ax.set_ylabel('Avg Strube Score (Higher is Better)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_title("Functional Harmony Rules Compliance (Strube Framework)\nComparison of Three Eras of Symbolic Music Models",
                 fontsize=14, fontweight='bold', pad=20, color='#111111')
    ax.set_xticks(x)

    # Nicer labels for conditions
    condition_labels = [
        'Condition A\n(Neutral / Unconstrained)',
        'Condition B\n(Key Constrained)',
        'Condition C\n(Soprano Melody)',
        'Condition D\n(Soprano & Bass)'
    ]
    ax.set_xticklabels(condition_labels, fontsize=10)
    ax.set_ylim(0, 1.1)

    # Premium legend styling
    ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#dddddd', fontsize=10, shadow=False, loc='upper left')

    # Clean grid lines
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#cccccc')
    ax.grid(axis='x', visible=False)

    # De-spine (remove top and right borders)
    for spine in ['top', 'right', 'left', 'bottom']:

        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG_PATH, dpi=300)
    plt.close()

    print(f"Successfully generated Strube evaluation chart at {OUTPUT_IMG_PATH}")

if __name__ == "__main__":
    main()
