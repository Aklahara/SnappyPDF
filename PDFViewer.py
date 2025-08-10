from PySide6.QtCore import *     ###
from PySide6.QtGui import *        #### This would be converted to import only the necessary classes when building with Nuitka
from PySide6.QtWidgets import *  ###


class AbstractImageViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()

    def paintEvent(self, event: QPaintEvent) -> None:
        if not self.image.isNull():
            painter = QPainter(self)
            painter.drawImage(self.rect(), self.image)
        else:
            painter = QPainter(self)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Nothing is loaded")

    def updateVisible(self) -> None:
        self.update(self.visibleRegion().boundingRect())

    def setImage(self, image: QImage) -> None:
        self.image = image
        self.resize(self.image.size())
        self.updateVisible()

class PDFViewerScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewer = AbstractImageViewer(self)
        self.setWidget(self.viewer)
        self.setWidgetResizable(False)
        self.pdf = None


if __name__ == "__main__":
    from PIL.ImageQt import ImageQt
    import pypdfium2 as pdfium

    class TestWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Test Widget")
            self.viewer = PDFViewerScrollArea(self)
            self.loadPDF("CoP_SUC2013e.pdf")
            self.viewer.setWindowTitle("PDF Viewer")

            layout = QVBoxLayout(self)
            layout.addWidget(self.viewer)
            self.setLayout(layout)

            self.showMaximized()

        def loadPDF(self, pdf_path, dpi=72):
            pdf_document = pdfium.PdfDocument(pdf_path)
            page = pdf_document[0]  # Load the first page
            bitmap = page.render(scale=dpi/72)
            pil_image = bitmap.to_pil()
            self.viewer.viewer.setImage(ImageQt(pil_image))
            self.viewer.viewer.updateVisible()

    app = QApplication([])
    window = TestWidget()
    app.exec()