from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle


# ---------------------------------------------------------------------
# Color settings
# ---------------------------------------------------------------------

CONVEX_FILL = "#76C893"
CONVEX_EDGE = "#2D6A4F"

NONCONVEX_FILL = "#F2B8A0"
NONCONVEX_EDGE = "#C96B4A"

POINT_COLOR = "#1F77B4"
GOOD_SEGMENT_COLOR = "#2D6A4F"
BAD_SEGMENT_COLOR = "#C62828"
TEXT_COLOR = "#262626"


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def setup_axis(ax, title):
    """Prepare a clean subplot."""
    ax.set_aspect("equal")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.axis("off")
    ax.set_title(title, fontsize=13, color=TEXT_COLOR, pad=10)


def draw_segment_example(ax, p1, p2, segment_color, caption):
    """Draw two example points and the segment connecting them."""
    ax.plot(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        color=segment_color,
        linewidth=2.8,
        zorder=4,
    )
    ax.scatter(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        s=45,
        color=POINT_COLOR,
        zorder=5,
    )
    ax.text(
        0.0,
        -2.12,
        caption,
        ha="center",
        va="top",
        fontsize=10.5,
        color=segment_color,
    )


# ---------------------------------------------------------------------
# Main figure
# ---------------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.ravel()


# ---------------------------------------------------------------------
# 1. Convex example: ellipse
# ---------------------------------------------------------------------

ax = axes[0]
setup_axis(ax, "Convex set")

ellipse = Ellipse(
    (0, 0),
    width=3.6,
    height=2.4,
    facecolor=CONVEX_FILL,
    edgecolor=CONVEX_EDGE,
    linewidth=2.5,
    alpha=0.85,
)
ax.add_patch(ellipse)

p1 = (-1.0, -0.45)
p2 = (1.15, 0.55)

draw_segment_example(
    ax,
    p1,
    p2,
    GOOD_SEGMENT_COLOR,
    "",
)


# ---------------------------------------------------------------------
# 2. Nonconvex example: jagged / notched polygon
# ---------------------------------------------------------------------

ax = axes[1]
setup_axis(ax, "Nonconvex set")

# Rectangle-like polygon with a notch on the top side
vertices = np.array([
    (-1.9, -1.5),
    ( 1.9, -1.5),
    ( 1.9,  1.6),
    ( 0.55, 1.6),
    ( 0.00, 0.55),
    (-0.55, 1.6),
    (-1.9,  1.6),
])

notched_polygon = Polygon(
    vertices,
    closed=True,
    facecolor=NONCONVEX_FILL,
    edgecolor=NONCONVEX_EDGE,
    linewidth=2.5,
    alpha=0.9,
)
ax.add_patch(notched_polygon)

p1 = (-1.05, 1.10)
p2 = ( 1.05, 1.10)

draw_segment_example(
    ax,
    p1,
    p2,
    BAD_SEGMENT_COLOR,
    "",
)

# ---------------------------------------------------------------------
# 3. Nonconvex example: star-shaped polygon
# ---------------------------------------------------------------------

ax = axes[2]
setup_axis(ax, "Nonconvex set")

# Define a star-shaped nonconvex polygon
star_vertices = np.array([
    ( 0.00,  1.90),
    ( 0.45,  0.55),
    ( 1.75,  0.55),
    ( 0.70, -0.20),
    ( 1.10, -1.65),
    ( 0.00, -0.75),
    (-1.10, -1.65),
    (-0.70, -0.20),
    (-1.75,  0.55),
    (-0.45,  0.55),
])

star_polygon = Polygon(
    star_vertices,
    closed=True,
    facecolor=NONCONVEX_FILL,
    edgecolor=NONCONVEX_EDGE,
    linewidth=2.5,
    alpha=0.9,
)
ax.add_patch(star_polygon)

# Choose two points in the upper left and upper right arms.
# The segment between them passes outside the set near the center notch.
p1 = (0.95, 0.35)
p2 = (0.75, -1.1)

draw_segment_example(
    ax,
    p1,
    p2,
    BAD_SEGMENT_COLOR,
    "",
)

# ---------------------------------------------------------------------
# 4. Nonconvex example: annulus (2D analogue of a donut shape)
# ---------------------------------------------------------------------

ax = axes[3]
setup_axis(ax, "Nonconvex set")

outer_ring = Circle(
    (0, 0),
    radius=1.75,
    facecolor=NONCONVEX_FILL,
    edgecolor=NONCONVEX_EDGE,
    linewidth=2.5,
    alpha=0.9,
)
inner_hole = Circle(
    (0, 0),
    radius=0.85,
    facecolor="white",
    edgecolor=NONCONVEX_EDGE,
    linewidth=2.0,
)

ax.add_patch(outer_ring)
ax.add_patch(inner_hole)

# These points lie in the ring, but the segment passes through the hole
p1 = (0.00, 1.15)
p2 = (0.00, -1.15)

draw_segment_example(
    ax,
    p1,
    p2,
    BAD_SEGMENT_COLOR,
    "",
)


# ---------------------------------------------------------------------
# Global title and save
# ---------------------------------------------------------------------

fig.suptitle(
    "Convex or Nonconvex",
    fontsize=18,
    color=TEXT_COLOR,
    y=0.98,
)

fig.tight_layout(rect=[0, 0, 1, 0.96])

# Save the figure to the article assets directory
output_dir = Path("assets/images/convex-optimization/01")
output_dir.mkdir(parents=True, exist_ok=True)

# Save both PNG and SVG for flexibility
fig.savefig(output_dir / "convex_vs_nonconvex_examples.png", dpi=220, bbox_inches="tight")
fig.savefig(output_dir / "convex_vs_nonconvex_examples.svg", bbox_inches="tight")

plt.show()
