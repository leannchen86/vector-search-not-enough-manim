from manim import *

class TokenizationAnimation(Scene):
    def construct(self):
        # Original number with color
        original_number = Text("3458723098", font_size=36, color=BLUE)
        self.play(FadeIn(original_number))
        self.wait(1)
        self.play(original_number.animate.to_edge(UP))

        # Different tokenization possibilities, including "..."
        tokenizations = [
            ["3", "4", "5", "8", "7", "2", "3", "0", "9", "8"],
            ["3458", "723", "098"],
            ["34", "587", "230", "98"],
            ["34", "587", "2309", "8"],
            ["34587", "23098"],
            ["345", "872", "3098"],
            ["..."]  # Add ellipsis as the last entry
        ]

        for i, tokens in enumerate(tokenizations):
            # Handle the special case for "..."
            if tokens == ["..."]:
                # No quotation marks for "..."
                token_texts = tokens
            else:
                # Include quotation marks around each token
                token_texts = [f'"{token}"' for token in tokens]

            token_group = VGroup(
                *[Text(token_text, font_size=24) for token_text in token_texts]
            ).arrange(RIGHT, buff=0.5)
            token_group.next_to(original_number, DOWN, buff=0.6 * (i + 1))
            
            # Use FadeIn to display the line instantly
            self.play(FadeIn(token_group))
            self.wait(0.5)

        self.wait(2)