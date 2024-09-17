from manim import *

class CapitalCountryEmbedding(Scene):
    def construct(self):
        # Create the text for the equation
        equation_text = Text("E(France) - E(Paris) ≈ E(Poland) - E(Warsaw)", font_size=36)
        
        # Create explanation text
        explanation = Text("Vector difference captures the concept of 'capital city'", font_size=24)
        
        # Position the explanation text just above the equation
        explanation.next_to(equation_text, UP, buff=0.5)  # You can adjust the buff value to change the spacing
        
        # Animate the writing of the texts with faster speed
        self.play(Write(equation_text, run_time=0.8))
        self.play(Write(explanation, run_time=0.8))
        
        # Wait for a moment to let the viewer read
        self.wait(2)

if __name__ == "__main__":
    scene = CapitalCountryEmbedding()
    scene.render()