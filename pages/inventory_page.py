from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Kho Đồ")
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label)
        self.setLayout(layout) 