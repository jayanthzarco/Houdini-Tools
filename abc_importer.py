from PySide2 import QtWidgets, QtCore
import hou


class AlembicImporter(QtWidgets.QWidget):
    def __init__(self):
        super(AlembicImporter, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Alembic Importer')

        # Layout
        self.layout = QtWidgets.QVBoxLayout()

        # File Selection
        self.file_label = QtWidgets.QLabel("Select Alembic File:")
        self.layout.addWidget(self.file_label)

        self.file_line_edit = QtWidgets.QLineEdit()
        self.layout.addWidget(self.file_line_edit)

        self.file_browse_button = QtWidgets.QPushButton("Browse")
        self.file_browse_button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.file_browse_button)

        # Import Button
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.clicked.connect(self.import_alembic)
        self.layout.addWidget(self.import_button)

        self.setLayout(self.layout)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Alembic File", "", "Alembic Files (*.abc)")
        if file_path:
            self.file_line_edit.setText(file_path)

    def import_alembic(self):
        file_path = self.file_line_edit.text()
        if file_path:
            self.import_abc_to_houdini(file_path)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select an Alembic file.")

    def import_abc_to_houdini(self, file_path):
        try:
            obj = hou.node("/obj")
            alembic_node = obj.createNode("alembic")
            alembic_node.parm("fileName").set(file_path)
            alembic_node.moveToGoodPosition()
            alembic_node.setDisplayFlag(True)
            alembic_node.setRenderFlag(True)
            QtWidgets.QMessageBox.information(self, "Success", f"Alembic file '{file_path}' imported successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    importer = AlembicImporter()
    importer.show()
