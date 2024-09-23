from manim import *
import numpy as np

def create_custom_3d_arrow(start, end, color=WHITE, thickness=0.02, min_length=0.01):
    vector = end - start
    length = np.linalg.norm(vector)
    if length < min_length:
        end = start + (vector / length) * min_length if length > 0 else start + np.array([min_length, 0, 0])
    line = Line3D(start=start, end=end, color=color, thickness=thickness)
    cone = Cone(direction=end - start, base_radius=0.1, height=0.2).move_to(end)
    cone.set_color(color)
    return VGroup(line, cone)

class AdditiveVectorRepresentation(ThreeDScene):
    def construct(self):
        # Set up the scene with a more zoomed-in view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(1.2)
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            z_range=[-1, 1, 0.2],
            x_length=6,
            y_length=6,
            z_length=6
        )
        self.add(axes)

        # Define concepts and their vectors (updated with shorter vectors)
        concepts = [
            ("royalty", np.array([0.25, 0.1, 0.05]), RED),
            ("leadership", np.array([0.1, 0.3, 0.15]), BLUE),
            ("masculinity", np.array([0.05, 0.05, 0.2]), GREEN),
            ("power", np.array([0.15, 0.15, 0.1]), YELLOW),
        ]

        # Initialize the cumulative vector
        cumulative_vector = np.zeros(3)
        arrows = VGroup()
        labels = VGroup()

        # Move camera to initial position
        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=1.3, run_time=2)
        self.wait(0.5)

        # Create and animate arrows for each concept
        for i, (concept, vector, color) in enumerate(concepts):
            start = axes.c2p(*cumulative_vector)
            end = axes.c2p(*(cumulative_vector + vector))
            
            arrow = create_custom_3d_arrow(start=start, end=end, color=color)
            self.play(Create(arrow), run_time=1)
            arrows.add(arrow)

            label = Text(concept, color=color).scale(0.4)
            label_position = self.get_label_position(start, end, i)
            label.move_to(label_position)
            self.add_fixed_in_frame_mobjects(label)
            self.play(Write(label), run_time=0.5)
            labels.add(label)

            cumulative_vector += vector

            # Rotate camera after every 2 additions (except the last one)
            if i < len(concepts) - 1 and (i + 1) % 2 == 0:
                camera_move_index = (i + 1) // 2
                self.move_camera(
                    phi=(65 + camera_move_index * 10) * DEGREES,
                    theta=(-60 + camera_move_index * 20) * DEGREES,
                    zoom=1.3 + camera_move_index * 0.05,
                    run_time=2
                )
                self.wait(0.5)

        # Rotate camera to a better view for the final "king" vector
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1.2, run_time=2)
        self.wait(0.5)

        # Show the final "king" vector
        king_start = axes.c2p(0, 0, 0)
        king_end = axes.c2p(*cumulative_vector)
        king_arrow = create_custom_3d_arrow(start=king_start, end=king_end, color=WHITE)
        self.play(Create(king_arrow), run_time=1.5)

        # Add the "king" label at the end of the final vector
        king_label = Text("king", color=WHITE).scale(0.5)
        king_label_position = self.get_label_position(king_start, king_end, -1)
        king_label.move_to(king_label_position)
        self.add_fixed_in_frame_mobjects(king_label)
        self.play(Write(king_label), run_time=1)

        # Fade out everything except the axes and the king vector
        self.play(
            *[FadeOut(arrow) for arrow in arrows],
            FadeOut(labels),
            run_time=1.5
        )
        self.wait(1)

        # Fade out the remaining objects
        self.play(
            FadeOut(king_arrow),
            FadeOut(king_label),
            FadeOut(axes),
            run_time=1.5
        )
        self.wait(1)

    def get_label_position(self, start, end, index):
        # Calculate a position for the label that avoids overlap
        mid_point = (np.array(start) + np.array(end)) / 2
        offset = np.array([0.2, 0.2, 0.2]) * (index + 1)
        return mid_point + offset