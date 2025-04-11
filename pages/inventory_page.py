from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QWheelEvent
from PyQt6.QtCore import Qt
import json
import os

class WeaponSlot(QLabel):
    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.setFixedSize(329, 137)
        self.move(x, y)
        self.setStyleSheet("background-color: transparent;")
        
        # Thiết lập ảnh nền
        self.set_background("REZ/UI/UI_ShopRenewal/Slot/slotbg_S.PNG")
        
        # Tạo label cho icon vũ khí
        self.weapon_icon_label = QLabel(self)
        self.weapon_icon_label.setFixedSize(256, 128)
        self.weapon_icon_label.move(36, 2)
        self.weapon_icon_label.setStyleSheet("background-color: transparent;")
        
        # Tạo label cho tên vũ khí
        self.weapon_name_label = QLabel(self)
        self.weapon_name_label.move(12, 0)
        self.weapon_name_label.setStyleSheet("color: white; font-size: 16px; background-color: transparent;")
        
        # Tạo label thời hạn vũ khí
        self.weapon_time_label = QLabel(self)
        self.weapon_time_label.move(240, 0)
        self.weapon_time_label.setStyleSheet("color: white; font-size: 16px; background-color: transparent;")
        self.weapon_time_label.setText("Permanent")

        # Tạo label cho hiệu ứng hover
        self.hover_label = QLabel(self)
        self.hover_label.setFixedSize(329, 137)
        self.hover_label.move(0, 0)
        self.hover_label.setStyleSheet("background-color: transparent;")
        hover_pixmap = QPixmap("REZ/UI/UI_ShopRenewal/Slot/slotbg_Select.PNG")
        self.hover_label.setPixmap(hover_pixmap)
        self.hover_label.setScaledContents(True)
        self.hover_label.hide()
        
        # Các thuộc tính sẽ được thêm sau
        self.weapon_name = None
        self.weapon_stats = None
        self.weapon_class = None
        
        # Thiết lập sự kiện hover
        self.enterEvent = self.on_hover_enter
        self.leaveEvent = self.on_hover_leave
        
    def on_hover_enter(self, event):
        """Xử lý khi chuột hover vào slot"""
        self.hover_label.show()
        
    def on_hover_leave(self, event):
        """Xử lý khi chuột rời khỏi slot"""
        self.hover_label.hide()
        
    def set_background(self, image_path):
        """Thiết lập ảnh nền cho slot"""
        try:
            bg = QPixmap(image_path)
            self.setPixmap(bg)
            self.setScaledContents(True)
        except Exception as e:
            print(f"Lỗi khi tải ảnh nền: {e}")
        
    def set_weapon_icon(self, icon_path):
        """Thiết lập icon vũ khí"""
        try:
            weapon_icon = QPixmap(icon_path)
            self.weapon_icon_label.setPixmap(weapon_icon)
            self.weapon_icon_label.setScaledContents(True)
        except Exception as e:
            print(f"Lỗi khi tải icon vũ khí: {e}")
        
    def set_weapon_name(self, name):
        """Thiết lập tên vũ khí"""
        self.weapon_name = name
        self.weapon_name_label.setText(name)

    def set_weapon_class(self, class_name):
        """Thiết lập tên lớp vũ khí"""
        self.weapon_class = class_name
        color = "#FDF7B1" if class_name == "S" else "white"
        self.weapon_name_label.setStyleSheet(f"color: {color}; font-size: 14px; background-color: transparent;")
        self.weapon_time_label.setStyleSheet(f"color: {color}; font-size: 14px; background-color: transparent;")
        self.set_background(f"REZ/UI/UI_ShopRenewal/Slot/slotbg_{class_name}.PNG")
        
    def set_weapon_stats(self, stats):
        """Thiết lập thông số vũ khí"""
        # TODO: Thêm thông số vũ khí
        pass
        
    def hide_slot(self):
        """Ẩn slot"""
        self.hide()
        self.weapon_icon_label.hide()
        self.weapon_name_label.hide()
        self.hover_label.hide()
        
    def show_slot(self):
        """Hiển thị slot"""
        self.show()
        self.weapon_icon_label.show()
        self.weapon_name_label.show()

