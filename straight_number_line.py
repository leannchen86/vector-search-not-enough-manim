from manim import *

class NumberLineScene(Scene):
    def construct(self):
        # Create the number line
        number_line = NumberLine(
            x_range=[0, 200, 50],
            length=10,
            include_numbers=True,
            numbers_to_include=[50, 100, 150],
            label_direction=DOWN
        )
        self.play(Create(number_line))

        # Create arrows and labels for the 50-unit jumps
        arrows = VGroup()
        labels = VGroup()
        for start, end in [(50, 100), (100, 150)]:
            arrow = Arrow(
                start=number_line.number_to_point(start),
                end=number_line.number_to_point(end),
                buff=0.1,
                stroke_width=3,
                color=RED
            )
            label = Text("50-unit", font_size=24).next_to(arrow, UP, buff=0.1)
            arrows.add(arrow)
            labels.add(label)

        # Animate arrows slowly
        self.play(Create(arrows), run_time=5)

        # Animate labels at normal speed
        self.play(Write(labels))
        self.wait(5)