import json
from itertools import groupby
from operator import itemgetter

import apace as ap
import numpy as np
import matplotlib.pyplot as plt

from . import FIG_SIZE, lattices_generated_dir


def results(lattice, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)
    name, namespace = itemgetter("name", "namespace")(lattice)
    print(f"\033[1m[apace] Generating results for {namespace}/{name}\033[0m")

    print(f"    Compute simulation data")
    lattice_path = (lattices_generated_dir / namespace / name).with_suffix(".json")
    lattice_obj = ap.Lattice.from_file(lattice_path)
    twiss_data = ap.Twiss(lattice_obj, energy=lattice["energy"], steps_per_meter=100)

    print(f"    Generating tables ๐")
    with (output_dir / "twiss_tables.json").open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"    Generating twiss plot ๐")
    twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")

    print(f"    Generating floor plan ๐")
    floor_plan_plot(lattice_obj).savefig(output_dir / "floor_plan_cell.svg")


def twiss_tables(twiss: ap.Twiss):
    return [
        [
            "Optical Functions",
            ["twiss.svg"],
        ],
        [
            "Detailed Lattice Parameter",
            [
                [
                    ["Qโ", twiss.tune_x],
                    # TODO: fix chroma in apace
                    # ["Chromaticity x", twiss.chromaticity_x],
                    ["ฮฒโ,โโโ / m", np.max(twiss.beta_x)],
                    ["ฮฒโ,โแตขโ / m", np.min(twiss.beta_x)],
                    ["ฮฒโ,โโโโ / m", np.mean(twiss.beta_x)],
                    ["ฮทโ,โโโ / m", np.max(twiss.eta_x)],
                ],
                [
                    ["Qแตง", twiss.tune_y],
                    # TODO: fix chroma in apace
                    # ["Chromaticity y", twiss.chromaticity_y],
                    ["ฮฒแตง,โโโ / m", np.max(twiss.beta_y)],
                    ["ฮฒแตง,โแตขโ / m", np.min(twiss.beta_y)],
                    ["ฮฒแตง,โโโโ / m", np.mean(twiss.beta_y)],
                    ["ฮทแตง,โโโ / m", 0],
                ],
                [
                    ["Mom. compaction", twiss.alpha_c],
                    ["Emittance", twiss.emittance_x],
                    ["Iโ", twiss.i1],
                    ["Iโ", twiss.i2],
                    ["Iโ", twiss.i3],
                    ["Iโ", twiss.i4],
                    ["Iโ", twiss.i5],
                ],
            ],
        ],
        [
            "Floor plan",
            ["floor_plan_cell.svg"],
        ],
    ]


def twiss_plot(twiss: ap.Twiss):
    from math import log10, floor
    from apace.plot import plot_twiss, draw_elements, draw_sub_lattices, Color

    factor = np.max(twiss.beta_x) / np.max(twiss.eta_x)
    eta_x_scale = 10 ** floor(log10(factor))
    cell = twiss.lattice.children[0]
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.set_xlim(0, cell.length)
    plot_twiss(ax, twiss, scales={"eta_x": eta_x_scale})
    draw_elements(ax, cell, labels=len(cell.sequence) < 150)
    draw_sub_lattices(ax, cell, labels=len(cell.children) < 5)
    ax.grid(axis="y", color=Color.LIGHT_GRAY, linestyle="--", linewidth=1)
    plt.legend(
        bbox_to_anchor=(0, 1.05, 1, 0.2),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    fig.tight_layout()

    return fig


def floor_plan_plot(lattice: ap.Lattice):
    from apace.plot import floor_plan

    # fig_ring, ax = plt.subplots()
    # ax.axis("off")
    # floor_plan(ax, lattice, labels=False)

    fig_cell, ax = plt.subplots(figsize=FIG_SIZE)
    ax.axis("off")
    cell = lattice.children[0]
    floor_plan(ax, cell)
    return fig_cell