class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.weapons_per_page = 12
        self.weapons_per_scroll = 3  # Số vũ khí di chuyển mỗi lần cuộn
        self.init_ui()
        
    def init_ui(self):
        # Tạo background
        self.create_background()
        
        # Tạo các slot vũ khí
        self.create_weapon_slots()
        
        # Tải và sắp xếp dữ liệu vũ khí từ file json
        self.load_weapons_data()
        
        # Hiển thị vũ khí lên các slot
        self.display_weapons()
        
    def wheelEvent(self, event: QWheelEvent):
        """Xử lý sự kiện cuộn chuột"""
        # Lấy góc cuộn (dương = lên, âm = xuống)
        delta = event.angleDelta().y()
        
        # Tính số trang tối đa
        max_page = (len(self.all_weapons) - 1) // self.weapons_per_page
        
        if delta > 0:  # Cuộn lên
            if self.current_page > 0:
                self.current_page -= 1
                self.display_weapons()
        elif delta < 0:  # Cuộn xuống
            if self.current_page < max_page:
                self.current_page += 1
                self.display_weapons()
        
    def load_weapons_data(self):
        """Tải dữ liệu vũ khí từ file json"""
        self.all_weapons = []
        try:
            with open("REZ/CONFIG/Weapons.json", "r", encoding="utf-8") as f:
                weapons = json.load(f)
                # Sắp xếp theo VIP, Class và loại vũ khí
                class_order = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4}
                type_order = {"sniper": 0, "rifle": 1, "pistol": 2, "melee": 3, "ge": 4}
                self.all_weapons = sorted(weapons, key=lambda x: (
                    -x["vip"],
                    class_order[x["class"]],
                    type_order.get(x["type"], 999)
                ))
        except FileNotFoundError:
            print("Không tìm thấy file Weapons.json")
        except json.JSONDecodeError:
            print("Lỗi định dạng file Weapons.json")
        except Exception as e:
            print(f"Lỗi khi đọc file Weapons.json: {e}")
            
    def display_weapons(self):
        """Hiển thị vũ khí lên các slot"""
        # Tính vị trí bắt đầu và kết thúc của trang hiện tại
        start_idx = self.current_page * self.weapons_per_scroll
        end_idx = start_idx + self.weapons_per_page
        
        # Lấy danh sách vũ khí của trang hiện tại
        displayed_weapons = self.all_weapons[start_idx:end_idx]
        
        # Hiển thị từng vũ khí lên slot tương ứng
        for i, weapon in enumerate(displayed_weapons):
            if i < len(self.weapon_slots):
                try:
                    icon_path = f"REZ/UI/BigItemIcon/{weapon['icon']}"
                    self.weapon_slots[i].set_weapon_icon(icon_path)
                    self.weapon_slots[i].set_weapon_name(weapon['name'])
                    self.weapon_slots[i].set_weapon_class(weapon['class'])
                    self.weapon_slots[i].show_slot()
                except Exception as e:
                    print(f"Lỗi khi hiển thị vũ khí {weapon.get('icon', 'unknown')}: {e}")
        
        # Ẩn các slot không có vũ khí
        for i in range(len(displayed_weapons), len(self.weapon_slots)):
            self.weapon_slots[i].hide_slot()
        
        # Nếu có nhiều hơn 2 trang, đảm bảo hiển thị đủ 4 hàng
        if len(self.all_weapons) > self.weapons_per_page * 2:
            # Hiển thị lại các slot trống ở cuối
            for i in range(len(displayed_weapons), min(len(displayed_weapons) + 3, len(self.weapon_slots))):
                self.weapon_slots[i].show_slot()
                self.weapon_slots[i].set_background("REZ/UI/UI_ShopRenewal/Slot/slotbg_S.PNG")
        
    def create_background(self):
        """Tạo background cho trang kho đồ"""
        # Tạo hình chữ nhật lớn
        rect_label = QLabel(self)
        rect_label.setFixedSize(1100, 675) 
        rect_label.move(475, 115)
        rect_label.setStyleSheet("background-color: rgba(25, 25, 25, 30%);")

        # Tạo thanh tiêu đề
        rect2_label = QLabel(self)
        rect2_label.setFixedSize(1100, 40) 
        rect2_label.move(475, 115)
        rect2_label.setStyleSheet("background-color: rgba(25, 25, 25, 50%);")
        
    def create_weapon_slots(self):
        """Tạo các slot vũ khí"""
        self.weapon_slots = []
        
        # Tọa độ ban đầu
        start_x = 500
        start_y = 180
        
        # Khoảng cách giữa các slot
        gap_x = 340
        gap_y = 151
        
        # Tạo 12 slot (3 hàng x 4 cột)
        for row in range(4):
            for col in range(3):
                x = start_x + (col * gap_x)
                y = start_y + (row * gap_y)
                slot = WeaponSlot(self, x, y)
                self.weapon_slots.append(slot)