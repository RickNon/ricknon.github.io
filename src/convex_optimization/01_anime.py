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

def graph_path(axes, function, start_x, end_x, samples=120):
    """Create a path that follows a graph between two x coordinates."""
    x_values = np.linspace(start_x, end_x, samples)

    path = VMobject()
    path.set_points_as_corners(
        [
            axes.c2p(x, function(x))
            for x in x_values
        ]
    )

    return path


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
            r"x^*",
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

# ---------------------------------------------------------------------------
# 02: Constraints define the feasible set
# ---------------------------------------------------------------------------

class FeasibleSet(Scene):
    def construct(self):
        title = Text(
            "Constraints define the feasible set",
            font_size=38,
            color=TEXT_COLOR,
        ).to_edge(UP)

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=6.0,
            y_length=5.5,
            tips=False,
            axis_config={
                "color": AUX_COLOR,
                "stroke_width": 2,
            },
        ).shift(RIGHT * 1.8 + DOWN * 0.3)

        x_label = MathTex(
            r"x_1",
            color=TEXT_COLOR,
        ).next_to(axes.x_axis.get_end(), RIGHT)

        y_label = MathTex(
            r"x_2",
            color=TEXT_COLOR,
        ).next_to(axes.y_axis.get_end(), UP)

        # Constraint labels shown on the left side.
        constraint_1 = MathTex(
            r"x_1 \ge 0",
            color=FEASIBLE_BORDER,
            font_size=38,
        ).move_to([-4.5, 1.3, 0])

        constraint_2 = MathTex(
            r"x_2 \ge 0",
            color=FEASIBLE_BORDER,
            font_size=38,
        ).next_to(
            constraint_1,
            DOWN,
            aligned_edge=LEFT,
            buff=0.45,
        )

        constraint_3 = MathTex(
            r"x_1+x_2\le4",
            color=FEASIBLE_BORDER,
            font_size=38,
        ).next_to(
            constraint_2,
            DOWN,
            aligned_edge=LEFT,
            buff=0.45,
        )

        # Boundary of x_1 >= 0.
        line_1 = Line(
            axes.c2p(0, -1),
            axes.c2p(0, 5),
            color=FEASIBLE_BORDER,
            stroke_width=4,
        )

        # Region satisfying only x_1 >= 0.
        region_1 = Polygon(
            axes.c2p(0, -1),
            axes.c2p(5, -1),
            axes.c2p(5, 5),
            axes.c2p(0, 5),
            stroke_width=0,
            fill_color=FEASIBLE_FILL,
            fill_opacity=0.25,
        )

        # Boundary of x_2 >= 0.
        line_2 = Line(
            axes.c2p(-1, 0),
            axes.c2p(5, 0),
            color=FEASIBLE_BORDER,
            stroke_width=4,
        )

        # Region satisfying x_1 >= 0 and x_2 >= 0.
        region_2 = Polygon(
            axes.c2p(0, 0),
            axes.c2p(5, 0),
            axes.c2p(5, 5),
            axes.c2p(0, 5),
            stroke_width=0,
            fill_color=FEASIBLE_FILL,
            fill_opacity=0.25,
        )

        # Boundary of x_1 + x_2 <= 4.
        line_3 = Line(
            axes.c2p(-1, 5),
            axes.c2p(5, -1),
            color=FEASIBLE_BORDER,
            stroke_width=4,
        )

        # Final feasible set satisfying all three constraints.
        final_region = Polygon(
            axes.c2p(0, 0),
            axes.c2p(4, 0),
            axes.c2p(0, 4),
            stroke_color=FEASIBLE_BORDER,
            stroke_width=4,
            fill_color=FEASIBLE_FILL,
            fill_opacity=0.30,
        )

        feasible_label = Text(
            "feasible set",
            font_size=28,
            color=FEASIBLE_BORDER,
        ).move_to(axes.c2p(1.15, 1.15))

        self.play(
            FadeIn(title),
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label),
        )

        self.wait(0.5)

        # Add the first constraint.
        self.play(
            Create(line_1),
            FadeIn(region_1),
            Write(constraint_1),
            run_time=1.3,
        )

        self.wait(0.8)

        # Add the second constraint and keep only the intersection.
        self.play(
            Transform(region_1, region_2),
            Create(line_2),
            Write(constraint_2),
            run_time=1.3,
        )

        self.wait(0.8)

        # Add the final constraint and obtain the feasible set.
        self.play(
            Transform(region_1, final_region),
            Create(line_3),
            Write(constraint_3),
            run_time=1.5,
        )

        self.play(
            FadeIn(feasible_label),
        )

        self.wait(2)

# ---------------------------------------------------------------------------
# 03: Nonconvex versus convex optimization
# ---------------------------------------------------------------------------

