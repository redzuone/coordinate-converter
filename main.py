from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget
from geopy.point import Point



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coordinate Converter")
        self.resize(400, 400)

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setAcceptRichText(False)
        self.input_text_edit.setPlaceholderText("Input coordinates\nExample:\n2.7433333, 101.6980556\n02°44′36″N 101°41′53″E")
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setAcceptRichText(False)
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setPlaceholderText("Output coordinates")
        self.copy_btn = QPushButton("Copy")

        layout = QVBoxLayout()
        layout.addWidget(self.input_text_edit)
        layout.addWidget(self.output_text_edit)
        layout.addWidget(self.copy_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.input_text_edit.textChanged.connect(self.convert_coordinates)

    def convert_coordinates(self):
        if self.input_text_edit.toPlainText() == "": self.output_text_edit.clear(); return
        coords = self.input_text_edit.toPlainText().split("\n")
        self.output_text_edit.clear()
        for coord in coords:
            try:
                if ',' in coord:
                    lat, lon = coord.split(',', 1) # Split the input at the comma
                    lat_dms, lon_dms = self.decimal_degrees_to_dms(float(lat.strip()), float(lon.strip()))
                    self.output_text_edit.append(f"{lat_dms} {lon_dms}")
                elif '°' in coord:
                    # Input is in DMS, convert to decimal degrees
                    point = Point(coord)
                    self.output_text_edit.append(f"{round(point.latitude, 7)}, {round(point.longitude, 7)}")
                else:
                    self.output_text_edit.append(f"{repr(coord)} - invalid coordinate")
            except Exception as e:
                self.output_text_edit.append(f"{coord} - invalid coordinate: {e}")

    def decimal_degrees_to_dms(self, lat, lon):
        def convert_to_dms(degree, is_latitude):
            is_positive = degree >= 0
            degree = abs(degree)
            minutes, seconds = divmod(degree * 3600, 60)
            degrees, minutes = divmod(minutes, 60)
            cardinal = ('N', 'S') if is_latitude else ('E', 'W')
            return f"{int(degrees)}°{int(minutes)}′{seconds:.2f}″{cardinal[0 if is_positive else 1]}"

        lat_dms = convert_to_dms(lat, True)
        lon_dms = convert_to_dms(lon, False)
        return lat_dms, lon_dms



app = QApplication([])
window = MainWindow()
window.show()
app.exec()