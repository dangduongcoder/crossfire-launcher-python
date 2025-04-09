from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

class LobbyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        # label = QLabel("Sảnh chơi")
        # label.setStyleSheet("font-size: 24px; color: white;")
        # layout.addWidget(label)
        
        # Tạo label để hiển thị ảnh nhân vật
        self.character_label = QLabel(self)
        self.character_label.setFixedSize(1300, 852)
        self.character_label.move(150, 50)  # Di chuyển lên trên để tránh bị che bởi bottom bar
        self.character_label.setStyleSheet("background-color: transparent;")
        
        # Load và hiển thị ảnh nhân vật
        self.current_character = "BL"  # Mặc định là BL
        self.update_character_image()

        # Nút chuyển đổi BL
        self.bl_btn = QPushButton(self)
        self.bl_btn.setFixedSize(155, 54)
        self.bl_btn.move(930, 90)
        self.bl_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.bl_btn.normal_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl.PNG")
        self.bl_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl_focus.PNG") 
        self.bl_btn.select_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_bl_select.PNG")
        
        # Thiết lập icon mặc định
        self.bl_btn.setIcon(QIcon(self.bl_btn.select_pixmap))  # BL được chọn mặc định
        self.bl_btn.setIconSize(QSize(155, 54))
        
        # Thiết lập sự kiện hover
        self.bl_btn.enterEvent = lambda event: self.bl_btn.setIcon(QIcon(self.bl_btn.focus_pixmap)) if self.current_character != "BL" else None
        self.bl_btn.leaveEvent = lambda event: self.bl_btn.setIcon(QIcon(self.bl_btn.normal_pixmap)) if self.current_character != "BL" else None
        
        # Thiết lập sự kiện click
        self.bl_btn.clicked.connect(self.switch_to_bl)

        # Nút chuyển đổi GR 
        self.gr_btn = QPushButton(self)
        self.gr_btn.setFixedSize(155, 54)
        self.gr_btn.move(930, 145)
        self.gr_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.gr_btn.normal_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr.PNG")
        self.gr_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr_focus.PNG")
        self.gr_btn.select_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/Ani/Lobby/bt_gr_select.PNG")
        
        # Thiết lập icon mặc định
        self.gr_btn.setIcon(QIcon(self.gr_btn.normal_pixmap))
        self.gr_btn.setIconSize(QSize(155, 54))
        
        # Thiết lập sự kiện hover
        self.gr_btn.enterEvent = lambda event: self.gr_btn.setIcon(QIcon(self.gr_btn.focus_pixmap)) if self.current_character != "GR" else None
        self.gr_btn.leaveEvent = lambda event: self.gr_btn.setIcon(QIcon(self.gr_btn.normal_pixmap)) if self.current_character != "GR" else None
        
        # Thiết lập sự kiện click
        self.gr_btn.clicked.connect(self.switch_to_gr)

        # Nút Start Game
        self.start_btn = QPushButton(self)
        self.start_btn.setFixedSize(173, 85)
        self.start_btn.move(1400, 715)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.start_btn.down_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/GameStart_Down.PNG")
        self.start_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/GameStart_Focus.PNG")
        self.start_btn.up_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/GameStart_Up.PNG")
        
        # Thiết lập icon mặc định
        self.start_btn.setIcon(QIcon(self.start_btn.up_pixmap))
        self.start_btn.setIconSize(QSize(173, 85))
        
        # Thiết lập sự kiện hover
        self.start_btn.enterEvent = lambda event: self.start_btn.setIcon(QIcon(self.start_btn.focus_pixmap))
        self.start_btn.leaveEvent = lambda event: self.start_btn.setIcon(QIcon(self.start_btn.up_pixmap))
        
        # Thiết lập sự kiện click
        self.start_btn.clicked.connect(self.start_game)

        # Nút chọn chế độ chơi
        self.match_setting_btn = QPushButton(self)
        self.match_setting_btn.setFixedSize(280, 50)
        self.match_setting_btn.move(1120, 715)
        self.match_setting_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Lưu trữ các trạng thái ảnh
        self.match_setting_btn.focus_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/MatchSetting_Focus.PNG")
        self.match_setting_btn.up_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/MatchSetting_Up.PNG")
        
        # Thiết lập icon mặc định
        self.match_setting_btn.setIcon(QIcon(self.match_setting_btn.up_pixmap))
        self.match_setting_btn.setIconSize(QSize(280, 50))
        
        
        # Label hiển thị chế độ chơi
        self.match_type_label = QLabel(self)
        self.match_type_label.setFixedSize(280, 50)
        self.match_type_label.move(1120, 715)
        self.match_type_label.setStyleSheet("background-color: transparent;")
        
        # Load và hiển thị ảnh chế độ chơi
        match_type_pixmap = QPixmap("REZ/UI/UI_LobbyRenewal/MatchType/MatchType_17.PNG")
        self.match_type_label.setPixmap(match_type_pixmap)
        self.match_type_label.setScaledContents(True)
        
        # Thiết lập sự kiện click cho label
        self.match_type_label.mousePressEvent = lambda event: self.open_match_setting()

        # Thiết lập sự kiện hover
        self.match_type_label.enterEvent = lambda event: self.match_setting_btn.setIcon(QIcon(self.match_setting_btn.focus_pixmap))
        self.match_type_label.leaveEvent = lambda event: self.match_setting_btn.setIcon(QIcon(self.match_setting_btn.up_pixmap))
        
        
        # Đặt label lên trên nút
        self.match_type_label.raise_()
        
        self.setLayout(layout)
        
    def update_character_image(self):
        character_pixmap = QPixmap(f"REZ/UI/UI_LobbyRenewal/Character/FOXHAWL_{self.current_character}.PNG")
        self.character_label.setPixmap(character_pixmap)
        self.character_label.setScaledContents(True)
        
    def switch_to_bl(self):
        self.current_character = "BL"
        self.bl_btn.setIcon(QIcon(self.bl_btn.select_pixmap))
        self.gr_btn.setIcon(QIcon(self.gr_btn.normal_pixmap))
        self.update_character_image()
        
    def switch_to_gr(self):
        self.current_character = "GR" 
        self.gr_btn.setIcon(QIcon(self.gr_btn.select_pixmap))
        self.bl_btn.setIcon(QIcon(self.bl_btn.normal_pixmap))
        self.update_character_image()

    def start_game(self):
        # Xử lý sự kiện khi nhấn nút Start Game
        print("Starting game...")

    def open_match_setting(self):
        # Xử lý sự kiện khi nhấn nút chọn chế độ chơi
        print("Opening match setting...")