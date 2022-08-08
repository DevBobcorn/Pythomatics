from manim import *

class ThreeDTest(ThreeDScene):
    def construct(self):
        # Initialize 3D axis and camera
        self.set_camera_orientation(phi=0, theta=0)

        face_data = [
            ([ 0, 0, 1],   0,  OUT),
            ([ 0, 0,-1],   0,  OUT),
            ([ 1, 0, 0],  90,   UP),
            ([-1, 0, 0],  90,   UP),
            ([ 0,-1, 0],  90, LEFT),
            ([ 0, 1, 0],  90, LEFT)
        ]

        # Make 2D Squares
        square_original = []
        square_changed  = []
        square_backup   = []
        square_texts    = []

        for i in range(6):
            square_original.append(Square(side_length=2, color=BLUE, fill_opacity=0))
            square_original[i].move_to(np.array(face_data[i][0]))
            square_original[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            square_original[i].stroke_color = WHITE
            square_original[i].stroke_width = 2
        
        for i in range(6):
            square_changed.append(Square(side_length=2, color=BLUE, fill_opacity=0.5))
            square_changed[i].move_to(np.multiply(1.4, np.array(face_data[i][0])))
            square_changed[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            square_changed[i].stroke_color = WHITE
            square_changed[i].stroke_width = 2
        
        for i in range(6):
            square_backup.append(Square(side_length=2, color=BLUE, fill_opacity=0.5))
            square_backup[i].move_to(np.array(face_data[i][0]))
            square_backup[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            square_backup[i].stroke_width = 2
        
        text_data = [
            ( 90,  OUT, '上'),
            ( 90,  OUT, '下'),
            (270, LEFT, '前'),
            (270, LEFT, '后'),
            (180,   UP, '左'),
            (180,   UP, '右')
        ]

        cube_text = Text('这是在Minecraft中最基本的图形', font_size=32)

        self.add_fixed_in_frame_mobjects(cube_text)
        cube_text.to_corner(UL)

        for i in range(6):
            square_texts.append(Text(text_data[i][2], color=WHITE, fill_opacity=1))
            square_texts[i].move_to(np.array(face_data[i][0]))
            square_texts[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            square_texts[i].rotate(text_data[i][0] * DEGREES, text_data[i][1])

        self.play(Create(square_original[0]), FadeIn(cube_text))
        self.play(Create(square_original[1]))
        self.play(Create(square_original[2]), Create(square_original[3]), Create(square_original[4]), Create(square_original[5]))

        # Rotate transform
        def update_theta(m, dt):
            origin_theta = m.get_value()
            m.set_value(origin_theta + 20 * DEGREES * dt) # 60 degs in total
        
        def update_phi(m, dt):
            origin_phi = m.get_value()
            m.set_value(origin_phi + 25 * DEGREES * dt)   # 75 degs in total

        self.renderer.camera.theta_tracker.add_updater(update_theta)
        self.add(self.renderer.camera.theta_tracker)

        self.renderer.camera.phi_tracker.add_updater(update_phi)
        self.add(self.renderer.camera.phi_tracker)

        self.wait(3)

        self.renderer.camera.theta_tracker.remove_updater(update_theta)
        self.renderer.camera.phi_tracker.remove_updater(update_phi)

        # Fill up the cube (animate opacity)
        op = ValueTracker(0)
        for face in square_original:
            face.add_updater(lambda f: f.set_fill(opacity=op.get_value()))
        
        self.play(op.animate.set_value(0.5))

        self.set_camera_orientation(phi=75 * DEGREES, theta=60 * DEGREES)

        question_text = Text('它有几个顶点?', font_size=32)
        question_text.to_corner(UL)
        self.play(Transform(cube_text, question_text))
        self.wait()

        answer_text = Text('8个?')
        self.add_fixed_in_frame_mobjects(answer_text)
        anims = [] # Show the 8 vertices...
        anims.append(FadeOut(cube_text)) # Alter texts...
        visual_dots = []
        for vert in square_original[0].get_vertices(): # 4 vertices on top face
            d = Dot(point=vert, color=BLUE)
            self.add_fixed_orientation_mobjects(d)
            visual_dots.append(d)
        for vert in square_original[1].get_vertices(): # And 4 vertices on bottom face
            d = Dot(point=vert, color=BLUE)
            self.add_fixed_orientation_mobjects(d)
            visual_dots.append(d)
        for d in visual_dots:
            anims.append(FadeIn(d))
        anims.append(Write(answer_text)) # Show text
        self.play(*anims)
        self.wait()

        anims = [] # Tear these faces apart
        # Fade out previous 8 dots
        for d in visual_dots:
            anims.append(FadeOut(d))
        anims.append(Unwrite(answer_text))
        for face1, face2 in zip(square_original, square_changed):
            anims.append(Transform(face1, face2))
        self.play(*anims)
        self.wait()

        visual_dots = []
        for face in square_original: # Add all 24 vertices
            for vert in face.get_vertices():
                d = Dot(point=vert, color=GREEN)
                self.add_fixed_orientation_mobjects(d)
                visual_dots.append(d)
        anims = [] # Show 24 vertices on the torn cube
        for d in visual_dots:
            anims.append(FadeIn(d))
        answer_text_correct = Text('不, 其实是24个')
        answer_text_correct.shift(DOWN * 3)
        self.add_fixed_in_frame_mobjects(answer_text_correct)
        anims.append(Write(answer_text_correct))
        self.play(*anims)
        self.wait()

        for d in visual_dots:
            anims.append(FadeOut(d))
        anims = [] # Clear 24 vertices on the torn cube
        for d in visual_dots:
            anims.append(FadeOut(d))
        anims.append(FadeOut(answer_text))
        self.play(*anims)
        self.wait()
        why_text = Text('为什么呢？')
        why_text.shift(DOWN * 3)
        self.add_fixed_in_frame_mobjects(why_text)
        self.play(FadeOut(answer_text_correct), FadeIn(why_text))
        self.wait()
        self.play(Unwrite(why_text))
        #self.wait()
        
        anims = [] # Then stitch the faces back
        for face1, face2 in zip(square_original, square_backup):
            anims.append(Transform(face1, face2))
        self.play(*anims)

        # Show transform
        axes = ThreeDAxes()
        axes.move_to(np.array([-1,-1,-1]))
        self.play(FadeIn(axes))

        # TEXT: We know that every face of a block has a texture
        #self.begin_3dillusion_camera_rotation(rate=-1)
        self.begin_3dillusion_camera_rotation()
        anims = [] # Show and explain textures
        anims.append(FadeOut(answer_text))

        for t in square_texts:
            anims.append(FadeIn(t))
        self.play(*anims)
        self.wait()

        #group = VGroup(*sq2)
        #self.play(group.animate(lag_ratio=0.1, run_time=1).rotate(PI))

        self.wait(3)
        self.stop_3dillusion_camera_rotation()

        # TEMP SETUP
        #self.set_camera_orientation(phi=75 * DEGREES, theta=60 * DEGREES)
        #self.add(Cube())

        sampleDot = Dot(np.array([1, 1, 1]))
        self.add_fixed_orientation_mobjects(sampleDot)
        self.play(FadeIn(sampleDot))

        # Set up front and right face for demonstration
        front_face = Square(side_length=2, color=YELLOW, fill_opacity=0.5)
        # Slightly offset a bit more, so that it won't get stuck in cube face
        front_face.move_to(np.multiply(1.01, np.array(face_data[2][0])))
        front_face.rotate(face_data[2][1] * DEGREES, face_data[2][2])
        front_face.stroke_color = WHITE
        front_face.stroke_width = 2
        front_text = Text('在前方的面上，这个点对应贴图的右上角\n它的UV坐标是（1，1）', font_size=36, color=WHITE, fill_opacity=1)
        front_text.rotate(face_data[2][1] * DEGREES, face_data[2][2])
        front_text.rotate(text_data[2][0] * DEGREES, text_data[2][1])
        front_text.move_to(np.array(np.array([0, 2, 2])))

        right_face = Square(side_length=2, color=YELLOW, fill_opacity=0.5)
        # Slightly offset a bit more, so that it won't get stuck in cube face
        right_face.move_to(np.multiply(1.01, np.array(face_data[5][0])))
        right_face.rotate(face_data[5][1] * DEGREES, face_data[5][2])
        right_face.stroke_color = WHITE
        right_face.stroke_width = 2
        right_text = Text('而右面的此点对应贴图的左上角\n它的UV坐标则是（0，1）', font_size=36, color=WHITE, fill_opacity=1)
        right_text.rotate(face_data[5][1] * DEGREES, face_data[5][2])
        right_text.rotate(text_data[5][0] * DEGREES, text_data[5][1])
        right_text.move_to(np.array(np.array([-5, 1, 1])))

        self.play(Create(front_face))
        self.wait()
        self.play(Create(front_text))
        self.wait(4)
        self.play(FadeOut(front_text), Transform(front_face, right_face))
        self.wait()
        self.play(Create(right_text))
        self.wait(4)
        self.play(FadeOut(front_face))
        self.wait()

        # Move camera further to show a wider area
        #self.move_camera(phi=1, zoom=0.5)

# manim -p 3dtest.py
# manim -p -ql 3dtest.py
