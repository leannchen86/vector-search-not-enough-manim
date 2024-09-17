from manim import *

class WordEmbeddingVectors(ThreeDScene):
    def construct(self):
        # Set up the scene with a view that captures parallel vector differences
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-5, 5, 1),
            axis_config={"include_tip": False, "include_numbers": False, "color": GRAY}
        )

        # Create vectors with mirrored positioning and aligned gender difference
        man_vector = Arrow3D(start=ORIGIN, end=[3, 1, 2], color=BLUE)
        woman_vector = Arrow3D(start=ORIGIN, end=[3, 3, 2], color=RED)
        king_vector = Arrow3D(start=ORIGIN, end=[-3, 1, 2], color=GREEN)
        queen_vector = Arrow3D(start=ORIGIN, end=[-3, 3, 2], color=PURPLE)

        # Create text labels
        def create_rotated_text(text, color=WHITE):
            text_obj = Text(text, font_size=28, color=color, font="Arial")
            text_obj.rotate(angle=PI/2, axis=RIGHT)
            return text_obj

        man_label = create_rotated_text("E(Man)", BLUE)
        woman_label = create_rotated_text("E(Woman)", RED)
        king_label = create_rotated_text("E(King)", GREEN)
        queen_label = create_rotated_text("E(Queen)", PURPLE)

        # Position labels in 3D space
        man_label.next_to(man_vector.get_end(), UP+RIGHT, buff=0.1)
        woman_label.next_to(woman_vector.get_end(), UP+RIGHT, buff=0.1)
        king_label.next_to(king_vector.get_end(), UP+LEFT, buff=0.1)
        queen_label.next_to(queen_vector.get_end(), UP+LEFT, buff=0.1)

        # Add elements to the scene
        self.add(axes)

        # Animate the creation of vectors and labels
        self.play(Create(man_vector), Create(woman_vector), Create(king_vector), Create(queen_vector))
        self.play(Write(man_label), Write(woman_label), Write(king_label), Write(queen_label))
        self.wait(1)

        # Show the vector operations
        operation_text = Text("E(king) - E(queen) ≈ E(man) - E(woman)", font_size=36).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(operation_text)
        self.play(Write(operation_text))
        self.wait(2)

        # Animate the vector differences
        gender_vector1 = Arrow3D(start=man_vector.get_end(), end=woman_vector.get_end(), color=YELLOW)
        gender_vector2 = Arrow3D(start=king_vector.get_end(), end=queen_vector.get_end(), color=YELLOW)
        
        gender_label = create_rotated_text("gender", YELLOW)
        gender_label.move_to((gender_vector1.get_center() + gender_vector2.get_center()) / 2 + UP * 0.5)

        self.play(Create(gender_vector1), Create(gender_vector2))
        self.play(Write(gender_label))
        self.wait(1)

        # Rotate the scene to showcase parallel vector differences
        self.move_camera(phi=70 * DEGREES, theta=-50 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # Highlight the parallel vectors
        self.play(
            gender_vector1.animate.set_color(YELLOW_A),
            gender_vector2.animate.set_color(YELLOW_A),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.wait(2)


if __name__ == "__main__":
    scene = WordEmbeddingVectors()
    scene.render()