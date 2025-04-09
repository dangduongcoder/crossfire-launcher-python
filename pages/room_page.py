from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class RoomPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Phòng chơi")
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label)
        self.setLayout(layout) 