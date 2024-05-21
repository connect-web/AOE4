from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QFontDatabase, QFont
import os
import re

from .fonts import get_font_object
from .css_cache import css_cache


class BaseWidget(QWidget):
    def __init__(self, size: tuple, stylesheet: str = None, font_name: str = None, font_size: int = 12):
        super().__init__()
        self.setGeometry(*size)
        self.stylesheet = stylesheet
        self.font_size = font_size

        self.setStyleSheet(self.stylesheet)

        self.QFont = QFont(get_font_object(font_name), self.font_size)
        self.setFont(self.QFont)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class BaseLabel(QLabel):
    def __init__(self, text: str, parent: QWidget, size: tuple, align_center: bool = False, stylesheet=None,
                 font_name: str = None, font_size: int = None):
        super().__init__(text=text, parent=parent)
        self.setGeometry(*size)
        self.setWordWrap(True)
        self.setGraphicsEffect(get_black_shadow())
        if align_center:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if stylesheet:
            self.setStyleSheet(stylesheet)

        self.QFont = QFont(get_font_object(font_name), font_size)
        self.setFont(self.QFont)


def get_black_shadow():
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setOffset(5, 5)  # Shadow offset
    shadow_effect.setBlurRadius(5)  # Shadow blur radius
    shadow_effect.setColor(QColor('black'))  # Shadow color
    return shadow_effect


class BaseButton(QPushButton):
    def __init__(self, size: tuple, text: str = None, parent: QWidget = None,
                 stylesheet: str = None, font_name: str = None, font_size: int = 12, click_connect: classmethod = None):
        super().__init__(text=text, parent=parent)
        self.setGeometry(*size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if stylesheet:
            self.setStyleSheet(stylesheet)
        self.setFont(
            QFont(get_font_object(font_name), font_size)
        )

        if click_connect is not None:
            self.clicked.connect(click_connect)


class MinimizeWidget(BaseWidget):
    def __init__(self, resources, css=None):
        super().__init__(size=(0, 400, 260, 60), stylesheet=css)
        # Keep a reference to the Resources instance
        self.resources = resources
        self.hidden = False

        self.widgets = [
            self.resources.food, self.resources.wood, self.resources.gold,
            self.resources.stone, self.resources.description,
            self.resources.navigationButtons
        ]

        self.toggleButton = BaseButton(size=(10, 10, 100, 40), text="Minimize", parent=self, stylesheet=css)
        self.toggleButton.clicked.connect(self.toggleWidgets)
        self.show()

    def toggleWidgets(self):
        # Toggle the visibility, text of the widgets
        self.hidden = False if self.hidden else True
        new_text = "Open" if self.hidden else "Minimize"

        for widget in self.widgets:
            widget.setHidden(not widget.isHidden())

        self.toggleButton.setText(new_text)


class NavigationButtons(BaseWidget):
    def __init__(self, resources):
        super().__init__(size=(0, 500, 260, 60))
        # Keep a reference to the Resources instance
        self.resources = resources
        self.backButton = BaseButton(size=(10, 10, 100, 40), text="BACK", parent=self,
                                     stylesheet=css_cache.load('buttons.css'), click_connect=self.resources.back)

        self.nextButton = BaseButton(size=(150, 10, 100, 40), text="NEXT", parent=self,
                                     stylesheet=css_cache.load('buttons.css'), click_connect=self.resources.next)
        self.show()


"""

        global font_storage
        print(f"OverlayWidget Font: {font}")

        font_id = font_storage.get_font_id() if font is None else font_storage.get_font_id(font)
        print(f"new font_id: {font_id}")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]  # Use the first family name

            self.label.setFont(QFont(font_family, font_size))
       """


class OverlayWidget(BaseWidget):
    def __init__(self, text, size, color='white', css=None, font=None, font_size=16,
                 centre=True):
        super().__init__(size=size, stylesheet=css, font_name=font, font_size=font_size)

        stylesheet = f"color: {color};" if css is None else css
        self.label = BaseLabel(text, self, size=(0, 0, size[2], size[3]), align_center=centre, stylesheet=stylesheet,
                               font_name=font, font_size=font_size)
        self.show()

    def setText(self, text):
        # Method to update the text of the child label
        self.label.setText(text)


class VillagerWidget(OverlayWidget):
    def __init__(self, text, x, y, maxWidth=200, maxHeight=50):
        super().__init__(text=text,
                         size=(x, y, maxWidth, maxHeight),
                         font='whitrabt.ttf',
                         font_size=24,
                         centre=False
                         )


class ResourceWidget:
    x_axis = 220
    y_start = 1210
    line_height = 50
    y_axis = {
        'food': y_start,
        'wood': y_start + 1 * line_height,
        'gold': y_start + 2 * line_height,
        'stone': y_start + 3 * line_height
    }

    def __init__(self):
        self.food = None
        self.wood = None
        self.gold = None
        self.stone = None

        self.update_methods = {
            'food': lambda food_villager_count: self.set_food(food_villager_count),
            'wood': lambda wood_villager_count: self.set_wood(wood_villager_count),
            'gold': lambda gold_villager_count: self.set_gold(gold_villager_count),
            'stone': lambda stone_villager_count: self.set_stone(stone_villager_count),
        }

    def update_map(self, update_dict: dict):
        for key, value in update_dict.items():
            func = self.update_methods.get(key)
            if func is not None:
                func(value)

    def set_food(self, value):
        if self.food is None:
            self.food = VillagerWidget(str(value), self.x_axis, self.y_axis.get('food'))
            self.food.show()
        else:
            self.food.setText(str(value))

    def set_wood(self, value):
        if self.wood is None:
            self.wood = VillagerWidget(str(value), self.x_axis, self.y_axis.get('wood'))
            self.wood.show()
        else:
            self.wood.setText(str(value))

    def set_gold(self, value):
        if self.gold is None:
            self.gold = VillagerWidget(str(value), self.x_axis, self.y_axis.get('gold'))
            self.gold.show()
        else:
            self.gold.setText(str(value))

    def set_stone(self, value):
        if self.stone is None:
            self.stone = VillagerWidget(str(value), self.x_axis, self.y_axis.get('stone'))
            self.stone.show()
        else:
            self.stone.setText(str(value))
