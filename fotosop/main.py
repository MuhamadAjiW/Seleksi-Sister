import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sotosop import *

class Camera(QObject):
    finished = pyqtSignal()
    prep_finished = pyqtSignal()
    frame_available = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        print(self.running)
        self.running = True

        print("Loading camera...")
        camera = cv2.VideoCapture(0)
        print("Camera is ready")
        self.prep_finished.emit()

        while self.running:
            ret, frame = camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                self.frame_available.emit(frame)
        self.finished.emit()

    def stop(self):
        self.running = False

class ImageViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Viewer')
        self.setFixedSize(1280, 720)

        self.imglabelmaxwidth = 1000
        self.imglabelmaxheight = 720

        self.image_label = QLabel(self)
        self.image_label.resize(self.imglabelmaxwidth, self.imglabelmaxheight)
        self.image_path = ""

        separator = QFrame(self)
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setGeometry(1000, 0, 1, 720)
        separator.setStyleSheet("background-color: black;")

        self.pick_button = QPushButton('Pick Image', self)
        self.pick_button.move(1060, 10)
        self.pick_button.resize(160, 30)
        self.pick_button.clicked.connect(self.pick_image)

        self.gs_button = QPushButton('Grayscale: OFF', self)
        self.gs_button.move(1060, 50)
        self.gs_button.resize(160, 30)
        self.gs_button.toggled.connect(self.on_grayscale) 
        self.gsMode = False

        self.edge_button = QPushButton('Edge View: OFF', self)
        self.edge_button.move(1060, 90)
        self.edge_button.resize(160, 30)
        self.edge_button.toggled.connect(self.on_edge) 
        self.edgeMode = False

        self.contrast_value_label = QLabel('Contrast: 1', self)
        self.contrast_value_label.setGeometry(1060, 120, 160, 30)

        self.contrast_slider = QSlider(Qt.Horizontal, self)
        self.contrast_slider.setGeometry(1060, 150, 160, 30)
        self.contrast_slider.valueChanged.connect(self.on_contrast_change)
        self.contrastVal = 1

        self.saturation_value_label = QLabel('Saturation: 1', self)
        self.saturation_value_label.setGeometry(1060, 180, 160, 30)

        self.saturation_slider = QSlider(Qt.Horizontal, self)
        self.saturation_slider.setGeometry(1060, 210, 160, 30)
        self.saturation_slider.valueChanged.connect(self.on_saturation_change)
        self.saturationVal = 1

        self.blur_value_label = QLabel('blur: 0', self)
        self.blur_value_label.setGeometry(1060, 240, 160, 30)

        self.blur_slider = QSlider(Qt.Horizontal, self)
        self.blur_slider.setGeometry(1060, 270, 160, 30)
        self.blur_slider.valueChanged.connect(self.on_blur_change)
        self.blurVal = 0

        self.camera = QPushButton('Camera: OFF', self)
        self.camera.move(1060, 600)
        self.camera.resize(160, 30)
        self.camera.setCheckable(True)
        self.camera.toggled.connect(self.on_camera) 
        self.cameraMode = False

        self.worker_thread = QThread()
        
        self.camera_thread = Camera()
        self.camera_thread.moveToThread(self.worker_thread)
        self.camera_thread.frame_available.connect(self.show_frame)
        self.camera_thread.prep_finished.connect(self.ready_camera)
        self.camera_thread.finished.connect(self.off_camera)
        self.worker_thread.started.connect(self.camera_thread.run)
        
        self.gs_button.setDisabled(True)
        self.edge_button.setDisabled(True)
        self.contrast_slider.setDisabled(True)
        self.saturation_slider.setDisabled(True)
        self.blur_slider.setDisabled(True)

    def on_camera(self, checked):
        if checked:
            self.camera.setText('Camera: ON')
            self.cameraMode = True

            self.pick_button.setDisabled(True)
            self.gs_button.setDisabled(True)
            self.edge_button.setDisabled(True)
            self.contrast_slider.setDisabled(True)
            self.saturation_slider.setDisabled(True)
            self.blur_slider.setDisabled(True)

            self.worker_thread.start()

        else:    
            self.gs_button.setDisabled(True)
            self.edge_button.setDisabled(True)
            self.contrast_slider.setDisabled(True)
            self.saturation_slider.setDisabled(True)
            self.blur_slider.setDisabled(True)
            
            self.gs_button.setText('Grayscale: OFF')
            self.gs_button.setCheckable(True)
            self.gs_button.setChecked(False)
            self.gsMode = False
            self.edge_button.setText('Edge View: OFF')
            self.edge_button.setCheckable(True)
            self.edge_button.setChecked(False)
            self.edgeMode = False
            self.contrast_slider.setValue(0)
            self.saturation_slider.setValue(0)
            self.blur_slider.setValue(0)
            self.contrast_slider.setDisabled(True)
            self.saturation_slider.setDisabled(True)
            self.blur_slider.setDisabled(True)
            self.image_path = ""
            self.image_label.clear()

            self.camera.setText('Camera: OFF')
            self.cameraMode = False
            self.camera_thread.stop()
    
    def ready_camera(self):
        self.pick_button.setDisabled(False)
        self.gs_button.setDisabled(False)
        self.edge_button.setDisabled(False)
        self.contrast_slider.setDisabled(False)
        self.saturation_slider.setDisabled(False)
        self.blur_slider.setDisabled(False)

        self.gs_button.setText('Grayscale: OFF')
        self.gs_button.setCheckable(True)
        self.gs_button.setChecked(False)
        self.gsMode = False
        
        self.edge_button.setText('Edge View: OFF')
        self.edge_button.setCheckable(True)
        self.edge_button.setChecked(False)
        self.edgeMode = False
        
        self.contrast_slider.setValue(0)
        self.saturation_slider.setValue(0)
        self.blur_slider.setValue(0)

        self.image_path = ""
        self.image_label.clear()

    def off_camera(self):
        self.worker_thread.quit()
        self.worker_thread.wait()
        print("Camera is stopped")

    def show_frame(self, frame):
        processed_image = frame
        if self.gsMode:
            processed_image = process_image(processed_image.astype(np.float32), "grayscale")
        if self.edgeMode:
            processed_image = process_image(processed_image.astype(np.float32), "edge")
        if self.contrastVal != 1:
            processed_image = process_image(processed_image.astype(np.float32), "contrast", self.contrastVal)
        if self.saturationVal != 1:
            processed_image = process_image(processed_image.astype(np.float32), "saturation", self.saturationVal)
        if self.blurVal != 0:
            processed_image = process_image(processed_image.astype(np.float32), "blur", self.blurVal)
        
        processed_image = processed_image.astype(np.uint8)

        height, width, channel = processed_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)

        aspect_ratio = pixmap.width() / pixmap.height()

        if self.imglabelmaxwidth / self.imglabelmaxheight > aspect_ratio:
            self.pic_scale = int(self.imglabelmaxheight * aspect_ratio)
            self.image_label.setPixmap(pixmap.scaledToWidth(self.pic_scale))
        else:
            self.pic_scale = int(self.imglabelmaxwidth / aspect_ratio)
            self.image_label.setPixmap(pixmap.scaledToHeight(self.pic_scale))

        self.image_label.setPixmap(pixmap)

    def pick_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Pick an image", "", "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.load_image(file_name)

    def on_grayscale(self, checked):
        if checked:
            self.gs_button.setText('Grayscale: ON')
            self.gsMode = True
            if self.image_path:
                self.update_image()
        else:
            self.gs_button.setText('Grayscale: OFF')
            self.gsMode = False
            if self.image_path:
                self.update_image()

    def on_edge(self, checked):
        if checked:
            self.edge_button.setText('Edge View: ON')
            self.edgeMode = True
            if self.image_path:
                self.update_image()
        else:
            self.edge_button.setText('Edge View: OFF')
            self.edgeMode = False
            if self.image_path:
                self.update_image()

    def on_contrast_change(self):
        slider_value = self.contrast_slider.value()
        self.contrast_value_label.setText(f'Contrast: {slider_value + 1}')
        self.contrastVal = slider_value + 1

        if self.image_path:
            self.update_image()

    def on_saturation_change(self):
        slider_value = self.saturation_slider.value()
        self.saturation_value_label.setText(f'Saturation: {slider_value + 1}')
        self.saturationVal = slider_value + 1

        if self.image_path:
            self.update_image()

    def on_blur_change(self):
        slider_value = self.blur_slider.value()
        self.blur_value_label.setText(f'Blur: {slider_value}')
        self.blurVal = slider_value

        if self.image_path:
            self.update_image()
            

    def load_image(self, image_path):
        if self.cameraMode:
            self.camera.setText('Camera: OFF')
            self.cameraMode = False
            self.camera_thread.stop()
        
        if self.image_path != None:
            self.image_path = image_path
            self.cv_image = cv2.imread(self.image_path)

            self.gs_button.setCheckable(True)
            self.edge_button.setCheckable(True)
            self.contrast_slider.setValue(0)
            self.saturation_slider.setValue(0)
            self.blur_slider.setValue(0)

            self.gs_button.setDisabled(False)
            self.edge_button.setDisabled(False)
            self.contrast_slider.setDisabled(False)
            self.saturation_slider.setDisabled(False)
            self.blur_slider.setDisabled(False)


            rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)

            self.height, self.width, self.channel = rgb_image.shape
            self.bytes_per_line = 3 * self.width
            q_image = QImage(rgb_image.data, self.width, self.height, self.bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_image)

            aspect_ratio = pixmap.width() / pixmap.height()

            if self.imglabelmaxwidth / self.imglabelmaxheight > aspect_ratio:
                self.pic_scale = int(self.imglabelmaxheight * aspect_ratio)
                self.image_label.setPixmap(pixmap.scaledToWidth(self.pic_scale))
                self.pic_scale_method = "width"
            else:
                self.pic_scale = int(self.imglabelmaxwidth / aspect_ratio)
                self.image_label.setPixmap(pixmap.scaledToHeight(self.pic_scale))
                self.pic_scale_method = "height"
        
    def update_image(self):
        processed_image = self.cv_image
        if self.gsMode:
            processed_image = process_image(processed_image.astype(np.float32), "grayscale")
        if self.edgeMode:
            processed_image = process_image(processed_image.astype(np.float32), "edge")
        if self.contrastVal != 1:
            processed_image = process_image(processed_image.astype(np.float32), "contrast", self.contrastVal)
        if self.saturationVal != 1:
            processed_image = process_image(processed_image.astype(np.float32), "saturation", self.saturationVal)
        if self.blurVal != 0:
            processed_image = process_image(processed_image.astype(np.float32), "blur", self.blurVal)
        
        processed_image = processed_image.astype(np.uint8)
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        q_image = QImage(rgb_image.data, self.width, self.height, self.bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)

        if self.pic_scale_method == "width":
            self.image_label.setPixmap(pixmap.scaledToWidth(self.pic_scale))
        else:
            self.image_label.setPixmap(pixmap.scaledToHeight(self.pic_scale))

        loop = QEventLoop()
        QTimer.singleShot(0, loop.quit)
        loop.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())