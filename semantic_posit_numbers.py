from manim import *
import numpy as np
import gensim.downloader
from sklearn.decomposition import PCA

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

        # Define words and their corresponding vector positions
        words = ["All", "data", "in", "deep", "learning", "must", "be", "represented", "as", "vectors"]
        vectors = [
            np.array([2, 1, 3]),
            np.array([-1, 4, 2]),
            np.array([3, -2, 1]),
            np.array([-2, -3, 4]),
            np.array([4, 2, -1]),
            np.array([1, -4, -3]),
            np.array([-3, 1, -2]),
            np.array([2, 3, 2]),
            np.array([-1, -1, 3]),
            np.array([3, 2, -4])
        ]

        # Create and animate words
        for word, vector in zip(words, vectors):
            # Create text object
            text = Text(word, font_size=24)
            text.move_to(LEFT * 5)  # Start position (left side of screen)
            
            # Create dot at vector position
            dot = Dot3D(axes.c2p(*vector), color=BLUE)
            
            # Animate text moving to vector position
            self.play(
                Write(text),
                text.animate.move_to(axes.c2p(*vector)),
                Create(dot),
                run_time=2
            )
            
            # Scale down the text and make it face the camera
            self.play(
                text.animate.scale(0.5).rotate(about_point=text.get_center(), angle=self.camera.get_theta()),
                run_time=1
            )

        # Final camera rotation for dramatic effect
        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.8, run_time=2)
        self.wait(2) 


class NumberEmbeddingVisualization(ThreeDScene):
    def construct(self):
        # Load pre-trained word2vec model
        self.model = gensim.downloader.load('glove-wiki-gigaword-50')

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],
        )

        # Numbers to visualize
        numbers = ["50", "100", "150"]
        colors = [BLUE, GREEN, RED]

        # Get embeddings and reduce to 3D
        embeddings = [self.model[num] for num in numbers]
        pca = PCA(n_components=3)
        reduced_embeddings = pca.fit_transform(embeddings)

        # Normalize the embeddings for visualization
        max_val = np.abs(reduced_embeddings).max()
        reduced_embeddings *= 4 / max_val

        # Create number vectors
        number_vectors = VGroup()
        for number, color, embedding in zip(numbers, colors, reduced_embeddings):
            arrow = Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(*embedding),
                color=color
            )
            label = Text(number, font_size=24).next_to(arrow.get_end(), UP)
            
            # Rotate the label to face the audience
            label.rotate(PI/2, axis=UP)
            label.rotate(PI/2, axis=RIGHT)
            
            number_vectors.add(VGroup(arrow, label))

        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Add elements to the scene
        self.add(axes)
        self.play(Create(axes))
        for vector in number_vectors:
            self.play(Create(vector[0]), Write(vector[1]))

        # Add lines between numbers to show relationships
        lines = VGroup()
        for i in range(len(number_vectors) - 1):
            start = number_vectors[i][0].get_end()
            end = number_vectors[i+1][0].get_end()
            line = Line3D(start=start, end=end, color=YELLOW)
            lines.add(line)

        self.play(Create(lines))

        # Wait for a moment to show the final result
        self.wait(10)

    def get_embedding(self, number):
        return self.model[str(number)]