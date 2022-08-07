from manim import *

class ThreeDTest(ThreeDScene):
    def construct(self):
        # Initialize 3D axis and camera
        self.set_camera_orientation(phi=0, theta=0)

        '''test = Square(side_length=1, fill_opacity = 0)
        test.stroke_width = 1
        test.stroke_color=WHITE
        self.add(test)
        test.get_vertices()'''

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

        texto = Text('在Minecraft中,最基本的模型便是立方体', font_size=32)
        text1 = Text('那么问题来了,一个这样的立方体有几个顶点?', font_size=32)
        text2 = Text('8个?', font_size=32)
        text3 = Text('不,其实是24个', font_size=32)
        text4 = Text('为什么呢?', font_size=32)
        text5 = Text('我们知道,MC中的方块每个面都是带有纹理的', font_size=32)
        text6 = Text('而纹理坐标,也就是uv,是保存在顶点信息中的', font_size=32)

        self.add_fixed_in_frame_mobjects(texto)
        texto.to_corner(UL)

        for i in range(6):
            square_texts.append(Text(text_data[i][2], color=WHITE, fill_opacity=1))
            square_texts[i].move_to(np.array(face_data[i][0]))
            square_texts[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            square_texts[i].rotate(text_data[i][0] * DEGREES, text_data[i][1])

        self.play(Create(square_original[0]), FadeIn(texto))
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

        text1.to_corner(UL)
        self.play(Transform(texto, text1))
        self.wait()

        # TEXT: Eight?
        text2.to_corner(UL)
        anims = [] # Show the 8 vertices...
        anims.append(Transform(texto, text2)) # Update text
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
        self.play(*anims)
        self.wait()

        # TEXT: No, actually there're 24
        text3.to_corner(UL)
        anims = [] # Tear these faces apart
        # Fade out previous 8 dots
        for d in visual_dots:
            anims.append(FadeOut(d))
        for face1, face2 in zip(square_original, square_changed):
            anims.append(Transform(face1, face2))
        anims.append(Transform(texto, text3))
        self.play(*anims)
        self.wait(0.2)
        visual_dots = []
        for face in square_original: # Add all 24 vertices
            for vert in face.get_vertices():
                d = Dot(point=vert, color=GREEN)
                self.add_fixed_orientation_mobjects(d)
                visual_dots.append(d)
        anims = [] # Show 24 vertices on the torn cube
        for d in visual_dots:
            anims.append(FadeIn(d))
        self.play(*anims)
        self.wait(0.5)

        # TEXT: Why?
        anims = [] # Clear 24 vertices on the torn cube
        for d in visual_dots:
            anims.append(FadeOut(d))
        text4.to_corner(UL)
        anims.append(Transform(texto, text4))
        self.play(*anims)
        self.wait(0.5)
        
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
        text5.to_corner(UL)
        anims.append(Transform(texto, text5))

        for t in square_texts:
            anims.append(FadeIn(t))
        self.play(*anims)
        self.wait()

        #group = VGroup(*sq2)
        #self.play(group.animate(lag_ratio=0.1, run_time=1).rotate(PI))

        text6.to_corner(UL)
        self.play(Transform(texto, text6))
        self.wait(1)

        #self.stop_3dillusion_camera_rotation()

        # Move camera further to show a wider area
        #self.move_camera(phi=1, zoom=0.5)

# manim -p 3dtest.py
# manim -p -ql 3dtest.py
