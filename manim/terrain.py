from multiprocessing.connection import wait
from manim import *

class ThreeDTest(ThreeDScene):
    def construct(self):
        # Temp Setup
        '''self.set_camera_orientation(phi=75 * DEGREES, theta=50 * DEGREES, zoom=0.1, frame_center=np.array([0, 0, 12.8]))
        test = Cube(side_length=1.6)
        test.move_to(np.array([0, 0, 12.8]))
        test.stretch(25.6, 2)

        self.play(Create(test))

        self.wait()
        self.move_camera(frame_center=np.array([-24, 24, 12.8]))
        self.wait()
        return'''

        # Initialize 3D axis and camera
        self.set_camera_orientation(phi=0, theta=0, zoom=25)

        face_data = [
            ([ 0, 0, 1],   0,  OUT),
            ([ 0, 0,-1],   0,  OUT),
            ([ 1, 0, 0],  90,   UP),
            ([-1, 0, 0],  90,   UP),
            ([ 0,-1, 0],  90, LEFT),
            ([ 0, 1, 0],  90, LEFT)
        ]

        # Make 2D Squares
        cube_faces = []

        for i in range(6):
            cube_faces.append(Square(side_length=0.1, color=BLUE, fill_opacity=0))
            cube_faces[i].move_to(np.multiply(0.05, np.array(face_data[i][0])))
            cube_faces[i].rotate(face_data[i][1] * DEGREES, face_data[i][2])
            cube_faces[i].stroke_color = WHITE
            cube_faces[i].stroke_width = 2

        self.play(Create(cube_faces[1]))

        # Rotate transform
        self.move_camera(phi=75 * DEGREES, theta=50 * DEGREES, added_anims=[Create(cube_faces[2]), Create(cube_faces[3]), Create(cube_faces[4]), Create(cube_faces[5])])

        # Fill up the cube (animate opacity)
        block_obj = Cube(side_length=0.1)
        op2 = ValueTracker(2)
        for face in cube_faces:
            face.add_updater(lambda f: f.set_stroke(width=op2.get_value()))
        
        cubex1 = Text('1个方块\n6个面\n12个三角面')
        self.add_fixed_in_frame_mobjects(cubex1)
        self.play(Write(cubex1))
        self.wait()
        self.play(FadeOut(cubex1))
        
        self.move_camera(zoom=2.5, frame_center=np.array([0.8, 0.8, 0]), added_anims=[FadeIn(block_obj), op2.animate.set_value(0)])
        #self.play(FadeIn(block_obj), op2.animate.set_value(0))

        cubex256 = Text('一层方块\n16 * 16 = 256个方块\n256 * 12 = 3072个三角面')

        layer_obj = VMobject()
        for i in range(16):
            for j in range(16):
                if i != 0 or j != 0:
                    bloc = Cube(side_length=0.1)
                    bloc.move_to(np.array([i * 0.1, j * 0.1, 0]))
                    layer_obj.submobjects.append(bloc)

        self.add_fixed_in_frame_mobjects(cubex256)
        cubex256.shift(DOWN)
        self.play(Write(cubex256), Create(layer_obj, lag_ratio=1))
        self.wait()

        self.wait()
        self.play(FadeOut(cubex256))

        self.move_camera(zoom=0.25)

        chunk_obj = VMobject()
        for y in range(1, 256):
            layr = Cube(side_length=1.6)
            layr.stretch(0.1, 2)
            layr.move_to(np.array([0.75, 0.75, y * 0.1]))
            chunk_obj.submobjects.append(layr)

        cubex65536 = Text('一个区块\n16 * 16 * 256 = 65536个方块\n65536 * 12 = 786432个三角面')
        self.add_fixed_in_frame_mobjects(cubex65536)
        cubex65536.shift(UP)
        cubex65536.shift(RIGHT * 2)

        #self.play(Write(cubex65536))

        self.move_camera(frame_center=np.array([-12, 12, 12.8]), added_anims=[Create(chunk_obj, lag_ratio=2), Write(cubex65536)])
        self.wait()



# manim -p -ql terrain.py
