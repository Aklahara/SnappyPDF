# from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6.QtCore import *     ###
from PySide6.QtGui import *        #### This would be converted to import only the necessary classes when building with Nuitka
from PySide6.QtWidgets import *  ###

from PDFViewer import AbstractImageViewer
from utils import getGitCommit

from PIL.ImageQt import ImageQt
import pypdfium2 as pdfium


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf: pdfium.PdfDocument|None = None

        self.loadAction = QAction("Load PDF", self)
        self.loadAction.setShortcut("Ctrl+O")
        self.loadAction.triggered.connect(self.loadPDF)
        menu_bar = self.menuBar().addMenu("File")
        menu_bar.addAction(self.loadAction)

        self.viewer = AbstractImageViewer(self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.viewer)

        w = QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(self.viewer)

        self.setWindowTitle(f"SnappyPDF build {getGitCommit()}")
        self.showMaximized()


    def loadPDF(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")

        pdf_document = pdfium.PdfDocument(path)
        self.pdf = pdf_document
        self.viewer.setImage(ImageQt(self.pdf[0].render(1).to_pil()))




if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()