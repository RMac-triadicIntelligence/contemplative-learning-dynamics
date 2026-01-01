import os
import numpy as np
import matplotlib.pyplot as plt

from src.triadic_model import hill, simulate

def main():
    t_full = np.linspace(0, 50, 500)
    intervention_time = 25.0

    # Initial state: modest partial activation, moderate dwelling already present
    y0 = (0.2, 0.1, 0.15, 0.6)

    # Choose: "jump" or "pulse"
    nudge_mode = "jump"

    sol_without, sol_with, idx, y0_used, y_nudge = simulate(
        t_full,
        y0=y0,
        intervention_time=intervention_time,
        nudge_mode=nudge_mode,
        # you can override model params here if desired:
        # gamma=10.0, threshold=0.5, steepness=6,
    )

    avg_without = np.mean(sol_without[-100:], axis=0)
    avg_with = np.mean(sol_with[-100:], axis=0)

    print("Without catalytic nudge (sustained contemplative holding):")
    print(f"facet1 ≈ {avg_without[0]:.3f}, facet2 ≈ {avg_without[1]:.3f}, facet3 ≈ {avg_without[2]:.3f}, dwelling ≈ {avg_without[3]:.3f}")

    print("\nWith gentle nudge (insight emerges):")
    print(f"facet1 ≈ {avg_with[0]:.3f}, facet2 ≈ {avg_with[1]:.3f}, facet3 ≈ {avg_with[2]:.3f}, dwelling ≈ {avg_with[3]:.3f}")

    coherence_with = np.mean(sol_with[:, :3], axis=1)
    hill_threshold = 0.5

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1) Dwelling vs coherence
    ax = axes[0, 0]
    ax.plot(coherence_with, sol_with[:, 3], linewidth=3, label="Model")
    coherence_rl = np.linspace(0, 1, 100)
    exploration_rate = 0.8 * (1 - coherence_rl) ** 2 + 0.1
    ax.plot(coherence_rl, exploration_rate, "--", linewidth=2, label="RL exploration rate")
    ax.set_xlabel("Coherence / Capability")
    ax.set_ylabel("Dwelling / Exploration")
    ax.set_title("Meta-Regulation: Both Systems Modulate Openness", fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)

    # 2) Activation functions
    ax = axes[0, 1]
    x_range = np.linspace(0, 1, 200)
    ax.plot(x_range, hill(x_range, gamma=10.0, threshold=0.5, steepness=6), linewidth=3, label="Hill (n=6)")
    relu = np.maximum(0, 10 * (x_range - 0.2))
    sigmoid = 10 / (1 + np.exp(-12 * (x_range - 0.5)))
    ax.plot(x_range, relu, "--", linewidth=2, label="ReLU-like")
    ax.plot(x_range, sigmoid, "--", linewidth=2, label="Sigmoid (gentler)")
    ax.axvline(x=hill_threshold, linestyle=":", alpha=0.5, linewidth=2)
    ax.set_xlabel("Input Activation")
    ax.set_ylabel("Output Response")
    ax.set_title("Nonlinear Activation Functions", fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)

    # 3) Temporal dynamics
    ax = axes[1, 0]
    ax.plot(t_full, coherence_with, linewidth=3, label="Contemplative: coherence")
    ax.axvline(x=intervention_time, linestyle=":", linewidth=2, alpha=0.8)
    t_rl = np.linspace(0, 50, 500)
    early_ramp = 0.10 * (1 - np.exp(-t_rl / 15))
    rl_performance = 0.10 + early_ramp + 0.80 / (1 + np.exp(-0.35 * (t_rl - 30)))
    ax.plot(t_rl, rl_performance, "--", linewidth=2, label="RL: capability (typical)")
    ax.fill_between(t_full[:idx], 0, 1, alpha=0.08, label="Dwelling / Exploration")
    ax.fill_between(t_full[idx:], 0, 1, alpha=0.08, label="Emergence / Exploitation")
    ax.set_xlabel("Time / Training Steps")
    ax.set_ylabel("Performance / Coherence")
    ax.set_title("Plateau → Breakthrough → Mastery", fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # 4) Basin sketch
    ax = axes[1, 1]
    ax.add_patch(plt.Circle((0.2, 0.2), 0.15, alpha=0.3, label="Low basin"))
    ax.add_patch(plt.Circle((0.85, 0.85), 0.12, alpha=0.3, label="High basin"))
    sep_x = np.linspace(0, 1, 50)
    sep_y = 0.5 + 0.3 * np.sin(3 * np.pi * sep_x)
    ax.plot(sep_x, sep_y, "--", linewidth=2, alpha=0.6, label="Separatrix (sketch)")
    ax.plot(sol_with[:, 0], sol_with[:, 1], linewidth=2.5, label="Model")
    ax.scatter(y0_used[0], y0_used[1], s=120, marker="o", edgecolors="black", linewidths=1.5, zorder=5, label="Start")
    if nudge_mode == "jump" and y_nudge is not None:
        ax.scatter(y_nudge[0], y_nudge[1], s=180, marker="*", edgecolors="black", linewidths=1.5, zorder=6, label="Nudge")
    else:
        ax.scatter(sol_with[idx, 0], sol_with[idx, 1], s=180, marker="*", edgecolors="black", linewidths=1.5, zorder=6, label="Nudge")
    ax.set_xlabel("Facet 1")
    ax.set_ylabel("Facet 2")
    ax.set_title("Bistability: Attractor Basins", fontweight="bold")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()

    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", "simulation_plots.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.show()

    print("\nSaved plot to:", out_path)

if __name__ == "__main__":
    main()