class ConvexVsNonconvex(Scene):
    def construct(self):
        title = Text(
            "Why convex?",
            font_size=38,
            color=TEXT_COLOR,
        ).to_edge(UP)

        left_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 4.2, 1],
            x_length=5.4,
            y_length=4.0,
            tips=False,
            axis_config={
                "color": AUX_COLOR,
                "stroke_width": 2,
            },
        ).shift(LEFT * 3.3 + DOWN * 0.2)

        right_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 4.2, 1],
            x_length=5.4,
            y_length=4.0,
            tips=False,
            axis_config={
                "color": AUX_COLOR,
                "stroke_width": 2,
            },
        ).shift(RIGHT * 3.3 + DOWN * 0.2)

        def nonconvex_function(x):
            """Return a tilted double-well function."""
            return 0.12 * (x**2 - 4) ** 2 + 0.18 * x + 0.45

        def convex_function(x):
            """Return a simple convex quadratic function."""
            return 0.35 * x**2 + 0.35

        nonconvex_graph = left_axes.plot(
            nonconvex_function,
            x_range=[-2.9, 2.9],
            color=NONCONVEX_COLOR,
            stroke_width=4,
        )

        convex_graph = right_axes.plot(
            convex_function,
            x_range=[-2.9, 2.9],
            color=FEASIBLE_BORDER,
            stroke_width=4,
        )

        nonconvex_title = Text(
            "Nonconvex",
            font_size=30,
            color=NONCONVEX_COLOR,
        ).next_to(left_axes, UP)

        convex_title = Text(
            "Convex",
            font_size=30,
            color=FEASIBLE_BORDER,
        ).next_to(right_axes, UP)

        # Numerically locate the two minima of the nonconvex example.
        left_candidates = np.linspace(-3.0, 0.0, 2000)
        right_candidates = np.linspace(0.0, 3.0, 2000)

        global_x = left_candidates[
            np.argmin(
                [nonconvex_function(x) for x in left_candidates]
            )
        ]

        local_x = right_candidates[
            np.argmin(
                [nonconvex_function(x) for x in right_candidates]
            )
        ]

        left_start = -2.8
        right_start = 2.8

        nonconvex_dot_1 = Dot(
            left_axes.c2p(
                left_start,
                nonconvex_function(left_start),
            ),
            color=POINT_COLOR,
            radius=0.09,
        )

        nonconvex_dot_2 = Dot(
            left_axes.c2p(
                right_start,
                nonconvex_function(right_start),
            ),
            color=POINT_COLOR,
            radius=0.09,
        )

        convex_dot_1 = Dot(
            right_axes.c2p(
                left_start,
                convex_function(left_start),
            ),
            color=POINT_COLOR,
            radius=0.09,
        )

        convex_dot_2 = Dot(
            right_axes.c2p(
                right_start,
                convex_function(right_start),
            ),
            color=POINT_COLOR,
            radius=0.09,
        )

        global_path = graph_path(
            left_axes,
            nonconvex_function,
            left_start,
            global_x,
        )

        local_path = graph_path(
            left_axes,
            nonconvex_function,
            right_start,
            local_x,
        )

        convex_path_1 = graph_path(
            right_axes,
            convex_function,
            left_start,
            0.0,
        )

        convex_path_2 = graph_path(
            right_axes,
            convex_function,
            right_start,
            0.0,
        )

        global_label = Text(
            "global",
            font_size=24,
            color=OPTIMUM_COLOR,
        ).next_to(
            left_axes.c2p(
                global_x,
                nonconvex_function(global_x),
            ),
            DOWN,
        )

        local_label = Text(
            "local",
            font_size=24,
            color=OBJECTIVE_COLOR,
        ).next_to(
            left_axes.c2p(
                local_x,
                nonconvex_function(local_x),
            ),
            DOWN,
        )

        convex_optimum = Dot(
            right_axes.c2p(
                0,
                convex_function(0),
            ),
            color=OPTIMUM_COLOR,
            radius=0.11,
        )

        conclusion = MathTex(
            r"\text{Every local optimum is global in convex optimization}",
            color=TEXT_COLOR,
            font_size=38,
        ).to_edge(DOWN)

        self.play(
            FadeIn(title),
            FadeIn(left_axes),
            FadeIn(right_axes),
            Create(nonconvex_graph),
            Create(convex_graph),
            Write(nonconvex_title),
            Write(convex_title),
            run_time=1.5,
        )

        self.play(
            FadeIn(nonconvex_dot_1),
            FadeIn(nonconvex_dot_2),
            FadeIn(convex_dot_1),
            FadeIn(convex_dot_2),
        )

        self.wait(0.5)

        # Illustrate how different valleys exist in a nonconvex function.
        self.play(
            MoveAlongPath(nonconvex_dot_1, global_path),
            MoveAlongPath(nonconvex_dot_2, local_path),
            MoveAlongPath(convex_dot_1, convex_path_1),
            MoveAlongPath(convex_dot_2, convex_path_2),
            run_time=3.0,
            rate_func=smooth,
        )

        self.play(
            nonconvex_dot_1.animate.set_color(OPTIMUM_COLOR),
            nonconvex_dot_2.animate.set_color(OBJECTIVE_COLOR),
            FadeIn(convex_optimum),
            FadeIn(global_label),
            FadeIn(local_label),
        )

        self.play(
            FadeIn(conclusion),
        )

        self.wait(2)
