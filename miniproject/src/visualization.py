from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_initial_domain_conditions_and_mask(
    u: np.ndarray,
    interior_mask: np.ndarray,
    bid: str,
    save_dir: Path | None = None,
) -> None:
    """Plot domain (initial conditions) and interior mask side by side for one building."""
    fig, (ax_domain, ax_mask) = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle(f"Building {bid}")

    im = ax_domain.imshow(u[1:-1, 1:-1], cmap="coolwarm", vmin=0, vmax=25)
    ax_domain.set_title("Domain (initial conditions)")
    divider = make_axes_locatable(ax_domain)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, cax=cax, label="Temperature (°C)")

    ax_mask.imshow(interior_mask, cmap="gray")
    ax_mask.set_title("Interior mask")
    divider_mask = make_axes_locatable(ax_mask)
    cax_dummy = divider_mask.append_axes("right", size="5%", pad=0.05)
    cax_dummy.set_visible(False)

    plt.tight_layout()

    if save_dir is not None:
        save_dir.mkdir(exist_ok=True)
        path = save_dir / f"{bid}_input.png"
        plt.savefig(path, dpi=150)
        plt.close(fig)
    else:
        plt.show()
