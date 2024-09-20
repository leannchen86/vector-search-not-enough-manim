from manim import *

class TFScoreLengthNormalization(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 24, 4],
            y_range=[0, 2, 0.5],
            axis_config={"color": GREY},
            x_axis_config={"numbers_to_include": range(0, 25, 4)},
            y_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
        ).scale(0.8)
        axes_labels = axes.get_axis_labels(x_label="Term Frequency", y_label="TF Score")

        # Create graphs
        avg_doc = axes.plot(lambda x: 1.2 * (1.2 * x) / (x + 1.2), color="#E49B86")
        short_doc = axes.plot(lambda x: 1.2 * (2 * x) / (x + 2.3), color="#A19AE8")
        long_doc = axes.plot(lambda x: 1.2 * (0.5 * x) / (x + 0.5), color="#F7C06C")

        # Labels
        avg_label = Text("TF Score of average doc", color="#E49B86").scale(0.4)
        short_label = Text("TF Score 1/5 length of average doc", color="#A19AE8").scale(0.4)
        long_label = Text("TF Score 5 times length of average doc", color="#F7C06C").scale(0.4)

        # Position labels
        avg_label.next_to(axes.c2p(24, avg_doc.underlying_function(24)), DOWN*2, buff=0.1)
        short_label.next_to(axes.c2p(24, short_doc.underlying_function(24)), DOWN*3, buff=0.1)
        long_label.next_to(axes.c2p(24, long_doc.underlying_function(24)), DOWN*1.5, buff=0.1)

        # Animation
        self.play(Create(axes), Write(axes_labels))
        
        # Animate average doc
        self.play(Create(avg_doc), Write(avg_label))
        self.wait(1)
        
        # Animate short doc
        self.play(Create(short_doc), Write(short_label))
        self.wait(1)
        
        # Animate long doc
        self.play(Create(long_doc), Write(long_label))
        self.wait(1)

        # Explanation text
        explanation = Text(
            "BM25 adjusts for document length.\nShorter documents may score higher with the same term frequency.",
            font_size=22,
            color=WHITE
        ).next_to(axes, DOWN, buff=0.5)
        self.play(Write(explanation))

        # Highlight differences
        x_tracker = ValueTracker(0)
        avg_dot = Dot(color="#E49B86")
        short_dot = Dot(color="#A19AE8")
        long_dot = Dot(color="#F7C06C")

        avg_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), avg_doc.underlying_function(x_tracker.get_value()))))
        short_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), short_doc.underlying_function(x_tracker.get_value()))))
        long_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), long_doc.underlying_function(x_tracker.get_value()))))

        self.add(avg_dot, short_dot, long_dot)
        self.play(x_tracker.animate.set_value(24), run_time=5)

        self.wait(2)