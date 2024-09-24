from manim import *
import numpy as np
import random

class WordEmbeddingScene(ThreeDScene):
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Create the 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        self.add(axes)

        words = ["neural", "network", "machine", "learning", 
                 "data", "artificial", "intelligence", "vector", "embedding"]

        # Generate random vector positions
        vectors = [np.random.uniform(-4, 4, 3) for _ in words]

        # Create text objects and dots for all words
        text_objects = []
        dots = []
        for word, vector in zip(words, vectors):
            # Create text as a 3D object
            text = Text(word, font_size=24)
            text.rotate(PI/2, RIGHT)  # Rotate to face up in 3D space
            text.move_to(LEFT * 5)  # Start position (left side of screen)
            text_objects.append(text)

            dot = Dot3D(axes.c2p(*vector), color=BLUE)
            dots.append(dot)

        # Add all text objects to the scene
        self.add(*text_objects)

        # Animate all words moving to their positions simultaneously
        animations = []
        for text, vector in zip(text_objects, vectors):
            target_position = axes.c2p(*vector) + UP * 0.3  # Position text slightly above the dot
            animations.append(text.animate.move_to(target_position))

        self.play(*animations, run_time=2)

        # Scale down all text objects
        scale_animations = [text.animate.scale(0.8) for text in text_objects]
        self.play(*scale_animations, run_time=1)

        # Create dots at vector positions
        self.play(*[Create(dot) for dot in dots], run_time=1)

        # Ensure all text objects face the camera
        for text in text_objects:
            self.add_fixed_orientation_mobjects(text)

        # Final camera rotation for dramatic effect
        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.8, run_time=2)
        self.wait(2)