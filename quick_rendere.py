from PySide2 import QtWidgets, QtCore
import hou


class RenderWindow(QtWidgets.QWidget):
    def __init__(self):
        super(RenderWindow, self).__init__()
        self.setWindowTitle("Camera Renderer")
        self.setGeometry(100, 100, 300, 100)
        layout = QtWidgets.QVBoxLayout()

        self.camera_combo = QtWidgets.QComboBox()
        self.populate_cameras()
        layout.addWidget(self.camera_combo)

        self.render_button = QtWidgets.QPushButton("Render")
        self.render_button.clicked.connect(self.render_camera)
        layout.addWidget(self.render_button)

        self.setLayout(layout)

    def populate_cameras(self):
        """Populates the camera dropdown with all cameras in the scene."""
        cameras = [node.path() for node in hou.node('/obj').children() if node.type().name() == 'cam']
        self.camera_combo.addItems(cameras)

    def render_camera(self):
        selected_camera = self.camera_combo.currentText()
        start_frame = hou.playbar.frameRange()[0]
        end_frame = hou.playbar.frameRange()[1]

        render_settings = {
            'soho_outputmode': hou.node('/out/mantra1').parm('soho_outputmode').eval(),
            'vm_picture': hou.node('/out/mantra1').parm('vm_picture').eval(),
            'camera': selected_camera
        }

        hou.node('/out/mantra1').parm('camera').set(selected_camera)

        camera_name = selected_camera.split('/')[-1]
        output_file = render_settings['vm_picture'].replace('$F', f'{start_frame}-{end_frame}').replace('.exr',
                                                                                                        f'_{camera_name}.exr')
        hou.node('/out/mantra1').parm('vm_picture').set(output_file)

        rop_node = hou.node('/out/mantra1')
        rop_node.render(frame_range=(start_frame, end_frame))


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    window = RenderWindow()
    window.show()
    app.exec_()
