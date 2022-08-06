from turtle import up
from manim import *

class Test02(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        # Initialize 3D axis and camera
        self.set_camera_orientation(phi=0, theta=0)

        #test = Square(side_length=1, fill_opacity = 0)
        #test.stroke_width = 1
        #self.add(test)

        # Make 2D Squares
        sqr = []
        # Top
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[0].move_to(np.array([ 0, 0, 1]))

        # Bottom
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[1].move_to(np.array([ 0, 0,-1]))
        sqr[1].rotate(180 * DEGREES, LEFT)

        # Front
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[2].move_to(np.array([ 1, 0, 0]))
        sqr[2].rotate(90 * DEGREES, UP)

        # Back
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[3].move_to(np.array([-1, 0, 0]))
        sqr[3].rotate(90 * DEGREES, UP)

        # Left
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[4].move_to(np.array([ 0, 1, 0]))
        sqr[4].rotate(90 * DEGREES, RIGHT)

        # Right
        sqr.append(Square(side_length = 2, color=BLUE, fill_opacity=0))
        sqr[5].move_to(np.array([ 0,-1, 0]))
        sqr[5].rotate(90 * DEGREES, RIGHT)

        for face in sqr:
            face.stroke_width = 2
        
        self.play(Create(sqr[0]), Create(sqr[1]))
        self.play(Create(sqr[2]), Create(sqr[3]), Create(sqr[4]), Create(sqr[5]))

        # Rotate transform
        def update_theta(m, dt):
            origin_theta = m.get_value()
            m.set_value(origin_theta + 60 * DEGREES * dt)
        
        def update_phi(m, dt):
            origin_phi = m.get_value()
            m.set_value(origin_phi + 75 * DEGREES * dt)

        self.renderer.camera.theta_tracker.add_updater(update_theta)
        self.add(self.renderer.camera.theta_tracker)

        self.renderer.camera.phi_tracker.add_updater(update_phi)
        self.add(self.renderer.camera.phi_tracker)

        self.wait(1)

        self.renderer.camera.theta_tracker.remove_updater(update_theta)
        self.renderer.camera.phi_tracker.remove_updater(update_phi)

        # Anim test function
        dot = Dot(color=GREEN)
        x = ValueTracker(0)
        dot.add_updater(lambda d: d.set_x(x.get_value()))
        self.add(dot)
        self.play(x.animate.set_value(5))

        # Fill up the cube (animate opacity)
        op = ValueTracker(0)
        for face in sqr:
            face.add_updater(lambda f: f.set_fill(color=BLUE, opacity=op.get_value()))
        
        self.play(op.animate.set_value(0.5))

        self.begin_ambient_camera_rotation(1)
        self.wait(360 * DEGREES)
        self.stop_ambient_camera_rotation()

        self.wait()

