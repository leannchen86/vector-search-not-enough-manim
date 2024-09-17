from manim import *
import numpy as np

class CustomArrowTip(Triangle):
    def __init__(self, color=WHITE, **kwargs):
        super().__init__(color=color, fill_opacity=1, **kwargs)
        self.scale(0.1)  # Scale down the triangle
        self.rotate(-90 * DEGREES)  # Rotate to point upwards

class Vector3DWith2DArrow(VGroup):
    def __init__(self, start, end, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.start = np.array(start)
        self.end = np.array(end)
        self.line = Line3D(self.start, self.end, color=color)
        self.arrow_tip = CustomArrowTip(color=color)
        self.add(self.line, self.arrow_tip)
        self.update_arrow_tip()

    def update_arrow_tip(self):
        self.arrow_tip.move_to(self.end)
        direction = self.end - self.start
        direction = direction / np.linalg.norm(direction)
        rotation_axis = np.cross([0, 0, 1], direction)
        rotation_angle = np.arccos(np.dot([0, 0, 1], direction))
        self.arrow_tip.rotate(rotation_angle, axis=rotation_axis)

    def create_animation(self):
        return AnimationGroup(Create(self.line), GrowFromCenter(self.arrow_tip))

class VectorSpace3DWith3DVectors(ThreeDScene):
    def construct(self):
        # Set up the initial camera view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.7)

        # Create a 3D grid
        grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            },
            axis_config={"include_numbers": False}
        )

        # Add vertical lines for depth perception
        vertical_lines = VGroup(*[
            Line(start=grid.c2p(x, y, 0), end=grid.c2p(x, y, 5), color=BLUE_E, stroke_width=1, stroke_opacity=0.5)
            for x in range(-5, 6) for y in range(-5, 6)
        ])

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(0, 5, 1),
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False}
        )

        # Add everything to the scene
        self.add(grid, vertical_lines, axes)

        # Create 3D vectors with 3D arrows
        vector1 = Arrow3D(start=[0, 0, 0], end=[2, 3, 2], color=RED)
        vector2 = Arrow3D(start=[0, 0, 0], end=[-1, 2, 3], color=GREEN)

        # Animate the creation of vectors
        self.play(Create(vector1))
        self.play(Create(vector2))

        # Rotate and zoom to get a better view
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, zoom=1.5, run_time=2)
        self.wait(1)

        # Create vector difference with 2D arrow tip
        vector_diff = Vector3DWith2DArrow(start=vector2.get_end(), end=vector1.get_end(), color=YELLOW)
        
        # Draw vector difference
        self.play(vector_diff.create_animation())
        self.wait(1)

        # Slowly rotate the camera for a dynamic view
        self.begin_ambient_camera_rotation(rate=0.1)

        # Create text labels for vectors
        label1 = Text("30-day challenge", font_size=24).next_to(vector1.get_end(), UR, buff=0.1)
        label2 = Text("100-day challenge", font_size=24).next_to(vector2.get_end(), DL, buff=0.1)

        # Add and animate the vector labels
        self.add_fixed_in_frame_mobjects(label1, label2)
        self.play(FadeIn(label1, run_time=0.5), FadeIn(label2, run_time=0.5))

        # Add semantic meaning to vector difference
        diff_label = Text("commitment", font_size=24).next_to(vector_diff.end, DL, buff=0.1)
        
        # Add and animate the difference label
        self.add_fixed_in_frame_mobjects(diff_label)
        self.play(FadeIn(diff_label, run_time=0.5))

        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(1)

if __name__ == "__main__":
    scene = VectorSpace3DWith3DVectors()
    scene.render()