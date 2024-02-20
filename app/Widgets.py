from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QFontDatabase, QFont
import os

class FontStorage:
    def __init__(self):
        self._fonts = {}

    def get_font_id(self, name="open-sans.regular.ttf"):
        font_id = self._fonts.get(name)
        if font_id is not None and font_id != -1:
            return font_id
        font_id = QFontDatabase.addApplicationFont(os.path.join('css',name))
        if font_id == -1:
            print("Failed to load font")
        else:
            print("Font loaded successfully")
            self._fonts[name] = font_id

        return font_id

font_storage = FontStorage()

class WindowMinimize(QWidget):
    def __init__(self, resources, css=None):
        self.hidden = False

        self.resources = resources  # Keep a reference to the Resources instance
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 400, 260, 60)  # Set the container's position and size

        # Initialize the toggle button
        self.toggleButton = QPushButton("Minimize", self)
        self.toggleButton.clicked.connect(self.toggleWidgets)
        self.toggleButton.setGeometry(10, 10, 100, 40)
        if css is not None: self.toggleButton.setStyleSheet(css)

        self.toggleButton.setCursor(Qt.CursorShape.PointingHandCursor)  # Sets the cursor to a pointing hand

        global font_storage

        font_families = QFontDatabase.applicationFontFamilies(font_storage.get_font_id())
        if font_families:
            font_family = font_families[0]  # Use the first family name

            self.toggleButton.setFont(QFont(font_family, 12))

    def toggleWidgets(self):
        self.hidden = False if self.hidden else True
        # Toggle the visibility of the widgets

        if self.hidden:
            self.toggleButton.setText("Open")
        else:
            self.toggleButton.setText("Minimize")

        for widget in [self.resources.food, self.resources.wood, self.resources.gold, self.resources.stone,
                       self.resources.description, self.resources.overlayButtons
                       ]:
            widget.setHidden(not widget.isHidden())

class OverlayButtons(QWidget):
    def __init__(self, resources):
        super().__init__()
        self.resources = resources  # Keep a reference to the Resources instance
        self.initUI()

    def initUI(self, css=None):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 500, 260, 60)  # Set the container's position and size

        self.backButton = QPushButton('BACK', self)
        self.backButton.clicked.connect(self.resources.back)
        self.backButton.setGeometry(10, 10, 100, 40)  # Position inside the container

        self.nextButton = QPushButton('NEXT', self)
        self.nextButton.clicked.connect(self.resources.next)
        self.nextButton.setGeometry(150, 10, 100, 40)  # Position inside the container

        #self.backButton.setStyleSheet("QPushButton { background-color: rgb(21,29,38); color: white; font-weight: 900; border: 4px solid #F3CD7C; border-radius: 20px}")
        #self.nextButton.setStyleSheet("QPushButton { background-color: rgb(21,29,38); color: white; font-weight: 900; border: 4px solid #F3CD7C; border-radius: 20px }")
        if css is None:
            with open('css/buttons.css', 'r') as x:
                buttons_css = x.read()
            self.backButton.setStyleSheet(buttons_css)
            self.nextButton.setStyleSheet(buttons_css)
        else:
            self.backButton.setStyleSheet(css)
            self.nextButton.setStyleSheet(css)


        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)  # Sets the cursor to a pointing hand
        self.nextButton.setCursor(Qt.CursorShape.PointingHandCursor)  # Sets the cursor to a pointing hand

        global font_storage

        font_families = QFontDatabase.applicationFontFamilies(font_storage.get_font_id())
        if font_families:
            font_family = font_families[0]  # Use the first family name

            self.backButton.setFont(QFont(font_family, 12))
            self.nextButton.setFont(QFont(font_family, 12))


        """
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(1800)  # 1 second
        self.animation.setStartValue(QColor(255, 255, 255))
        self.animation.setEndValue(QColor(243, 205, 124))

        def enterEvent(self, event):
            self.animation.start()
            super(OverlayButtons, self).enterEvent(event)
    
        def leaveEvent(self, event):
            self.animation.stop()
            self.setStyleSheet(self.styleSheet())  # Reset to original style
            super(OverlayButtons, self).leaveEvent(event)
        """



class OverlayWidget(QWidget):
    def __init__(self, text, x, y, maxWidth=200, maxHeight=50, color='green', css=None, font = None, font_size=16, centre = True):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x, y, maxWidth, maxHeight)
        self.label = QLabel(text, self)  # Store label as an instance attribute
        if css is None:
            self.label.setStyleSheet(f"color: {color};")
        else:
            self.label.setStyleSheet(css)

        if centre:
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
        self.label.setWordWrap(True)  # Enable word wrapping
        self.label.setGeometry(0, 0, maxWidth, maxHeight)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(5, 5)  # Shadow offset
        shadow_effect.setBlurRadius(5)  # Shadow blur radius
        shadow_effect.setColor(QColor('black'))  # Shadow color
        self.label.setGraphicsEffect(shadow_effect)

        global font_storage
        print(f"OverlayWidget Font: {font}")

        font_id = font_storage.get_font_id() if font is None else font_storage.get_font_id(font)
        print(f"new font_id: {font_id}")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]  # Use the first family name

            self.label.setFont(QFont(font_family, font_size))


    def setText(self, text):  # Define a method to update the text of the label
        self.label.setText(text)

class VillagerWidget(OverlayWidget):
    def __init__(self, text, x, y, maxWidth=200, maxHeight=50):
        color = "green"
        super().__init__(text=text,
                         x=x,
                         y=y,
                         css=f'color: {color};',
                         maxWidth=maxWidth,
                         maxHeight=maxHeight,
                         font='whitrabt.ttf',
                         font_size=24,
                         centre=False
                         )