# script helps to render a camera with custom path
# script created o 16-07-2024

from PySide2 import QtWidgets, QtCore
import hou
import os


class RenderWindow(QtWidgets.QWidget):
    def __init__(self):
        super(RenderWindow, self).__init__()

        # Set up the window
        self.setWindowTitle("Camera Renderer")
        self.setGeometry(100, 100, 400, 150)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Camera dropdown
        self.camera_combo = QtWidgets.QComboBox()
        self.populate_cameras()
        layout.addWidget(QtWidgets.QLabel("Select Camera:"))
        layout.addWidget(self.camera_combo)

        # Output path
        self.output_path_edit = QtWidgets.QLineEdit()
        self.output_path_edit.setPlaceholderText("Select output path")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output_path)

        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.output_path_edit)
        path_layout.addWidget(self.browse_button)

        layout.addWidget(QtWidgets.QLabel("Output Path:"))
        layout.addLayout(path_layout)

        # Render button
        self.render_button = QtWidgets.QPushButton("Render")
        self.render_button.clicked.connect(self.render_camera)
        layout.addWidget(self.render_button)

        self.setLayout(layout)

    def populate_cameras(self):
        """Populates the camera dropdown with all cameras in the scene."""
        cameras = [node.path() for node in hou.node('/obj').children() if node.type().name() == 'cam']
        self.camera_combo.addItems(cameras)

    def browse_output_path(self):
        """Opens a file dialog to select the output path."""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def render_camera(self):
        """Renders the selected camera for the timeline range."""
        selected_camera = self.camera_combo.currentText()
        start_frame = hou.playbar.frameRange()[0]
        end_frame = hou.playbar.frameRange()[1]
        output_directory = self.output_path_edit.text()

        if not output_directory:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select an output directory.")
            return

        # Set the render settings
        render_settings = {
            'soho_outputmode': hou.node('/out/mantra1').parm('soho_outputmode').eval(),
            'vm_picture': os.path.join(output_directory, "render_$F.exr"),
            'camera': selected_camera
        }

        # Set the camera for rendering
        hou.node('/out/mantra1').parm('camera').set(selected_camera)

        # Update the output file path to include the camera name
        camera_name = selected_camera.split('/')[-1]
        output_file = render_settings['vm_picture'].replace('$F', f'{start_frame}-{end_frame}').replace('.exr',
                                                                                                        f'_{camera_name}.exr')
        hou.node('/out/mantra1').parm('vm_picture').set(output_file)

        # Render the camera for the timeline range
        rop_node = hou.node('/out/mantra1')
        rop_node.render(frame_range=(start_frame, end_frame))

if __name__ == '__main__':
    # Create and display the window
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    window = RenderWindow()
    window.show()
    app.exec_()

"""
created by Jayanth
"""