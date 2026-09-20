from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Global visual style
# ---------------------------------------------------------------------------

config.background_color = "#FFFFFF"

TEXT_COLOR = "#262626"
AUX_COLOR = "#7A7A7A"

# Feasible region
FEASIBLE_FILL = "#76C893"
FEASIBLE_BORDER = "#2D6A4F"

# Objective
OBJECTIVE_COLOR = "#F28C28"

# Ordinary points
POINT_COLOR = "#1F77B4"

# Optimal solution
OPTIMUM_COLOR = "#D81B60"

# Nonconvex / warning
NONCONVEX_COLOR = "#C62828"


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def nearest_point_on_segment(point, start, end):
    """Return the nearest point on a line segment."""
    segment = end - start
    denominator = np.dot(segment, segment)

    if denominator == 0:
        return start.copy()

    t = np.dot(point - start, segment) / denominator
    t = np.clip(t, 0.0, 1.0)

    return start + t * segment


def nearest_point_on_polygon(point, vertices):
    """Return the nearest boundary point of a polygon."""
    nearest = None
    minimum_distance = np.inf

    for i in range(len(vertices)):
        start = vertices[i]
        end = vertices[(i + 1) % len(vertices)]

        candidate = nearest_point_on_segment(point, start, end)
        distance = np.linalg.norm(candidate - point)

        if distance < minimum_distance:
            minimum_distance = distance
            nearest = candidate

    return nearest, minimum_distance

def nearest_point_on_segment(point, start, end):
    """Return the closest point on a line segment."""
    segment = end - start

    # Avoid division by zero for a degenerate segment
    if np.dot(segment, segment) == 0:
        return start

    t = np.dot(point - start, segment) / np.dot(segment, segment)

    # Clamp the projection to the segment
    t = np.clip(t, 0.0, 1.0)

    return start + t * segment


def coordinate_circle(axes, center, radius, color=OBJECTIVE_COLOR):
    """Create a circle expressed in axis coordinates."""
    return ParametricFunction(
        lambda t: axes.c2p(
            center[0] + radius * np.cos(t),
            center[1] + radius * np.sin(t),
        ),
        t_range=[0, TAU],
        color=color,
        stroke_width=4,
    )


# ---------------------------------------------------------------------------
# 01: Hero animation
# ---------------------------------------------------------------------------

class Hero(Scene):
    def construct(self):
        title = Text(
            "Where is the best point closest to the destination?",
            font_size=38,
            color=TEXT_COLOR,
        )
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)

        vertices = [
            np.array([-4.0, -2.0, 0.0]),
            np.array([-3.0,  0.8, 0.0]),
            np.array([-0.5,  1.3, 0.0]),
            np.array([ 2.3,  0.3, 0.0]),
            np.array([ 1.5, -2.1, 0.0]),
            np.array([-1.5, -2.5, 0.0]),
        ]
        feasible_set = Polygon(
            *vertices,
            color=FEASIBLE_BORDER,
            fill_color=FEASIBLE_BORDER,
            fill_opacity=0.18,
            stroke_width=4,
        )
        feasible_label = Text(
            "feasible set",
            font_size=28,
            color=TEXT_COLOR,
        )
        feasible_label.move_to([-1.0, -1.4, 0.0])
        self.play(
            Create(feasible_set),
            FadeIn(feasible_label),
        )
        self.wait(0.5)

        destination_position = np.array([4.2, 1.4, 0.0])
        destination = Dot(
            destination_position,
            radius=0.11,
            color=OBJECTIVE_COLOR,
        )
        destination_label = Text(
            "destination",
            font="Noto Sans JP",
            font_size=26,
            color=OBJECTIVE_COLOR,
        )
        destination_label.next_to(destination, RIGHT, buff=0.15)
        self.play(
            FadeIn(destination, scale=0.5),
            FadeIn(destination_label),
        )
        self.wait(0.5)
        optimal_position, _ = nearest_point_on_polygon(
            destination_position,
            vertices,
        )

        initial_position = np.array([-2.0, -0.6, 0.0])
        current_point = Dot(
            initial_position,
            radius=0.10,
            color=POINT_COLOR,
        )
        current_label = MathTex(
            "x",
            color=POINT_COLOR,
        )
        current_label.next_to(current_point, UP, buff=0.12)
        self.play(
            FadeIn(current_point),
            FadeIn(current_label),
        )
        distance_line = always_redraw(
            lambda: DashedLine(
                current_point.get_center(),
                destination.get_center(),
                color=POINT_COLOR,
                stroke_width=3,
            )
        )
        current_label.add_updater(
            lambda label: label.next_to(
                current_point,
                UP,
                buff=0.12,
            )
        )
        self.play(Create(distance_line))
        self.wait(1)

        self.play(
            current_point.animate.move_to(optimal_position),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(0.5)

        current_label.clear_updaters()
        optimal_label = MathTex(
            r"x^\star",
            color=OPTIMUM_COLOR,
        )
        optimal_label.next_to(
            current_point,
            UP,
            buff=0.15,
        )
        self.play(
            current_point.animate.set_color(OPTIMUM_COLOR),
            FadeOut(current_label),
            FadeIn(optimal_label),
            distance_line.animate.set_color(OPTIMUM_COLOR),
        )
        # self.play(
        #     Circumscribe(
        #         current_point,
        #         color=OPTIMUM_COLOR,
        #         fade_out=True,
        #     )
        # )
        self.wait(2)
