import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt UI on Raspberry Pi 4")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Press the button")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_click)  # Connect button to function
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def on_button_click(self):
        self.label.setText("Button Clicked!")  # Update label text

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())