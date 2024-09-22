from manim import *

class TimeRelatedTermsScene(ThreeDScene):
    def construct(self):
        # Create a 2D timeline
        timeline = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=False,
            label_direction=UP,
        )
        timeline_labels = VGroup(
            Text('Past', font_size=24).next_to(timeline.n2p(-4), DOWN),
            Text('Present', font_size=24).next_to(timeline.n2p(0), DOWN),
            Text('Future', font_size=24).next_to(timeline.n2p(4), DOWN)
        )

        model_text = Text("Chronological Order", font_size=24).to_edge(UP)
        self.play(Write(model_text))
        self.wait(1)

        self.play(Create(timeline), Write(timeline_labels))
        self.wait(1)

        # Define word positions on the timeline
        terms = {
            'oldest': -3,
            'recent': -1,
            'latest': 0,
            'future': 3.5
        }

        # Create dots and labels for words
        dots = VGroup()
        labels = VGroup()
        for term, pos in terms.items():
            dot = Dot(point=timeline.n2p(pos), color=BLUE)
            label = Text(term, font_size=20).next_to(dot, UP, buff=0.1)
            dots.add(dot)
            labels.add(label)

        self.play(FadeIn(dots), FadeIn(labels))
        self.wait(2)

        # Transition to 3D space
        self.play(FadeOut(timeline), FadeOut(timeline_labels), 
                  FadeOut(dots), FadeOut(labels), FadeOut(model_text))

        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=(-3, 3),
            y_range=(-3, 3),
            z_range=(-3, 3),
            x_length=6,
            y_length=6,
            z_length=6
        )

        # Set up the scene for initial 3D view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, zoom=0.6)
        self.add(axes_3d)

        vector_space_text = Text("Vector Space", font_size=24).to_edge(UP)
        self.add_fixed_in_frame_mobjects(vector_space_text)
        self.play(Write(vector_space_text))

        # Zoom in
        self.move_camera(zoom=0.8, run_time=3)

        # Rotate to show 3D nature
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, zoom=0.6, run_time=3)

        # Define new 3D positions for the terms
        new_positions_3d = {
            'oldest': [-2, -1, -2],
            'recent': [1, 1.5, 0.5],
            'current': [1.5, 0, 1],
            'latest': [2, 1, 1.5],
            'future': [0, -2, 2]
        }

        # Create 3D dots and labels
        dots_3d = VGroup()
        labels_3d = VGroup()

        for term, pos in new_positions_3d.items():
            dot_3d = Dot3D(point=axes_3d.c2p(*pos), color=BLUE, radius=0.1)
            label_3d = Text(term, font_size=22)
            label_3d.next_to(dot_3d, UP+OUT, buff=0.1)
            self.add_fixed_orientation_mobjects(label_3d)
            dots_3d.add(dot_3d)
            labels_3d.add(label_3d)

        self.play(Create(dots_3d), Write(labels_3d))
        self.wait(2)

        # Smooth transition to sky view
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, zoom=0.8, run_time=3)
        self.wait(2)

        # Replace the existing text with the new one
        self.play(FadeOut(vector_space_text))
        new_text = Text("Without explicit chronological order", font_size=24).to_edge(UP)
        self.add_fixed_in_frame_mobjects(new_text)
        self.play(Write(new_text))
        self.wait(2)  # Wait for 2 seconds to show the new text

        # Highlight contextual similarity
        similar_terms = VGroup(dots_3d[1], dots_3d[2], dots_3d[3])  # recent, current, latest
        context_circle = Circle(color=YELLOW, radius=1.5).move_to(similar_terms.get_center())
        context_text = Text("Contextually Similar", color=YELLOW, font_size=22)
        context_text.next_to(context_circle, RIGHT)
        self.add_fixed_orientation_mobjects(context_text)

        self.play(Create(context_circle), Write(context_text))
        self.wait(2)

        # Fade out everything
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)