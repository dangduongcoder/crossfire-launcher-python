from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize
import json
import os

class LobbyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.config_path = "REZ/CONFIG/User.json"
        self.load_config()  # Load config khi khởi tạo
        self.init_ui()
        
    def load_config(self):
        """Đọc thông tin từ file config"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.character_name = config['player']['character']
                self.current_character = config['player']['team']
                self.config = config  # Lưu toàn bộ config để sử dụng sau này
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Nếu file không tồn tại hoặc có lỗi, tạo config mặc định
            self.config = {
                'player': {
                    'character': 'FOXHAWL',
                    'team': 'BL',
                    'money': 0,
                    'level': 1,
                    'experience': 0
                }
            }
            self.character_name = self.config['player']['character']
            self.current_character = self.config['player']['team']
            self.save_config()
            
    def save_config(self):
        """Lưu thông tin vào file config, chỉ cập nhật các trường cần thiết"""
        # Cập nhật các trường cần thay đổi
        self.config['player']['character'] = self.character_name
        self.config['player']['team'] = self.current_character
        
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Lưu toàn bộ config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
    def init_ui(self):
        """Khởi tạo giao diện của trang lobby"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.init_character_display()
        self.init_team_buttons()
        self.init_game_buttons()
        
    def init_character_display(self):
        """Khởi tạo phần hiển thị nhân vật"""
        self.character_label = QLabel(self)
        self.character_label.setFixedSize(1300, 852)
        self.character_label.move(150, 50)
        self.character_label.setStyleSheet("background-color: transparent;")
        self.update_character_image()
        
    def init_team_buttons(self):
        """Khởi tạo các nút chọn team"""
        # Nút chọn team BL
        self.bl_btn = self.create_team_button(
            "BL", 
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl.PNG",
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl_focus.PNG",
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl_select.PNG",
            930, 90
        )
        self.bl_btn.clicked.connect(self.switch_to_bl)
        
        # Nút chọn team GR
        self.gr_btn = self.create_team_button(
            "GR",
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr.PNG",
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr_focus.PNG",
            "REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr_select.PNG",
            930, 145
        )
        self.gr_btn.clicked.connect(self.switch_to_gr)
        
        # Thiết lập trạng thái ban đầu
        self.update_team_buttons_state()
        
    def init_game_buttons(self):
        """Khởi tạo các nút điều khiển game"""
        # Nút Start Game
        self.start_btn = self.create_game_button(
            "REZ/UI/UI_LobbyRenewal/GameStart_Down.PNG",
            "REZ/UI/UI_LobbyRenewal/GameStart_Focus.PNG",
            "REZ/UI/UI_LobbyRenewal/GameStart_Up.PNG",
            173, 85, 1400, 715
        )
        self.start_btn.clicked.connect(self.start_game)
        
        # Nút chọn chế độ chơi
        self.match_setting_btn = self.create_game_button(
            "REZ/UI/UI_LobbyRenewal/MatchSetting_Up.PNG",
            "REZ/UI/UI_LobbyRenewal/MatchSetting_Focus.PNG",
            "REZ/UI/UI_LobbyRenewal/MatchSetting_Up.PNG",
            280, 50, 1120, 715
        )
        
        # Label hiển thị chế độ chơi
        self.match_type_label = self.create_match_type_label()
        
    def create_team_button(self, team, normal_img, focus_img, select_img, x, y):
        """Tạo nút chọn team với các thuộc tính cho trước"""
        btn = QPushButton(self)
        btn.setFixedSize(155, 54)
        btn.move(x, y)
        btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        
        # Lưu trữ các trạng thái ảnh
        btn.normal_pixmap = QPixmap(normal_img)
        btn.focus_pixmap = QPixmap(focus_img)
        btn.select_pixmap = QPixmap(select_img)
        
        # Thiết lập icon mặc định
        btn.setIcon(QIcon(btn.normal_pixmap))
        btn.setIconSize(QSize(155, 54))
        
        # Thiết lập sự kiện hover
        btn.enterEvent = lambda event: btn.setIcon(QIcon(btn.focus_pixmap)) if self.current_character != team else None
        btn.leaveEvent = lambda event: btn.setIcon(QIcon(btn.normal_pixmap)) if self.current_character != team else None
        
        return btn
        
    def create_game_button(self, down_img, focus_img, up_img, width, height, x, y):
        """Tạo nút điều khiển game với các thuộc tính cho trước"""
        btn = QPushButton(self)
        btn.setFixedSize(width, height)
        btn.move(x, y)
        btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        
        # Lưu trữ các trạng thái ảnh
        btn.down_pixmap = QPixmap(down_img)
        btn.focus_pixmap = QPixmap(focus_img)
        if up_img:
            btn.up_pixmap = QPixmap(up_img)
            btn.setIcon(QIcon(btn.up_pixmap))
        
        btn.setIconSize(QSize(width, height))
        
        # Thiết lập sự kiện hover
        btn.enterEvent = lambda event: btn.setIcon(QIcon(btn.focus_pixmap))
        btn.leaveEvent = lambda event: btn.setIcon(QIcon(btn.up_pixmap)) if hasattr(btn, 'up_pixmap') else None
        
        return btn
        
    def create_match_type_label(self):
        """Tạo label hiển thị chế độ chơi"""
        label = QLabel(self)
        label.setFixedSize(280, 50)
        label.move(1120, 715)
        label.setStyleSheet("background-color: transparent;")
        
        # Load và hiển thị ảnh chế độ chơi
        match_type_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/MatchType/MatchType_17.PNG")
        label.setPixmap(match_type_pixmap)
        label.setScaledContents(True)
        
        # Thiết lập sự kiện click
        label.mousePressEvent = lambda event: self.open_match_setting()
        
        # Thiết lập sự kiện hover
        label.enterEvent = lambda event: self.match_setting_btn.setIcon(QIcon(self.match_setting_btn.focus_pixmap))
        label.leaveEvent = lambda event: self.match_setting_btn.setIcon(QIcon(self.match_setting_btn.down_pixmap))
        
        # Đặt label lên trên nút
        label.raise_()
        
        return label
        
    def update_character_image(self):
        """Cập nhật ảnh nhân vật dựa trên team đang chọn"""
        character_pixmap = QPixmap(f"REZ/UI/UI_LobbyRenewal/Character/{self.character_name}_{self.current_character}.PNG")
        self.character_label.setPixmap(character_pixmap)
        self.character_label.setScaledContents(True)
        
    def update_team_buttons_state(self):
        """Cập nhật trạng thái của các nút chọn team"""
        self.bl_btn.setIcon(QIcon(self.bl_btn.select_pixmap if self.current_character == "BL" else self.bl_btn.normal_pixmap))
        self.gr_btn.setIcon(QIcon(self.gr_btn.select_pixmap if self.current_character == "GR" else self.gr_btn.normal_pixmap))
        
    def switch_to_bl(self):
        """Chuyển sang team BL"""
        self.current_character = "BL"
        self.update_team_buttons_state()
        self.update_character_image()
        self.save_config()  # Lưu thay đổi vào config
        
    def switch_to_gr(self):
        """Chuyển sang team GR"""
        self.current_character = "GR"
        self.update_team_buttons_state()
        self.update_character_image()
        self.save_config()  # Lưu thay đổi vào config

    def start_game(self):
        """Xử lý sự kiện khi nhấn nút Start Game"""
        print("Starting game...")

    def open_match_setting(self):
        """Xử lý sự kiện khi nhấn nút chọn chế độ chơi"""
        print("Opening match setting...")