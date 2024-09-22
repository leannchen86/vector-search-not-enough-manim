from manim import *
import numpy as np

class BM25IDFVisualization(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 100000, 20000],
            y_range=[0, 5, 1],
            axis_config={"color": GREY},
            x_axis_config={"numbers_to_include": range(0, 100001, 20000)},
            y_axis_config={"numbers_to_include": []}
        ).scale(0.7)
        
        # Custom y-axis labels
        y_labels = VGroup()
        for i, label in enumerate(["10⁻²", "10⁻¹", "10⁰", "10¹", "10²"]):
            y_labels.add(Text(label, font_size=16).next_to(axes.c2p(0, i+1), LEFT))
        
        axes_labels = axes.get_axis_labels(
            x_label="Document Frequency",
            y_label="IDF"
        )

        # Assume N (total documents) is 100,000
        N = 100000

        # Custom log-like function
        def custom_log(x):
            return np.log1p(x) / np.log(10) + 1

        # BM25 IDF function
        def bm25_idf(x):
            return custom_log(((N - x + 0.5) / (x + 0.5)) + 1)

        bm25_curve = axes.plot(bm25_idf, color=RED, x_range=[1, N-1])

        bm25_label = Text("IDF from BM25", color=RED).scale(0.7)
        
        legend = VGroup(bm25_label).to_edge(DOWN)

        # Add markers for rare and common terms
        rare_term_x = 2000
        common_term_x = 90000
        medium_term_x = 30000

        rare_dot = Dot(color=GREEN).move_to(axes.c2p(rare_term_x, bm25_idf(rare_term_x)))
        common_dot = Dot(color=RED).move_to(axes.c2p(common_term_x, bm25_idf(common_term_x)))
        medium_dot = Dot(color=YELLOW).move_to(axes.c2p(medium_term_x, bm25_idf(medium_term_x)))

        rare_label = Text("hybrid search", font_size=22, color=GREEN).next_to(rare_dot, RIGHT, buff=0.1)
        common_label = Text("the", font_size=22, color=WHITE).next_to(common_dot, UP, buff=0.1)
        medium_label = Text("system", font_size=22, color=YELLOW).next_to(medium_dot, UP, buff=0.1)

        # Add BM25 IDF formula
        formula = MathTex(
            r"\text{IDF} = \log\left(\frac{N - df_t + 0.5}{df_t + 0.5} + 1\right)"
        ).scale(0.5).to_corner(UR)

        # Add explanation for N and df_t, positioned below the formula
        explanation = VGroup(
            Text("N = number of documents", font_size=30),
            Text("df_t = number of docs that contain the term", font_size=30)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5)

        explanation.next_to(formula, DOWN, buff=0.1)  # Positioning explanation below formula

        # Animation
        self.play(Write(formula))
        self.play(Write(explanation))  # Display formula and explanation together
        self.play(Create(axes), Write(axes_labels), Write(y_labels))
        self.play(Create(bm25_curve))
        self.play(Write(legend))
        self.play(FadeIn(rare_dot), Write(rare_label))
        self.wait(0.5)
        self.play(FadeIn(medium_dot), Write(medium_label))
        self.wait(0.5)
        self.play(FadeIn(common_dot), Write(common_label))
        self.wait(2)

        # Add a final text explanation
        bm25_core = Text("Higher IDF scores mean the  terms are rarer and more important\nfor identifying relevant documents.", font_size=20)
        bm25_core.next_to(medium_label, UR, buff=0.5)
        self.play(Write(bm25_core))
        self.wait(2)

        self.play(
            FadeOut(rare_dot), FadeOut(common_dot), FadeOut(medium_dot),
            FadeOut(rare_label), FadeOut(common_label), FadeOut(medium_label),
            FadeOut(legend), FadeOut(explanation), FadeOut(formula), FadeOut(bm25_core)
        )