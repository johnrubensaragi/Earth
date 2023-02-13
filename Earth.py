from manim import *
import math

config.disable_caching = True

def exponential_growth(t: float) -> float:
    earth_circumference_in_inches = 4007501700/2.54
    return (earth_circumference_in_inches/2)**(t-1)

def exponential_decay(t: float) -> float:
    earth_circumference_in_inches = 4007501700/2.54
    return 1-(earth_circumference_in_inches/2)**(-t)

class Earth(Scene):  
    def construct(self):
        DEFAULT_FONT_SIZE = 36

        def x(angle): #cos
            if isinstance(angle, np.float64):
                return r*math.cos(angle)
            return r*math.cos(angle.get_value())
        
        def x_D(angle): #cot
            if x(angle) != 0 and y(angle) > 0:
                return r / math.tan(angle.get_value())
            else: return 0
            
        def y(angle): #sin
            if isinstance(angle, np.float64):
                return r*math.sin(angle)
            return r*math.sin(angle.get_value())
        
        def animated_font_size(var, angle_ValueTracker):
            angle = angle_ValueTracker.get_value()
            if var == "d": 
                if angle < 1.4*PI/2:
                    return (angle-(PI/2))/(0.4*PI/2)*(DEFAULT_FONT_SIZE-1)+1
                else:
                    return DEFAULT_FONT_SIZE
        
        θ = ValueTracker(PI/2)
        origin = np.array([0, 0, 0])
        r = 2

        # Circle
        circle = Circle(radius=r, color=GREEN, stroke_width=0.5).set_fill(BLUE, opacity=0.5).shift(origin)
        
        # Middle Dot O(0,0)
        O = [0, 0, 0]
        dot_O = Dot(point=O, color=WHITE)

        # Observer Dot A(0,r)
        def A(angle):   # Coordinates for A
            return [0, r, 0]
        
        dot_A = Dot(point=A(θ), color=WHITE).shift(origin)

        # Horizon dot B(rcosθ, rsinθ)
        def B(angle):
            return [x(angle), y(angle)+0.01, 0] # Kalau tidak ditambah 0.01 akan error, gak tau kenapa. Mungkin karena panjang garis tidak boleh pas nol.
        
        dot_B = always_redraw(
            lambda: Dot(point=A(θ), color=WHITE)
                    .move_to(point_or_mobject=B(θ)).shift(origin)
        )

        # Dot for d_2 C(rcosθ, r)
        def C(angle):
            return [x(angle), r, 0]
        
        dot_C = always_redraw(
            lambda: Dot(point=A(θ), color=WHITE)
                    .move_to(point_or_mobject=C(θ)).shift(origin)
        )

        # Dot for h_2 D(rcotθ, r)

        def D(angle):
            return [x_D(angle), r, 0]
        dot_D = always_redraw(
            lambda: Dot(point=A(θ), color=WHITE)
                    .move_to(point_or_mobject=D(θ)).shift(origin)
        )

        line_OA = Line(start=O, end=A(θ)).shift(origin)
        line_AC = always_redraw(
            lambda: Line(start=A(θ), end=C(θ)).shift(origin)
        )
        line_BC = always_redraw(
            lambda: Line(start=B(θ), end=C(θ)).shift(origin)
        )
        line_AD = always_redraw(
            lambda: Line(start=A(θ), end=D(θ)).shift(origin)
        )
        line_OD = always_redraw(
            lambda: Line(start=O, end=D(θ)).shift(origin)
        )
        line_BD = always_redraw(
            lambda: Line(start=B(θ), end=D(θ)).shift(origin)
        )
        
        text_angle = always_redraw(
            lambda: MathTex(r"\theta", font_size=animated_font_size("d", θ)).move_to(
                Angle(
                    line_OA, line_OD, radius=0.8, other_angle=False
                ).point_from_proportion(0.5)
            )
        )
        
        arc_angle = always_redraw(
            lambda: Angle(line_OA, line_OD, radius=0.5, other_angle=False)
        )

        text_r1 = MathTex("r", font_size=DEFAULT_FONT_SIZE).next_to(line_OA, RIGHT)
        text_r2 = always_redraw(
            lambda: MathTex("r", font_size=DEFAULT_FONT_SIZE).move_to([x(θ.get_value()+0.3)*0.52, y(θ.get_value()+0.3)*0.52, 0]+origin)
        )
        text_O = MathTex("O", font_size=DEFAULT_FONT_SIZE).next_to(dot_O, DOWN)
        text_A = MathTex("A", font_size=DEFAULT_FONT_SIZE).next_to(dot_A, UP, buff=0.5)
        text_B = always_redraw(
            lambda: MathTex("B", font_size=DEFAULT_FONT_SIZE).move_to([x(θ.get_value()+0.2)*0.9, y(θ.get_value()+0.2)*0.9, 0]+origin)
        )
        text_C = always_redraw(
            lambda: MathTex("C", font_size=animated_font_size("d", θ)).next_to(dot_C, UP, buff=0.5)
        )
        text_D = always_redraw(
            lambda: MathTex("D", font_size=animated_font_size("d", θ)).next_to(dot_D, UP, buff=0.5)
        )
        
        arc_AB = always_redraw(
            lambda: Angle(line_OA, line_OD, radius=r, other_angle=False, color=RED)
        )
        
        text_d1 = always_redraw(
            lambda: MathTex("d_1", font_size=animated_font_size("d", θ)).move_to(
                Angle(
                    line_OA, line_OD, radius=r-0.3, other_angle=False
                ).point_from_proportion(0.5)
            )
        )
        brace_d2 = always_redraw(lambda: Brace(line_AC, direction=UP))
        text_d2 = always_redraw(
            lambda: MathTex("d_2", font_size=animated_font_size("d", θ)).next_to(brace_d2, UP)
        )
        brace_d3 = always_redraw(lambda: Brace(line_AD, buff=1, direction=UP))
        text_d3 = always_redraw(
            lambda: MathTex("d_3", font_size=animated_font_size("d", θ)).next_to(brace_d3, UP)
        )
        text_h1 = always_redraw(
            lambda: MathTex("h_1", font_size=animated_font_size("d", θ)).next_to(line_BC, RIGHT, buff=0.1)
        )
        brace_h2 = always_redraw(lambda: BraceBetweenPoints(D(θ), B(θ))) # D dulu baru B supaya bracenya di bawah garis, bukan di atas
        text_h2 = always_redraw(
            lambda: MathTex("h_2", font_size=animated_font_size("d", θ)).next_to(line_BD, ORIGIN).shift([-y(θ)/r*0.7,x(θ)/r*0.7,0])
        )
        self.add(circle,
                  
                 line_AD, 
                 line_AC,
                 line_BC,
                 line_BD,
                 line_OD, 
                 line_OA,

                 dot_O,
                 dot_A,
                 dot_B,
                 dot_C, 
                 dot_D,
                 
                 text_angle,
                 text_r1,
                 text_r2,
                 text_O, 
                 text_A, 
                 text_B, 
                 text_C, 
                 text_D, 
                 text_d1,
                 text_d2, 
                 text_d3,
                 text_h1,
                 text_h2, 

                 arc_AB, 
                 arc_angle,
                 
                 brace_d2,
                 brace_d3,
                 brace_h2
        )
        self.bring_to_front(text_h1)
        self.play(θ.animate.set_value(PI), run_time=10, rate_func=linear)
    