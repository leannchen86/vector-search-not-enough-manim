from manim import *
from manim.animation.indication import Flash

class VectorComparison(Scene):
    def construct(self):
        # Title
        title = Text("Sparse vs Dense Vectors").scale(0.8)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Create sparse and dense vector data
        sparse_vector = [0, 0, 3, 0, 2, 0, 0, 1, 0, 0]
        dense_vector = [0.1, -0.3, 0.7, 0.2, 0.5, -0.1, 0.4, 0.6, -0.2, 0.3]

        # Create visuals
        sparse_visual = self.create_vector_visual(
            sparse_vector,
            "Sparse Vector (BM25)",
            fill_colors=[YELLOW if val != 0 else None for val in sparse_vector]
        )
        dense_visual = self.create_vector_visual(
            dense_vector,
            "Dense Vector (Semantic)",
            # No fill_colors specified, squares will not be colored
        )


        # Animate both visuals appearing
        self.play(Create(dense_visual))
        self.wait(1)

        # Zoom in and amplify dense vector
        self.play(dense_visual.animate.scale(1.5).move_to(ORIGIN))
        self.wait(2)

        dense_txt = Text(
            "Non-zero values in all dimensions capture semantic meaning.",
            font_size=22
        ).next_to(dense_visual, DOWN)


        self.play(Write(dense_txt))
        self.wait(2)
        self.play(FadeOut(dense_txt))

        # De-amplify and return dense vector to its original position
        self.play(dense_visual.animate.scale(1 / 1.5).move_to(ORIGIN))
        self.wait(1)

        # Shift the dense vector up slightly from the top
        self.play(dense_visual.animate.shift(DOWN * 3.0))  # Moves down from the top slightly
        self.wait(0.5)

        self.play(Create(sparse_visual))
        self.wait(1)

        # Zoom in and amplify sparse vector with highlights
        self.play(sparse_visual.animate.scale(1.5).move_to(ORIGIN))
        self.wait(2)

        sparse_txt = Text(
            "Non-zero values only for exact keyword matches.",
            font_size=22
        ).next_to(sparse_visual, DOWN)
        self.play(Write(sparse_txt))

        # Highlight specific values (keyword matches) in transparent yellow
        self.highlight_sparse_values(sparse_visual)
        self.wait(2)
        self.play(FadeOut(sparse_txt))

        # De-amplify and shift sparse vector slightly from the bottom
        self.play(sparse_visual.animate.scale(1 / 1.5).move_to(ORIGIN))
        self.play(sparse_visual.animate.shift(UP * 1.0))  # Moves up slightly from the bottom
        self.wait(2)

    def create_vector_visual(self, vector, label, fill_colors=None):
        cells = VGroup(*[
            Square(side_length=0.5)
            for _ in vector
        ]).arrange(RIGHT, buff=0)

        if fill_colors:
            for cell, color in zip(cells, fill_colors):
                cell.set_fill(color=color, opacity=0.5)  # Transparent fill for highlights
        else:
            for cell in cells:
                cell.set_fill(opacity=0)

        values = VGroup(*[
            Text(str(val), font_size=20).move_to(cell)
            for val, cell in zip(vector, cells)
        ])

        label_text = Text(label, font_size=24).next_to(cells, LEFT)

        return VGroup(cells, values, label_text)

    def highlight_sparse_values(self, sparse_visual):
        cells, values, _ = sparse_visual
        for i, (cell, value) in enumerate(zip(cells, values)):
            if float(value.text) != 0:
                # Highlight the cell and the value at the same time
                cell_highlight = cell.animate.set_fill(color=YELLOW, opacity=0.5)
                value_highlight = Indicate(value, color=YELLOW)
                self.play(cell_highlight, value_highlight)

if __name__ == "__main__":
    scene = VectorComparison()
    scene.render()