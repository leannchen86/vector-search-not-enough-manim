from manim import *

class TFScoreComparison(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 28, 4],
            y_range=[0, 6, 1],
            axis_config={"color": GREY},
            x_axis_config={"numbers_to_include": range(0, 29, 4)},
            y_axis_config={"numbers_to_include": range(0, 7, 1)},
        ).scale(0.6)
        axes_labels = axes.get_axis_labels(x_label="Term Frequency", y_label="TF Score")

        # Create graphs
        classic_tf = axes.plot(lambda x: min(5.3, 1.2 * x ** 0.45), color=RED)
        bm25_tf = axes.plot(lambda x: 2.2 * (1.2 * x) / (x + 1.2), color=BLUE)

        # Labels
        classic_label = Text("Classic TF score", color=RED).scale(0.42).next_to(classic_tf, UR, buff=0.3)
        # Adjust BM25 label position
        bm25_label = Text("BM25 TF Score", color=BLUE).scale(0.42)
        bm25_label.next_to(axes.c2p(28, bm25_tf.underlying_function(28)), UR, buff=0.3)

        # Saturation area (dotted rectangle)
        saturation_start = 5
        saturation_end = 13.5
        
        start_point = axes.c2p(saturation_start, 1.9)
        end_point = axes.c2p(saturation_end, 2.398)
        saturation_area = DashedVMobject(
            Rectangle(
                width=end_point[0] - start_point[0],
                height=end_point[1] - start_point[1],
                stroke_color=YELLOW,
                stroke_width=2,
                fill_opacity=0
            ).move_to((start_point + end_point) / 2)
        )

        saturation_label = Text("Saturation", color=YELLOW).scale(0.5).next_to(saturation_area, UR, buff=0.1)

        # Animation
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(classic_tf), Create(bm25_tf))
        self.play(Write(classic_label), Write(bm25_label))
        
        self.wait(1)
        
        self.play(Create(saturation_area), Write(saturation_label))
        
        # Highlight both curves
        x_tracker = ValueTracker(1)
        classic_dot = Dot(color=RED)
        bm25_dot = Dot(color=BLUE)
        
        classic_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), classic_tf.underlying_function(x_tracker.get_value()))))
        bm25_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), bm25_tf.underlying_function(x_tracker.get_value()))))
        
        self.add(classic_dot, bm25_dot)
        self.play(x_tracker.animate.set_value(28), run_time=5)
        
        self.wait(2)