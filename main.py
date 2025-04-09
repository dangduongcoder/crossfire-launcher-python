import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QPixmap

from pages.lobby_page import LobbyPage
from pages.inventory_page import InventoryPage
from pages.room_page import RoomPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        self.setFixedSize(1600, 900)
        
        # Đặt cửa sổ ở giữa màn hình
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Tạo label để hiển thị ảnh nền
        self.background = QLabel(central_widget)
        self.background.setFixedSize(1600, 900)
        pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/LobbyBG/SuperRush.PNG")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        
        # Khởi tạo các thành phần
        self.init_top_bar()
        self.init_bottom_bar()
        self.init_pages()
        
        # Đặt stacked widget chiếm toàn bộ cửa sổ
        self.stacked_widget.setParent(central_widget)
        self.stacked_widget.setGeometry(0, 0, 1600, 900)
        
        # Đặt top bar và bottom bar lên trên
        self.top_bar.setParent(central_widget)
        self.bottom_bar.setParent(central_widget)
        
        # Đặt vị trí cho top bar và bottom bar
        self.top_bar.move(0, 0)
        self.bottom_bar.move(0, 871)  # 900 - 29 (chiều cao của bottom bar)
        
        # Đảm bảo top bar và bottom bar luôn hiển thị trên cùng
        self.top_bar.raise_()
        self.bottom_bar.raise_()
        
        # Đặt trang mặc định
        self.change_page(0)
        
        # Load thông tin người chơi
        self.load_player_info()
    
    def load_player_info(self):
        config_path = "REZ/CONFIG/User.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.player_name = config['player']['name']
                    self.player_level = config['player']['level']
                    self.player_exp = config['player']['exp']
                    self.player_gp = config['player']['gp']
                    self.player_zp = config['player']['zp']
            else:
                # Nếu file không tồn tại, tạo file mới với giá trị mặc định
                self.player_name = "Player"
                self.player_level = 1
                self.player_exp = 0
                self.player_gp = 0
                self.player_zp = 0
                self.save_player_info()
        except Exception as e:
            print(f"Lỗi khi đọc file config: {e}")
            # Sử dụng giá trị mặc định nếu có lỗi
            self.player_name = "Player"
            self.player_level = 1
            self.player_exp = 0
            self.player_gp = 0
            self.player_zp = 0
        
        # Cập nhật tên người chơi trên bottom bar
        self.player_name_label.setText(self.player_name)
    
    def save_player_info(self):
        config_path = "REZ/CONFIG/User.json"
        try:
            config = {
                "player": {
                    "name": self.player_name,
                    "level": self.player_level,
                    "exp": self.player_exp,
                    "gp": self.player_gp,
                    "zp": self.player_zp
                }
            }
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu file config: {e}")
    
    def init_top_bar(self):
        # Top Bar
        self.top_bar = QWidget()
        self.top_bar.setFixedSize(1600, 62)
        
        # Tạo label để hiển thị ảnh nền
        top_bar_bg = QLabel(self.top_bar)
        top_bar_bg.setFixedSize(1600, 62)
        pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/TopMenuBG.PNG")
        top_bar_bg.setPixmap(pixmap)
        top_bar_bg.setScaledContents(True)
        
        # Layout cho top bar
        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(10, 0, 10, 0)
        
        # Logo với animation
        self.logo = QLabel(self.top_bar)
        self.logo.setFixedSize(210, 75)
        self.logo.setScaledContents(True)
        self.logo.move(16, -10)

        # Tạo danh sách các frame cho animation
        self.logo_frames = []
        for i in range(1, 52):  # 51 frames từ 001 đến 051
            frame = QPixmap(f"REZ/UI/UI_FX/BI_FX{i:03d}.PNG")
            self.logo_frames.append(frame)

        # Timer để update animation
        self.logo_timer = QTimer()
        self.logo_timer.timeout.connect(self.update_logo_frame)
        self.current_frame = 0
        
        # Thiết lập frame đầu tiên và bắt đầu animation
        self.logo.setPixmap(self.logo_frames[0])
        self.logo_timer.start(50)  # Update mỗi 50ms (20fps)

        # Nút Play
        self.play_btn = QPushButton(self.top_bar)
        self.play_btn.setFixedSize(190, 44)
        self.play_btn.move(215, 2)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.play_btn.down_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Play_Down.PNG")
        self.play_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Play_Focus.PNG")
        self.play_btn.up_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Play_Up.PNG")
        
        # Thiết lập kích thước icon
        self.play_btn.setIconSize(QSize(190, 44))
        
        # Thiết lập sự kiện hover
        self.play_btn.enterEvent = lambda event: self.on_play_hover(True)
        self.play_btn.leaveEvent = lambda event: self.on_play_hover(False)
        
        # Kết nối sự kiện click
        self.play_btn.clicked.connect(lambda: self.change_page(0))
        
        # Thiết lập trạng thái ban đầu
        self.update_play_button_state(True)  # Mặc định là trang Sảnh

        # Nút Kho đồ
        self.inventory_btn_top = QPushButton(self.top_bar)
        self.inventory_btn_top.setFixedSize(190, 44)
        self.inventory_btn_top.move(367, 2)
        self.inventory_btn_top.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.inventory_btn_top.down_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Inven_Down.PNG")
        self.inventory_btn_top.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Inven_Focus.PNG")
        self.inventory_btn_top.up_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Inven_Up.PNG")
        
        # Thiết lập kích thước icon
        self.inventory_btn_top.setIconSize(QSize(190, 44))
        
        # Thiết lập sự kiện hover
        self.inventory_btn_top.enterEvent = lambda event: self.on_inventory_hover(True)
        self.inventory_btn_top.leaveEvent = lambda event: self.on_inventory_hover(False)
        
        # Kết nối sự kiện click
        self.inventory_btn_top.clicked.connect(lambda: self.change_page(1))
        
        # Thiết lập trạng thái ban đầu
        self.update_inventory_button_state(False)

        # Nút Close
        self.close_btn = QPushButton(self.top_bar)
        self.close_btn.setFixedSize(100, 50)
        self.close_btn.move(1500, 0)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.close_btn.down_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Exit_Down.PNG")
        self.close_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Exit_Focus.PNG")
        self.close_btn.up_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/TopMenu/Exit_Up.PNG")
        
        # Thiết lập kích thước icon
        self.close_btn.setIconSize(QSize(100, 50))
        
        # Thiết lập sự kiện hover
        self.close_btn.enterEvent = lambda event: self.on_close_hover(True)
        self.close_btn.leaveEvent = lambda event: self.on_close_hover(False)
        
        # Kết nối sự kiện click
        self.close_btn.clicked.connect(self.close)
        
        # Thiết lập trạng thái ban đầu
        self.update_close_button_state(False)
    
    def init_bottom_bar(self):
        # Bottom Bar
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedSize(1600, 29)
        
        # Tạo label để hiển thị ảnh nền
        bottom_bar_bg = QLabel(self.bottom_bar)
        bottom_bar_bg.setFixedSize(1600, 29)
        pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Bottom_BG.PNG")
        bottom_bar_bg.setPixmap(pixmap)
        bottom_bar_bg.setScaledContents(True)
        
        # Layout cho bottom bar
        bottom_layout = QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(20, 0, 20, 0)
        
        # Label hiển thị tên nhân vật
        self.player_name_label = QLabel("Tên nhân vật")
        self.player_name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        # Thêm label vào layout
        bottom_layout.addWidget(self.player_name_label)
        bottom_layout.addStretch()  # Thêm khoảng trống để đẩy label sang trái
    
    def init_pages(self):
        # Stacked Widget cho các trang
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")
        
        # Thêm các trang vào stacked widget
        self.lobby_page = LobbyPage()
        self.inventory_page = InventoryPage()
        self.room_page = RoomPage()
        
        self.stacked_widget.addWidget(self.lobby_page)
        self.stacked_widget.addWidget(self.inventory_page)
        self.stacked_widget.addWidget(self.room_page)
    
    def update_logo_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.logo_frames)
        self.logo.setPixmap(self.logo_frames[self.current_frame])
    
    def create_nav_button(self, text, icon_name):
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
            }
        """)
        btn.setCheckable(True)
        return btn
    
    def on_inventory_hover(self, is_hover):
        if self.stacked_widget.currentIndex() != 1:  # Nếu không phải trang Kho đồ
            if is_hover:
                self.inventory_btn_top.setIcon(QIcon(self.inventory_btn_top.focus_pixmap))
            else:
                self.inventory_btn_top.setIcon(QIcon(self.inventory_btn_top.up_pixmap))
    
    def update_inventory_button_state(self, is_active):
        if is_active:
            self.inventory_btn_top.setIcon(QIcon(self.inventory_btn_top.down_pixmap))
        else:
            self.inventory_btn_top.setIcon(QIcon(self.inventory_btn_top.up_pixmap))
    
    def on_play_hover(self, is_hover):
        if self.stacked_widget.currentIndex() != 0:  # Nếu không phải trang Sảnh
            if is_hover:
                self.play_btn.setIcon(QIcon(self.play_btn.focus_pixmap))
            else:
                self.play_btn.setIcon(QIcon(self.play_btn.up_pixmap))
    
    def update_play_button_state(self, is_active):
        if is_active:
            self.play_btn.setIcon(QIcon(self.play_btn.down_pixmap))
        else:
            self.play_btn.setIcon(QIcon(self.play_btn.up_pixmap))
    
    def on_close_hover(self, is_hover):
        if is_hover:
            self.close_btn.setIcon(QIcon(self.close_btn.focus_pixmap))
        else:
            self.close_btn.setIcon(QIcon(self.close_btn.up_pixmap))
    
    def update_close_button_state(self, is_active):
        if is_active:
            self.close_btn.setIcon(QIcon(self.close_btn.down_pixmap))
        else:
            self.close_btn.setIcon(QIcon(self.close_btn.up_pixmap))
    
    def change_page(self, index):
        # Cập nhật trạng thái các nút
        self.update_play_button_state(index == 0)
        self.update_inventory_button_state(index == 1)
        
        # Chuyển trang
        self.stacked_widget.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 